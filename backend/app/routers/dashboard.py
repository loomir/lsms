from fastapi import APIRouter

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/test")
def dashboard_test():
    return {"message": "Dashboard router working"}
