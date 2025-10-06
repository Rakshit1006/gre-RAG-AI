"""Explanation endpoints for on-the-fly help."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.explain import ExplainRequest, ExplainResponse, Reference
from app.services.gemini_client import get_gemini_client
from app.prompts.explanation import create_explanation_prompt

router = APIRouter(prefix="/api/v1", tags=["explain"])


@router.post("/explain", response_model=ExplainResponse)
async def explain_selection(
    request: ExplainRequest,
    db: Session = Depends(get_db)
):
    """Provide ETS-aligned explanation for selected text."""
    try:
        client = get_gemini_client()
        
        # Create explanation prompt
        prompt = create_explanation_prompt(
            selection_text=request.selection_text,
            domain=request.domain,
            depth=request.depth
        )
        
        # Generate explanation
        result = client.generate_json(prompt)
        
        # Extract explanation components
        explanation = result.get("summary", "") + "\n\n" + result.get("details", "")
        references_data = result.get("references", [])
        references = [Reference(**ref) for ref in references_data if isinstance(ref, dict)]
        
        saved_id = None
        
        # Save if requested
        if request.save:
            # TODO: Implement saving explanation as a note or concept
            pass
        
        return ExplainResponse(
            explanation=explanation,
            references=references,
            saved_id=saved_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate explanation: {str(e)}")
