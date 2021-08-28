from config import *


def export_to_json(data, file_path=DEFAULT_OUTPUT_FILE_PATH):
    import json
    import os

    # Make directory if it is needed
    directory = os.path.dirname(file_path)
    if not os.path.exists("/" + directory):
        os.makedirs(directory, exist_ok=True)

    # Write data to file_path
    with open(file_path, 'w') as f:
        json.dump(data, f)

    print("Zapisano dane w formacie json w", file_path)
