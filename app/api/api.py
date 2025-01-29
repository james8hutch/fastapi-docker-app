from fastapi import APIRouter

# Create a router object for your API endpoints
router = APIRouter()

@router.get("/hello")
def read_hello():
    return {"message": "Hello, from api!"}

@router.get("/health")
def health():
    return {"status": "ok"}
