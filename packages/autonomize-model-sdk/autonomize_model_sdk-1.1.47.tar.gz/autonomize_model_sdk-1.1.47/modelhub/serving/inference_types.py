"""
Inference type definitions and detection logic for ModelHub serving.

This module provides a unified way to handle different input types
and automatically detect the appropriate processing method.
"""

import json
import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class InferenceType(str, Enum):
    """Supported inference types for model serving."""

    AUTO = "auto"
    TEXT = "text"
    IMAGE = "image"
    IMAGE_BASE64 = "image_base64"
    PDF_BYTES = "pdf_bytes"
    BYTE_STREAM = "byte_stream"
    OCR_TEXT = "ocr_text"
    STRUCTURED = "structured"
    RAW = "raw"
    TABULAR = "tabular"


class InferenceDetector:
    """Detects inference type from input data."""

    @staticmethod
    def detect_type(data: Dict[str, Any]) -> InferenceType:
        """
        Detect inference type from input data structure.

        Args:
            data: Input data dictionary

        Returns:
            Detected InferenceType
        """
        # Priority 1: Explicit inference_type in request
        if "inference_type" in data:
            return InferenceType(data["inference_type"])

        # Priority 2: Generic data field (new standard)
        if "data" in data:
            data_content = data["data"]

            # Detect binary data
            if isinstance(data_content, bytes):
                return InferenceType.BYTE_STREAM

            # Detect base64 strings (heuristic check)
            if isinstance(data_content, str) and len(data_content) > 100:
                # Check for common base64 image/PDF prefixes
                if any(
                    data_content.startswith(prefix)
                    for prefix in ["iVBOR", "/9j/", "JVBER"]
                ):
                    return (
                        InferenceType.IMAGE_BASE64
                        if data_content.startswith(("iVBOR", "/9j/"))
                        else InferenceType.BYTE_STREAM
                    )

            # Detect structured data (dict with multiple fields)
            if isinstance(data_content, dict):
                return InferenceType.STRUCTURED

            # Detect tabular data (list of dicts)
            if isinstance(data_content, list) and data_content:
                # Check if all items are dictionaries (tabular format)
                if all(isinstance(item, dict) for item in data_content):
                    return InferenceType.TABULAR

            # Default for other data types
            return InferenceType.RAW

        # Priority 3: Legacy field names (backward compatibility)
        # Byte stream patterns (PDF processing)
        if "byte_stream" in data:
            return InferenceType.BYTE_STREAM

        # Image patterns
        if "image_base64" in data:
            return InferenceType.IMAGE_BASE64
        if "image" in data or "images" in data:
            return InferenceType.IMAGE

        # OCR text pattern
        if "ocr_text_list" in data:
            return InferenceType.OCR_TEXT

        # Simple text
        if "text" in data:
            return InferenceType.TEXT

        # Structured data (check for specific field combinations)
        if InferenceDetector._is_structured_data(data):
            return InferenceType.STRUCTURED

        # Default to raw
        return InferenceType.RAW

    @staticmethod
    def _is_structured_data(data: Dict[str, Any]) -> bool:
        """Check if data matches known structured patterns."""
        # Known structured patterns
        structured_patterns = [
            {"hcpcs_code", "rate", "start_date", "end_date"},  # Accumulator
            {"contract_id", "member_id", "claim_id"},  # Claims
            {"patient_id", "provider_id", "diagnosis_code"},  # Medical records
        ]

        data_keys = set(data.keys())

        # Check if data keys match any known pattern
        for pattern in structured_patterns:
            if pattern.issubset(data_keys):
                return True

        return False


