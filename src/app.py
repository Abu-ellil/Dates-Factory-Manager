from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from database import get_connection, init_db
from datetime import datetime
import os
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
import license_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Class
class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    conn = get_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(user['id'], user['username'], user['role'])
    return None

# Initialize database on first run
if not os.path.exists('date_factory.db'):
    init_db()

# Start backup scheduler
from backup_scheduler import start_scheduler
scheduler = start_scheduler()

@app.before_request
def check_license_status():
    """Check if application is activated"""
    # Allow static files and activation page
    if request.endpoint in ['static', 'activate', 'activate_post']:
        return
        
    # Check license
    if not license_manager.check_license():
        return redirect(url_for('activate'))

@app.route('/activate', methods=['GET'])
def activate():
    """Activation page"""
    if license_manager.check_license():
        return redirect(url_for('index'))
        
    machine_id = license_manager.get_machine_id()
    return render_template('activate.html', machine_id=machine_id)

@app.route('/activate', methods=['POST'])
def activate_post():
    """Handle activation"""
    license_key = request.form.get('license_key', '').strip()
    machine_id = license_manager.get_machine_id()
    
    is_valid, message = license_manager.verify_license_key(license_key, machine_id)
    
    if is_valid:
        license_manager.save_license(license_key)
        flash('تم تفعيل البرنامج بنجاح!', 'success')
        return redirect(url_for('index'))
    else:
        return render_template('activate.html', machine_id=machine_id, error=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        # Simple password check for demo (in production use check_password_hash)
        # We will support both plain text (for initial setup) and hashed
        if user:
            is_valid = False
            if user['password'].startswith('scrypt:'):
                is_valid = check_password_hash(user['password'], password)
            else:
                is_valid = user['password'] == password
                
            if is_valid:
                user_obj = User(user['id'], user['username'], user['role'])
                login_user(user_obj)
                return redirect(url_for('dashboard'))
        
        return render_template('login.html', error='اسم المستخدم أو كلمة المرور غير صحيحة')
        
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    """Redirect to dashboard"""
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard view"""
    return render_template('dashboard.html')

@app.route('/customers')
@login_required
def customers():
    """Customers management page"""
    conn = get_connection()
    customers_list = conn.execute('SELECT * FROM customers ORDER BY name').fetchall()
    conn.close()
    return render_template('customers.html', customers=customers_list)

@app.route('/weighbridge')
@login_required
def weighbridge():
    """Weighbridge transactions page"""
    conn = get_connection()
    transactions = conn.execute('''
        SELECT w.*, c.name as customer_name 
        FROM weighbridge w
        JOIN customers c ON w.customer_id = c.id
        ORDER BY w.date DESC, w.created_at DESC
        LIMIT 100
    ''').fetchall()
    conn.close()
    return render_template('weighbridge.html', transactions=transactions)

@app.route('/crates')
@login_required
def crates():
    """Crates management page"""
    conn = get_connection()
    crates_list = conn.execute('''
        SELECT cr.*, c.name as customer_name 
        FROM crates cr
        JOIN customers c ON cr.customer_id = c.id
        ORDER BY cr.date DESC
        LIMIT 100
    ''').fetchall()
    conn.close()
    return render_template('crates.html', crates=crates_list)

@app.route('/finance')
@login_required
def finance():
    """Finance management page"""
    conn = get_connection()
    transactions = conn.execute('''
        SELECT f.*, c.name as customer_name 
        FROM finance f
        JOIN customers c ON f.customer_id = c.id
        ORDER BY f.date DESC
        LIMIT 100
    ''').fetchall()
    conn.close()
    return render_template('finance.html', transactions=transactions)

# API Endpoints
@app.route('/api/customers', methods=['GET', 'POST'])
def api_customers():
    """API for customers"""
    conn = get_connection()
    
    if request.method == 'POST':
        data = request.json
        try:
            conn.execute('INSERT INTO customers (name, type, phone) VALUES (?, ?, ?)',
                        (data['name'], data['type'], data.get('phone', '')))
            conn.commit()
            return jsonify({'success': True, 'message': 'تم إضافة العميل بنجاح'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 400
        finally:
            conn.close()
    
    # GET request
    customers = conn.execute('SELECT * FROM customers ORDER BY name').fetchall()
    conn.close()
    return jsonify([dict(c) for c in customers])

@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def api_delete_customer(customer_id):
    """Delete a customer"""
    conn = get_connection()
    
    try:
        # Check if customer has any transactions
        weighbridge_count = conn.execute('SELECT COUNT(*) as count FROM weighbridge WHERE customer_id = ?', (customer_id,)).fetchone()['count']
        crates_count = conn.execute('SELECT COUNT(*) as count FROM crates WHERE customer_id = ?', (customer_id,)).fetchone()['count']
        finance_count = conn.execute('SELECT COUNT(*) as count FROM finance WHERE customer_id = ?', (customer_id,)).fetchone()['count']
        
        if weighbridge_count > 0 or crates_count > 0 or finance_count > 0:
            return jsonify({
                'success': False, 
                'message': f'لا يمكن حذف العميل لأنه لديه معاملات ({weighbridge_count} ميزان، {crates_count} صناديق، {finance_count} مالية)'
            }), 400
        
        # Delete customer
        conn.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
        conn.commit()
        return jsonify({'success': True, 'message': 'تم حذف العميل بنجاح'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    finally:
        conn.close()

@app.route('/api/dashboard/<int:customer_id>')
def api_dashboard(customer_id):
    """Get dashboard metrics for a specific customer"""
    conn = get_connection()
    
    # Total weight and value from weighbridge
    weighbridge_stats = conn.execute('''
        SELECT 
            COALESCE(SUM(net_weight), 0) as total_weight,
            COALESCE(SUM(total), 0) as total_value
        FROM weighbridge 
        WHERE customer_id = ?
    ''', (customer_id,)).fetchone()
    
    # Finance stats
    finance_stats = conn.execute('''
        SELECT 
            COALESCE(SUM(amount_paid), 0) as total_paid,
            COALESCE(SUM(amount_received), 0) as total_received
        FROM finance 
        WHERE customer_id = ?
    ''', (customer_id,)).fetchone()
    
    # Crates balance
    crates_stats = conn.execute('''
        SELECT 
            COALESCE(SUM(crates_out), 0) as total_out,
            COALESCE(SUM(crates_returned), 0) as total_returned
        FROM crates 
        WHERE customer_id = ?
    ''', (customer_id,)).fetchone()
    
    conn.close()
    
    return jsonify({
        'total_weight': weighbridge_stats['total_weight'],
        'total_value': weighbridge_stats['total_value'],
        'total_paid': finance_stats['total_paid'],
        'total_received': finance_stats['total_received'],
        'balance': weighbridge_stats['total_value'] + finance_stats['total_received'] - finance_stats['total_paid'],
        'crates_out': crates_stats['total_out'],
        'crates_returned': crates_stats['total_returned'],
        'crates_balance': crates_stats['total_out'] - crates_stats['total_returned']
    })

@app.route('/api/weighbridge', methods=['POST'])
def api_add_weighbridge():
    """Add new weighbridge transaction"""
    data = request.json
    conn = get_connection()
    
    try:
        # Get qantar weight from settings
        qantar_weight = conn.execute(
            'SELECT qantar_weight FROM daily_prices WHERE date = ? LIMIT 1',
            (data['date'],)
        ).fetchone()
        
        if not qantar_weight:
            qantar_weight = 100.0  # Default
        else:
            qantar_weight = qantar_weight['qantar_weight']
        
        # Calculate total
        total = (float(data['net_weight']) / qantar_weight) * float(data['price_per_qantar'])
        
        conn.execute('''
            INSERT INTO weighbridge (date, customer_id, net_weight, price_per_qantar, total)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['date'], data['customer_id'], data['net_weight'], 
              data['price_per_qantar'], total))
        
        conn.commit()
        return jsonify({'success': True, 'message': 'تم إضافة المعاملة بنجاح'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    finally:
        conn.close()

@app.route('/api/weighbridge/<int:id>', methods=['PUT', 'DELETE'])
def api_manage_weighbridge(id):
    """Update or Delete weighbridge transaction"""
    conn = get_connection()
    try:
        if request.method == 'DELETE':
            conn.execute('DELETE FROM weighbridge WHERE id = ?', (id,))
            conn.commit()
            return jsonify({'success': True, 'message': 'تم حذف المعاملة بنجاح'})
        
        # PUT - Update
        data = request.json
        # Recalculate total
        total = (float(data['net_weight']) / 100.0) * float(data['price_per_qantar']) # Assuming 100kg qantar for edit
        
        conn.execute('''
            UPDATE weighbridge 
            SET date = ?, customer_id = ?, net_weight = ?, price_per_qantar = ?, total = ?
            WHERE id = ?
        ''', (data['date'], data['customer_id'], data['net_weight'], 
              data['price_per_qantar'], total, id))
        conn.commit()
        return jsonify({'success': True, 'message': 'تم تعديل المعاملة بنجاح'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    finally:
        conn.close()

@app.route('/api/crates', methods=['POST'])
def api_add_crate():
    """Add new crate transaction"""
    data = request.json
    conn = get_connection()
    
    try:
        conn.execute('''
            INSERT INTO crates (date, customer_id, crates_out, crates_returned, handler, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['date'], data['customer_id'], data.get('crates_out', 0), 
              data.get('crates_returned', 0), data.get('handler', ''), data.get('notes', '')))
        
        conn.commit()
        return jsonify({'success': True, 'message': 'تم إضافة حركة الصناديق بنجاح'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    finally:
        conn.close()

@app.route('/api/crates/<int:id>', methods=['PUT', 'DELETE'])
def api_manage_crate(id):
    """Update or Delete crate transaction"""
    conn = get_connection()
    try:
        if request.method == 'DELETE':
            conn.execute('DELETE FROM crates WHERE id = ?', (id,))
            conn.commit()
            return jsonify({'success': True, 'message': 'تم حذف الحركة بنجاح'})
        
        # PUT - Update
        data = request.json
        conn.execute('''
            UPDATE crates 
            SET date = ?, customer_id = ?, crates_out = ?, crates_returned = ?, handler = ?, notes = ?
            WHERE id = ?
        ''', (data['date'], data['customer_id'], data.get('crates_out', 0), 
              data.get('crates_returned', 0), data.get('handler', ''), data.get('notes', ''), id))
        conn.commit()
        return jsonify({'success': True, 'message': 'تم تعديل الحركة بنجاح'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    finally:
        conn.close()

@app.route('/api/finance', methods=['POST'])
def api_add_finance():
    """Add new finance transaction"""
    data = request.json
    conn = get_connection()
    
    try:
        conn.execute('''
            INSERT INTO finance (date, customer_id, transaction_type, amount_paid, amount_received, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['date'], data['customer_id'], data['transaction_type'],
              data.get('amount_paid', 0), data.get('amount_received', 0), data.get('notes', '')))
        
        conn.commit()
        return jsonify({'success': True, 'message': 'تم إضافة المعاملة المالية بنجاح'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    finally:
        conn.close()

@app.route('/api/finance/<int:id>', methods=['PUT', 'DELETE'])
def api_manage_finance(id):
    """Update or Delete finance transaction"""
    conn = get_connection()
    try:
        if request.method == 'DELETE':
            conn.execute('DELETE FROM finance WHERE id = ?', (id,))
            conn.commit()
            return jsonify({'success': True, 'message': 'تم حذف المعاملة بنجاح'})
        
        # PUT - Update
        data = request.json
        conn.execute('''
            UPDATE finance 
            SET date = ?, customer_id = ?, transaction_type = ?, amount_paid = ?, amount_received = ?, notes = ?
            WHERE id = ?
        ''', (data['date'], data['customer_id'], data['transaction_type'],
              data.get('amount_paid', 0), data.get('amount_received', 0), data.get('notes', ''), id))
        conn.commit()
        return jsonify({'success': True, 'message': 'تم تعديل المعاملة بنجاح'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    finally:
        conn.close()

@app.route('/settings')
@login_required
def settings():
    """Settings page"""
    return render_template('settings.html')

@app.route('/api/settings/prices', methods=['GET', 'POST'])
def api_settings_prices():
    """Get or Set daily prices"""
    conn = get_connection()
    try:
        if request.method == 'POST':
            data = request.json
            conn.execute('''
                INSERT OR REPLACE INTO daily_prices (date, price_per_qantar)
                VALUES (?, ?)
            ''', (data['date'], data['price']))
            conn.commit()
            return jsonify({'success': True, 'message': 'تم حفظ السعر بنجاح'})
        
        # GET - Last 30 prices
        prices = conn.execute('''
            SELECT * FROM daily_prices 
            ORDER BY date DESC LIMIT 30
        ''').fetchall()
        return jsonify([dict(p) for p in prices])
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    finally:
        conn.close()

@app.route('/api/settings/backup', methods=['POST'])
def api_settings_backup():
    """Trigger manual backup"""
    try:
        from backup_scheduler import create_backup
        backup_file = create_backup()
        if backup_file:
            return jsonify({'success': True, 'message': 'تم إنشاء النسخة الاحتياطية بنجاح'})
        else:
            return jsonify({'success': False, 'message': 'فشل إنشاء النسخة الاحتياطية'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/reports')
@login_required
def reports():
    """Reports page"""
    return render_template('reports.html')

@app.route('/api/reports')
def api_reports():
    """Get filtered reports"""
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    customer_id = request.args.get('customer')
    
    conn = get_connection()
    try:
        # Base queries
        wb_query = "SELECT w.*, c.name as customer_name FROM weighbridge w JOIN customers c ON w.customer_id = c.id WHERE w.date BETWEEN ? AND ?"
        fin_query = "SELECT f.*, c.name as customer_name FROM finance f JOIN customers c ON f.customer_id = c.id WHERE f.date BETWEEN ? AND ?"
        cr_query = "SELECT cr.*, c.name as customer_name FROM crates cr JOIN customers c ON cr.customer_id = c.id WHERE cr.date BETWEEN ? AND ?"
        
        params = [start_date, end_date]
        
        if customer_id:
            wb_query += " AND w.customer_id = ?"
            fin_query += " AND f.customer_id = ?"
            cr_query += " AND cr.customer_id = ?"
            params.append(customer_id)
            
        weighbridge = [dict(r) for r in conn.execute(wb_query, params).fetchall()]
        finance = [dict(r) for r in conn.execute(fin_query, params).fetchall()]
        crates = [dict(r) for r in conn.execute(cr_query, params).fetchall()]
        
        # Calculate summaries
        total_weight = sum(r['net_weight'] for r in weighbridge)
        total_weight_value = sum(r['total'] for r in weighbridge)
        total_received = sum(r['amount_received'] for r in finance)
        total_paid = sum(r['amount_paid'] for r in finance)
        
        return jsonify({
            'weighbridge': weighbridge,
            'finance': finance,
            'crates': crates,
            'summary': {
                'total_weight': total_weight,
                'total_weight_value': total_weight_value,
                'total_received': total_received,
                'total_paid': total_paid
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()

@app.route('/import', methods=['GET', 'POST'])
@login_required
def import_customers():
    """Import customers from Excel file"""
    if request.method == 'GET':
        return render_template('import.html')
    
    # POST - handle file upload
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'لم يتم اختيار ملف'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'لم يتم اختيار ملف'}), 400
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        return jsonify({'success': False, 'message': 'يجب أن يكون الملف بصيغة Excel (.xlsx أو .xls)'}), 400
    
    try:
        # Save file temporarily
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name
        
        # Import from file
        from bulk_import import import_customers_from_excel
        success_count, error_count, errors = import_customers_from_excel(tmp_path)
        
        # Clean up temp file
        os.remove(tmp_path)
        
        return jsonify({
            'success': True,
            'message': f'تم استيراد {success_count} عميل بنجاح',
            'success_count': success_count,
            'error_count': error_count,
            'errors': errors[:10]  # Return first 10 errors only
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/export')
@login_required
def export_excel():
    """Export database to Excel file"""
    from export import export_to_excel
    from flask import send_file
    
    try:
        # Create exports directory if it doesn't exist
        if not os.path.exists('exports'):
            os.makedirs('exports')
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'Date_Factory_Export_{timestamp}.xlsx'
        filepath = os.path.join('exports', filename)
        
        export_to_excel(filepath)
        
        return send_file(filepath, 
                        as_attachment=True, 
                        download_name=filename,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    import webbrowser
    import threading
    
    print("=" * 60)
    print("🌴 Date Factory Manager - مدير مصنع التمور 🌴")
    print("=" * 60)
    print()
    print("🚀 Starting server...")
    print()
    print("🌐 Access URLs:")
    print("   • From this PC: http://localhost:5000")
    print("   • From mobile: http://<YOUR-PC-IP>:5000")
    print()
    print("💡 Tip: Find your PC IP by running 'ipconfig' in CMD")
    print()
    print("⚠️  Keep this window open while using the application")
    print("=" * 60)
    print()
    
    # Auto-open browser after 3 seconds
    def open_browser():
        import time
        time.sleep(3)
        webbrowser.open('http://localhost:5000')
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    app.run(host='0.0.0.0', port=5000, debug=False)
