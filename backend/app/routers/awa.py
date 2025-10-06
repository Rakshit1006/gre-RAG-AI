"""AWA grading endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.awa import AWAGradeRequest, AWAGradeResponse, RubricScore
from app.services.gemini_client import get_gemini_client
from app.prompts.explanation import create_awa_grading_prompt

router = APIRouter(prefix="/api/v1/awa", tags=["awa"])


@router.post("/grade", response_model=AWAGradeResponse)
async def grade_essay(
    request: AWAGradeRequest,
    db: Session = Depends(get_db)
):
    """Grade an AWA essay using ETS-aligned rubrics."""
    try:
        client = get_gemini_client()
        
        # Create grading prompt
        prompt = create_awa_grading_prompt(
            essay_text=request.essay_text,
            task_type=request.task_type
        )
        
        # Generate grading
        result = client.generate_json(prompt)
        
        # Extract rubric scores
        rubric_data = result.get("rubric", {})
        rubric = RubricScore(
            thesis=rubric_data.get("thesis", 0.0),
            development=rubric_data.get("development", 0.0),
            organization=rubric_data.get("organization", 0.0),
            language=rubric_data.get("language", 0.0),
            justification=rubric_data.get("justification", {})
        )
        
        # Calculate total score
        total_score = int(rubric.thesis + rubric.development + rubric.organization + rubric.language)
        
        return AWAGradeResponse(
            score=total_score,
            rubric=rubric,
            suggested_draft=result.get("suggested_draft", ""),
            weaknesses=result.get("weaknesses", []),
            improvements=result.get("improvements", [])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to grade essay: {str(e)}")
