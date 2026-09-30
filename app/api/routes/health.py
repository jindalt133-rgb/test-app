from fastapi import APIRouter

router = APIRouter()


@router.get("/health", response_model=dict[str, str], tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
