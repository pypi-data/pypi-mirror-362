import re
from django.core.management.base import BaseCommand
import os
import subprocess
from .function import *

class Command(BaseCommand):
    help = 'Generate models'
    def update_proprety(self,new_directory,proprety_name,new_line):
        with open(f"{new_directory}/models.py", "r") as file:
            lines = file.readlines()
        print({"proprety_name":proprety_name})
        found = False
        for i, line in enumerate(lines):
            if proprety_name in line:
                lines[i] = new_line
                found = True
                break

        if found:
            with open(f"{new_directory}/models.py", "w") as file:
                file.writelines(lines)
            print(f"The line containing '{proprety_name}' has been replaced.")
        else:
            meta_index = None
            for i, line in enumerate(lines):
                if line.strip().startswith("class Meta:"):
                    meta_index = i
                    break

            if meta_index is not None:
                # Add the new property before class Meta
                indentation = lines[meta_index - 1].find("class ")
                new_property_line = f"{' ' * indentation}{new_line}\n"  # Replace '...' with the actual definition of the new property
                lines.insert(meta_index, new_property_line)

                with open(f"{new_directory}/models.py", "w") as file:
                    file.writelines(lines)
            
    def generate_models(self,new_directory,app_name):
        modal_name = input('Class name of the modal to create:\n> ')
        class_name = modal_name.capitalize()
        if checkModelExist(app_name,class_name) == False:
            model_class_str = f'from django.db import models \n\nclass {class_name}(models.Model):\n'
            while True:
                property_name = input('New property name (press Enter to stop adding fields):\n> ')
                if not property_name:
                    break
                while True:
                    field_type = input('Field type (enter ? to see all types) [CharField]:\n> ')
                    if field_type == "?":
                        print('- CharField\n- BooleanField\n- IntegerField\n- DateTimeField\n- JSONField\n- URLField\n- FloatField\n- EmailField\n- relation')
                    elif field_type in ['CharField', 'BooleanField', 'IntegerField', 'DateTimeField', 'JSONField', 'URLField', 'FloatField', 'EmailField', 'relation']:
                        break
                    else:
                        print('Invalid field type. Please enter a valid field type or "?" to see all types.')
                if field_type =="CharField":
                    model_class_str += f'    {property_name} = models.CharField('
                    max_length = input('Field length [200]:\n> ')
                    if max_length=='':
                        max_length=200
                    model_class_str += f'max_length={max_length}, '
                    while True:    
                        null = input('Can this field be null in the database (nullable) (yes/no)\n> ')
                        if null =='yes':
                            model_class_str += f'null=True, '
                            break
                        elif null =='no':
                            model_class_str += f'null=False, '
                            break
                        else:
                            choice = print("Must be yes or no")
                    while True:
                        unique = input('Can this field be unique in the database (yes/no)\n> ')
                        if unique =='yes':
                            model_class_str += f'unique=True)\n'
                            break
                        elif unique =='no':
                            model_class_str += f'unique=False)\n'
                            break
                        else:
                            choice = print("Must be yes or no")
                if field_type =="EmailField":
                    model_class_str += f'    {property_name} = models.EmailField('
                    max_length = input('Field length [200]:\n> ')
                    if max_length=='':
                        max_length=200
                    model_class_str += f'max_length={max_length}, '
                    while True:    
                        null = input('Can this field be null in the database (nullable) (yes/no)\n> ')
                        if null =='yes':
                            model_class_str += f'null=True, '
                            break
                        elif null =='no':
                            model_class_str += f'null=False, '
                            break
                        else:
                            choice = print("Must be yes or no")
                    while True:
                        unique = input('Can this field be unique in the database (yes/no)\n> ')
                        if unique =='yes':
                            model_class_str += f'unique=True)\n'
                            break
                        elif unique =='no':
                            model_class_str += f'unique=False)\n'
                            break
                        else:
                            choice = print("Must be yes or no")
                if field_type =="URLField":
                    model_class_str += f'    {property_name} = models.URLField('
                    max_length = input('Field length [800]:\n> ')
                    if max_length=='':
                        max_length=800
                    model_class_str += f'max_length={max_length}, '
                    while True:    
                        null = input('Can this field be null in the database (nullable) (yes/no)\n> ')
                        if null =='yes':
                            model_class_str += f'null=True, '
                            break
                        elif null =='no':
                            model_class_str += f'null=False, '
                            break
                        else:
                            choice = print("Must be yes or no")
                    while True:
                        unique = input('Can this field be unique in the database (yes/no)\n> ')
                        if unique =='yes':
                            model_class_str += f'unique=True)\n'
                            break
                        elif unique =='no':
                            model_class_str += f'unique=False)\n'
                            break
                        else:
                            choice = print("Must be yes or no")
                if field_type =="BooleanField":
                    model_class_str += f'    {property_name} = models.BooleanField('
                    while True:
                        null = input('Can this field be null in the database (nullable) (yes/no)\n> ')
                        if null =='yes':
                            model_class_str += f'null=True, '
                            break
                        elif null =='no':
                            model_class_str += f'null=False, '
                            break
                        else:
                            choice = print("Must be yes or no")
                    while True:
                        default = input('Can this field be default in the database (true/false)\n> ')
                        if default =='true':
                            model_class_str += f'default=True)\n'
                            break
                        elif default =='false':
                            model_class_str += f'default=False)\n'
                            break
                        else:
                            choice = print("Must be true or false")
                if field_type =="IntegerField":
                    model_class_str += f'    {property_name} = models.IntegerField('
                    while True:
                        null = input('Can this field be null in the database (nullable) (yes/no)\n> ')
                        if null =='yes':
                            model_class_str += f'null=True, '
                            break
                        elif null =='no':
                            model_class_str += f'null=False, '
                            break
                        else:
                            choice = print("Must be yes or no")
                    while True:
                        unique = input('Can this field be unique in the database (yes/no)\n> ')
                        if unique =='yes':
                            model_class_str += f'unique=True)\n'
                            break
                        elif unique =='no':
                            model_class_str += f'unique=False)\n'
                            break
                        else:
                            choice = print("Must be yes or no")
                    while True:
                        default = input('Can this field be default in the database (true/false)\n> ')
                        if default !='':
                            default_value  = input('entre your default value:\n> ')
                            model_class_str += f'default={default_value})\n'
                            break
                        else:
                            break
                if field_type =="FloatField":
                    model_class_str += f'    {property_name} = models.FloatField('
                    while True:
                        null = input('Can this field be null in the database (nullable) (yes/no)\n> ')
                        if null =='yes':
                            model_class_str += f'null=True, '
                            break
                        elif null =='no':
                            model_class_str += f'null=False, '
                            break
                        else:
                            choice = print("Must be yes or no")
                    while True:
                        unique = input('Can this field be unique in the database (yes/no)\n> ')
                        if unique =='yes':
                            model_class_str += f'unique=True)\n'
                            break
                        elif unique =='no':
                            model_class_str += f'unique=False)\n'
                            break
                        else:
                            choice = print("Must be yes or no")
                    while True:
                        default = input('Can this field be default in the database (true/false)\n> ')
                        if default !='':
                            default_value  = input('entre your default value:\n> ')
                            model_class_str += f'default={default_value})\n'
                            break
                        else:
                            break
                if field_type =="DateTimeField":
                    model_class_str += f'    {property_name} = models.DateTimeField('
                    while True:
                        null = input('Can this field be null in the database (nullable) (yes/no)\n> ')
                        if null =='yes':
                            model_class_str += f'null=True, '
                            break
                        elif null =='no':
                            model_class_str += f'null=False, '
                            break
                        else:
                            choice = print("Must be yes or no")
                if field_type =="JSONField":
                    model_class_str += f'    {property_name} = models.JSONField('
                    while True:
                        null = input('Can this field be null in the database (nullable) (yes/no)\n> ')
                        if null =='yes':
                            model_class_str += f'null=True, '
                            break
                        elif null =='no':
                            model_class_str += f'null=False, '
                            break
                        else:
                            choice = print("Must be yes or no")
                if field_type =="relation":
                    while True:
                        class_relation = input('What class should this entity be related to?:\n> ')
                        result = subprocess.run(['python', 'manage.py', 'find_model', class_relation],
                                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        if 'Found the model class' in result.stdout:
                            lines = result.stdout.split('\n')
                            model_class_line = next((line for line in lines if 'Found the model class' in line), None)
                            
                            if model_class_line:
                                # Extract the app name using string manipulation or regex
                                app_name_start = model_class_line.find("in app '") + len("in app '")
                                app_name_end = model_class_line.find("'", app_name_start)
                                app_name = model_class_line[app_name_start:app_name_end]
                                print(f"Found the model class '{class_relation}' in app '{app_name}'.")
                                if app_name in new_directory:
                                    pass
                                else:
                                    formatted_model_class_str = f'from {app_name}.models import {class_relation}\n'+model_class_str
                                    model_class_str=formatted_model_class_str
                                type_relation = input('Relation type? [ManyToOne, ManyToMany]:\n> ')
                                while True:
                                    if type_relation == 'ManyToOne':
                                        model_class_str += f'    {property_name} = models.ForeignKey({class_relation}, on_delete=models.CASCADE)'
                                        break
                                    elif type_relation == 'ManyToMany':
                                        model_class_str += f'    {property_name} = models.ManyToManyField({class_relation})'
                                        break
                                    else:
                                        print('Invalid relation type. Please enter a valid field type.')
                                break
                            else:
                                print("Model class line not found in the output.")
                                break
                        else:
                            print("Model class not found.")
                            break

            model_class_str += '\n    class Meta:\n        db_table = \'' + modal_name.lower() + '\'\n\n'
            with open(f"{new_directory}/models.py", 'r') as file:
                line_count = sum(1 for line in file)
            if line_count >=10:
                lines = model_class_str.split('\n')
                new_lines = lines[1:]
                new_content = '\n'.join(new_lines)
                with open(f"{new_directory}/models.py", "a") as model_file:
                    model_file.write(new_content) 
            else:
                with open(f"{new_directory}/models.py", "a") as model_file:
                    model_file.write(model_class_str) 
        else:
            print('Modal exist')
            while True:
                model_class_str = ''
                property_name = input('New property name (press Enter to stop adding fields):\n> ')
                if not property_name:
                    break
                while True:
                    field_type = input('Field type (enter ? to see all types) [CharField]:\n> ')
                    if field_type == "?":
                        print('- CharField\n- BooleanField\n- IntegerField\n- DateTimeField\n- JSONField\n- URLField\n- FloatField\n- EmailField\n- relation')
                    elif field_type in ['CharField', 'BooleanField', 'IntegerField', 'DateTimeField', 'JSONField', 'URLField', 'FloatField', 'EmailField', 'relation']:
                        break
                    else:
                        print('Invalid field type. Please enter a valid field type or "?" to see all types.')
                if field_type =="CharField":
                    model_class_str += f'    {property_name} = models.CharField('
                    max_length = input('Field length [200]:\n> ')
                    if max_length=='':
                        max_length=200
                    model_class_str += f'max_length={max_length}, '
                    while True:    
                        null = input('Can this field be null in the database (nullable) (yes/no)\n> ')
                        if null =='yes':
                            model_class_str += f'null=True, '
                            break
                        elif null =='no':
                            model_class_str += f'null=False, '
                            break
                        else:
                            choice = print("Must be yes or no")
                    while True:
                        unique = input('Can this field be unique in the database (yes/no)\n> ')
                        if unique =='yes':
                            model_class_str += f'unique=True)\n'
                            break
                        elif unique =='no':
                            model_class_str += f'unique=False)\n'
                            break
                        else:
                            choice = print("Must be yes or no")
                if field_type =="EmailField":
                    model_class_str += f'    {property_name} = models.EmailField('
                    max_length = input('Field length [200]:\n> ')
                    if max_length=='':
                        max_length=200
                    model_class_str += f'max_length={max_length}, '
                    while True:    
                        null = input('Can this field be null in the database (nullable) (yes/no)\n> ')
                        if null =='yes':
                            model_class_str += f'null=True, '
                            break
                        elif null =='no':
                            model_class_str += f'null=False, '
                            break
                        else:
                            choice = print("Must be yes or no")
                    while True:
                        unique = input('Can this field be unique in the database (yes/no)\n> ')
                        if unique =='yes':
                            model_class_str += f'unique=True)\n'
                            break
                        elif unique =='no':
                            model_class_str += f'unique=False)\n'
                            break
                        else:
                            choice = print("Must be yes or no")
                if field_type =="URLField":
                    model_class_str += f'    {property_name} = models.URLField('
                    max_length = input('Field length [800]:\n> ')
                    if max_length=='':
                        max_length=800
                    model_class_str += f'max_length={max_length}, '
                    while True:    
                        null = input('Can this field be null in the database (nullable) (yes/no)\n> ')
                        if null =='yes':
                            model_class_str += f'null=True, '
                            break
                        elif null =='no':
                            model_class_str += f'null=False, '
                            break
                        else:
                            choice = print("Must be yes or no")
                    while True:
                        unique = input('Can this field be unique in the database (yes/no)\n> ')
                        if unique =='yes':
                            model_class_str += f'unique=True)\n'
                            break
                        elif unique =='no':
                            model_class_str += f'unique=False)\n'
                            break
                        else:
                            choice = print("Must be yes or no")
                if field_type =="BooleanField":
                    model_class_str += f'    {property_name} = models.BooleanField('
                    while True:
                        null = input('Can this field be null in the database (nullable) (yes/no)\n> ')
                        if null =='yes':
                            model_class_str += f'null=True, '
                            break
                        elif null =='no':
                            model_class_str += f'null=False, '
                            break
                        else:
                            choice = print("Must be yes or no")
                    while True:
                        default = input('Can this field be default in the database (true/false)\n> ')
                        if default =='true':
                            model_class_str += f'default=True)\n'
                            break
                        elif default =='false':
                            model_class_str += f'default=False)\n'
                            break
                        else:
                            choice = print("Must be true or false")
                if field_type =="IntegerField":
                    model_class_str += f'    {property_name} = models.IntegerField('
                    while True:
                        null = input('Can this field be null in the database (nullable) (yes/no)\n> ')
                        if null =='yes':
                            model_class_str += f'null=True, '
                            break
                        elif null =='no':
                            model_class_str += f'null=False, '
                            break
                        else:
                            choice = print("Must be yes or no")
                    while True:
                        unique = input('Can this field be unique in the database (yes/no)\n> ')
                        if unique =='yes':
                            model_class_str += f'unique=True)\n'
                            break
                        elif unique =='no':
                            model_class_str += f'unique=False)\n'
                            break
                        else:
                            choice = print("Must be yes or no")
                    while True:
                        default = input('Can this field be default in the database (true/false)\n> ')
                        if default !='':
                            default_value  = input('entre your default value:\n> ')
                            model_class_str += f'default={default_value})\n'
                            break
                        else:
                            break
                if field_type =="FloatField":
                    model_class_str += f'    {property_name} = models.FloatField('
                    while True:
                        null = input('Can this field be null in the database (nullable) (yes/no)\n> ')
                        if null =='yes':
                            model_class_str += f'null=True, '
                            break
                        elif null =='no':
                            model_class_str += f'null=False, '
                            break
                        else:
                            choice = print("Must be yes or no")
                    while True:
                        unique = input('Can this field be unique in the database (yes/no)\n> ')
                        if unique =='yes':
                            model_class_str += f'unique=True)\n'
                            break
                        elif unique =='no':
                            model_class_str += f'unique=False)\n'
                            break
                        else:
                            choice = print("Must be yes or no")
                    while True:
                        default = input('Can this field be default in the database (true/false)\n> ')
                        if default !='':
                            default_value  = input('entre your default value:\n> ')
                            model_class_str += f'default={default_value})\n'
                            break
                        else:
                            break
                if field_type =="DateTimeField":
                    model_class_str += f'    {property_name} = models.DateTimeField('
                    while True:
                        null = input('Can this field be null in the database (nullable) (yes/no)\n> ')
                        if null =='yes':
                            model_class_str += f'null=True, '
                            break
                        elif null =='no':
                            model_class_str += f'null=False, '
                            break
                        else:
                            choice = print("Must be yes or no")
                if field_type =="JSONField":
                    model_class_str += f'    {property_name} = models.JSONField('
                    while True:
                        null = input('Can this field be null in the database (nullable) (yes/no)\n> ')
                        if null =='yes':
                            model_class_str += f'null=True, '
                            break
                        elif null =='no':
                            model_class_str += f'null=False, '
                            break
                        else:
                            choice = print("Must be yes or no")
                if field_type =="relation":
                    while True:
                        class_relation = input('What class should this entity be related to?:\n> ')
                        result = subprocess.run(['python', 'manage.py', 'find_model', class_relation],
                                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        if 'Found the model class' in result.stdout:
                            lines = result.stdout.split('\n')
                            model_class_line = next((line for line in lines if 'Found the model class' in line), None)
                            
                            if model_class_line:
                                # Extract the app name using string manipulation or regex
                                app_name_start = model_class_line.find("in app '") + len("in app '")
                                app_name_end = model_class_line.find("'", app_name_start)
                                app_name = model_class_line[app_name_start:app_name_end]
                                print(f"Found the model class '{class_relation}' in app '{app_name}'.")
                                if app_name in new_directory:
                                    pass
                                else:
                                    formatted_model_class_str = f'from {app_name}.models import {class_relation}\n'+model_class_str
                                    model_class_str=formatted_model_class_str
                                type_relation = input('Relation type? [ManyToOne, ManyToMany]:\n> ')
                                while True:
                                    if type_relation == 'ManyToOne':
                                        model_class_str += f'    {property_name} = models.ForeignKey({class_relation}, on_delete=models.CASCADE)'
                                        break
                                    elif type_relation == 'ManyToMany':
                                        model_class_str += f'    {property_name} = models.ManyToManyField({class_relation})'
                                        break
                                    else:
                                        print('Invalid relation type. Please enter a valid field type.')
                                break
                            else:
                                print("Model class line not found in the output.")
                                break
                        else:
                            print("Model class not found.")
                            break
                self.update_proprety(new_directory,property_name,model_class_str)
            
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
            settings_path = self.find_manage_directory(directory_path, 'settings.py')
            
            while True:
                app_name = input('tape your app_name:\n> ')
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
            self.generate_models(folder_path,app_name)
        except KeyboardInterrupt:
            print("\nOperation interrupted. Exiting gracefully.")