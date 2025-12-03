"""
Security utilities for Date Factory Manager
Handles password hashing, input validation, and security functions
"""
from werkzeug.security import generate_password_hash, check_password_hash
import re
import html
import json
import os
from datetime import datetime, timedelta

class SecurityUtils:
    """Security utility functions"""
    
    @staticmethod
    def hash_password(password):
        """Generate a secure hash for password"""
        return generate_password_hash(password, method='scrypt', salt_length=16)
    
    @staticmethod
    def verify_password(password_hash, password):
        """Verify password against hash"""
        try:
            return check_password_hash(password_hash, password)
        except Exception:
            return False
    
    @staticmethod
    def validate_input(data, field_name, field_type='string', required=True, min_length=0, max_length=1000):
        """
        Validate and sanitize input data
        
        Args:
            data: Input data to validate
            field_name: Name of the field (for error messages)
            field_type: Type of validation ('string', 'email', 'number', 'date')
            required: Whether field is required
            min_length: Minimum length for strings
            max_length: Maximum length for strings
        
        Returns:
            tuple: (is_valid, sanitized_data, error_message)
        """
        if data is None or data == '':
            if required:
                return False, None, f"{field_name} is required"
            return True, None, None
        
        try:
            # Type validation and sanitization
            if field_type == 'string':
                if not isinstance(data, str):
                    return False, None, f"{field_name} must be a string"
                
                # Sanitize HTML and trim
                sanitized = html.escape(data.strip())
                
                # Length validation
                if len(sanitized) < min_length:
                    return False, None, f"{field_name} must be at least {min_length} characters"
                if len(sanitized) > max_length:
                    return False, None, f"{field_name} must be less than {max_length} characters"
                
                return True, sanitized, None
                
            elif field_type == 'email':
                email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_regex, data):
                    return False, None, f"{field_name} must be a valid email"
                return True, data.strip().lower(), None
                
            elif field_type == 'number':
                try:
                    num = float(data)
                    return True, num, None
                except ValueError:
                    return False, None, f"{field_name} must be a number"
                    
            elif field_type == 'date':
                try:
                    # Validate date format (YYYY-MM-DD)
                    datetime.strptime(data, '%Y-%m-%d')
                    return True, data, None
                except ValueError:
                    return False, None, f"{field_name} must be in YYYY-MM-DD format"
                    
            else:
                return False, None, f"Invalid field type: {field_type}"
                
        except Exception as e:
            return False, None, f"Error validating {field_name}: {str(e)}"
    
    @staticmethod
    def validate_customer_data(data):
        """Validate customer data"""
        errors = []
        
        # Validate name
        is_valid, name, error = SecurityUtils.validate_input(
            data.get('name'), 'Name', 'string', required=True, min_length=1, max_length=100
        )
        if not is_valid:
            errors.append(error)
        
        # Validate type
        valid_types = ['تاجر', 'عميل عادي', 'retail', 'wholesale']
        customer_type = data.get('type', '').strip()
        if customer_type not in valid_types:
            errors.append("Customer type must be 'تاجر' or 'عميل عادي'")
        
        # Validate phone (optional)
        if data.get('phone'):
            is_valid, phone, error = SecurityUtils.validate_input(
                data.get('phone'), 'Phone', 'string', required=False, max_length=20
            )
            if not is_valid:
                errors.append(error)
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_transaction_data(data, transaction_type='weighbridge'):
        """Validate transaction data"""
        errors = []
        
        # Validate date
        is_valid, date, error = SecurityUtils.validate_input(
            data.get('date'), 'Date', 'date', required=True
        )
        if not is_valid:
            errors.append(error)
        
        # Validate customer_id
        try:
            customer_id = int(data.get('customer_id'))
            if customer_id <= 0:
                errors.append("Customer ID must be a positive integer")
        except (ValueError, TypeError):
            errors.append("Customer ID is required and must be a number")
        
        if transaction_type == 'weighbridge':
            # Validate net_weight
            try:
                net_weight = float(data.get('net_weight'))
                if net_weight <= 0:
                    errors.append("Net weight must be positive")
            except (ValueError, TypeError):
                errors.append("Net weight is required and must be a number")
            
            # Validate price_per_qantar
            try:
                price_per_qantar = float(data.get('price_per_qantar'))
                if price_per_qantar <= 0:
                    errors.append("Price per qantar must be positive")
            except (ValueError, TypeError):
                errors.append("Price per qantar is required and must be a number")
        
        elif transaction_type == 'finance':
            # Validate transaction_type
            valid_transaction_types = ['دفع', 'قبض', 'payment', 'receipt']
            trans_type = data.get('transaction_type', '').strip()
            if trans_type not in valid_transaction_types:
                errors.append("Transaction type must be 'دفع' or 'قبض'")
            
            # Validate amounts
            amount_paid = data.get('amount_paid', 0) or 0
            amount_received = data.get('amount_received', 0) or 0
            
            try:
                amount_paid = float(amount_paid)
                amount_received = float(amount_received)
                
                if amount_paid < 0 or amount_received < 0:
                    errors.append("Amounts cannot be negative")
                
                if amount_paid == 0 and amount_received == 0:
                    errors.append("At least one amount (paid or received) must be greater than 0")
                    
            except (ValueError, TypeError):
                errors.append("Amounts must be valid numbers")
        
        elif transaction_type == 'crates':
            # Validate crate numbers
            try:
                crates_out = int(data.get('crates_out', 0) or 0)
                crates_returned = int(data.get('crates_returned', 0) or 0)
                
                if crates_out < 0 or crates_returned < 0:
                    errors.append("Crate numbers cannot be negative")
                    
            except (ValueError, TypeError):
                errors.append("Crate numbers must be valid integers")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def sanitize_filename(filename):
        """Sanitize filename for safe file operations"""
        # Remove or replace dangerous characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
        sanitized = re.sub(r'\.\.+', '.', sanitized)  # Remove multiple dots
        sanitized = sanitized.strip('. ')  # Remove leading/trailing dots and spaces
        
        # Limit length
        if len(sanitized) > 255:
            name, ext = os.path.splitext(sanitized)
            sanitized = name[:251-len(ext)] + ext
        
        return sanitized
    
    @staticmethod
    def log_security_event(event_type, details, user_id=None):
        """
        Log security events (implementation can be expanded)
        For now, just print to console - in production, send to proper logging system
        """
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'event_type': event_type,
            'user_id': user_id,
            'details': details,
            'ip_address': 'unknown'  # Can be enhanced to capture actual IP
        }
        
        print(f"SECURITY LOG: {json.dumps(log_entry, ensure_ascii=False)}")
        
        # In production, you might want to:
        # - Send to dedicated logging service
        # - Store in secure log database
        # - Alert administrators for critical events