from fastapi import FastAPI
from app.routers import auth, cluster, deployment
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(cluster.router, prefix="/clusters")
app.include_router(deployment.router, prefix="/deployments")
