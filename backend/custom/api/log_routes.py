from fastapi import APIRouter

router = APIRouter()


@router.get("/errors")
def get_errors():
    return {"message": "Custom Logs Data"}