class InputTransformer:
    """Transforms various input formats to DataFrame for model prediction."""

    @staticmethod
    def transform(
        data: Dict[str, Any], inference_type: InferenceType
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Transform input data to DataFrame based on inference type.

        Args:
            data: Input data
            inference_type: Type of inference

        Returns:
            Tuple of (DataFrame, metadata)
        """
        metadata = {"inference_type": inference_type.value}

        if inference_type == InferenceType.TEXT:
            # Support both new "data" field and legacy "text" field
            if "data" in data:
                df = pd.DataFrame({"text": [data["data"]]})
            elif "text" in data:
                df = pd.DataFrame({"text": [data["text"]]})
            else:
                # Use the entire data dict as text if no specific field found
                df = pd.DataFrame({"text": [str(data)]})

        elif inference_type == InferenceType.BYTE_STREAM:
            # Support both new "data" field and legacy "byte_stream" field
            data_content = data.get("data", data.get("byte_stream"))
            df_data = {"data": [data_content]}
            if "page_numbers" in data:
                df_data["page_numbers"] = [data["page_numbers"]]
            df = pd.DataFrame(df_data)

        elif inference_type == InferenceType.IMAGE_BASE64:
            # Support both new "data" field and legacy "image_base64" field
            data_content = data.get("data", data.get("image_base64"))
            if not isinstance(data_content, list):
                data_content = [data_content]
            df = pd.DataFrame({"data": data_content})

        elif inference_type == InferenceType.IMAGE:
            # Handle binary image data
            if "image" in data:
                images = [data["image"]]
            else:
                images = data.get("images", [])
            df = pd.DataFrame({"image": images})

        elif inference_type == InferenceType.OCR_TEXT:
            # Handle OCR text with optional page numbers
            df_data = {"ocr_text": data["ocr_text_list"]}
            if "page_number_list" in data:
                df_data["page_number"] = data["page_number_list"]
            df = pd.DataFrame(df_data)

        elif inference_type == InferenceType.TABULAR:
            # Handle tabular data
            tabular_data = data["data"]
            if isinstance(tabular_data, list):
                df = pd.DataFrame(tabular_data)
            else:
                df = pd.DataFrame([tabular_data])

        elif inference_type == InferenceType.STRUCTURED:
            # Handle structured data in new and legacy formats
            if "data" in data:
                data_content = data["data"]
                if isinstance(data_content, dict):
                    # Flatten structured data: {"data": {"field1": "val1"}} -> {"field1": "val1"}
                    df = pd.DataFrame([data_content])
                else:
                    df = pd.DataFrame({"data": [data_content]})
            else:
                # Legacy format: structured fields directly in data
                df = pd.DataFrame([data])

        else:  # RAW
            # Pass through as-is
            df = pd.DataFrame([data])

        # Add any additional parameters as metadata
        if "parameters" in data:
            metadata["parameters"] = data["parameters"]

        return df, metadata


class OutputTransformer:
    """Transforms model output to consistent response format."""

    @staticmethod
    def transform(
        result: Any,
        output_columns: Optional[List[str]] = None,
        parse_json: bool = True,
        extract_single_column: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Transform model output to consistent format.

        Args:
            result: Raw model output
            output_columns: Specific columns to extract
            parse_json: Whether to parse JSON strings
            extract_single_column: Extract only this column
            metadata: Additional metadata to include

        Returns:
            Formatted response dictionary
        """
        response = {"status": 200, "data": {}, "error": None}

        # Add metadata
        if metadata:
            response["metadata"] = metadata

        try:
            # Handle DataFrame output
            if isinstance(result, pd.DataFrame):
                # Extract specific column if requested
                if extract_single_column and extract_single_column in result.columns:
                    data = result.at[0, extract_single_column]
                    # Convert pandas types to native Python types
                    if pd.api.types.is_bool_dtype(result[extract_single_column]):
                        data = bool(data)
                    elif pd.api.types.is_integer_dtype(result[extract_single_column]):
                        data = int(data)
                    elif pd.api.types.is_float_dtype(result[extract_single_column]):
                        data = float(data)
                    elif parse_json and isinstance(data, str):
                        try:
                            data = json.loads(data)
                        except json.JSONDecodeError:
                            pass
                    response["data"] = data

                # Extract multiple columns
                elif output_columns:
                    data = {}
                    for col in output_columns:
                        if col in result.columns:
                            value = result.at[0, col]
                            # Convert pandas types to native Python types
                            if pd.api.types.is_bool_dtype(result[col]):
                                value = bool(value)
                            elif pd.api.types.is_integer_dtype(result[col]):
                                value = int(value)
                            elif pd.api.types.is_float_dtype(result[col]):
                                value = float(value)
                            elif parse_json and isinstance(value, str):
                                try:
                                    value = json.loads(value)
                                except json.JSONDecodeError:
                                    pass
                            data[col] = value
                    response["data"] = data

                # Include all columns
                else:
                    data = {}
                    for col in result.columns:
                        if len(result) == 1:
                            # Single row
                            value = result.at[0, col]
                            # Convert pandas types to native Python types
                            if pd.api.types.is_bool_dtype(result[col]):
                                value = bool(value)
                            elif pd.api.types.is_integer_dtype(result[col]):
                                value = int(value)
                            elif pd.api.types.is_float_dtype(result[col]):
                                value = float(value)
                            elif parse_json and isinstance(value, str):
                                try:
                                    value = json.loads(value)
                                except json.JSONDecodeError:
                                    pass
                        else:
                            # Multiple rows
                            values = result[col].tolist()
                            if parse_json:
                                # Try to parse each item in the list
                                parsed_values = []
                                for v in values:
                                    if isinstance(v, str):
                                        try:
                                            parsed_values.append(json.loads(v))
                                        except json.JSONDecodeError:
                                            parsed_values.append(v)
                                    else:
                                        parsed_values.append(v)
                                value = parsed_values
                            else:
                                value = values
                        data[col] = value

                    response["data"] = data

            # Handle dictionary output
            elif isinstance(result, dict):
                # Check for special keys
                if "body" in result:
                    response["data"] = result["body"]
                else:
                    response["data"] = result

            # Handle list output
            elif isinstance(result, list):
                response["data"] = {"predictions": result}

            # Handle numpy arrays
            elif isinstance(result, np.ndarray):
                response["data"] = {"predictions": result.tolist()}

            # Handle scalar values
            else:
                response["data"] = {"prediction": result}

        except Exception as e:
            logger.error(f"Error transforming output: {str(e)}")
            response["status"] = 500
            response["error"] = str(e)

        return response


def create_unified_request(
    inputs: Dict[str, Any], inference_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a unified request format.

    Args:
        inputs: Input data
        inference_type: Optional inference type override

    Returns:
        Unified request dictionary
    """
    request = {"inputs": inputs}

    if inference_type:
        request["inference_type"] = inference_type

    return request


def parse_unified_request(
    request: Dict[str, Any]
) -> Tuple[Dict[str, Any], Optional[str]]:
    """
    Parse unified request format.

    Args:
        request: Request dictionary

    Returns:
        Tuple of (inputs, inference_type)
    """
    # Handle unified format
    if "inputs" in request:
        return request["inputs"], request.get("inference_type")

    # Handle legacy format (entire request is inputs)
    return request, None
