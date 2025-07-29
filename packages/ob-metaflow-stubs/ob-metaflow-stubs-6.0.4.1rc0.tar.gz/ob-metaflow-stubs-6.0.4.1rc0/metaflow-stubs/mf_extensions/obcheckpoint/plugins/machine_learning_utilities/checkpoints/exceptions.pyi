######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.16.0.1+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-07-14T20:03:25.617782                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ......exception import MetaflowException as MetaflowException

class CheckpointNotAvailableException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

class CheckpointException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

