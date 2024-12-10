from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db
from app.utils.hashing import Hash
from app.utils.token import create_access_token
from app.utils.dependencies import get_current_user

router = APIRouter()

@router.post("/register/")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    API endpoint to register a new user.
    """
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username is already registered")

    else :
        # Hash the password
        hashed_password = Hash.hash_password(user.password)
        new_user = models.User(username=user.username, password_hash=hashed_password)

        # Save user to the database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    return {"message": "User registered successfully!", "user_id": new_user.id}



@router.post("/login/")
def login(user_credentials: schemas.Login, db: Session = Depends(get_db)):
    """
    API endpoint to login a user with JSON payload.
    """
    # Retrieve user by username
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
    if not user or not Hash.verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Generate an access token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/join-organization/")
def join_organization(
    invite_code: schemas.InviteCode,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    API to join an organization using an invite code.
    """
    # Check if the invite code is valid
    organization = db.query(models.Organization).filter(models.Organization.invite_code == invite_code.code).first()
    if not organization:
        raise HTTPException(status_code=400, detail="Invalid invite code")

    # Add the current user to the organization
    if current_user.organization_id:
        raise HTTPException(status_code=400, detail="User already belongs to an organization")
    
    current_user.organization_id = organization.id
    db.commit()
    return {"message": f"User {current_user.username} successfully joined the organization {organization.name}"}