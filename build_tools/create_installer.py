"""
Automated Installer Builder for Date Factory Manager
This script automates the entire process of creating a Windows installer:
1. Checks for/installs Inno Setup
2. Builds portable application with PyInstaller
3. Compiles installer with Inno Setup
"""

import os
import sys
import subprocess
import shutil
import urllib.request
import tempfile
from pathlib import Path

# ANSI color codes for Windows console
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def enable_ansi_colors():
    """Enable ANSI color support on Windows"""
    if sys.platform == 'win32':
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

def print_header(text):
    """Print a styled header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text:^70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.ENDC}\n")

def print_step(text):
    """Print a step message"""
    print(f"{Colors.BOLD}{Colors.BLUE}▶ {text}{Colors.ENDC}")

def print_success(text):
    """Print a success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    """Print an error message"""
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")

def print_warning(text):
    """Print a warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")

def print_info(text):
    """Print an info message"""
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.ENDC}")

def find_inno_setup():
    """Find Inno Setup compiler in common installation paths"""
    common_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe",
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    return None

def download_inno_setup():
    """Download and install Inno Setup"""
    print_step("Inno Setup not found. Downloading...")
    
    # Inno Setup download URL (latest stable version)
    url = "https://jrsoftware.org/download.php/is.exe"
    
    try:
        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        installer_path = os.path.join(temp_dir, "innosetup_installer.exe")
        
        print_info(f"Downloading from {url}")
        print_info("This may take a few minutes...")
        
        # Download with progress
        urllib.request.urlretrieve(url, installer_path)
        print_success("Download completed")
        
        # Install silently
        print_step("Installing Inno Setup...")
        print_info("Installing to default location (C:\\Program Files (x86)\\Inno Setup 6)")
        
        result = subprocess.run(
            [installer_path, "/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART"],
            capture_output=True
        )
        
        if result.returncode == 0:
            print_success("Inno Setup installed successfully")
            
            # Clean up
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            # Find the newly installed compiler
            return find_inno_setup()
        else:
            print_error("Failed to install Inno Setup")
            print_error(f"Error: {result.stderr.decode('utf-8', errors='ignore')}")
            return None
            
    except Exception as e:
        print_error(f"Error downloading/installing Inno Setup: {str(e)}")
        return None

def check_inno_setup():
    """Check if Inno Setup is installed, install if not"""
    print_step("Checking for Inno Setup...")
    
    iscc_path = find_inno_setup()
    
    if iscc_path:
        print_success(f"Found Inno Setup at: {iscc_path}")
        return iscc_path
    
    print_warning("Inno Setup not found")
    print_info("Inno Setup is required to create the installer")
    
    response = input(f"\n{Colors.YELLOW}Would you like to download and install it now? (y/n): {Colors.ENDC}").lower()
    
    if response == 'y':
        iscc_path = download_inno_setup()
        if iscc_path:
            return iscc_path
        else:
            print_error("Failed to install Inno Setup automatically")
            print_info("Please download and install manually from: https://jrsoftware.org/isdl.php")
            return None
    else:
        print_info("Please install Inno Setup manually from: https://jrsoftware.org/isdl.php")
        return None

def check_dependencies():
    """Check and install required Python dependencies"""
    print_step("Checking Python dependencies...")
    
    required_packages = {
        'PyInstaller': 'pyinstaller==6.3.0',
        'Pillow': 'Pillow',
    }
    
    for package_name, package_spec in required_packages.items():
        try:
            __import__('PIL' if package_name == 'Pillow' else 'PyInstaller')
            print_success(f"{package_name} is installed")
        except ImportError:
            print_warning(f"{package_name} not found. Installing...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package_spec],
                capture_output=True
            )
            if result.returncode == 0:
                print_success(f"{package_name} installed successfully")
            else:
                print_error(f"Failed to install {package_name}")
                return False
    
    return True

def build_portable_app():
    """Build the portable application using PyInstaller"""
    print_step("Building portable application with PyInstaller...")
    
    # Check if gui_launcher.spec exists
    if not os.path.exists("gui_launcher.spec"):
        print_error("gui_launcher.spec not found!")
        return False
    
    print_info("This may take several minutes...")
    
    # Run PyInstaller
    result = subprocess.run(
        [sys.executable, "-m", "PyInstaller", "--clean", "--noconfirm", "gui_launcher.spec"],
        capture_output=False  # Show output in real-time
    )
    
    if result.returncode != 0:
        print_error("PyInstaller build failed!")
        return False
    
    # Check if output exists
    dist_folder = os.path.join("dist", "DateFactoryPortable")
    if not os.path.exists(dist_folder):
        print_error(f"Build folder not found: {dist_folder}")
        return False
    
    print_success("Portable application built successfully")
    
    # Copy additional files
    print_step("Copying additional files...")
    
    files_to_copy = [
        "../bin/START_SERVER.bat",
        "../bin/STOP_SERVER.bat",
        "../docs/PORTABLE_README.md",
        "../requirements.txt",
        "../README.md",
        "icon.ico",
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, dist_folder)
            print_info(f"Copied {file}")
        else:
            print_warning(f"File not found: {file}")
    
    # Copy database if exists
    db_path = "../src/date_factory.db"
    if os.path.exists(db_path):
        shutil.copy2(db_path, dist_folder)
        print_info("Copied date_factory.db")
    
    # Create exports folder
    exports_folder = os.path.join(dist_folder, "exports")
    if not os.path.exists(exports_folder):
        os.makedirs(exports_folder)
        print_info("Created exports folder")
    
    # Create backups folder
    backups_folder = os.path.join(dist_folder, "backups")
    if not os.path.exists(backups_folder):
        os.makedirs(backups_folder)
        print_info("Created backups folder")
    
    print_success("All files copied successfully")
    return True

def compile_installer(iscc_path):
    """Compile the installer using Inno Setup"""
    print_step("Compiling installer with Inno Setup...")
    
    # Check if installer.iss exists
    if not os.path.exists("installer.iss"):
        print_error("installer.iss not found!")
        return False
    
    print_info("This may take a few minutes...")
    
    # Run Inno Setup compiler
    result = subprocess.run(
        [iscc_path, "installer.iss"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print_error("Inno Setup compilation failed!")
        print_error(result.stderr)
        return False
    
    # Check if output exists
    output_file = os.path.join("..", "installer_output", "DateFactoryManager_Setup.exe")
    if not os.path.exists(output_file):
        print_error(f"Installer not found: {output_file}")
        return False
    
    # Get file size
    file_size = os.path.getsize(output_file)
    file_size_mb = file_size / (1024 * 1024)
    
    print_success(f"Installer compiled successfully")
    print_info(f"File: {os.path.abspath(output_file)}")
    print_info(f"Size: {file_size_mb:.2f} MB")
    
    return True

def main():
    """Main build process"""
    enable_ansi_colors()
    
    # Change CWD to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print_header("🏭 Date Factory Manager - Installer Builder")
    
    print(f"{Colors.BOLD}This script will:{Colors.ENDC}")
    print("  1. Check/install Inno Setup")
    print("  2. Check Python dependencies")
    print("  3. Build portable application")
    print("  4. Compile Windows installer")
    print()
    
    # Step 1: Check Inno Setup
    iscc_path = check_inno_setup()
    if not iscc_path:
        print_error("Cannot proceed without Inno Setup")
        return False
    
    # Step 2: Check dependencies
    if not check_dependencies():
        print_error("Failed to install required dependencies")
        return False
    
    # Step 3: Build portable app
    if not build_portable_app():
        print_error("Failed to build portable application")
        return False
    
    # Step 4: Compile installer
    if not compile_installer(iscc_path):
        print_error("Failed to compile installer")
        return False
    
    # Success!
    print_header("🎉 Build Completed Successfully!")
    
    print(f"{Colors.BOLD}Your installer is ready:{Colors.ENDC}")
    print(f"  📁 Location: {Colors.GREEN}{os.path.abspath('installer_output')}{Colors.ENDC}")
    print(f"  📦 File: {Colors.GREEN}DateFactoryManager_Setup.exe{Colors.ENDC}")
    print()
    print(f"{Colors.BOLD}Next steps:{Colors.ENDC}")
    print("  1. Test the installer on your computer")
    print("  2. Test on a computer without Python installed")
    print("  3. Distribute the installer to users")
    print()
    print(f"{Colors.CYAN}Users just need to:{Colors.ENDC}")
    print("  • Download the installer")
    print("  • Run it")
    print("  • Follow the wizard")
    print("  • Launch from desktop or Start Menu")
    print()
    print(f"{Colors.GREEN}✨ No Python or dependencies required on target machines!{Colors.ENDC}")
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print()
        print_warning("Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print()
        print_error(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
