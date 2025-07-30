#!/usr/bin/env python3
"""
augint-quickstart

Automate the boiler-plate repo-bootstrap described in the
README of the Augmenting Integrations library template.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

import boto3
import click
from botocore.exceptions import ClientError

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #


def run(
    cmd: list[str] | str,
    *,
    check: bool = True,
    capture: bool = False,
    **kw,
) -> str | None:
    """Subprocess helper."""
    if isinstance(cmd, str):
        cmd = cmd.split()
    kw.setdefault("text", True)
    if capture:
        kw["stdout"] = subprocess.PIPE
        kw["stderr"] = subprocess.STDOUT
    click.echo(f"» {' '.join(cmd)}")
    result = subprocess.run(cmd, check=check, **kw)
    return result.stdout.strip() if capture else None


def replace_in_file(path: Path, pattern: str, replacement: str):
    """Simple in-place regex replace with sanity output."""
    txt = path.read_text()
    new = re.sub(pattern, replacement, txt)
    if txt != new:
        path.write_text(new)
        click.echo(f"✓ patched {path}")
    else:
        click.echo(f"• no change in {path}")


def load_env() -> dict[str, str]:
    env = {}
    for line in Path(".env").read_text().splitlines():
        if line.startswith("#") or not line.strip():
            continue
        key, val = line.split("=", 1)
        env[key.strip()] = val.strip()
    return env


def write_env(env: dict[str, str]):
    lines: list[str] = []
    for k, v in env.items():
        lines.append(f"{k}={v}")
    Path(".env").write_text("\n".join(lines) + "\n")
    click.echo("✓ updated .env")


def chezmoi_commit(msg: str):
    run(["chezmoi", "add", ".env"])
    run(["chezmoi", "git", "add", "."])
    run(["chezmoi", "git", "commit", "--", "-m", msg])
    click.echo("✓ chezmoi committed .env")


# --------------------------------------------------------------------------- #
# Click CLI
# --------------------------------------------------------------------------- #


@click.group()
def cli():
    """Augmenting Integrations repo bootstrap helper."""
    pass


# --------------------------------------------------------------------------- #
# 1. .env creation
# --------------------------------------------------------------------------- #
@cli.command("env")
@click.option(
    "--module-name",
    prompt="Python package name (no dashes)",
    help="Used by docs/tests/stubs (e.g. augint_math)",
)
@click.option(
    "--python-version",
    default="3.12",
    prompt="Default Python runtime used in CI",
    show_default=True,
)
@click.option(
    "--aws-region",
    default="us-east-1",
    prompt="Default AWS region for testing stage",
    show_default=True,
)
def create_env(module_name: str, python_version: str, aws_region: str):
    """
    Generate .env from template and commit it encrypted with chezmoi.
    """
    repo_url = run("git config --get remote.origin.url", capture=True)
    match = re.search(r"[:/](?P<acct>[^/]+)/(?P<name>[^/.]+)", repo_url)
    if not match:
        click.echo("Could not parse GitHub repo from remote URL", err=True)
        sys.exit(1)

    gh_account, gh_repo = match.group("acct"), match.group("name")

    tpl = f"""\
GH_REPO={gh_repo}
GH_ACCOUNT={gh_account}

GH_TOKEN=<your_personal_access_token>
MODULE_NAME={module_name}
PYTHON_VERSION={python_version}

