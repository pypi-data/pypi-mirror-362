"""
FastAPI server implementation for ModelHub serving with KServe V2 protocol support.
"""

import asyncio
import logging
import os
from typing import Dict, List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from .base import ModelHubPredictor

logger = logging.getLogger(__name__)


class ModelServer:
    """
    FastAPI-based model server that implements KServe V2 protocol.

    Can be used standalone or deployed as a KServe custom container.
    """

    def __init__(self, models: Optional[List[ModelHubPredictor]] = None):
        """
        Initialize the model server.

        Args:
            models: List of model predictors to serve
        """
        self.app = FastAPI(
            title="ModelHub Inference Server",
            description="KServe V2 protocol compliant inference server",
            version="2.0.0",
        )

        self.models: Dict[str, ModelHubPredictor] = {}
        if models:
            for model in models:
                self.models[model.name] = model

        self._setup_routes()

    def _setup_routes(self):
        """Setup FastAPI routes for V2 protocol."""

        @self.app.get("/")
        async def root():
            return {"message": "ModelHub Inference Server", "protocol": "v2"}

        @self.app.get("/v2/health/live")
        async def health_live():
            return {"live": True}

        @self.app.get("/v2/health/ready")
        async def health_ready():
            # Check if all models are ready
            all_ready = all(model.ready for model in self.models.values())
            if not all_ready:
                raise HTTPException(status_code=503, detail="Models not ready")
            return {"ready": True}

        @self.app.get("/v2/models")
        async def list_models():
            """List all available models."""
            models = []
            for name, model in self.models.items():
                models.append({"name": name, "ready": model.ready})
            return {"models": models}

        @self.app.get("/v2/models/{model_name}")
        async def model_metadata(model_name: str):
            """Get model metadata."""
            if model_name not in self.models:
                raise HTTPException(
                    status_code=404, detail=f"Model {model_name} not found"
                )

            model = self.models[model_name]
            return model.get_model_metadata()

        @self.app.get("/v2/models/{model_name}/ready")
        async def model_ready(model_name: str):
            """Check if specific model is ready."""
            if model_name not in self.models:
                raise HTTPException(
                    status_code=404, detail=f"Model {model_name} not found"
                )

            model = self.models[model_name]
            if not model.ready:
                raise HTTPException(
                    status_code=503, detail=f"Model {model_name} not ready"
                )

            return {"ready": True, "name": model_name}

        @self.app.post("/v2/models/{model_name}/infer")
        async def infer(model_name: str, request: Request):
            """V2 inference endpoint."""
            if model_name not in self.models:
                raise HTTPException(
                    status_code=404, detail=f"Model {model_name} not found"
                )

            model = self.models[model_name]
            if not model.ready:
                raise HTTPException(
                    status_code=503, detail=f"Model {model_name} not ready"
                )

            try:
                # Get content type and handle different request formats
                content_type = request.headers.get(
                    "content-type", "application/json"
                ).lower()

                if content_type == "application/octet-stream":
                    # Handle direct binary upload
                    raw_bytes = await request.body()
                    # Create unified format with inputs wrapper
                    body = {
                        "inputs": {
                            "data": raw_bytes,
                        },
                        "inference_type": "byte_stream",  # Default for binary data
                    }
                    # Allow override via query parameter: ?inference_type=image_base64
                    if "inference_type" in request.query_params:
                        body["inference_type"] = request.query_params["inference_type"]

                elif content_type.startswith("application/json"):
                    # Handle JSON requests (existing behavior + new data field)
                    body = await request.json()

                else:
                    # Unsupported content type
                    raise HTTPException(
                        status_code=400,
                        detail=f"Unsupported content-type: {content_type}",
                    )

                # Add model name if not present
                if "model_name" not in body:
                    body["model_name"] = model_name

                # Get headers
                headers = dict(request.headers)

                # Run prediction in thread pool to avoid blocking
                result = await asyncio.to_thread(model.predict, body, headers)

                # Check if result indicates an error
                if isinstance(result, dict) and result.get("status") == 400:
                    error_detail = result.get("error", "Prediction failed")
                    raise HTTPException(status_code=400, detail=error_detail)

                return JSONResponse(content=result)

            except Exception as e:
                logger.error(f"Inference error: {str(e)}")
                raise HTTPException(status_code=400, detail=str(e))

    def add_model(self, model: ModelHubPredictor):
        """Add a model to the server."""
        self.models[model.name] = model
        logger.info(f"Added model: {model.name}")

    async def load_models(self):
        """Load all models asynchronously."""
        tasks = []
        for model in self.models.values():
            if not model.ready:
                tasks.append(asyncio.to_thread(model.load))

        if tasks:
            await asyncio.gather(*tasks)
            logger.info("All models loaded")

    def start(self, host: str = "0.0.0.0", port: int = 8080):
        """Start the server."""
        # Load models before starting
        asyncio.run(self.load_models())

        # Start server
        uvicorn.run(self.app, host=host, port=port, log_level="info")


def create_server_from_env() -> ModelServer:
    """
    Create a model server from environment variables.

    Environment variables:
    - MODEL_NAME: Name of the model
    - MODEL_URI: MLflow model URI (e.g., runs:/abc123/model)
    - MODEL_NAME_REGISTRY: Model name in registry
    - MODEL_VERSION: Model version in registry
    """
    from .base import AutoModelPredictor

    models = []

    # Check for single model configuration
    model_name = os.getenv("MODEL_NAME", "default-model")
    model_uri = os.getenv("MODEL_URI")
    model_name_registry = os.getenv("MODEL_NAME_REGISTRY")
    model_version = os.getenv("MODEL_VERSION")

    if model_uri or model_name_registry:
        model = AutoModelPredictor(
            name=model_name,
            model_uri=model_uri,
            model_name=model_name_registry,
            model_version=model_version,
        )
        models.append(model)

    # Check for multiple models (MODEL_NAME_1, MODEL_URI_1, etc.)
    i = 1
    while True:
        name = os.getenv(f"MODEL_NAME_{i}")
        uri = os.getenv(f"MODEL_URI_{i}")
        name_reg = os.getenv(f"MODEL_NAME_REGISTRY_{i}")
        version = os.getenv(f"MODEL_VERSION_{i}")

        if not (uri or name_reg):
            break

        if not name:
            name = f"model-{i}"

        model = AutoModelPredictor(
            name=name, model_uri=uri, model_name=name_reg, model_version=version
        )
        models.append(model)
        i += 1

    if not models:
        raise ValueError(
            "No models configured. Set MODEL_URI or MODEL_NAME_REGISTRY environment variables."
        )

    return ModelServer(models=models)


if __name__ == "__main__":
    # For standalone execution
    server = create_server_from_env()
    server.start()
