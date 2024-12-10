from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)

    organization = relationship("Organization", back_populates="members")

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    invite_code = Column(String, unique=True)

    members = relationship("User", back_populates="organization")

class Cluster(Base):
    __tablename__ = "clusters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    total_cpu = Column(Float, nullable=False)
    total_ram = Column(Float, nullable=False)
    total_gpu = Column(Float, nullable=False)
    used_cpu = Column(Float, default=0.0)
    used_ram = Column(Float, default=0.0)
    used_gpu = Column(Float, default=0.0)

    organization = relationship("Organization", back_populates="clusters")

Organization.clusters = relationship("Cluster", back_populates="organization")

class Deployment(Base):
    __tablename__ = "deployments"
    id = Column(Integer, primary_key=True, index=True)
    cluster_id = Column(Integer, ForeignKey("clusters.id"))
    name = Column(String, nullable=False)  # Add the name column here
    image_path = Column(String, nullable=False)
    required_cpu = Column(Float, nullable=False)
    required_ram = Column(Float, nullable=False)
    required_gpu = Column(Float, nullable=False)
    priority = Column(Integer, nullable=False)
    status = Column(String, default="Pending")  # "Pending", "Running", "Completed", "Failed"

    cluster = relationship("Cluster", back_populates="deployments")

Cluster.deployments = relationship("Deployment", back_populates="cluster")