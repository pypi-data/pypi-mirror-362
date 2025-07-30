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

### Bootstrap your project

Run the bootstrap script to set up your project:
```bash
# Complete setup (creates .env and AWS resources)
python bootstrap.py setup

# Or run steps individually:
python bootstrap.py init      # Create .env file
python bootstrap.py aws       # Set up AWS pipeline resources and fix trust policy
```

The bootstrap script will:
1. Auto-detect your GitHub info from git remote
2. Create a `.env` file with all required variables
3. Run `sam pipeline bootstrap` and capture the generated ARNs
4. Automatically fix the trust policy for GitHub Actions OIDC

### Manual setup steps

1. **Fill in your GitHub token** in `.env`
2. **Save your .env file** to chezmoi:
   ```bash
   chezmoi add .env
   chezmoi git add .
   chezmoi git commit -- -am "Add .env file for your-repo-name"
   ```

3. **Replace template names**:
   - Search and replace `augint-library` → your project name
   - Search and replace `augint_library` → your module name
   - Rename directory: `src/augint_library` → `src/<your_module_name>`
   - Clear contents of `CHANGELOG.md`
   - Set version to `0.0.0` in `pyproject.toml`

4. **Initialize development environment**:
   ```bash
   poetry install
   poetry lock
   pre-commit install
   pre-commit install --install-hooks
   pre-commit run --all-files
   ```

5. **Push secrets to GitHub**:
   ```bash
   ai-gh-push
   ```

6. **Push your repo!**
Don't for get to set your repository's branch protection rules to require a successful run of the pipeline before merging PRs.

7. To use Claude Code remember to have this in your environment one way or another:
```powershell
$env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
```

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
