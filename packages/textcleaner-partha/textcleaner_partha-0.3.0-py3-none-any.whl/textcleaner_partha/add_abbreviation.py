# textcleaner_partha/add_abbreviation.py

import os
import json

def add_abbreviation(file_name, abbreviation, full_form):
    # Define correct folder path inside the package
    abbrev_dir = os.path.join(os.path.dirname(__file__), "abbreviation_mappings")
    os.makedirs(abbrev_dir, exist_ok=True)

    # Ensure file name ends with .json
    if not file_name.endswith(".json"):
        file_name += ".json"

    file_path = os.path.join(abbrev_dir, file_name)

    # Load existing mappings
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            mapping = json.load(f)
    else:
        mapping = {}

    # Add new abbreviation
    mapping[abbreviation] = full_form

    # Write back to the file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)