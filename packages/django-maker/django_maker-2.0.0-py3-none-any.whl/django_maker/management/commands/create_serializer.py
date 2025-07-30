import re
from django.core.management.base import BaseCommand
import os
import subprocess
from .function import *

class Command(BaseCommand):
    help = 'Generate serializers'
    
    def find_folder(self,start_path, folder_name):
        for root, dirs, files in os.walk(start_path):
            if folder_name in dirs:
                return os.path.join(root, folder_name)

        return None
    
    def read_from_file(self,file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                return True, content
        except FileNotFoundError:
            msg = f"File '{file_path}' not found."
            return False, msg
        
    def extract_classes(self,file_content):
        classes = re.findall(r'class (\w+)\(.*?\):(?:.*?\n)*?((?:\s{4}.+\n)+)', file_content)
        class_dict = {}

        for class_name, class_content in classes:
            fields = re.findall(r'\s{4}(\w+) = models.(\w+)\((.*?)\)', class_content)
            class_dict[class_name] = fields

        return class_dict

    def format_field_info(self,field_name, field_type, field_args):
        if field_type == 'ForeignKey':
            related_model = re.search(r'to=\'(.+?)\'', field_args)
            return f"{field_name} ({field_type})({related_model.group(1)})" if related_model else f"{field_name} ({field_type})"
        elif field_type == 'ManyToManyField':
            related_model = re.search(r'to=\'(.+?)\'', field_args)
            return f"{field_name} ({field_type})({related_model.group(1)})" if related_model else f"{field_name} ({field_type})"
        else:
            return f"{field_name} ({field_type})"
        
    def generate_serializer(self,new_directory,your_app_name,list_models):
        code = f"""from rest_framework import serializers
from .models import *
    """
        with open(f"{new_directory}"+"/serializer.py", "w") as model_file:
            model_file.write(code)
        for i in list_models:
            class_name = i[0].capitalize()+'Serializer'
            related_fields=[]
            
            if len(i[1]) == 0:
                add_code = f"""
class {class_name}(serializers.ModelSerializer):
    """
                add_code += f"""
    class Meta:
        model = {i[0].capitalize()}
        fields = '__all__'
            
    """
                # print(add_code)
                with open(f"{new_directory}"+"/serializer.py", "a") as model_file:
                    model_file.write(add_code)
            else:
                add_code = f"""
class {class_name}(serializers.ModelSerializer):
        """
                for n in i[1]:
                    result = subprocess.run(['python', 'manage.py', 'find_model', n[0][2]],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    if 'Found the model class' in result.stdout:
                        lines = result.stdout.split('\n')
                        model_class_line = next((line for line in lines if 'Found the model class' in line), None)
                        
                        if model_class_line:
                            app_name_start = model_class_line.find("in app '") + len("in app '")
                            app_name_end = model_class_line.find("'", app_name_start)
                            app_name = model_class_line[app_name_start:app_name_end]
                            
                            # if app_name == your_app_name:
                            #     formated_code = f'from {n[0][2]}.models import *\n'
                            #     with open("/home/serializer.py", "r") as model_file:
                            #         content = model_file.read()
                            #     with open("/home/serializer.py", "w") as model_file:
                            #         model_file.write(formated_code + content)
                            print(f"Found the model class '{n[0][2]}' in app '{app_name}'.")
                            if app_name in new_directory:
                                with open(f"{new_directory}"+"/serializer.py", "r") as model_file:
                                    content = model_file.read()
                                with open(f"{new_directory}"+"/serializer.py", "w") as model_file:
                                    model_file.write(content)
                                # pass
                            else:
                                formated_code = f'from {n[0][2]}.models import *\n'
                                with open(f"{new_directory}"+"/serializer.py", "r") as model_file:
                                    content = model_file.read()
                                with open(f"{new_directory}"+"/serializer.py", "w") as model_file:
                                    model_file.write(formated_code + content)
                                # formatted_model_class_str = f'from {app_name}.models import {n[0][2]}\n'+model_class_str
                                # model_class_str=formatted_model_class_str
                        else:
                            print("Model class line not found in the output.")
                    else:
                        print("Model class not found.")
                    # formated_code = f'from {n[0][2]}.models import *\n'
                    # with open("/home/serializer.py", "r") as model_file:
                    #     content = model_file.read()
                    # with open("/home/serializer.py", "w") as model_file:
                    #     model_file.write(formated_code + content)
                    if "ManyToManyField" in n[0] :
                        related_fields.append({"field_name": n[0][0], "type": "serializers.PrimaryKeyRelatedField", "many": True, "queryset": n[0][2]+".objects.all()"})
                    else:
                        related_fields.append({"field_name": n[0][0], "type": "serializers.PrimaryKeyRelatedField", "queryset": n[0][2]+".objects.all()"})
                for field in related_fields:
                    field_name = field["field_name"]
                    field_type = field["type"]
                    add_code += f"{field_name} = {field_type}({', '.join([f'{key}={value}' for key, value in field.items() if key not in ['field_name', 'type']])})"
                    add_code += "\n    "
                add_code += f"""
        class Meta:
            model = {i[0].capitalize()}
            fields = '__all__'
        """
                print(add_code)

                with open(f"{new_directory}"+"/serializer.py", "a") as model_file:
                    model_file.write(add_code)
            
    
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
            l1= []
            l2= []
            directory_path = os.getcwd()
            settings_path = self.find_manage_directory(directory_path, 'settings.py')
            folder_path = self.find_folder('/', app_name)
            while True:
                file_content  = self.read_from_file(folder_path+'/models.py')
                if file_content[0] == True:
                    file_content =  ''.join(map(str, file_content[1]))
                    break
                else:
                    print(file_content[0])
            class_dict = self.extract_classes(file_content)
            result = []
            for class_name, fields in class_dict.items():
                class_info = [class_name, []]
                for field_name, field_type, field_args in fields:
                    if "ForeignKey" in field_type or "ManyToManyField" in field_type:
                        target =field_args.split(',')
                        l1.append(field_name)
                        l1.append(field_type)
                        l1.append(target[0])
                        l2.append(l1)
                        l1 = []
                        class_info[1].append(l2)
                        l2 = []
                result.append(class_info)        
            self.generate_serializer(folder_path,app_name,result)
            
        except KeyboardInterrupt:
            # Handle Ctrl+C
            print("\nOperation interrupted. Exiting gracefully.")