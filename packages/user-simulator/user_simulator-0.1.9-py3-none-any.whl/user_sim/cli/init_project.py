import os
from argparse import ArgumentParser

def generate_untitled_name(path):
    i = 1
    while True:
        name = f"Untitled_{i}"
        full_path = os.path.join(path, name)
        if not os.path.exists(full_path):
            return name
        i += 1

def init_proj(project_name, path):
    project_path = os.path.join(path, project_name)
    os.makedirs(project_path, exist_ok=True)

    run_yml_content = f"""\
    project_folder: {project_name}

    user_profile:
    technology:
    connector:
    connector_parameters:
    extract:
    #execution_parameters:
        # - verbose
        # - clean_cache
        # - update_cache
        # - ignore_cache
    """
    project_path = os.path.join(path, project_name)

    folder_list = ["profiles", "rules", "types", "personalities"]
    for folder in folder_list:
        folder_path = os.path.join(project_path, folder)
        os.makedirs(folder_path)
        with open(f'{folder_path}/PlaceDataHere.txt', 'w') as f:
            pass

    run_yml_path = os.path.join(project_path, "run.yml")
    if not os.path.exists(run_yml_path):
        with open(run_yml_path, "w") as archivo:
            archivo.write(run_yml_content)

    return project_path

def main():
    parser = ArgumentParser(description='Conversation generator for a chatbot')
    parser.add_argument('--path', default='.',
                        help='Directory where the project will be created (default: current directory).')
    parser.add_argument('--name', help='Name of the project (optional).')
    args = parser.parse_args()

    base_path = os.path.abspath(args.path)

    if not args.name:
        project_name = generate_untitled_name(base_path)
    else:
        project_name = args.name

    final_path = init_proj(project_name, base_path)
    print(f"--- Project created at: '{final_path}' ---")

if __name__ == "__main__":
    main()