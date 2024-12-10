Steps to run the code :-

1. Install requirements - pip install -r requirements.txt
2. Export Python path - export PATH="$PATH:~/Library/Python/3.11/bin"
3. Add an organization using - python ppopulate_database.py
4. Start the server - uvicorn app.main:app --reload


API's -

    1. User Management -

        i. Register - 
                POST http://127.0.0.1:8000/auth/register
                Body - { "username": "testuser", "password":        "securepassword"}

        ii. Login - 
                POST http://127.0.0.1:8000/auth/login
                Body - { "username": "testuser", "password": "securepassword"}

        iii. Join-organization - 
                POST http://127.0.0.1:8000/auth/join-organization
                Body - { "code": "XYZ123" }
                Also add Bearer token received using login api

    2. Cluster Management -

        i. Create cluster
                POST http://127.0.0.1:8000/clusters/create
                Body - { "name": "TestCluster1",
                        "total_cpu": 8.0,
                        "total_ram": 16.0,
                        "total_gpu": 1.0,
                        "organization_id": 1 }

        ii. List all clusters -
                GET http://127.0.0.1:8000/clusters/list-all 
    

    2. Deployments Management -

        i. Create Deployment
                POST http://127.0.0.1:8000/deployments/create
                Body - { "name": "TestDeployment10",
                        "image_path": "/path/to/docker/image",
                        "cluster_id": 1,
                        "priority": 1,
                        "required_cpu": 1.0,
                        "required_ram": 2.0,
                        "required_gpu": 0.5 }

        ii. List all deployments -
                GET http://127.0.0.1:8000/deployments/list-all 










1. Database Design
    Here’s a proposed schema (represented in a UML diagram in the deliverables):

        i. User Table
            id: Primary key.
            username: Unique identifier.
            password_hash: Password stored securely.
            organization_id: Foreign key to the organization.

        ii. Organization Table
            id: Primary key.
            name: Name of the organization.
            invite_code: Unique code for joining the organization.
        
        iii. Cluster Table
            id: Primary key.
            name: Unique identifier for the cluster.
            organization_id: Foreign key to the organization.
            total_cpu, total_ram, total_gpu: Total resources.
            used_cpu, used_ram, used_gpu: Allocated resources.
        
        iv. Deployment Table
            id: Primary key.
            cluster_id: Foreign key to the cluster.
            image_path: Path to the Docker image.
            required_cpu, required_ram, required_gpu: Resources required for deployment.
            priority: Deployment priority.
            status: Pending, Running, Completed, Failed, etc.


2. Backend Service Design
    Endpoints:
        i. User Authentication & Organization Management
            POST /register: Register a new user.
            POST /login: Authenticate user and return a token.
            POST /join-organization: Join an organization using an invite code.

        ii. Cluster Management
            POST /clusters: Create a new cluster.
            GET /clusters: List clusters and their resource usage.

        iii. Deployment Management
            POST /deployments: Create a new deployment and schedule them.
            GET /deployments: List all deployments and their statuses.
