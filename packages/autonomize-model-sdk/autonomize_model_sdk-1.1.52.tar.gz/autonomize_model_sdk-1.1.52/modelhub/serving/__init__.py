# Legacy imports for backward compatibility
# TODO: Remove when model_service.py is updated to remove kserve dependency
# from modelhub.serving.model_service import (
#     ImageModelService,
#     ModelhubModelService,
#     ModelServiceGroup,
# )

# New protocol-compliant imports
from modelhub.serving.base import AutoModelPredictor, ModelHubPredictor
from modelhub.serving.protocol import (
    DataType,
    InferInputTensor,
    InferOutputTensor,
    InferRequest,
    InferResponse,
)
from modelhub.serving.server import ModelServer, create_server_from_env

__all__ = [
    # Legacy classes (temporarily disabled)
    # "ModelhubModelService",
    # "ImageModelService",
    # "ModelServiceGroup",
    # New classes
    "ModelHubPredictor",
    "AutoModelPredictor",
    "ModelServer",
    "create_server_from_env",
    # Protocol types
    "InferRequest",
    "InferResponse",
    "InferInputTensor",
    "InferOutputTensor",
    "DataType",
]
