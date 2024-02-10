import importlib.metadata
import subprocess

def install_package(package_name):
    try:
        subprocess.check_call(['pip', 'install', package_name])
        print(f"Successfully installed {package_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}: {e.output}")
        
lib_name_list = ["pandas", "pygame"]
lib_version_list = ["2.1.3", "2.52"]


for i, lib in enumerate(lib_version_list):
    print("Package name: %s, version to be installed %s" % (lib_name_list[i], lib))
    
print('\nDo you want to install these packages?\nType y if yes and n if no')

x = input()

if x == 'y':
    # Install packages
    for i, lib in enumerate(lib_version_list):
        package_name = lib_name_list[i] + "==" + lib
        install_package(package_name)
