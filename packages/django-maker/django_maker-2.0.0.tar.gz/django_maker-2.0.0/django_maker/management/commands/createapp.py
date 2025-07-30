import shutil
from django.core.management.base import BaseCommand
import os
import subprocess

class Command(BaseCommand):
    help = 'Creates a new Django app'
    
    def copy_directory(self, source_path, destination_path):
        try:
            shutil.move(source_path, destination_path)
            print(f"Directory copied from {source_path} to {destination_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def update_app_name(self,path_app):
        path_app = path_app + '/apps.py'
        try:
            with open(path_app, 'r') as file:
                content = file.read()
            start_index = content.find("name = '") + len("name = '")
            end_index = content.find("'", start_index)
            app_name = content[start_index:end_index]
            old_name_pattern = f"name = '{app_name}'"
            new_name_pattern = f"name = 'backend.{app_name}'"
            content = content.replace(old_name_pattern, new_name_pattern)
            with open(path_app, 'w') as file:
                file.write(content)
            print(f"Updated the name attribute in {path_app} to backend.{app_name}")
        except FileNotFoundError:
            print(f"Error: {app_name} app not found in {path_app}")
    
    def config_settings(self,bool,your_app_name,your_settingFile_directory):
        with open(your_settingFile_directory+'/settings.py', "r") as f:
            content = f.read()
        # Find the INSTALLED_APPS list in the content
        start_index = content.find("INSTALLED_APPS = [") + len("INSTALLED_APPS = [")
        end_index = content.find("]", start_index)
        # Extract the INSTALLED_APPS list
        installed_apps = content[start_index:end_index].strip()
        if bool==True:
            # Add the new app to the list
            updated_installed_apps = installed_apps[:-1] + installed_apps[-1] + f'\n    "backend.{your_app_name}",\n' 
        else:
            # Add the new app to the list
            updated_installed_apps = installed_apps[:-1] + installed_apps[-1] + f'\n    "{your_app_name}",\n' 
        # Replace the old INSTALLED_APPS list with the updated one
        updated_content = content[:start_index] + updated_installed_apps + content[end_index:]
        # Write the updated content back to the settings.py file
        with open(your_settingFile_directory+'/settings.py', "w") as f:
            f.write(updated_content)
    
    def find_folder(self,start_path, folder_name):
        for root, dirs, files in os.walk(start_path):
            if folder_name in dirs:
                return os.path.join(root, folder_name)
        return None
    
    def find_settings_directory(self,start_dir, file_name):
        for root, dirs, files in os.walk(start_dir):
            if file_name in files:
                return os.path.abspath(root)
        return None
    
    def checkappname(self,app_name,setting_file_path):
        with open(setting_file_path+'/settings.py', "r") as f:
            content = f.read()
        start_index = content.find("INSTALLED_APPS = [") + len("INSTALLED_APPS = [")
        end_index = content.find("]", start_index)
        installed_apps = content[start_index:end_index].strip('\n')
        if app_name in installed_apps:
            return True
        else:
            return False
        
    def handle(self, *args, **options):
        try:
            directory_path = os.getcwd()
            app_name = input("Your app name?: ")
            if app_name !='':
                settings_path = self.find_settings_directory(directory_path, 'settings.py')
                while True:
                    if self.checkappname(app_name,settings_path) == False:
                        try:
                            os.chdir(directory_path)
                            subprocess.run(['python', 'manage.py', 'startapp', app_name], check=True, capture_output=True, text=True)
                            app_added = True
                            break
                        finally:
                            os.chdir(os.path.dirname(os.path.realpath(__file__)))
                            break
                    else:
                        print('Application labels are exist try another name')
                        app_added = False
                        break
                while app_added:
                    choice = input("Are you sure you want to change directory to backend? (yes/no): ").strip().lower()
                    if choice == "yes":
                        folder_path = self.find_folder('/', app_name)
                        # Split the path using the directory separator '/'
                        path_elements = folder_path.split(os.path.sep)
                        # Remove the last element
                        new_path_elements = path_elements[:-1]
                        # Join the remaining elements back into a path
                        new_path = os.path.sep.join(new_path_elements)
                        destination_path = new_path+'/backend'
                        self.copy_directory(folder_path, destination_path)
                        self.update_app_name(destination_path+'/'+app_name)
                        settings_path = self.find_settings_directory(new_path, 'settings.py')
                        self.config_settings(True,app_name,settings_path)
                        break
                    elif choice == "no":
                        print("Operation cancelled.")
                        folder_path = self.find_folder('/', app_name)
                        # Split the path using the directory separator '/'
                        path_elements = folder_path.split(os.path.sep)
                        # Remove the last element
                        new_path_elements = path_elements[:-1]
                        # Join the remaining elements back into a path
                        new_path = os.path.sep.join(new_path_elements)
                        settings_path = self.find_settings_directory(new_path, 'settings.py')
                        self.config_settings(False,app_name,settings_path)
                        break
                    else:
                        choice = input("Must be yes or no: ").strip().lower()
            else:
                print('app name must not be empty')
        except KeyboardInterrupt:
            # Handle Ctrl+C
            print("\nOperation interrupted. Exiting gracefully.")