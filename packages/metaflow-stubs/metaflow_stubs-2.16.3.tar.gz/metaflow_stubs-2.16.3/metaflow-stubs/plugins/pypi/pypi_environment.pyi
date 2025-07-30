######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.16.3                                                                                 #
# Generated on 2025-07-16T15:23:11.202081                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...

