import os
import json
import datetime
import uuid

def get_folder_structure(root_dir, max_depth=4):
    def _walk(dir_path, depth):
        if depth > max_depth:
            return None
        structure = {}
        files_list = []
        try:
            entries = os.listdir(dir_path)
        except PermissionError:
            return None
        for entry in entries:
            full_path = os.path.join(dir_path, entry)
            if os.path.isdir(full_path):
                sub = _walk(full_path, depth + 1)
                if sub is not None:
                    structure[entry] = sub
            else:
                creation_time = os.path.getctime(full_path)
                creation_date = datetime.datetime.fromtimestamp(creation_time).isoformat()
                modified_time = os.path.getmtime(full_path)
                modified_time = max(creation_time, modified_time)
                modified_date = datetime.datetime.fromtimestamp(modified_time).isoformat()
                files_list.append({"name": entry, "creation_date": creation_date, "modified_date": modified_date})
        if files_list:
            structure['file_list'] = files_list
        return structure
    return _walk(root_dir, 0)

if __name__ == "__main__":
    start_folder = input("Enter the starting folder path: ")
    if not os.path.isdir(start_folder):
        print("Invalid directory")
        exit()
    structure = get_folder_structure(start_folder, 4)
    folder_name = os.path.basename(start_folder)
    output_file = os.path.join(start_folder, f"{folder_name}.json")
    last_modified = None
    if os.path.exists(output_file):
        last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(output_file)).isoformat()
    generated_at = datetime.datetime.now().isoformat()
    short_guid = str(uuid.uuid4())[:8]
    structure['generated_at'] = generated_at
    structure['guid'] = short_guid
    if last_modified:
        structure['last_modified'] = last_modified
    with open(output_file, 'w') as f:
        json.dump(structure, f, indent=4)
    print(f"JSON output saved to {output_file}")