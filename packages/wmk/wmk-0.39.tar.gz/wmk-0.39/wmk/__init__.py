from .client_messages import ClientMessages
from .loader import Loader
from .media_consumer import MediaConsumer
from .messenger import Messenger
from .packager import Packager
from .player import Player
from .system_messages import SystemMessages
from .world_messages import WorldMessages


# Lazy loading for Pipecat transport classes
def __getattr__(name):
    pipecat_classes = [
        "PipecatVideoOutputProcessor",
        "PipecatAudioTransportParams",
        "PipecatAudioOutputTransport",
        "PipecatAudioInputTransport",
    ]

    if name in pipecat_classes:
        from .pipecat_transport import (
            PipecatAudioInputTransport,
            PipecatAudioOutputTransport,
            PipecatAudioTransportParams,
            PipecatVideoOutputProcessor,
        )

        return locals()[name]

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
    "Player",
    "Messenger",
    "WorldMessages",
    "ClientMessages",
    "SystemMessages",
    "Packager",
    "Loader",
    "MediaConsumer",
    "PipecatVideoOutputProcessor",
    "PipecatAudioTransportParams",
    "PipecatAudioOutputTransport",
    "PipecatAudioInputTransport",
]
