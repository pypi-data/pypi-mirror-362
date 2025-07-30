"""
KServe V2 Protocol implementation for ModelHub serving.

This module provides protocol-compliant classes that work with KServe
without requiring KServe as a dependency.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import numpy as np


class DataType(str, Enum):
    """Data types supported by the V2 protocol."""

    BOOL = "BOOL"
    UINT8 = "UINT8"
    UINT16 = "UINT16"
    UINT32 = "UINT32"
    UINT64 = "UINT64"
    INT8 = "INT8"
    INT16 = "INT16"
    INT32 = "INT32"
    INT64 = "INT64"
    FP16 = "FP16"
    FP32 = "FP32"
    FP64 = "FP64"
    BYTES = "BYTES"


@dataclass
class InferTensorContents:
    """Contents of an inference tensor."""

    # Only include the fields that are actually used
    int_contents: Optional[List[int]] = None
    int64_contents: Optional[List[int]] = None
    uint_contents: Optional[List[int]] = None
    uint64_contents: Optional[List[int]] = None
    fp32_contents: Optional[List[float]] = None
    fp64_contents: Optional[List[float]] = None
    bytes_contents: Optional[List[bytes]] = None


@dataclass
class InferInputTensor:
    """Input tensor for inference request."""

    name: str
    shape: List[int]
    datatype: str
    data: List[Any] = field(default_factory=list)
    contents: Optional[InferTensorContents] = None
    parameters: Optional[Dict[str, Any]] = field(default_factory=dict)


@dataclass
class InferOutputTensor:
    """Output tensor for inference response."""

    name: str
    shape: List[int]
    datatype: str
    data: List[Any] = field(default_factory=list)
    contents: Optional[InferTensorContents] = None
    parameters: Optional[Dict[str, Any]] = field(default_factory=dict)


@dataclass
class InferRequest:
    """V2 Inference Request."""

    model_name: Optional[str] = None
    model_version: Optional[str] = None
    id: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = field(default_factory=dict)
    inputs: List[InferInputTensor] = field(default_factory=list)
    outputs: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    raw_input_contents: Optional[List[bytes]] = None


@dataclass
class InferResponse:
    """V2 Inference Response."""

    model_name: str
    model_version: Optional[str] = None
    id: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = field(default_factory=dict)
    outputs: List[InferOutputTensor] = field(default_factory=list)
    raw_output_contents: Optional[List[bytes]] = None


@dataclass
class ModelMetadata:
    """Model metadata response."""

    name: str
    versions: Optional[List[str]] = None
    platform: str = "mlflow"
    inputs: Optional[List[Dict[str, Any]]] = None
    outputs: Optional[List[Dict[str, Any]]] = None


def serialize_tensor(
    tensor: Union[InferInputTensor, InferOutputTensor]
) -> Dict[str, Any]:
    """Serialize tensor to dictionary format."""
    result = {"name": tensor.name, "shape": tensor.shape, "datatype": tensor.datatype}

    if tensor.data:
        result["data"] = tensor.data

    if tensor.parameters:
        result["parameters"] = tensor.parameters

    return result


def deserialize_input_tensor(data: Dict[str, Any]) -> InferInputTensor:
    """Deserialize input tensor from dictionary."""
    return InferInputTensor(
        name=data["name"],
        shape=data["shape"],
        datatype=data["datatype"],
        data=data.get("data", []),
        parameters=data.get("parameters", {}),
    )


def serialize_request(request: InferRequest) -> Dict[str, Any]:
    """Serialize inference request to dictionary."""
    result = {}

    if request.model_name:
        result["model_name"] = request.model_name
    if request.model_version:
        result["model_version"] = request.model_version
    if request.id:
        result["id"] = request.id
    if request.parameters:
        result["parameters"] = request.parameters

    result["inputs"] = [serialize_tensor(inp) for inp in request.inputs]

    if request.outputs:
        result["outputs"] = request.outputs

    return result


def deserialize_request(data: Dict[str, Any]) -> InferRequest:
    """Deserialize inference request from dictionary."""
    return InferRequest(
        model_name=data.get("model_name"),
        model_version=data.get("model_version"),
        id=data.get("id"),
        parameters=data.get("parameters", {}),
        inputs=[deserialize_input_tensor(inp) for inp in data.get("inputs", [])],
        outputs=data.get("outputs", []),
    )


def serialize_response(response: InferResponse) -> Dict[str, Any]:
    """Serialize inference response to dictionary."""
    result = {
        "model_name": response.model_name,
        "outputs": [serialize_tensor(out) for out in response.outputs],
    }

    if response.model_version:
        result["model_version"] = response.model_version
    if response.id:
        result["id"] = response.id
    if response.parameters:
        result["parameters"] = response.parameters

    return result


def numpy_to_infer_tensor(name: str, array: np.ndarray) -> InferOutputTensor:
    """Convert numpy array to inference tensor."""
    # Map numpy dtypes to protocol data types
    dtype_map = {
        np.bool_: DataType.BOOL,
        np.uint8: DataType.UINT8,
        np.uint16: DataType.UINT16,
        np.uint32: DataType.UINT32,
        np.uint64: DataType.UINT64,
        np.int8: DataType.INT8,
        np.int16: DataType.INT16,
        np.int32: DataType.INT32,
        np.int64: DataType.INT64,
        np.float32: DataType.FP32,
        np.float64: DataType.FP64,
    }

    # Get the protocol datatype
    protocol_dtype = dtype_map.get(array.dtype.type, DataType.FP32)

    # Flatten the array and convert to list
    data = array.flatten().tolist()

    return InferOutputTensor(
        name=name, shape=list(array.shape), datatype=protocol_dtype, data=data
    )
