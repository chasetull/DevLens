# MAIN

# imports
from pprint import pprint

from app.analyzers.project_scanner import scan_project

from app.core.constants import LOCAL_PATH

if __name__ == "__main__":
    project_path = input("\nEnter project path: ")

    # change project path to local path for easy dev
    if project_path == "":
        project_path = LOCAL_PATH

    result = scan_project(project_path)

#    print("------------------- DevLens Info: -------------------\n")
    pprint(result.model_dump())