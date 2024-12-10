import heapq
from sqlalchemy.orm import Session
from app.models import Deployment, Cluster

class DeploymentScheduler:
    def __init__(self):
        self.queue = []
        self.processed_deployments = []  # List to track processed deployments

    def add_to_queue(self, deployment: Deployment):
        """Add a deployment to the scheduling queue."""
        heapq.heappush(self.queue, (deployment.priority, deployment))

    def schedule_deployments(self, db: Session):
        """Schedule deployments from the queue to available clusters."""
        while self.queue:
            _, deployment = heapq.heappop(self.queue)

            # Fetch the associated cluster
            cluster = db.query(Cluster).filter(Cluster.id == deployment.cluster_id).first()
            if not cluster:
                print(f"Cluster {deployment.cluster_id} not found. Skipping deployment.")
                continue

            # Try to schedule the deployment
            if self._can_allocate_resources(cluster, deployment):
                self._allocate_resources(cluster, deployment, db)
                print(f"Deployment {deployment.id} scheduled successfully.")
                self.processed_deployments.append(deployment)  # Mark deployment as processed
            else:
                # Re-queue if resources are insufficient
                deployment.status = "Pending"
                db.add(deployment)
                db.commit()
                print(f"Deployment {deployment.id} re-queued due to insufficient resources.")

                # Add to processed list if not already processed in this iteration
                if deployment not in self.processed_deployments:
                    self.processed_deployments.append(deployment)

        # After the loop, re-add all processed deployments to the queue
        for dep in self.processed_deployments:
            self.add_to_queue(dep)

        # Clear the processed list after the loop ends
        self.processed_deployments.clear()

    def _can_allocate_resources(self, cluster: Cluster, deployment: Deployment) -> bool:
        """Check if a deployment can be accommodated in a cluster."""
        if (cluster.total_cpu - cluster.used_cpu < deployment.required_cpu or
            cluster.total_ram - cluster.used_ram < deployment.required_ram or
            cluster.total_gpu - cluster.used_gpu < deployment.required_gpu):
            return False
        return True

    def _allocate_resources(self, cluster: Cluster, deployment: Deployment, db: Session):
        """Allocate resources to a deployment and update the cluster state."""
        cluster.used_cpu += deployment.required_cpu
        cluster.used_ram += deployment.required_ram
        cluster.used_gpu += deployment.required_gpu

        # Update deployment status
        deployment.status = "Running"

        # Save changes to the database
        db.add(cluster)
        db.add(deployment)
        db.commit()