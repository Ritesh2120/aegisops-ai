import os

from anthropic import Anthropic
from dotenv import load_dotenv


load_dotenv()


class DeploymentPlanner:
    """Claude-powered deployment planning service."""

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not configured. "
                "Add it to the .env file."
            )

        self.client = Anthropic(api_key=api_key)

    def create_plan(self, request: str) -> str:
        """Generate a safe deployment plan from a user request."""

        prompt = f"""
You are AegisOps AI, a senior cloud and DevOps planning assistant.

Your job is to analyze deployment requests and produce a SAFE,
structured deployment plan.

Project:
AegisOps AI

Technology stack:
- Python
- FastAPI
- Docker
- AWS
- Terraform
- Kubernetes
- GitHub Actions
- Prometheus
- Grafana

User deployment request:
<request>
{request}
</request>

Create a deployment plan with exactly these sections:

1. Request Summary
2. Pre-Deployment Checks
3. Infrastructure Changes
4. Docker Changes
5. Kubernetes Changes
6. CI/CD Changes
7. Monitoring and Validation
8. Rollback Plan
9. Security Considerations

Important safety rules:
- Do NOT execute commands.
- Do NOT provide AWS access keys, passwords, tokens, or secrets.
- Do NOT request unrestricted AWS permissions.
- Do NOT recommend deleting production infrastructure unless explicitly required.
- Prefer reversible changes.
- Clearly identify potentially destructive operations.
- If important information is missing, state the assumption.
- Keep the plan practical for a real DevOps environment.
"""

        response = self.client.messages.create(
            model="claude-sonnet-5",
            max_tokens=2500,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.content[0].text