from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import auth_routes, project_routes, task_routes, dashboard_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()



"origins"= [
    "http://localhost:5173",
    "https://vercel.app"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(project_routes.router)
app.include_router(task_routes.router)
app.include_router(dashboard_routes.router)


@app.get("/")
def home():
    return {"message": "Task Manager API Running"}