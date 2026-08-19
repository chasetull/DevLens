# MAIN

# imports
from pprint import pprint

from app.analyzers.project_scanner import scan_project

if __name__ == "__main__":
    project_path = input("\nEnter project path: ")
    result = scan_project(project_path)

#    print("------------------- DevLens Info: -------------------\n")
    pprint(result.model_dump())