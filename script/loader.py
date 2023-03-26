import os
import pathlib

class noFiles(Exception):
    pass

def create_variable(target: str, path: str):
    files = os.listdir(os.path.join(path, target))

    if len(files) == 0:
        raise noFiles()
    
    
    variable = f"const {target} = ["
    for file in files:
        variable += f'"../immagini/{target}/{file}",'
    variable = list(variable)
    variable[-1] = "]"
    return "".join(variable)

def create_case(target: str):
    generated = f'''        case "{target}":
            return {target}'''
    return generated



def start():

    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    full_path = os.path.join(file_path, "immagini")

    if not os.path.exists(full_path):
        print(f"la cartella {full_path} non esiste")
        return

    files = os.listdir(path=full_path)


    targets = []
    for file in files:
        if os.path.isdir(os.path.join(full_path, file)):
            targets.append(file)

    if len(targets) == 0:
        print("non ci sono cartelle in immagini")
        return
    
    variables = []
    cases = []
    for target in targets:
        try:
            variable = create_variable(target, full_path)
            generated = create_case(target)
        except noFiles:
            print(f"The dir {target} doesn't have any files")
            return
        
        variables.append(variable + "\n")
        cases.append(generated + "\n")
    
    for variable in variables:
        mjs_path = os.path.join(file_path, "html")


        if not os.path.exists(mjs_path):
            print("the html path doesn't exists")
            return
        
        with open(os.path.join(mjs_path, "immagini.mjs"), "w+") as file:
            file.writelines(variables)
            file.write("\nfunction getByName(name) {" + "\n")
            file.write("    switch (name) {\n")
            file.writelines(cases)
            file.write("        default:\n")
            file.write("            return []\n")
            file.write("    }\n")
            file.write("}")
            file.close()
start()
