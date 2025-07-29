# SPDX-FileCopyrightText: 2025 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path
from typing import Optional

import gitlab
from termcolor import colored

from .. import pullyfile
from ..constants import BASE_DIR
from ..pullyfile import PullyProject


def get_gitlab_group_id_from_full_path(gl: gitlab.Gitlab, group_path: str) -> int:
    print("searching for group id by full path")
    groups = gl.groups.list(search=group_path)
    for group in groups:
        if group.full_path == group_path:
            return group.id
    raise ValueError("group id not found")


def get_gitlab_project_id_from_full_path(glgroup, project_path: str) -> int:
    print("searching for project id by full path")
    glprojects = glgroup.projects.list(search=project_path)
    for glproject in glprojects:
        if glproject.path == project_path:
            return glproject.id
    raise ValueError("project id not found")


def get_gitlab_group_id(gl: gitlab.Gitlab, args) -> Optional[int]:
    if args.group_path:
        return get_gitlab_group_id_from_full_path(gl, args.group_path)
    return args.group_id


def get_gitlab_project_id(gl: gitlab.Gitlab, args) -> Optional[int]:
    if args.project_path:
        return get_gitlab_project_id_from_full_path(gl, args.project_path)
    return args.project_id


def add_command(args):
    gl = gitlab.Gitlab()

    group_id = None
    project_id = None

    if args.group_path:
        group_id = get_gitlab_group_id_from_full_path(gl, args.group_path)
    elif args.group_id:
        group_id = args.group_id
    elif args.project_path:
        project_path = Path(args.project_path)
        group_path = str(project_path.parent)
        group_id = get_gitlab_group_id_from_full_path(gl, group_path)
        glgroup = gl.groups.get(group_id)
        project_id = get_gitlab_project_id_from_full_path(
            glgroup, str(project_path.name)
        )
        group_id = None
    elif args.project_id:
        project_id = args.project_id

    if group_id and project_id:
        raise ValueError("found both group id and project id")

    if group_id:
        print("found group id:", group_id)
    elif project_id:
        print("found project id:", project_id)

    if group_id:
        glgroup = gl.groups.get(id=group_id)
        glprojects = glgroup.projects.list(
            archived=False,
            visibility="public",
            include_subgroups=True,
            order_by="name",
            sort="asc",
            limit=3,
            all=True,
        )
    elif project_id:
        glprojects = [gl.projects.get(id=project_id)]

    with pullyfile.project_context(BASE_DIR) as context:
        config_dir, projects = context
        for glproject in glprojects:
            if glproject.id in projects:
                continue
            projects[glproject.id] = PullyProject(
                project_id=glproject.id,
                local_path=glproject.path_with_namespace,
                ssh_url=glproject.ssh_url_to_repo,
            )
            print(colored("adding", "green"), glproject.path_with_namespace)
