# SPDX-FileCopyrightText: 2025 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

import subprocess
from pathlib import Path

from termcolor import colored

from .. import pullyfile
from ..constants import BASE_DIR
from ..pullyfile import PullyProject


def clone_project(config_dir: Path, project: PullyProject):
    repo_dir = config_dir / project.local_path
    repo_dir.mkdir(exist_ok=True, parents=True)
    print(
        colored("cloning", "green"),
        project.local_path,
        colored(f"({project.project_id})", "green"),
    )
    try:
        subprocess.run(
            ["git", "clone", project.ssh_url, repo_dir / project.local_path],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as excinfo:
        print(
            colored("failed", "yellow"),
            project.local_path,
            colored("(git error)", "yellow"),
        )


def sync_project(config_dir: Path, project: PullyProject):
    git_dir = config_dir / project.local_path / ".git"
    if not git_dir.exists():
        clone_project(config_dir, project)


def sync_command(args):
    with pullyfile.project_context(BASE_DIR) as context:
        config_dir, projects = context
        for project_id, project in projects.items():
            sync_project(config_dir, project)
