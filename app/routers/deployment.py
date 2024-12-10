from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db
from app.services.scheduler import DeploymentScheduler

router = APIRouter()

# Instantiate the scheduler
scheduler = DeploymentScheduler()

@router.post("/create/")
def create_deployment(deployment: schemas.DeploymentCreate, db: Session = Depends(get_db)):
    # Ensure the associated cluster exists
    cluster = db.query(models.Cluster).filter(models.Cluster.id == deployment.cluster_id).first()
    if not cluster:
        raise HTTPException(status_code=400, detail="Cluster not found")

    # Ensure deployment with the same name does not already exist in the cluster
    existing_deployment = db.query(models.Deployment).filter(
        models.Deployment.name == deployment.name,
        models.Deployment.cluster_id == deployment.cluster_id
    ).first()

    if existing_deployment:
        raise HTTPException(status_code=400, detail="Deployment already exists for this cluster.")

    # Create deployment
    db_deployment = models.Deployment(
        name=deployment.name,
        required_cpu=deployment.required_cpu,
        required_ram=deployment.required_ram,
        required_gpu=deployment.required_gpu,
        priority=deployment.priority,
        cluster_id=deployment.cluster_id,
        image_path=deployment.image_path  # Ensure this is correctly assigned
    )

    db.add(db_deployment)
    db.commit()
    db.refresh(db_deployment)

    # Add to scheduling queue
    scheduler.add_to_queue(db_deployment)

    # Run the scheduler
    scheduler.schedule_deployments(db)

    return {"message": "Deployment created and scheduled!", "deployment_id": db_deployment.id}

@router.get("/list-all/")
def get_all_deployments(db: Session = Depends(get_db)):
    """
    API endpoint to list all deployments and their statuses.
    """
    deployments = db.query(models.Deployment).all()
    return deployments