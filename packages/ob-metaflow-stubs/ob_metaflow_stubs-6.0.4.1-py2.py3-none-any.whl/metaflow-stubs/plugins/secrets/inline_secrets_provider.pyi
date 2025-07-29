######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.16.0.1+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-07-14T20:31:43.621816                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import abc
import typing
if typing.TYPE_CHECKING:
    import abc
    import metaflow.plugins.secrets

from . import SecretsProvider as SecretsProvider

class InlineSecretsProvider(metaflow.plugins.secrets.SecretsProvider, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None):
        """
        Intended to be used for testing purposes only.
        """
        ...
    ...

