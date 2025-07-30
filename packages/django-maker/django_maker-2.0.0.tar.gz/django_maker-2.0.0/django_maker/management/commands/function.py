from difflib import get_close_matches
import subprocess


def list_app(setting_file_path):
    with open(setting_file_path+'/settings.py', "r") as f:
        content = f.read()
    start_index = content.find("INSTALLED_APPS = [") + len("INSTALLED_APPS = [")
    end_index = content.find("]", start_index)
    installed_apps = content[start_index:end_index].strip('\n')
    return installed_apps


def find_closest_match(query, items, threshold=0.8):
    for string in items:
        if query in string:
            return True
    if query in items:
        return True
    else:
        matches = get_close_matches(query, items, n=1, cutoff=threshold)
        if matches:
            return matches[0]
        else:
            return None

def checkModelExist(app_name,class_relation):
    result = subprocess.run(['python', 'manage.py', 'find_model', class_relation],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if 'Found the model class' in result.stdout:
        lines = result.stdout.split('\n')
        model_class_line = next((line for line in lines if 'Found the model class' in line), None)
        
        if model_class_line:
            # Extract the app name using string manipulation or regex
            app_name_start = model_class_line.find("in app '") + len("in app '")
            app_name_end = model_class_line.find("'", app_name_start)
            app_name_from_model = model_class_line[app_name_start:app_name_end]
            print(f"Found the model class '{class_relation}' in app '{app_name_from_model}'.")
            if app_name_from_model == app_name:
                return True
            else:
                return False
    else:
        return False
    