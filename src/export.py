import xlsxwriter
from datetime import datetime
from database import get_connection
import os

from config import config

def export_to_excel(output_path=None):
    """
    Export all database data to Excel file
    Returns the file path
    """
    if output_path is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(config.EXPORTS_DIR, f'Date_Factory_Export_{timestamp}.xlsx')
    
    # Ensure the output path is absolute and the directory exists
    output_path = os.path.abspath(output_path)
    
    # Ensure the export directory exists
    export_dir = os.path.dirname(output_path)
    if not os.path.exists(export_dir):
        os.makedirs(export_dir, exist_ok=True)
        print(f"DEBUG: Created export directory: {export_dir}")
    
    print(f"DEBUG: Attempting to create Excel file at: {output_path}")
    print(f"DEBUG: Output directory exists: {os.path.exists(export_dir)}")
    print(f"DEBUG: Output directory is writable: {os.access(export_dir, os.W_OK) if os.path.exists(export_dir) else 'N/A'}")
    
    # Create workbook
    # Try to create the workbook, and if it fails due to permissions, try a fallback location
    original_output_path = output_path
    try:
        workbook = xlsxwriter.Workbook(output_path)
    except PermissionError:
        print(f"Permission denied to write to: {output_path}")
        print("Attempting to use fallback export directory...")
        
        # Try to use a fallback directory in the current working directory
        fallback_dir = os.path.join(os.getcwd(), 'exports')
        if not os.path.exists(fallback_dir):
            os.makedirs(fallback_dir, exist_ok=True)
        
        fallback_path = os.path.join(fallback_dir, os.path.basename(output_path))
        print(f"Using fallback path: {fallback_path}")
        workbook = xlsxwriter.Workbook(fallback_path)
        # Update output_path to the fallback path
        output_path = fallback_path
    except Exception as e:
        print(f"Unexpected error creating workbook: {e}")
        # If there's any other error, also try the fallback
        fallback_dir = os.path.join(os.getcwd(), 'exports')
        if not os.path.exists(fallback_dir):
            os.makedirs(fallback_dir, exist_ok=True)
        
        fallback_path = os.path.join(fallback_dir, os.path.basename(output_path))
        print(f"Using fallback path due to error: {fallback_path}")
        workbook = xlsxwriter.Workbook(fallback_path)
        output_path = fallback_path
    
    # Formats
    header_fmt = workbook.add_format({
        'bold': True, 
        'align': 'center', 
        'valign': 'vcenter', 
        'fg_color': '#2F75B5', 
        'font_color': 'white', 
        'border': 1
    })
    cell_fmt = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
    date_fmt = workbook.add_format({'num_format': 'dd/mm/yyyy', 'align': 'center', 'valign': 'vcenter', 'border': 1})
    num_fmt = workbook.add_format({'num_format': '#,##0.00', 'align': 'center', 'valign': 'vcenter', 'border': 1})
    
    conn = get_connection()
    
    # 1. Customers Sheet
    sheet_customers = workbook.add_worksheet('العملاء (Customers)')
    sheet_customers.right_to_left()
    
    headers_cust = ['#', 'اسم العميل', 'النوع', 'رقم الهاتف', 'تاريخ الإضافة']
    sheet_customers.write_row('A1', headers_cust, header_fmt)
    sheet_customers.set_column('A:A', 10)
    sheet_customers.set_column('B:B', 30)
    sheet_customers.set_column('C:C', 15)
    sheet_customers.set_column('D:D', 20)
    sheet_customers.set_column('E:E', 20)
    
    customers = conn.execute('SELECT * FROM customers ORDER BY name').fetchall()
    for idx, customer in enumerate(customers, start=2):
        sheet_customers.write(idx-1, 0, idx-1, cell_fmt)
        sheet_customers.write(idx-1, 1, customer['name'], cell_fmt)
        sheet_customers.write(idx-1, 2, customer['type'], cell_fmt)
        sheet_customers.write(idx-1, 3, customer['phone'] or '-', cell_fmt)
        sheet_customers.write(idx-1, 4, customer['created_at'][:10] if customer['created_at'] else '-', cell_fmt)
    
    # 2. Weighbridge Sheet
    sheet_wb = workbook.add_worksheet('الميزان (Weighbridge)')
    sheet_wb.right_to_left()
    
    headers_wb = ['التاريخ', 'اسم العميل', 'الوزن الصافي (كجم)', 'سعر القنطار', 'الإجمالي']
    sheet_wb.write_row('A1', headers_wb, header_fmt)
    sheet_wb.set_column('A:A', 15)
    sheet_wb.set_column('B:B', 30)
    sheet_wb.set_column('C:E', 20)
    
    weighbridge = conn.execute('''
        SELECT w.*, c.name as customer_name 
        FROM weighbridge w
        JOIN customers c ON w.customer_id = c.id
        ORDER BY w.date DESC
    ''').fetchall()
    
    for idx, trans in enumerate(weighbridge, start=2):
        sheet_wb.write(idx-1, 0, trans['date'], date_fmt)
        sheet_wb.write(idx-1, 1, trans['customer_name'], cell_fmt)
        sheet_wb.write(idx-1, 2, trans['net_weight'], num_fmt)
        sheet_wb.write(idx-1, 3, trans['price_per_qantar'], num_fmt)
        sheet_wb.write(idx-1, 4, trans['total'], num_fmt)
    
    # 3. Crates Sheet
    sheet_crates = workbook.add_worksheet('الصناديق (Crates)')
    sheet_crates.right_to_left()
    
    headers_crates = ['التاريخ', 'اسم العميل', 'صناديق منصرفة', 'صناديق مرتدة', 'القائم بالتسليم', 'ملاحظات']
    sheet_crates.write_row('A1', headers_crates, header_fmt)
    sheet_crates.set_column('A:A', 15)
    sheet_crates.set_column('B:B', 30)
    sheet_crates.set_column('C:D', 18)
    sheet_crates.set_column('E:F', 25)
    
    crates = conn.execute('''
        SELECT cr.*, c.name as customer_name 
        FROM crates cr
        JOIN customers c ON cr.customer_id = c.id
        ORDER BY cr.date DESC
    ''').fetchall()
    
    for idx, crate in enumerate(crates, start=2):
        sheet_crates.write(idx-1, 0, crate['date'], date_fmt)
        sheet_crates.write(idx-1, 1, crate['customer_name'], cell_fmt)
        sheet_crates.write(idx-1, 2, crate['crates_out'], cell_fmt)
        sheet_crates.write(idx-1, 3, crate['crates_returned'], cell_fmt)
        sheet_crates.write(idx-1, 4, crate['handler'] or '-', cell_fmt)
        sheet_crates.write(idx-1, 5, crate['notes'] or '-', cell_fmt)
    
    # 4. Finance Sheet
    sheet_finance = workbook.add_worksheet('المالية (Finance)')
    sheet_finance.right_to_left()
    
    headers_fin = ['التاريخ', 'اسم العميل', 'نوع المعاملة', 'مدفوع للعميل', 'مقبوض من العميل', 'ملاحظات']
    sheet_finance.write_row('A1', headers_fin, header_fmt)
    sheet_finance.set_column('A:A', 15)
    sheet_finance.set_column('B:B', 30)
    sheet_finance.set_column('C:C', 15)
    sheet_finance.set_column('D:E', 20)
    sheet_finance.set_column('F:F', 25)
    
    finance = conn.execute('''
        SELECT f.*, c.name as customer_name 
        FROM finance f
        JOIN customers c ON f.customer_id = c.id
        ORDER BY f.date DESC
    ''').fetchall()
    
    for idx, fin in enumerate(finance, start=2):
        sheet_finance.write(idx-1, 0, fin['date'], date_fmt)
        sheet_finance.write(idx-1, 1, fin['customer_name'], cell_fmt)
        sheet_finance.write(idx-1, 2, fin['transaction_type'], cell_fmt)
        sheet_finance.write(idx-1, 3, fin['amount_paid'], num_fmt)
        sheet_finance.write(idx-1, 4, fin['amount_received'], num_fmt)
        sheet_finance.write(idx-1, 5, fin['notes'] or '-', cell_fmt)
    
    # 5. Dashboard Summary Sheet
    sheet_summary = workbook.add_worksheet('ملخص العملاء (Summary)')
    sheet_summary.right_to_left()
    
    headers_summary = ['اسم العميل', 'إجمالي الوزن', 'قيمة التوريدات', 'المدفوعات', 'المقبوضات', 'الرصيد', 'صناديق منصرفة', 'صناديق مرتدة', 'رصيد الصناديق']
    sheet_summary.write_row('A1', headers_summary, header_fmt)
    sheet_summary.set_column('A:A', 30)
    sheet_summary.set_column('B:I', 18)
    
    for idx, customer in enumerate(customers, start=2):
        customer_id = customer['id']
        
        # Weighbridge stats
        wb_stats = conn.execute('''
            SELECT 
                COALESCE(SUM(net_weight), 0) as total_weight,
                COALESCE(SUM(total), 0) as total_value
            FROM weighbridge WHERE customer_id = ?
        ''', (customer_id,)).fetchone()
        
        # Finance stats
        fin_stats = conn.execute('''
            SELECT 
                COALESCE(SUM(amount_paid), 0) as total_paid,
                COALESCE(SUM(amount_received), 0) as total_received
            FROM finance WHERE customer_id = ?
        ''', (customer_id,)).fetchone()
        
        # Crates stats
        crate_stats = conn.execute('''
            SELECT 
                COALESCE(SUM(crates_out), 0) as total_out,
                COALESCE(SUM(crates_returned), 0) as total_returned
            FROM crates WHERE customer_id = ?
        ''', (customer_id,)).fetchone()
        
        balance = wb_stats['total_value'] + fin_stats['total_received'] - fin_stats['total_paid']
        crates_balance = crate_stats['total_out'] - crate_stats['total_returned']
        
        sheet_summary.write(idx-1, 0, customer['name'], cell_fmt)
        sheet_summary.write(idx-1, 1, wb_stats['total_weight'], num_fmt)
        sheet_summary.write(idx-1, 2, wb_stats['total_value'], num_fmt)
        sheet_summary.write(idx-1, 3, fin_stats['total_paid'], num_fmt)
        sheet_summary.write(idx-1, 4, fin_stats['total_received'], num_fmt)
        sheet_summary.write(idx-1, 5, balance, num_fmt)
        sheet_summary.write(idx-1, 6, crate_stats['total_out'], cell_fmt)
        sheet_summary.write(idx-1, 7, crate_stats['total_returned'], cell_fmt)
        sheet_summary.write(idx-1, 8, crates_balance, cell_fmt)
    
    conn.close()
    workbook.close()
    
    print(f"Excel file exported successfully: {output_path}")
    return output_path

if __name__ == '__main__':
    export_to_excel()
