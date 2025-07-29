"""
Base classes for ModelHub serving that are protocol-compliant with KServe V2.
"""

import json
import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from autonomize.core.credential import ModelhubCredential
from modelhub.clients import MLflowClient

from .inference_types import (
    InferenceDetector,
    InferenceType,
    InputTransformer,
    OutputTransformer,
    parse_unified_request,
)
from .protocol import (
    InferOutputTensor,
    InferRequest,
    InferResponse,
    ModelMetadata,
    deserialize_request,
    serialize_response,
)

logger = logging.getLogger(__name__)


class ModelHubPredictor(ABC):
    """
    Base predictor class that implements KServe V2 protocol.

    This class can be used standalone or deployed in KServe.
    """

    def __init__(
        self,
        name: str,
        model_uri: Optional[str] = None,
        model_name: Optional[str] = None,
        model_version: Optional[str] = None,
    ):
        """
        Initialize the predictor.

        Args:
            name: Name of the model service
            model_uri: MLflow model URI (e.g., "runs:/abc123/model")
            model_name: Model name for registry lookup
            model_version: Model version for registry lookup
        """
        self.name = name
        self.model_uri = model_uri
        self.model_name = model_name
        self.model_version = model_version
        self.model = None
        self.ready = False
        self.model_metadata = None

        # Initialize MLflow client
        credential = ModelhubCredential()
        self.mlflow_client = MLflowClient(
            credential=credential,
            client_id=os.getenv("CLIENT_ID"),
            copilot_id=os.getenv("COPILOT_ID"),
        )

        logger.info(
            f"Initialized ModelHubPredictor: {name} "
            f"(uri: {model_uri}, name: {model_name}, version: {model_version})"
        )

    def load(self) -> bool:
        """Load the model from MLflow."""
        try:
            # Determine model URI
            if self.model_uri:
                uri = self.model_uri
            elif self.model_name and self.model_version:
                uri = f"models:/{self.model_name}/{self.model_version}"
            elif self.model_name:
                uri = f"models:/{self.model_name}/latest"
            else:
                raise ValueError("Either model_uri or model_name must be provided")

            logger.info(f"Loading model from URI: {uri}")

            # Load model
            self.model = self.mlflow_client.mlflow.pyfunc.load_model(uri)

            # Get model signature and metadata
            model_info = self.mlflow_client.mlflow.models.get_model_info(uri)
            self.model_metadata = self._extract_metadata(model_info)

            self.ready = True
            logger.info("Model loaded successfully")
            return True

        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def _extract_metadata(self, model_info: Any) -> ModelMetadata:
        """Extract metadata from MLflow model info."""
        inputs = []
        outputs = []

        if hasattr(model_info, "signature") and model_info.signature:
            # Extract input schema
            if model_info.signature.inputs:
                schema = model_info.signature.inputs
                if hasattr(schema, "inputs"):
                    for inp in schema.inputs:
                        inputs.append(
                            {
                                "name": inp.name or "input",
                                "datatype": str(inp.type),
                                "shape": [-1],  # Dynamic shape
                            }
                        )

            # Extract output schema
            if model_info.signature.outputs:
                schema = model_info.signature.outputs
                if hasattr(schema, "outputs"):
                    for out in schema.outputs:
                        outputs.append(
                            {
                                "name": out.name or "output",
                                "datatype": str(out.type),
                                "shape": [-1],
                            }
                        )

        return ModelMetadata(
            name=self.name, platform="mlflow", inputs=inputs, outputs=outputs
        )

    @abstractmethod
    def predict(
        self,
        request: Union[InferRequest, Dict[str, Any]],
        headers: Optional[Dict[str, str]] = None,
    ) -> Union[InferResponse, Dict[str, Any]]:
        """
        Make a prediction. Must be implemented by subclasses.

        Args:
            request: Inference request (either InferRequest or dict)
            headers: Optional HTTP headers

        Returns:
            Inference response (either InferResponse or dict)
        """

    def health_check(self) -> Dict[str, Any]:
        """Health check endpoint."""
        return {
            "status": "ready" if self.ready else "loading",
            "model_name": self.name,
            "model_uri": self.model_uri,
        }

    def model_ready(self) -> bool:
        """Check if model is ready."""
        return self.ready

    def get_model_metadata(self) -> Dict[str, Any]:
        """Get model metadata."""
        if not self.model_metadata:
            return {"name": self.name, "platform": "mlflow", "versions": ["1"]}

        return {
            "name": self.model_metadata.name,
            "platform": self.model_metadata.platform,
            "inputs": self.model_metadata.inputs,
            "outputs": self.model_metadata.outputs,
        }


