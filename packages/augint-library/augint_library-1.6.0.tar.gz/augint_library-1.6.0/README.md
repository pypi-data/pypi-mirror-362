# Augmenting Integrations Library Template Repository


[![CI Status](https://github.com/svange/augint-library/actions/workflows/pipeline.yaml/badge.svg?branch=main)](https://github.com/svange/augint-library/actions/workflows/pipeline.yaml)

[![PyPI](https://img.shields.io/pypi/v/augint-library?style=flat-square)](https://pypi.org/project/augint-library/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=flat-square&logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-automated-blue?style=flat-square&logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?style=flat-square)](https://conventionalcommits.org)
[![semantic-release](https://img.shields.io/badge/%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg?style=flat-square)](https://github.com/semantic-release/semantic-release)
[![License](https://img.shields.io/github/license/svange/augint-library?style=flat-square)](https://github.com/svange/augint-library/blob/main/LICENSE)
[![Sponsor](https://img.shields.io/badge/donate-github%20sponsors-blueviolet?style=flat-square&logo=github-sponsors)](https://github.com/sponsors/svange)


---

## 📚 Project Resources

| [📖 Current Documentation](https://svange.github.io/augint-library) |[🧪 Test report for last release ](https://svange.github.io/augint-library/test-report.html) |
|:----------------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|

---
## Pre-requisites
### Install Poetry, AWS CLI, and SAM CLI
Google it and follow the instructions for your platform.

### Secret Management
Install chezmoi and age

```powershell
winget install twpayne.chezmoi
winget install --id FiloSottile.age
```
Don't forget to setup chezmoi to use age for encryption and github for remote storage.

### Set up your AWS OIDC provider (once per account)
Run this once per AWS account (safe to re-run; will no-op if it exists):
```powershell
aws iam create-open-id-connect-provider `
  --url https://token.actions.githubusercontent.com `
  --client-id-list sts.amazonaws.com
```
---

## ⚡ Getting Started

### Very important: Grab your  PyPi and TestPyPi names right away, they may not be available later!
---
### Configure Trusted Publisher on PyPI and TestPyPI
  - Go to [PyPI Trusted Publishers](https://pypi.org/manage/account/#trusted-publishers)
  - Click **Add a trusted publisher**, link this repo, and authorize publishing from `main`
  - Repeat on [TestPyPI Trusted Publishers](https://test.pypi.org/manage/account/#trusted-publishers) for `dev`

---

### Create a `.env` file for your repository
Copy the following template to a file named `.env` in the root of your repository. You will fill this out along the way.
```env
# Needed for augint-github to find the repo
GH_REPO=
GH_ACCOUNT=

# Needed to publish to GitHub pages and to push to GitHub during release
GH_TOKEN=

# Needed for pipeline generate docs stage (module name can't contain dashes)
MODULE_NAME=

# Needed for pipeline the test runner in non-matrix mode
PYTHON_VERSION=

##############################
# AWS Pipeline Resources
##############################
TESTING_REGION=us-east-1
TESTING_PIPELINE_EXECUTION_ROLE=
TESTING_CLOUDFORMATION_EXECUTION_ROLE=
TESTING_ARTIFACTS_BUCKET=
```

### Setup your AWS pipeline resources:

1. Create pipeline resources for stages DEV and PROD. Consider stage names like DevApiPortal and ProdApiPortal.
```powershell
sam pipeline bootstrap --stage augint-test-testing
```

### Fix the trust policy on the generated PipelineExecutionRole
SAM CLI generates an invalid trust policy (uses ForAllValues:StringLike which fails).
Run this after bootstrap:

```powershell
# Load environment variables from .env file
get-content .env | foreach {
    $name, $value = $_.split('=')
    if ([string]::IsNullOrWhiteSpace($name) -or $name.Contains('#')) {
        # skip empty or comment line in ENV file
        return
    }
    set-content env:\$name $value
}

# Get AWS account ID
$accountId = (aws sts get-caller-identity --query 'Account' --output text)
# Set your GitHub org/user and repo
$githubUserOrOrg = $env:GH_ACCOUNT  
$githubRepo = $env:GH_REPO
$projectPrefix = ($githubRepo.Substring(0, [Math]::Min(9, $githubRepo.Length)))  # first 9 chars

echo "Project prefix: $projectPrefix"
echo "GitHub User/Org: $githubUserOrOrg"
echo "GitHub Repo: $githubRepo"


# Find the generated pipeline execution role
$roleName = aws iam list-roles `
  --query "Roles[?starts_with(RoleName, 'aws-sam-cli-managed-${projectPrefix}') && contains(RoleName, 'PipelineExecutionRole')].RoleName" `
  --output text

if (-not $roleName) {
    Write-Error "Could not find a PipelineExecutionRole for project prefix $projectPrefix"
    exit 1
}

# Define the trust policy
$trustPolicy = @"
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::${accountId}:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": [
            "repo:${githubUserOrOrg}/${githubRepo}:ref:refs/heads/fix/*",
            "repo:${githubUserOrOrg}/${githubRepo}:ref:refs/heads/feat/*",
            "repo:${githubUserOrOrg}/${githubRepo}:ref:refs/heads/dev",
            "repo:${githubUserOrOrg}/${githubRepo}:ref:refs/heads/main"
          ]
        }
      }
    }
  ]
}

"@

echo "Updating trust policy for role: $roleName"
echo "Trust policy: $trustPolicy"

# Update the role trust policy
aws iam update-assume-role-policy `
  --role-name $roleName `
  --policy-document $trustPolicy
```

Save your .env file
```bash
$githubRepo = $env:GH_REPO
chezmoi add .env
chezmoi git add .
chezmoi git commit -- -am "Add .env file for $githubRepo"
```

Enable pre-commit hooks
```bash
pre-commit install
pre-commit install --install-hooks
pre-commit run --all-files
```
---


---
### Change `augint-library` to your project name:
- in `pyproject.toml` also, change the version to `0.0.0`
- in `.github/workflows/pipeline.yaml`
- in `README.md`
- Rename directory: `src/augint_library` → `src/<your_project_name>`
- Clear contents of `CHANGELOG.md`

---

Push the `.env` file vars and secrets to your repository
```bash
ai-gh-push
```

Fix up your poetry lock file:
```bash
poetry install
poetry lock
```

Enable Claude Code with MCP servers:
```bash
claude mcp add --transport http context7 https://mcp.context7.com/mcp
```

Finally, push your repo!
Don't for get to set your repository's branch protection rules to require a successful run of the pipeline before merging PRs.

---

### Helpful Commands
```pwsh
# "source" an .env file in PowerShell
get-content .env | foreach {
    $name, $value = $_.split('=')
    if ([string]::IsNullOrWhiteSpace($name) -or $name.Contains('#')) {
        # skip empty or comment line in ENV file
        return
    }
    set-content env:\$name $value
}
```
