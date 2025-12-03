"""
Direct test of the activate route
"""
import sys
import os

# Set up the environment
os.chdir(r'c:\Users\MAS\Desktop\QQQ\src')

try:
    print("Importing app...")
    from app import app
    
    print("Creating test client...")
    with app.app_context():
        with app.test_client() as client:
            print("\nTesting GET /activate...")
            try:
                response = client.get('/activate')
                print(f"Status Code: {response.status_code}")
                print(f"Content-Type: {response.content_type}")
                
                if response.status_code == 500:
                    print("\n❌ INTERNAL SERVER ERROR!")
                    print("Response:")
                    print(response.data.decode('utf-8'))
                elif response.status_code == 302:
                    print(f"✓ Redirect to: {response.location}")
                else:
                    print(f"✓ Success! Content length: {len(response.data)}")
                    
            except Exception as e:
                print(f"\n❌ Exception occurred: {e}")
                import traceback
                traceback.print_exc()
                
except Exception as e:
    print(f"\n❌ Fatal error: {e}")
    import traceback
    traceback.print_exc()
