import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import license_manager

# ANSI Colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print(f"{Colors.HEADER}{Colors.BOLD}╔════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}║      Date Factory Manager - KeyGen         ║{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}╚════════════════════════════════════════════╝{Colors.ENDC}")
    print(f"{Colors.RED}{Colors.BOLD}KEEP THIS TOOL PRIVATE! DO NOT DISTRIBUTE!{Colors.ENDC}")
    print()
    
    while True:
        print(f"{Colors.BLUE}Enter Customer Machine ID (XXXX-XXXX-XXXX-XXXX):{Colors.ENDC}")
        machine_id = input("> ").strip().upper()
        
        if not machine_id:
            print(f"{Colors.RED}Machine ID cannot be empty.{Colors.ENDC}")
            continue
            
        print(f"\n{Colors.BLUE}Enter Customer Name (Optional):{Colors.ENDC}")
        client_name = input("> ").strip()
        if not client_name:
            client_name = "Valued Customer"
            
        print(f"\n{Colors.BLUE}Enter Expiration Date (YYYY-MM-DD) or press Enter for Lifetime:{Colors.ENDC}")
        exp_date = input("> ").strip()
        if not exp_date:
            exp_date = None
            
        # Generate Key
        try:
            license_key = license_manager.generate_license_key(machine_id, client_name, exp_date)
            
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ License Key Generated Successfully!{Colors.ENDC}")
            print("-" * 60)
            print(f"{Colors.YELLOW}{license_key}{Colors.ENDC}")
            print("-" * 60)
            print("Copy this key and send it to the customer.")
            
        except Exception as e:
            print(f"{Colors.RED}Error generating key: {e}{Colors.ENDC}")
            
        print("\nGenerate another? (y/n)")
        if input("> ").lower() != 'y':
            break
        print("\n" * 2)

if __name__ == "__main__":
    main()
