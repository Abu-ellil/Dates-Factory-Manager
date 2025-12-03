"""
Build script to create portable version of Date Factory Manager
"""
import os
import sys
import shutil
import subprocess

def main():
    print("=" * 60)
    print("🔨 Building Portable Date Factory Manager")
    print("=" * 60)
    print()
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller==6.3.0"])
        print("✅ PyInstaller installed")
    
    print()
    print("📦 Building executable with PyInstaller...")
    print()
    
    # Run PyInstaller with spec file
    result = subprocess.run([
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        "app.spec"
    ])
    
    if result.returncode != 0:
        print()
        print("❌ Build failed!")
        return False
    
    print()
    print("=" * 60)
    print("✅ Build completed successfully!")
    print("=" * 60)
    print()
    
    # Copy additional files to dist folder
    dist_folder = os.path.join("dist", "DateFactoryPortable")
    
    if os.path.exists(dist_folder):
        print("📋 Copying additional files...")
        
        # Copy batch files
        files_to_copy = [
            "START_SERVER.bat",
            "STOP_SERVER.bat",
            "PORTABLE_README.md",
        ]
        
        for file in files_to_copy:
            if os.path.exists(file):
                shutil.copy2(file, dist_folder)
                print(f"   ✓ {file}")
        
        # Copy database if exists
        if os.path.exists("date_factory.db"):
            shutil.copy2("date_factory.db", dist_folder)
            print(f"   ✓ date_factory.db")
        
        # Create exports folder
        exports_folder = os.path.join(dist_folder, "exports")
        if not os.path.exists(exports_folder):
            os.makedirs(exports_folder)
            print(f"   ✓ exports folder created")
        
        print()
        print("=" * 60)
        print("🎉 Portable application is ready!")
        print("=" * 60)
        print()
        print(f"📁 Location: {os.path.abspath(dist_folder)}")
        print()
        print("📝 Next steps:")
        print("   1. Go to the 'dist/DateFactoryPortable' folder")
        print("   2. Double-click 'START_SERVER.bat' to run")
        print("   3. Copy the entire folder to any Windows PC")
        print()
        print("💡 The portable version includes:")
        print("   ✓ Python runtime")
        print("   ✓ All required libraries")
        print("   ✓ Database and templates")
        print("   ✓ Easy startup script")
        print()
        
        return True
    else:
        print("❌ Build folder not found!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
