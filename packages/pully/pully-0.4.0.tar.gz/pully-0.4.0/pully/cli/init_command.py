# SPDX-FileCopyrightText: 2025 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0


from .. import pullyfile
from ..constants import BASE_DIR
from ..pullyfile import PullyFile


def init_command(args):
    print("creating empty pully workspace at", BASE_DIR)
    new_config = PullyFile()
    pullyfile.dump(new_config, BASE_DIR)
