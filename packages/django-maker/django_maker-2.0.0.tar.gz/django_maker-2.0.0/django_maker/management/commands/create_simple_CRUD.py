import re
from django.core.management.base import BaseCommand
import os
from .function import *

class Command(BaseCommand):
    help = 'Generate simple CRUD'
    
    def generate_crud(self,new_directory,app_name,modal_name):
        class_name = modal_name.capitalize()
        code = f"""from django.core import serializers
import json
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from .models import {class_name}

"""
        code+=f"""
def {class_name}All(request):
    {modal_name} = {class_name}.objects.all()
    {modal_name}_dict = serializers.serialize("json", {modal_name})
    res = json.loads({modal_name}_dict)
    return JsonResponse({{"resultat": res}})\n\n
"""

        code+=f"""
def {class_name}Detail(request,id):
    {modal_name} = {class_name}.objects.filter(id=id)
    {modal_name}_dict = serializers.serialize("json", {modal_name})
    res = json.loads({modal_name}_dict)
    return JsonResponse({{"resultat": res}})\n\n
"""
        
        formated_code = f'from .serializer import *\n'+code
        code = formated_code
        code+=f"""
def {class_name}Create(request):
    data = JSONParser().parse(request)
    serializer  = {class_name}Serializer(data=data)
    if serializer.is_valid():
        serializer.save()
    return JsonResponse({{"message": "added successfully"}})\n\n
"""
        
        code+=f"""
def {class_name}Delete(request,id):
    {modal_name} = {class_name}.objects.get(id=id)
    {modal_name}.delete()
    return JsonResponse({{"message": "deleted successfully"}})\n\n
"""
        
        code+=f"""
def {class_name}Update(request,id):
    data = JSONParser().parse(request)
    {modal_name} = {class_name}.objects.get(id=id)
    serializer = {class_name}Serializer({modal_name},data=data)
    if serializer.is_valid():
        serializer.save()
    return JsonResponse({{"message": "updated successfully"}})\n\n
"""

        with open(f"{new_directory}/views.py", "w") as model_file:
            model_file.write(code)
        
    def generate_url(self,new_directory,app_name,modal_name,bool,your_settingFile_directory):
        code=f"""from django.urls import path, include
from . import views
"""
        urlpatterns = []
        urlpatterns_content = f"""
        path('{modal_name.capitalize()}All', views.{modal_name.capitalize()}All, name='{modal_name.capitalize()}All'),
        path('{modal_name.capitalize()}Detail/<int:id>', views.{modal_name.capitalize()}Detail, name='{modal_name.capitalize()}Detail'),
        path('{modal_name.capitalize()}Create', views.{modal_name.capitalize()}Create, name='{modal_name.capitalize()}Create'),
        path('{modal_name.capitalize()}Delete/<int:id>', views.{modal_name.capitalize()}Delete, name='{modal_name.capitalize()}Delete'),
        path('{modal_name.capitalize()}Update/<int:id>', views.{modal_name.capitalize()}Update, name='{modal_name.capitalize()}Update'),
        """
        urlpatterns.append(urlpatterns_content)
        urlpatterns_string = 'urlpatterns = ['+''.join(urlpatterns)
        code+=urlpatterns_string+']'
        
        with open(your_settingFile_directory+'/urls.py', "r") as f:
            content = f.read()
        # Define the pattern to look for the import statement
        import_pattern = r"from\s+django\.urls\s+import\s+path"

        # Find the match using regular expression
        match = re.search(import_pattern, content)

        # If the import statement is found, insert "include" after it
        if match:
            index = match.end()
            updated_content = content[:index] + ', include ' + content[index:]
        with open(your_settingFile_directory+'/urls.py', "w") as f:
            f.write(updated_content)
        with open(your_settingFile_directory+'/urls.py', "r") as f:
            content = f.read()
        # Find the INSTALLED_APPS list in the content
        start_index = content.find("urlpatterns  = [") + len("urlpatterns  = [")
        end_index = content.find("]", start_index)

        # Extract the INSTALLED_APPS list
        installed_apps = content[start_index:end_index].strip()
        if bool==True:
            # Add the new app to the list
            path = f"path('backend.{app_name}/', include('backend.{app_name}.urls'))"
            updated_installed_apps = installed_apps[:-1] + installed_apps[-1] + f'\n    {path},\n' 
        else:
            path = f"path('{app_name}/', include('{app_name}.urls'))"
            # Add the new app to the list
            updated_installed_apps = installed_apps[:-1] + installed_apps[-1] + f'\n    {path},\n' 

        # Replace the old INSTALLED_APPS list with the updated one
        updated_content = content[:start_index] + updated_installed_apps + content[end_index:]

        with open(your_settingFile_directory+'/urls.py', "w") as f:
            f.write(updated_content)
        with open(f"{new_directory}/urls.py", "w") as model_file:
            model_file.write(code)
            
    def find_folder(self,start_path, folder_name):
        for root, dirs, files in os.walk(start_path):
            if folder_name in dirs:
                return os.path.join(root, folder_name)

        return None
    
    def find_manage_directory(self,start_dir, file_name):
        for root, dirs, files in os.walk(start_dir):
            if file_name in files:
                return os.path.abspath(root)

        return None
    
    def list_app(setting_file_path):
        with open(setting_file_path+'/settings.py', "r") as f:
            content = f.read()
        start_index = content.find("INSTALLED_APPS = [") + len("INSTALLED_APPS = [")
        end_index = content.find("]", start_index)
        installed_apps = content[start_index:end_index].strip('\n')
        return installed_apps

    def handle(self, *args, **options):
        try:
            directory_path = os.getcwd()
            manage_path = self.find_manage_directory(directory_path, 'manage.py')
            settings_path = self.find_manage_directory(directory_path, 'settings.py')
            
            while True:
                app_name = input('tape ur app_name:\n> ')
                options = list_app(settings_path)
                app_names_list = [app.strip().strip("'\"") for app in options.split(',')]

                words = app_name.split()
                last_element = words[-1]

                closest_match = find_closest_match(app_name, app_names_list)
                if closest_match == None:
                    print("please try again")
                elif closest_match != True:
                    print(f"Unknown app: '{last_element}' Did you mean '{closest_match}'?.")
                elif app_name == '':
                    print('app name must not be empty')
                else:
                    break
            folder_path = self.find_folder('/', app_name)
            modal_name = input("name of models do you want to create a simple CRUD?:\n> ")
            self.generate_crud(folder_path,app_name,modal_name)
            folder_path = self.find_folder('/', app_name)
            # Split the path using the directory separator '/'
            path_elements = folder_path.split(os.path.sep)
            new_path_elements = path_elements[:-1]
            new_path = os.path.sep.join(new_path_elements)
            manage_path = self.find_manage_directory(new_path, 'manage.py')
            settings_path = self.find_manage_directory(new_path, 'settings.py')
            if settings_path ==None:
                new_path_elements = path_elements[:-2]
                new_path = os.path.sep.join(new_path_elements)
                manage_path = self.find_manage_directory(new_path, 'manage.py')
                settings_path = self.find_manage_directory(new_path, 'settings.py')
            if folder_path != manage_path+'/'+app_name:
                self.generate_url(folder_path,app_name,modal_name,True,settings_path)
            else:
                self.generate_url(folder_path,app_name,modal_name,False,settings_path)
        except KeyboardInterrupt:
            # Handle Ctrl+C
            print("\nOperation interrupted. Exiting gracefully.")