TESTING_REGION={aws_region}
TESTING_PIPELINE_EXECUTION_ROLE=
TESTING_CLOUDFORMATION_EXECUTION_ROLE=
TESTING_ARTIFACTS_BUCKET=
"""
    env_file = Path(".env")
    if env_file.exists():
        click.confirm(".env already exists – overwrite?", abort=True)

    env_file.write_text(tpl)
    click.echo("✓ wrote .env")

    chezmoi_commit(f"Add initial .env for {gh_repo}")


# --------------------------------------------------------------------------- #
# 2. AWS SAM bootstrap (now also patches .env afterwards)
# --------------------------------------------------------------------------- #
@cli.command("aws-bootstrap")
@click.option(
    "--stage",
    default=lambda: Path.cwd().name + "-testing",
    prompt="SAM stage name",
    show_default="‹repo›-testing",
)
@click.option("--profile", default="default", help="AWS CLI profile to use.")
@click.option("--region", default="us-east-1", show_default=True)
@click.option("--gh-branch", default="main", show_default=True)
@click.option("--dry-run", is_flag=True, help="Print the command only.")
def aws_bootstrap(stage: str, profile: str, region: str, gh_branch: str, dry_run: bool):
    """
    Run `sam pipeline bootstrap` non-interactively with GitHub OIDC and
    then patch .env with the generated resource ARNs / bucket.
    """
    repo_url = run("git config --get remote.origin.url", capture=True)
    match = re.search(r"[:/](?P<acct>[^/]+)/(?P<name>[^/.]+)", repo_url)
    gh_account, gh_repo = match.group("acct"), match.group("name")

    cmd = [
        "sam",
        "pipeline",
        "bootstrap",
        "--no-interactive",
        "--stage",
        stage,
        "--region",
        region,
        "--profile",
        profile,
        "--permissions-provider",
        "oidc",
        "--oidc-provider",
        "github-actions",
        "--oidc-provider-url",
        "https://token.actions.githubusercontent.com",
        "--oidc-client-id",
        "sts.amazonaws.com",
        "--oidc-github-organization",
        gh_account,
        "--oidc-github-repository",
        gh_repo,
        "--oidc-github-branch",
        gh_branch,
    ]
    if dry_run:
        click.echo(" ".join(cmd))
        return

    output = run(cmd, capture=True)
    click.echo(output)

    # ------------------------------------------------------------------- #
    # Extract resource info from CLI output or .aws-sam files
    # ------------------------------------------------------------------- #
    artefacts_bucket = _extract(output, r"Artifacts bucket:\s*(\S+)")
    pipeline_role = _extract(output, r"Pipeline execution role:\s*(arn:aws:[^\s]+)")
    cfn_role = _extract(output, r"CloudFormation execution role:\s*(arn:aws:[^\s]+)")

    if not (artefacts_bucket and pipeline_role and cfn_role):
        click.echo("• Could not parse all outputs from CLI; scanning .aws-sam …")
        artefacts_bucket, pipeline_role, cfn_role = _scan_aws_sam(stage)

    if artefacts_bucket and pipeline_role and cfn_role:
        env = load_env()
        env["TESTING_ARTIFACTS_BUCKET"] = artefacts_bucket
        env["TESTING_PIPELINE_EXECUTION_ROLE"] = pipeline_role
        env["TESTING_CLOUDFORMATION_EXECUTION_ROLE"] = cfn_role
        write_env(env)
        chezmoi_commit("Fill .env with SAM bootstrap outputs")
    else:
        click.echo(
            "⚠  SAM bootstrap succeeded but resource discovery failed – "
            "please update .env manually.",
            err=True,
        )


def _extract(text: str, pattern: str) -> Optional[str]:
    m = re.search(pattern, text, flags=re.IGNORECASE)
    return m.group(1) if m else None


def _scan_aws_sam(stage: str) -> tuple[Optional[str], Optional[str], Optional[str]]:
    artefacts_bucket = pipeline_role = cfn_role = None
    for path in Path(".aws-sam").rglob("*"):
        if not path.is_file() or path.suffix not in {".json", ".toml"}:
            continue
        try:
            content = path.read_text()
        except Exception:
            continue
        artefacts_bucket = artefacts_bucket or _extract(
            content, r"ArtifactsBucket[\"']?\s*[:=]\s*[\"']?([^\s\"']+)"
        )
        pipeline_role = pipeline_role or _extract(
            content,
            r"(?:PipelineExecutionRoleArn|PipelineExecutionRole)[\"']?\s*[:=]\s*[\"']?(arn:aws:[^\s\"']+)",
        )
        cfn_role = cfn_role or _extract(
            content,
            r"(?:CloudFormationExecutionRoleArn|CloudFormationExecutionRole)[\"']?\s*[:=]\s*[\"']?(arn:aws:[^\s\"']+)",
        )
    return artefacts_bucket, pipeline_role, cfn_role


# --------------------------------------------------------------------------- #
# 3. Fix broken PipelineExecutionRole trust policy
# --------------------------------------------------------------------------- #
@cli.command("fix-trust")
@click.option(
    "--stages-prefix",
    default=lambda: Path.cwd().name[:9],
    show_default="first 9 chars of repo",
    help="Prefix the SAM CLI adds to role names.",
)
def fix_trust(stages_prefix: str):
    """
    Locate the pipeline execution role created by SAM bootstrap and fix its
    trust policy (remove ForAllValues:StringLike issue).
    """
    env = load_env()
    gh_user, gh_repo = env["GH_ACCOUNT"], env["GH_REPO"]

    iam = boto3.client("iam")
    sts = boto3.client("sts")
    account_id = sts.get_caller_identity()["Account"]

    # Find role
    roles = iam.list_roles()["Roles"]
    candidates = [
        r["RoleName"]
        for r in roles
        if r["RoleName"].startswith(f"aws-sam-cli-managed-{stages_prefix}")
        and "PipelineExecutionRole" in r["RoleName"]
    ]
    if not candidates:
        click.echo("✗ No candidate PipelineExecutionRole found", err=True)
        sys.exit(1)
    role_name = candidates[0]
    click.echo(f"✓ found role {role_name}")

    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Federated": f"arn:aws:iam::{account_id}:oidc-provider/token.actions.githubusercontent.com"
                },
                "Action": "sts:AssumeRoleWithWebIdentity",
                "Condition": {
                    "StringLike": {
                        "token.actions.githubusercontent.com:sub": [
                            f"repo:{gh_user}/{gh_repo}:ref:refs/heads/main",
                            f"repo:{gh_user}/{gh_repo}:ref:refs/heads/dev",
                        ]
                    },
                    "StringEquals": {
                        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
                    },
                },
            }
        ],
    }

    try:
        iam.update_assume_role_policy(
            RoleName=role_name, PolicyDocument=json.dumps(policy)
        )
        click.echo("✓ trust policy fixed")
    except ClientError as e:
        click.echo(f"✗ update failed: {e}", err=True)
        sys.exit(1)


# --------------------------------------------------------------------------- #
# 4. Project rename
# --------------------------------------------------------------------------- #
@cli.command("rename")
@click.argument("new_name")
def rename_project(new_name: str):
    """
    Replace the default 'augint_library' occurrences with NEW_NAME and
    rename src/ directory. (Also sets version 0.0.0 in pyproject.toml.)
    """
    old_pkg_dir = Path("src/augint_library")
    if not old_pkg_dir.exists():
        click.echo("Expected src/augint_library to exist – aborting.", err=True)
        sys.exit(1)

    # Text replacements ---------------------------------------------------- #
    replace_in_file(
        Path("pyproject.toml"), r'name\s*=\s*"[A-Za-z0-9_\-]+"', f'name = "{new_name}"'
    )
    replace_in_file(
        Path("pyproject.toml"),
        r'version\s*=\s*"[0-9]+\.[0-9]+\.[0-9]+"',
        'version = "0.0.0"',
    )

    files_to_patch = [Path("README.md"), Path(".github/workflows/pipeline.yaml")]
    for f in files_to_patch:
        replace_in_file(f, r"augint-library", new_name)

    # Directory rename ----------------------------------------------------- #
    new_pkg_dir = Path(f"src/{new_name.replace('-', '_')}")
    new_pkg_dir.parent.mkdir(parents=True, exist_ok=True)
    old_pkg_dir.rename(new_pkg_dir)
    click.echo(f"✓ renamed package directory to {new_pkg_dir}")

    # Clear CHANGELOG
    Path("CHANGELOG.md").write_text("")
    click.echo("✓ cleared CHANGELOG.md")


# --------------------------------------------------------------------------- #
# 5. Finishing touches
# --------------------------------------------------------------------------- #
@cli.command("finalize")
def finalize():
    """
    Run pre-commit hooks, Poetry lock, and point user to PyPI Trusted Publisher.
    """
    run(["pre-commit", "install"])
    run(["pre-commit", "install", "--install-hooks"])
    run(["pre-commit", "run", "--all-files"])

    run(["poetry", "install"])
    run(["poetry", "lock"])

    click.echo(
        "\n➡  Final manual step: configure **Trusted Publishers**\n"
        "   1. https://pypi.org/manage/account/#trusted-publishers\n"
        "   2. https://test.pypi.org/manage/account/#trusted-publishers\n"
        "   Add this repo and approve branches main & dev.\n"
        "   PyPI does not (yet) expose an API for this – see docs:\n"
        "   https://docs.pypi.org/trusted-publishers/  "
    )


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    cli()
