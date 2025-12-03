"""
More detailed test to find the internal server error
"""
import sys
import traceback

try:
    from app import app
    
    print("Testing all main routes...")
    with app.test_client() as client:
        routes_to_test = [
            ('/', 'Root'),
            ('/activate', 'Activate'),
            ('/login', 'Login'),
            ('/dashboard', 'Dashboard'),
            ('/customers', 'Customers'),
            ('/weighbridge', 'Weighbridge'),
            ('/crates', 'Crates'),
            ('/finance', 'Finance'),
            ('/settings', 'Settings'),
            ('/reports', 'Reports'),
        ]
        
        for route, name in routes_to_test:
            try:
                print(f"\n{'='*50}")
                print(f"Testing: {name} ({route})")
                response = client.get(route, follow_redirects=True)
                print(f"Status: {response.status_code}")
                
                if response.status_code == 500:
                    print(f"❌ INTERNAL SERVER ERROR!")
                    print(f"Response preview: {response.data.decode()[:500]}")
                elif response.status_code >= 400:
                    print(f"⚠️  Error status")
                    print(f"Response preview: {response.data.decode()[:200]}")
                else:
                    print(f"✓ OK")
                    
            except Exception as e:
                print(f"❌ Exception: {e}")
                traceback.print_exc()
        
except Exception as e:
    print(f"\n❌ FATAL ERROR: {e}")
    traceback.print_exc()
