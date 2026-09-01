# IMPORTS
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.analyzers.project_scanner import scan_project
from app.models.analysis import AnalysisResult

router = APIRouter()

class AnalysisRequest(BaseModel):
    project_path: str

@router.post("/analysis", response_model=AnalysisResult)

def analyze_project(request: AnalysisRequest):
    try:
        return scan_project(request.project_path)
    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )
    except NotADirectoryError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {error}",
        )