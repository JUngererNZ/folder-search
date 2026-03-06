# Folder Search Project

## Execution Commands
* Run search: `python util/folder-search.py`

## Core Logic Requirements
* **Recursion Depth**: Maximum of 6 levels deep.
* **Input**: Prompt user for the starting directory path.
* **Output Format**: JSON file.
* **Output Naming**: `[parent_folder_name].json` (e.g., searching `/Users/Desktop/Photos` creates `Photos.json`).

## Technical Specs
* **Language**: Python 3.x
* **Libraries**: `os`, `json`
* **Structure**: Use a recursive or walked approach that tracks depth relative to the start path.