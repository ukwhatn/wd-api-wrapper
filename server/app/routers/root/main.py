from fastapi import APIRouter

# define router
router = APIRouter(
    tags=["pages"],
)


# define route
@router.get("/")
async def get_root():
    return {"message": "Hello World"}
