from fastapi import APIRouter

router = APIRouter(
    prefix="/admissions",
    tags=["Admissions"]
)


@router.get("/test")
def admissions_test():
    return {"message": "Admissions router working"}