class AutoModelPredictor(ModelHubPredictor):
    """
    Automatic model predictor that detects input type and routes accordingly.
    """

    def __init__(self, *args, **kwargs):
        """Initialize with optional inference type override."""
        self.inference_type_override = kwargs.pop("inference_type", None)
        if self.inference_type_override:
            self.inference_type_override = InferenceType(self.inference_type_override)
        super().__init__(*args, **kwargs)

    def predict(
        self,
        request: Union[InferRequest, Dict[str, Any]],
        headers: Optional[Dict[str, str]] = None,
    ) -> Union[InferResponse, Dict[str, Any]]:
        """
        Predict with automatic input type detection.
        """
        if not self.ready:
            return {"error": "Model not loaded", "status": 503}

        try:
            # Handle both InferRequest and dict formats
            if isinstance(request, dict):
                # Check if it's a V2 protocol request
                if "inputs" in request and isinstance(request.get("inputs"), list):
                    request_obj = deserialize_request(request)
                    return self._predict_v2(request_obj)
                else:
                    # Unified or legacy format
                    return self._predict_unified(request)
            else:
                return self._predict_v2(request)

        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return {"error": str(e), "status": 400}

    def _predict_v2(self, request: InferRequest) -> Dict[str, Any]:
        """Handle V2 protocol prediction."""
        # Extract data from first input tensor
        if not request.inputs:
            raise ValueError("No inputs provided")

        input_tensor = request.inputs[0]

        # Handle different input types based on datatype
        if input_tensor.datatype == "BYTES":
            # Binary data (image, PDF)
            if len(input_tensor.data) == 1:
                # Single file
                data = input_tensor.data[0]
                df = pd.DataFrame({"data": [data]})
            else:
                # Multiple files
                df = pd.DataFrame({"data": input_tensor.data})
        else:
            # Numeric data
            import numpy as np

            shape = input_tensor.shape
            data = np.array(input_tensor.data).reshape(shape)
            df = pd.DataFrame(data)

        # Make prediction
        result = self.model.predict(df)

        # Convert result to output tensor
        outputs = self._convert_to_output_tensors(result)

        response = InferResponse(
            model_name=self.name, model_version="1", id=request.id, outputs=outputs
        )

        return serialize_response(response)

    def _predict_unified(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle unified format prediction with automatic type detection."""
        # Parse unified request format
        inputs, inference_type_str = parse_unified_request(request)

        # Determine inference type
        if (
            self.inference_type_override
            and self.inference_type_override != InferenceType.AUTO
        ):
            inference_type = self.inference_type_override
        elif inference_type_str:
            inference_type = InferenceType(inference_type_str)
        else:
            inference_type = InferenceDetector.detect_type(inputs)

        logger.info(f"Detected inference type: {inference_type}")

        # Transform input to DataFrame
        df, metadata = InputTransformer.transform(inputs, inference_type)

        # Make prediction
        result = self.model.predict(df)

        # Extract output columns from model metadata if available
        output_columns = None
        if self.model_metadata and self.model_metadata.outputs:
            output_columns = [
                output.get("name") for output in self.model_metadata.outputs
            ]

        # Transform output to consistent format
        response = OutputTransformer.transform(
            result, output_columns=output_columns, metadata=metadata
        )

        return response

    def _convert_to_output_tensors(self, result: Any) -> List[InferOutputTensor]:
        """Convert prediction result to output tensors."""
        import numpy as np

        from .protocol import numpy_to_infer_tensor

        outputs = []

        if isinstance(result, np.ndarray):
            outputs.append(numpy_to_infer_tensor("output", result))
        elif isinstance(result, pd.DataFrame):
            # Convert dataframe to dict and then to JSON bytes
            data = result.to_dict(orient="records")
            json_str = json.dumps(data)
            outputs.append(
                InferOutputTensor(
                    name="output",
                    shape=[1],
                    datatype="BYTES",
                    data=[json_str.encode("utf-8")],
                )
            )
        elif isinstance(result, (list, dict)):
            # Convert to JSON bytes
            json_str = json.dumps(result)
            outputs.append(
                InferOutputTensor(
                    name="output",
                    shape=[1],
                    datatype="BYTES",
                    data=[json_str.encode("utf-8")],
                )
            )
        else:
            # Convert to string
            outputs.append(
                InferOutputTensor(
                    name="output",
                    shape=[1],
                    datatype="BYTES",
                    data=[str(result).encode("utf-8")],
                )
            )

        return outputs
