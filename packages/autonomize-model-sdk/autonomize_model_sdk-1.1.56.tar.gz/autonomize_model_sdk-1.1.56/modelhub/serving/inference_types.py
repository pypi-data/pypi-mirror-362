"""
Inference type definitions and detection logic for ModelHub serving.

This module provides a unified way to handle different input types
and automatically detect the appropriate processing method.

Key features:
- Magic byte detection for binary data (PNG, JPEG, PDF, GIF, BMP, TIFF)
- Automatic image format detection for application/octet-stream uploads
- Backward compatibility with base64 string detection
- Robust error handling and fallback mechanisms
"""

import base64
import json
import logging
from enum import Enum
from io import BytesIO
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

try:
    from pdf2image import convert_from_bytes
    from PIL import Image

    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

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
    EMBEDDING = "embedding"


class InferenceDetector:
    """Detects inference type from input data."""

    @staticmethod
    def _detect_binary_content_type(data_content: bytes) -> InferenceType:
        """
        Detect content type from binary data using magic bytes.

        Args:
            data_content: Binary data to analyze

        Returns:
            Appropriate InferenceType based on magic bytes
        """
        # Check magic bytes for different file formats
        if len(data_content) >= 8:
            # PNG magic bytes: 89 50 4E 47 0D 0A 1A 0A
            if data_content[:8] == b"\x89PNG\r\n\x1a\n":
                return InferenceType.IMAGE_BASE64

            # JPEG magic bytes: FF D8 FF
            elif data_content[:3] == b"\xff\xd8\xff":
                return InferenceType.IMAGE_BASE64

            # PDF magic bytes: %PDF
            elif data_content[:4] == b"%PDF":
                return InferenceType.BYTE_STREAM

            # GIF magic bytes: GIF87a or GIF89a
            elif data_content[:6] in [b"GIF87a", b"GIF89a"]:
                return InferenceType.IMAGE_BASE64

            # BMP magic bytes: BM
            elif data_content[:2] == b"BM":
                return InferenceType.IMAGE_BASE64

            # TIFF magic bytes: II*\0 or MM\0*
            elif data_content[:4] in [b"II*\x00", b"MM\x00*"]:
                return InferenceType.IMAGE_BASE64

        # If magic bytes don't match known formats, default to BYTE_STREAM
        return InferenceType.BYTE_STREAM

    @staticmethod
    def detect_type(data: Dict[str, Any]) -> InferenceType:
        """
        Detect inference type from input data structure.

        Detection priority:
        1. Explicit inference_type parameter
        2. Embedding request patterns (texts field)
        3. Binary data with magic byte detection for images/PDFs
        4. Base64 strings with prefix detection
        5. Structured data patterns
        6. Legacy field names (backward compatibility)
        7. Fallback to RAW

        Args:
            data: Input data dictionary

        Returns:
            Detected InferenceType
        """
        # Priority 1: Explicit inference_type in request
        if "inference_type" in data:
            return InferenceType(data["inference_type"])

        # Priority 2: Check for embedding request pattern
        if "texts" in data and isinstance(data.get("texts"), list):
            return InferenceType.EMBEDDING

        # Priority 3: Generic data field (new standard)
        if "data" in data:
            data_content = data["data"]

            # Detect binary data using magic bytes
            if isinstance(data_content, bytes):
                return InferenceDetector._detect_binary_content_type(data_content)

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

        # Structured data (check for specific field combinations)
        if InferenceDetector._is_structured_data(data):
            return InferenceType.STRUCTURED

        # Simple text (after structured check to avoid misclassification)
        if "text" in data:
            return InferenceType.TEXT

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
            {"source_text", "text_to_be_cited"},  # Citation generator
            {
                "document_uuid",
                "collection_name",
                "requested_medication",
            },  # Detailed summary
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
    def decode_input_data(data_content: Any) -> bytes:
        """
        Decode input data from various formats to bytes.

        Args:
            data_content: Input data in bytes, hex string, or base64 string format

        Returns:
            Decoded bytes

        Raises:
            ValueError: If data cannot be decoded
        """
        if isinstance(data_content, bytes):
            # Direct binary data
            return data_content
        elif isinstance(data_content, str):
            # Try hex decoding first (genesis-service-inference uses hex)
            try:
                return bytes.fromhex(data_content)
            except ValueError:
                # Fallback to base64 decoding
                try:
                    return base64.b64decode(data_content)
                except Exception as e:
                    raise ValueError(f"Failed to decode data as hex or base64: {e}")
        else:
            raise ValueError(f"Unsupported data type: {type(data_content)}")

    @staticmethod
    def pil_image_to_base64_str(image: "Image.Image") -> str:
        """
        Convert PIL Image to base64 string.

        Args:
            image: PIL Image object

        Returns:
            Base64 encoded string
        """
        if not PDF_SUPPORT:
            raise ImportError("PIL is required for image processing")

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return img_str

    @staticmethod
    def convert_pdf_to_images(
        pdf_bytes: bytes, page_numbers: Optional[List[int]] = None
    ) -> List["Image.Image"]:
        """
        Convert PDF bytes to PIL Images.

        Args:
            pdf_bytes: PDF content as bytes
            page_numbers: Optional list of page numbers to extract (1-indexed)

        Returns:
            List of PIL Image objects

        Raises:
            ImportError: If pdf2image is not available
            ValueError: If PDF conversion fails
        """
        if not PDF_SUPPORT:
            raise ImportError("pdf2image and PIL are required for PDF processing")

        try:
            all_images = convert_from_bytes(pdf_bytes)

            # Filter pages if specified
            if page_numbers:
                filtered_images = []
                for pg in page_numbers:
                    if pg < 1 or pg > len(all_images):
                        logger.warning(f"Page {pg} out of range (1–{len(all_images)})")
                        continue
                    filtered_images.append(all_images[pg - 1])  # Convert to 0-indexed
                return filtered_images
            else:
                return all_images
        except Exception as e:
            raise ValueError(f"Failed to convert PDF to images: {e}")

    @staticmethod
    def process_image_base64_list(data_content: List[str]) -> List["Image.Image"]:
        """
        Process a list of base64 image strings to PIL Images.

        Args:
            data_content: List of base64 encoded image strings

        Returns:
            List of PIL Image objects
        """
        if not PDF_SUPPORT:
            raise ImportError("PIL is required for image processing")

        images = []
        for img_b64 in data_content:
            try:
                img_bytes = base64.b64decode(img_b64)
                img = Image.open(BytesIO(img_bytes))
                images.append(img)
            except Exception as e:
                logger.error(f"Error decoding base64 image: {e}")
                continue
        return images

    @staticmethod
    def process_multiformat_input(
        data_content: Any, page_numbers: Optional[List[int]] = None
    ) -> List["Image.Image"]:
        """
        Process input data in multiple formats to PIL Images.
        This method handles the common patterns found in pharmacy models.

        Args:
            data_content: Input data in various formats (bytes, str, list)
            page_numbers: Optional list of page numbers to extract (1-indexed)

        Returns:
            List of PIL Image objects

        Raises:
            ImportError: If required dependencies are not available
            ValueError: If data cannot be processed
        """
        if not PDF_SUPPORT:
            raise ImportError(
                "pdf2image and PIL are required for multiformat processing"
            )

        # Handle list of base64 images (image_base64 inference type)
        if isinstance(data_content, list):
            return InputTransformer.process_image_base64_list(data_content)

        # Handle string data (could be hex-encoded PDF or base64 image/PDF)
        elif isinstance(data_content, str):
            # First, try to decode as hex (from byte_stream inference type)
            try:
                pdf_bytes = bytes.fromhex(data_content)
                return InputTransformer.convert_pdf_to_images(pdf_bytes, page_numbers)
            except ValueError:
                # Not hex encoded, try as base64 PDF
                try:
                    pdf_bytes = base64.b64decode(data_content)
                    return InputTransformer.convert_pdf_to_images(
                        pdf_bytes, page_numbers
                    )
                except Exception:
                    # Try as single base64 image
                    try:
                        img_bytes = base64.b64decode(data_content)
                        img = Image.open(BytesIO(img_bytes))
                        return [img]
                    except Exception as e:
                        raise ValueError(
                            f"Failed to process string data as PDF or image: {e}"
                        )

        # Handle direct binary data (application/octet-stream)
        elif isinstance(data_content, bytes):
            return InputTransformer.convert_pdf_to_images(data_content, page_numbers)

        else:
            raise ValueError(f"Unsupported data type: {type(data_content)}")

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
            page_numbers = data.get("page_numbers")

            try:
                # Decode input data to bytes
                pdf_bytes = InputTransformer.decode_input_data(data_content)

                # Check magic bytes to determine if this is actually a PDF or image
                detected_type = InferenceDetector._detect_binary_content_type(pdf_bytes)

                # If detected as IMAGE_BASE64, skip PDF conversion to avoid warnings
                if detected_type == InferenceType.IMAGE_BASE64:
                    logger.info(
                        "Binary data detected as image format, skipping PDF conversion"
                    )
                    # Store raw data without PDF conversion attempt
                    # For image data, only include the data column to match model signatures
                    df_data = {
                        "data": [data_content],
                    }
                    if page_numbers:
                        df_data["page_numbers"] = [page_numbers]
                    df = pd.DataFrame(df_data)
                    metadata["pdf_processed"] = False
                    metadata["detected_as_image"] = True

                # Only try PDF conversion if it's actually a PDF or unknown format
                elif PDF_SUPPORT:
                    try:
                        images = InputTransformer.convert_pdf_to_images(
                            pdf_bytes, page_numbers
                        )
                        # Convert images to base64 strings for DataFrame compatibility
                        image_base64_list = [
                            InputTransformer.pil_image_to_base64_str(img)
                            for img in images
                        ]
                        df_data = {
                            "data": [
                                data_content
                            ],  # Keep original data format for models
                            "images": [image_base64_list],  # Add converted images
                            "decoded_bytes": [
                                pdf_bytes.hex()
                            ],  # Add hex representation
                        }
                        if page_numbers:
                            df_data["page_numbers"] = [page_numbers]
                        df = pd.DataFrame(df_data)
                        # Add PDF processing metadata
                        metadata["pdf_processed"] = True
                        metadata["num_pages"] = len(images)
                    except ValueError as e:
                        logger.warning(f"PDF conversion failed, storing raw data: {e}")
                        # Fallback to storing raw data
                        df_data = {
                            "data": [data_content],
                            "decoded_bytes": [pdf_bytes.hex()],
                        }
                        if page_numbers:
                            df_data["page_numbers"] = [page_numbers]
                        df = pd.DataFrame(df_data)
                        metadata["pdf_processed"] = False
                else:
                    # No PDF support, store raw data
                    df_data = {
                        "data": [data_content],
                        "decoded_bytes": [pdf_bytes.hex()],
                    }
                    if page_numbers:
                        df_data["page_numbers"] = [page_numbers]
                    df = pd.DataFrame(df_data)
                    metadata["pdf_processed"] = False

            except ValueError as e:
                logger.error(f"Failed to decode byte stream data: {e}")
                # Fallback to original behavior
                if isinstance(data_content, bytes):
                    data_content = data_content.hex()
                df_data = {"data": [data_content]}
                if page_numbers:
                    df_data["page_numbers"] = [page_numbers]
                df = pd.DataFrame(df_data)
                metadata["decode_error"] = str(e)

        elif inference_type == InferenceType.IMAGE_BASE64:
            # Support both new "data" field and legacy "image_base64" field
            data_content = data.get("data", data.get("image_base64"))

            # Handle binary image data (detected by magic bytes)
            # This handles cases where binary images (PNG, JPEG, etc.) are sent
            # via application/octet-stream but detected as IMAGE_BASE64 type
            if isinstance(data_content, bytes):
                if PDF_SUPPORT:
                    try:
                        import io

                        from PIL import Image

                        # Convert binary image to PIL Image
                        img = Image.open(io.BytesIO(data_content))
                        # Convert to base64 string for consistency
                        img_b64 = InputTransformer.pil_image_to_base64_str(img)

                        df_data = {
                            "data": [
                                img_b64
                            ],  # Store as base64 for model compatibility
                            "processed_images": [
                                [img_b64]
                            ],  # Store as list of base64 strings
                        }
                        metadata["num_images"] = 1
                        metadata["images_processed"] = True
                    except Exception as e:
                        logger.warning(f"Binary image processing failed: {e}")
                        # Fallback to storing raw data
                        df_data = {"data": [data_content]}
                        metadata["images_processed"] = False
                else:
                    # No PIL support, store raw data
                    df_data = {"data": [data_content]}
                    metadata["images_processed"] = False

                df = pd.DataFrame(df_data)

            # Handle different input formats
            elif isinstance(data_content, list):
                # List of base64 images - create multiple rows for each image
                df_data = {"data": data_content}
                metadata["num_images"] = len(data_content)
                metadata["images_processed"] = False
            else:
                # Single base64 image
                df_data = {"data": [data_content]}
                metadata["num_images"] = 1
                metadata["images_processed"] = False

            df = pd.DataFrame(df_data)

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

        elif inference_type == InferenceType.EMBEDDING:
            # Handle embedding request format
            texts = data.get("texts", [])
            # Store as single row with list of texts
            df = pd.DataFrame({"texts": [texts]})
            # Add model_name to metadata if provided
            if "model_name" in data:
                metadata["model_name"] = data["model_name"]

        elif inference_type == InferenceType.STRUCTURED:
            # Handle structured data in new and legacy formats
            if "data" in data:
                df = pd.DataFrame([data])
            else:
                # Legacy format: structured fields directly in data
                # Handle multimodal content in text fields
                processed_data = {}
                for key, value in data.items():
                    if key == "text" and isinstance(value, list):
                        # Extract text from multimodal content
                        text_parts = []
                        for item in value:
                            if isinstance(item, dict) and item.get("type") == "text":
                                text_parts.append(item.get("text", ""))
                        # Join all text parts
                        processed_data[key] = " ".join(text_parts) if text_parts else ""
                    else:
                        processed_data[key] = value
                df = pd.DataFrame([processed_data])

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
            # Special handling for embedding response format
            if (
                metadata
                and metadata.get("inference_type") == InferenceType.EMBEDDING.value
            ):
                # Check if result is a DataFrame with embeddings
                if isinstance(result, pd.DataFrame):
                    # Look for common embedding column names
                    embedding_columns = [
                        "embeddings",
                        "embedding",
                        "prediction",
                        "predictions",
                    ]
                    for col in embedding_columns:
                        if col in result.columns:
                            embeddings = result.at[0, col]
                            # Parse JSON if needed
                            if isinstance(embeddings, str):
                                try:
                                    embeddings = json.loads(embeddings)
                                except json.JSONDecodeError:
                                    pass
                            # Return in the exact format required
                            return {"prediction": embeddings}

                    # If no standard column found, try to extract from first column
                    if len(result.columns) > 0:
                        embeddings = result.iloc[0, 0]
                        if isinstance(embeddings, str):
                            try:
                                embeddings = json.loads(embeddings)
                            except json.JSONDecodeError:
                                pass
                        return {"prediction": embeddings}

                # Handle dict result
                elif isinstance(result, dict):
                    # Look for embeddings in common keys
                    for key in ["embeddings", "embedding", "prediction", "predictions"]:
                        if key in result:
                            return {"prediction": result[key]}
                    # If has 'data' wrapper, check inside
                    if "data" in result:
                        data = result["data"]
                        if isinstance(data, dict):
                            for key in [
                                "embeddings",
                                "embedding",
                                "prediction",
                                "predictions",
                            ]:
                                if key in data:
                                    return {"prediction": data[key]}

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
                    body_data = result["body"]
                    # Convert numpy arrays to lists for JSON serialization
                    if isinstance(body_data, np.ndarray):
                        response["data"] = body_data.tolist()
                    else:
                        response["data"] = body_data
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
