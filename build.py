# Edge Light - Build Script
# Creates standalone Windows executable using PyInstaller

import subprocess
import sys
import os

def build():
    """Build the Edge Light executable."""
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(script_dir, 'src')
    main_script = os.path.join(src_dir, 'main.py')
    icon_path = os.path.join(script_dir, 'icon.ico')
    
    # Check if icon exists
    icon_option = []
    if os.path.exists(icon_path):
        icon_option = [f'--icon={icon_path}']
        print(f"Using custom icon: {icon_path}")
    else:
        print("Warning: icon.ico not found, using default icon")
    
    # PyInstaller options
    options = [
        'pyinstaller',
        '--name=EdgeLight',
        '--onefile',                    # Single executable
        '--windowed',                   # No console window
        '--noconsole',                  # Suppress console
        f'--distpath={script_dir}\\dist',
        f'--workpath={script_dir}\\build',
        f'--specpath={script_dir}',
        '--clean',                      # Clean cache before building
        
        # Add icon file as data so it can be loaded at runtime
        f'--add-data={icon_path};.',
        
        # Hidden imports that PyInstaller might miss
        '--hidden-import=keyboard',
        '--hidden-import=PyQt5.sip',
        
        *icon_option,  # Add icon to executable
        
        main_script
    ]
    
    print("=" * 60)
    print("Building Edge Light executable...")
    print("=" * 60)
    
    try:
        subprocess.run(options, check=True)
        print("\n" + "=" * 60)
        print("✅ Build successful!")
        print(f"   Executable: {script_dir}\\dist\\EdgeLight.exe")
        print("=" * 60)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build()
