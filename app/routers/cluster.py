from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db

router = APIRouter()

@router.post("/create/")
def create_cluster(cluster: schemas.ClusterCreate, db: Session = Depends(get_db)):
    # Ensure the organization exists
    organization = db.query(models.Organization).filter(models.Organization.id == cluster.organization_id).first()
    if not organization:
        raise HTTPException(status_code=400, detail="Organization not found")

    # Check for duplicate cluster name
    existing_cluster = db.query(models.Cluster).filter(models.Cluster.name == cluster.name).first()
    if existing_cluster:
        raise HTTPException(status_code=400, detail="Cluster with this name already exists")

    # Create the cluster
    db_cluster = models.Cluster(**cluster.dict())
    db.add(db_cluster)
    db.commit()
    return {"message": "Cluster created successfully!", "cluster_id": db_cluster.id}

@router.get("/list-all/")
def list_clusters(db: Session = Depends(get_db)):
    """
    API endpoint to list all clusters.
    """
    clusters = db.query(models.Cluster).all()
    if not clusters:
        raise HTTPException(status_code=404, detail="No clusters found")

    return {"clusters": clusters}