######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.16.2                                                                                 #
# Generated on 2025-07-15T23:31:58.869116                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import abc
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.secrets
    import abc

from . import SecretsProvider as SecretsProvider

class InlineSecretsProvider(metaflow.plugins.secrets.SecretsProvider, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None):
        """
        Intended to be used for testing purposes only.
        """
        ...
    ...

