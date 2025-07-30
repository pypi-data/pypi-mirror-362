######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.16.2                                                                                 #
# Generated on 2025-07-15T23:31:58.856406                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...

