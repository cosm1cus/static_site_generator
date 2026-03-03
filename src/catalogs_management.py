import os
import shutil

def copy_static_to_public():
    if os.path.exists("static"):
        del_public = clear_public()
        copy = copy_to_public("static", "docs")
        return copy
    else:
        raise Exception("Error: Docs is not exist")

def clear_public():
    if os.path.exists("docs"):
         shutil.rmtree("docs")
         os.mkdir("docs")
    else:
        os.mkdir("docs")

def copy_to_public(curr_static, curr_public):
    file_list = os.listdir(curr_static)
    log = []
    for file in file_list:
        file_path = os.path.join(curr_static, file)
        if os.path.isfile(file_path):
            file_copy = shutil.copy(file_path, curr_public)
            log.append(file_copy)
        else:
            dest_path = os.path.join(curr_public, file)
            os.mkdir(dest_path)
            log.append(dest_path)
            log.extend(copy_to_public(file_path, dest_path))
    return log
