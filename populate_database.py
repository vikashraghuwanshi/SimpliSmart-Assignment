from app.database import get_db
from app.models import Organization

def add_test_organization(db):
    test_org = Organization(name="TestOrg", invite_code="ABC123")
    db.add(test_org)
    db.commit()

if __name__ == "__main__":
    # Get a database session
    from sqlalchemy.orm import Session

    db: Session = next(get_db())
    add_test_organization(db)
    # print("Test organization added successfully!")
