# MAIN

# imports
from pprint import pprint

from app.analyzers.project_scanner import scan_project

if __name__ == "__main__":
    project_path = input("Enter project path: ")
    result = scan_project(project_path)

    pprint(result.model_dump())