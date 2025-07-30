######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.2+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-16T22:08:50.165050                                                            #
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

