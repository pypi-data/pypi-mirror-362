from solocompany import utils


department_setting = utils.read_json_file("department.json")

def get_department_path(department_name):
    if department_name is None:
        None
    all_department_paths = department_setting["allDepartmentPaths"]
    if department_name in all_department_paths:
        return all_department_paths[department_name]
    else:
        raise Exception("Department not found: " + department_name)