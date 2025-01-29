import debugpy
from fastapi import FastAPI
from app.api.api import router as api_router
from app.api.tasks import router as tasks_router
from app.api.tasktypes import router as task_types_router
from app.db import engine, Base
from app.models.task import Task

app = FastAPI()

# Include the router in the main application
app.include_router(api_router)
app.include_router(tasks_router)
app.include_router(task_types_router)

# Enable debugpy if needed
debug_port = 5678
debugpy.listen(("0.0.0.0", debug_port))  # Debug server listens on all interfaces
print(f"Debugpy is listening on port {debug_port}")

# Create the database tables
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
