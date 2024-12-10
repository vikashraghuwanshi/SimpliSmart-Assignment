from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class InviteCode(BaseModel):
    code: str

class UserResponse(BaseModel):
    id: int
    username: str
    organization_id: Optional[int]

    class Config:
        orm_mode = True

class OrganizationCreate(BaseModel):
    name: str
    invite_code: str

class OrganizationResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class ClusterCreate(BaseModel):
    name: str
    total_cpu: float
    total_ram: float
    total_gpu: float
    organization_id: int

class DeploymentCreate(BaseModel):
    name: str
    image_path: str
    required_cpu: float
    required_ram: float
    required_gpu: float
    priority: int
    cluster_id: int
