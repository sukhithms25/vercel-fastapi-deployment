from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    """
    Root endpoint that returns a welcome message
    """
    return {
        "message": "Welcome to FastAPI on Vercel!",
        "status": "success"
    }
