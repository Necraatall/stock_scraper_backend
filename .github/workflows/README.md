# GitHub Workflows

This directory contains various GitHub Actions workflow files for automating different tasks in this repository.

## CI/CD Pipeline

**File:** `ci_cd_pipeline.yaml`

**Purpose:** This workflow file includes steps for Continuous Integration and Continuous Deployment (CI/CD). It covers the following tasks:
- Setting up AWS credentials.
- Building and pushing Docker images to AWS ECR Public.
- Scanning Docker images for vulnerabilities using Trivy.
- Running static code analysis with Ruff.
- Running tests with code coverage using Pytest.
- Automatically creating a release when a new version is tagged.

**Triggers:**
- Push to branches `main`, `feature/**`, `bug/**`, `chore/**`.
- Pull request to the `main` branch.
- Push tags in the format `v*.*.*`.

## Terraform Setup

**File:** `terraform.yaml`

**Purpose:** This workflow file includes steps for setting up and applying Terraform configurations. It covers the following tasks:
- Checking out the code.
- Setting up Terraform using the official GitHub action.
- Initializing Terraform configuration.
- Applying Terraform configuration with auto-approval.

**Triggers:**
- Workflow call (can be triggered from another workflow).

## Notes

- **Sequential Execution:** Steps in the CI/CD workflow are executed sequentially using the `needs` clause, ensuring the correct order of execution.
- **Vulnerability Scanning:** Trivy scanning is configured to detect only critical and high-severity vulnerabilities.
- **Automated Release:** Release steps are triggered only when pushing tags in the specified format.

If you have any questions or need assistance with these workflows, please contact the repository administrator.
