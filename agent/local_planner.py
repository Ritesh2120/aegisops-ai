class LocalDeploymentPlanner:
    """Free local deployment planner for AegisOps AI development."""

    def create_plan(self, request: str) -> str:
        return f"""
# AegisOps AI — Deployment Plan

## 1. Request Summary

Deployment request:
{request}

The request has been analyzed using the local AegisOps AI development planner.

## 2. Pre-Deployment Checks

- Verify the application starts successfully.
- Run the automated test suite.
- Check Python dependencies.
- Verify the Dockerfile.
- Check required environment variables.
- Confirm that no secrets are committed to Git.

## 3. Infrastructure Changes

Recommended infrastructure:

- AWS networking
- Amazon ECR for container images
- Amazon EKS for Kubernetes
- IAM roles with least-privilege permissions
- CloudWatch for AWS-level logging

## 4. Docker Changes

- Build the FastAPI application image.
- Install dependencies from requirements.txt.
- Expose port 8000.
- Run the application with Uvicorn.
- Scan the image before deployment.

## 5. Kubernetes Changes

Recommended resources:

- Deployment
- Service
- ConfigMap
- Secret
- Readiness probe
- Liveness probe
- Resource requests and limits
- Horizontal Pod Autoscaler

## 6. CI/CD Changes

GitHub Actions pipeline:

1. Checkout source code.
2. Install Python dependencies.
3. Run pytest.
4. Build Docker image.
5. Security scan.
6. Push image to Amazon ECR.
7. Deploy to Amazon EKS.
8. Verify deployment health.

## 7. Monitoring and Validation

Monitor:

- Application health
- CPU usage
- Memory usage
- Pod restarts
- HTTP errors
- Deployment status

Prometheus and Grafana can be added for observability.

## 8. Rollback Plan

If deployment validation fails:

1. Stop the rollout.
2. Keep the previous working version available.
3. Roll back the Kubernetes deployment.
4. Verify application health.
5. Record the incident for later analysis.

## 9. Security Considerations

- Never commit API keys or passwords.
- Use environment variables or secret managers.
- Use IAM least privilege.
- Use GitHub OIDC instead of long-lived AWS access keys.
- Do not give an AI agent unrestricted infrastructure permissions.
- Require policy validation before automated remediation.

## Next Recommended Step

Start with Docker containerization of the FastAPI application.
"""