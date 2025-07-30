"""
Model Interface for the Unified Fingerprinting Framework

This module provides a standard interface for working with models in the fingerprinting framework.
"""

import dataclasses
import hashlib
import importlib
import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

import torch
from huggingface_hub import login
from transformers import AutoTokenizer

from vail.utils import load_onnx_model, setup_logging
from vail.utils.env import load_env

# Track if we've already authenticated to avoid duplicate logins
_HF_ALREADY_AUTHENTICATED = False
logger = setup_logging(log_file_name="models.log")
load_env()


class Model:
    """
    Standard interface for models in the fingerprinting framework.

    This class wraps model loaders and provides a consistent interface for operations
    needed by the fingerprinting methods.
    """

    def __init__(self, name: str, model_info: Dict, **model_loader_kwargs):
        """
        Initialize a model wrapper.

        Args:
            name: Model name or identifier
            model_info: Comprehensive information about the model from the registry
            model_loader_kwargs: Additional keyword arguments to pass to the model loader

        Notes:
            The model_info dictionary can include quantization information in the model_info['quantization']
            field. For models where the quantization specified in the registry should be enforced during loading,
            you can include a 'loader_kwargs' key in the source_identifier JSON. For example:

            {
                "loader_class": "AutoModelForCausalLM",
                "checkpoint": "mistralai/Mistral-7B-v0.1",
                "loader_kwargs": {
                    "load_in_8bit": true
                }
            }

            These loader_kwargs will be passed to the model's from_pretrained method to ensure
            it's loaded with the desired quantization settings.
        """
        self.name = name
        self.model_info = model_info
        self.model_source_type = self._get_primary_source_type()
        self.model_loader_kwargs = model_loader_kwargs

        # Check if authentication is required for the primary source
        self.requires_auth = False
        sources = self.model_info.get("sources", [])
        if sources:
            self.requires_auth = sources[0].get("requires_auth", False)

        # Set loaders using internal methods
        self.model_loader = self._get_model_loader_func()
        self.tokenizer_loader = self._get_tokenizer_loader_func()

        # Will be populated when loaded
        self.loaded_model = None
        self.loaded_tokenizer = None
        self.embedding_dimension = None
        self.vocab_size = None

    def _authenticate_huggingface(self):
        """Authenticate with Hugging Face if not already authenticated."""
        global _HF_ALREADY_AUTHENTICATED

        # Check if we've already authenticated in this session
        if _HF_ALREADY_AUTHENTICATED:
            logger.info(
                f"Using existing Hugging Face authentication for model {self.name}"
            )
            return

        # Standard authentication logic
        token_path = os.path.expanduser("~/.huggingface")
        if os.path.exists(token_path):
            with open(token_path, "r") as f:
                token = f.read().strip()
            login(token=token)
            logger.info(
                f"Logged in to Hugging Face for model {self.name} using token from ~/.huggingface/token"
            )
        else:
            raw_token = os.getenv("HUGGINGFACE_TOKEN")
            if raw_token:
                login(token=raw_token)
                logger.info(f"Logged in to Hugging Face for model {self.name}")
            else:
                logger.warning(
                    "No Hugging Face token found. Please set the HUGGINGFACE_TOKEN environment variable."
                )

        _HF_ALREADY_AUTHENTICATED = True

    def _get_primary_source_type(self) -> str:
        """Get the primary source type from model info."""
        sources = self.model_info.get("sources", [])
        if sources:
            return sources[0].get("source_type", "unknown")
        return "unknown"

    def _get_primary_source_identifier(self) -> Dict:
        """Get the primary source identifier from model info."""
        sources = self.model_info.get("sources", [])
        if sources:
            return sources[0].get("source_identifier", {})
        return {}

    def _get_model_loader_func(self) -> Callable:
        """Get a function to load the model based on model info."""
        source_identifier = self._get_primary_source_identifier()
        if not source_identifier:
            raise ValueError(f"No source identifier found for model {self.name}")

        source_type = self.model_source_type

        if source_type == "huggingface_api":
            # Parse the JSON source identifier for huggingface_api
            # Example: {loader_class: T5ForConditionalGeneration, checkpoint: 'google/t5-v1_1-small'}
            if isinstance(source_identifier, str):
                # If it's a string, try to parse it as JSON
                try:
                    source_identifier = json.loads(source_identifier)
                except json.JSONDecodeError:
                    raise ValueError(
                        f"Invalid source_identifier format for huggingface_api: {source_identifier}"
                    )

            loader_class_name = source_identifier.get("loader_class")
            checkpoint = source_identifier.get("checkpoint")

            if not loader_class_name or not checkpoint:
                raise ValueError(
                    f"Missing loader_class or checkpoint in source_identifier: {source_identifier}"
                )

            # Import the specified loader class from transformer
            # Dynamically import the class from transformers
            transformers_module = importlib.import_module("transformers")
            if hasattr(transformers_module, loader_class_name):
                loader_class = getattr(transformers_module, loader_class_name)

            # Extract loader_kwargs if present in source_identifier
            loader_kwargs = source_identifier.get("loader_kwargs", {})

            # Return a function that loads the model
            def load_model(**kwargs):
                import os

                # Authenticate if required for this model before loading
                if self.requires_auth:
                    self._authenticate_huggingface()

                os.environ["TRANSFORMERS_ATTENTION_BACKEND"] = "torch"

                # Define and create offload directory
                offload_folder = os.path.abspath("./.hf_offload_cache")
                os.makedirs(offload_folder, exist_ok=True)
                logger.info(f"Using offload directory: {offload_folder}")

                # GPU-optimized parameters for model loading
                load_kwargs = {
                    "trust_remote_code": True,
                    "low_cpu_mem_usage": True,  # Minimize CPU memory during loading
                    "device_map": "auto",  # Let accelerate handle device mapping
                    "offload_folder": offload_folder,  # Specify offload directory
                    "attn_implementation": "eager",  # Use eager attention for broader compatibility
                }

                # Combine all kwargs
                load_kwargs.update(loader_kwargs)
                load_kwargs.update(kwargs)

                # Load model directly into memory
                return loader_class.from_pretrained(checkpoint, **load_kwargs)

            return load_model

        elif source_type in ["onnx_file"]:
            # Return a function that prioritizes file_path from kwargs, then falls back to path in source_identifier
            return lambda **kwargs: load_onnx_model(kwargs.get("file_path"))

        elif source_type in ["gguf_file", "llama.cpp"]:
            # TODO: Implement proper GGUF model loading
            pass

        else:
            raise ValueError(f"Unsupported model source type: {source_type}")

    def _get_tokenizer_loader_func(self) -> Optional[Callable]:
        """Get a function to load the tokenizer based on model info."""
        source_identifier = self._get_primary_source_identifier()
        if not source_identifier:
            raise ValueError(f"No source identifier found for model {self.name}")

        source_type = self.model_source_type

        if source_type in ["huggingface_api"]:
            if isinstance(source_identifier, str):
                # If it's a string, try to parse it as JSON
                try:
                    source_identifier = json.loads(source_identifier)
                    checkpoint = source_identifier.get("checkpoint", "")
                except json.JSONDecodeError:
                    raise ValueError(
                        f"Invalid source_identifier format for huggingface_api: {source_identifier}"
                    )
            else:
                checkpoint = source_identifier.get("checkpoint", "")

            # Return a function that loads the tokenizer
            def load_tokenizer():
                import os

                os.environ["TRANSFORMERS_ATTENTION_BACKEND"] = "torch"

                # Just use modern parameters for recent transformers
                return AutoTokenizer.from_pretrained(
                    checkpoint,
                    trust_remote_code=True,
                    use_fast=True,
                )

            return load_tokenizer
        else:
            return None

    def load(self):
        """Load the model if not already loaded."""
        import time

        if self.loaded_model is None:
            start_time = time.time()
            logger.info(f"Loading model {self.name} (using cache if available)...")
            # The model_loader function already merges source_identifier's loader_kwargs with any additional kwargs
            self.loaded_model = self.model_loader(**self.model_loader_kwargs)
            self.loaded_model.eval()  # Ensure model is in evaluation mode
            load_time = time.time() - start_time
            # Print informative message about loading time
            logger.info(f"Model {self.name} loaded in {load_time:.2f} seconds")
        return self.loaded_model

    def load_tokenizer(self):
        """Load the tokenizer if available and not already loaded."""
        if self.loaded_tokenizer is None and self.tokenizer_loader is not None:
            logger.info(
                f"Loading tokenizer for {self.name} (using cache if available)..."
            )
            self.loaded_tokenizer = self.tokenizer_loader()
            logger.info(f"Tokenizer for {self.name} loaded")
        return self.loaded_tokenizer

    def get_input_embeddings(self):
        """Get the input embedding layer of the model."""
        if self.loaded_model is None:
            self.load()

        if hasattr(self.loaded_model, "get_input_embeddings"):
            return self.loaded_model.get_input_embeddings()
        elif hasattr(self.loaded_model, "embeddings"):
            return self.loaded_model.embeddings
        elif hasattr(self.loaded_model, "model") and hasattr(
            self.loaded_model.model, "get_input_embeddings"
        ):
            return self.loaded_model.model.get_input_embeddings()
        else:
            raise AttributeError(
                f"Could not find input embeddings for model {self.name}"
            )

    def get_embedding_dimension(self):
        """Get the dimension of the model's embeddings."""
        if self.embedding_dimension is None:
            if self.model_source_type == "gguf":
                model = self.load()
                self.embedding_dimension = model.n_embd()
            else:
                embedding_layer = self.get_input_embeddings()
                if hasattr(embedding_layer, "weight"):
                    self.embedding_dimension = embedding_layer.weight.shape[1]
                elif hasattr(embedding_layer, "embedding_dim"):
                    self.embedding_dimension = embedding_layer.embedding_dim
                else:
                    raise AttributeError(
                        f"Could not determine embedding dimension for model {self.name}"
                    )

        return self.embedding_dimension

    def get_vocab_size(self):
        """Get the vocabulary size of the model."""
        if self.vocab_size is None:
            loaded_model = self.load()
            if hasattr(loaded_model, "config") and hasattr(
                loaded_model.config, "vocab_size"
            ):
                self.vocab_size = loaded_model.config.vocab_size
            elif self.model_source_type == "gguf":
                # TODO: Implement GGUF vocabulary size retrieval
                pass
            else:
                embedding_layer = self.get_input_embeddings()
                if hasattr(embedding_layer, "weight"):
                    self.vocab_size = embedding_layer.weight.shape[0]
                elif hasattr(embedding_layer, "num_embeddings"):
                    self.vocab_size = embedding_layer.num_embeddings
                elif hasattr(embedding_layer, "vocab_size"):
                    self.vocab_size = embedding_layer.vocab_size
                else:
                    raise AttributeError(
                        f"Could not determine vocabulary size for model {self.name}"
                    )

        return self.vocab_size

    def get_device(self):
        """Get the device the model is on."""
        if self.loaded_model is None:
            self.load()

        if hasattr(self.loaded_model, "device"):
            return self.loaded_model.device
        elif hasattr(self.loaded_model, "get_device"):
            return self.loaded_model.get_device()
        elif hasattr(self.loaded_model, "parameters"):
            # Get device from first parameter
            try:
                return next(self.loaded_model.parameters()).device
            except StopIteration:
                return torch.device("cpu")
        else:
            return torch.device("cpu")

    def run_inference(self, input_ids):
        """Run inference with the model on the given input IDs."""
        if self.loaded_model is None:
            self.load()

        # Different models might have different inference methods
        if hasattr(self.loaded_model, "run_inference"):
            return self.loaded_model.run_inference(input_ids)
        else:
            try:
                with torch.no_grad():
                    # Special handling for encoder-decoder models like T5
                    model_type = self.loaded_model.__class__.__name__
                    if (
                        "T5" in model_type
                        or hasattr(self.loaded_model, "encoder")
                        and hasattr(self.loaded_model, "decoder")
                    ):
                        # For encoder-decoder models, we need to provide decoder_input_ids
                        # Use the first token ID as the decoder start token
                        decoder_input_ids = torch.tensor([[0]]).to(
                            input_ids.device
                        )  # Usually 0 is the decoder start token

                        # Try with decoder_input_ids
                        return self.loaded_model(
                            input_ids=input_ids, decoder_input_ids=decoder_input_ids
                        )
                    else:
                        # Standard forward pass for other models
                        return self.loaded_model(input_ids)
            except Exception as e:
                raise RuntimeError(
                    f"Error running inference with model {self.name}: {e}"
                )

    def get_hash(self) -> str:
        """
        Get a hash that uniquely identifies this model and its configuration.

        Returns:
            Hash string
        """
        # Create a dictionary of all the components that make up the model's identity
        model_dict = {
            "name": self.name,
            "model_source_type": self.model_source_type,
            "model_loader": self.model_loader.__name__
            if hasattr(self.model_loader, "__name__")
            else str(self.model_loader),
            "tokenizer_loader": self.tokenizer_loader.__name__
            if self.tokenizer_loader and hasattr(self.tokenizer_loader, "__name__")
            else str(self.tokenizer_loader),
            "model_loader_kwargs": json.dumps(self.model_loader_kwargs, sort_keys=True),
        }

        # Convert to string and hash
        model_str = json.dumps(model_dict, sort_keys=True)
        return hashlib.md5(model_str.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict:
        """
        Convert the Model object to a dictionary that can be serialized.

        Returns:
            Dictionary representation of the Model object
        """
        # Create a dictionary with the model's basic information
        model_dict = {
            "id": self.model_info.get("id", ""),
            "canonical_id": self.model_info.get("canonical_id"),
            "model_maker": self.model_info.get("model_maker", ""),
            "model_name": self.model_info.get("model_name", ""),
            "params_count": self.model_info.get("params_count", None),
            "context_length": self.model_info.get("context_length", None),
            "quantization": self.model_info.get("quantization", ""),
            "license": self.model_info.get("license", ""),
            "created_at": self.model_info.get("created_at", datetime.now()),
            "last_updated": self.model_info.get("last_updated"),
            "sources": [],
        }

        # Add sources
        for source in self.model_info.get("sources", []):
            source_dict = {
                "source_id": source.get("source_id", ""),
                "source_type": source.get("source_type", ""),
                "source_identifier": source.get("source_identifier", {}),
                "requires_auth": source.get("requires_auth", False),
                "created_at": source.get("created_at", datetime.now()),
            }
            model_dict["sources"].append(source_dict)

        return model_dict

    def get_canonical_id(self) -> Optional[str]:
        """
        Get the canonical ID for this model.

        Returns:
            The canonical ID if available, None otherwise
        """
        return self.model_info.get("canonical_id")

    @classmethod
    def from_dict(cls, model_dict: Dict, **kwargs) -> "Model":
        """
        Create a Model object from a dictionary.

        Args:
            model_dict: Dictionary representation of a Model object
            **kwargs: Additional keyword arguments to pass to the Model constructor

        Returns:
            Model object
        """
        name = model_dict.get("model_name", "")
        model_info = {
            "id": model_dict.get("id", ""),
            "canonical_id": model_dict.get("canonical_id"),
            "model_maker": model_dict.get("model_maker", ""),
            "model_name": name,
            "params_count": model_dict.get("params_count", None),
            "context_length": model_dict.get("context_length", None),
            "quantization": model_dict.get("quantization", ""),
            "created_at": model_dict.get("created_at", datetime.now()),
            "last_updated": model_dict.get("last_updated"),
            "sources": model_dict.get("sources", []),
        }

        return cls(name=name, model_info=model_info, **kwargs)

    @classmethod
    def validate_source(cls, source_info: Dict) -> bool:
        """
        Validate that the source info is present and valid.

        Args:
            source_info: Dictionary containing source information with:
                - source_type: Type of source (huggingface_api, onnx, gguf)
                - source_identifier: Source-specific information
                - requires_auth: Whether authentication is required (optional)

        Returns:
            bool: True if the model can be loaded, False otherwise
        """
        try:
            # Create a temporary model instance to validate the source
            temp_model = cls(
                name="validation_model",
                model_info={
                    "model_name": "validation_model",
                    "sources": [
                        {
                            "source_type": source_info["source_type"],
                            "source_identifier": source_info["source_identifier"],
                            "requires_auth": source_info.get("requires_auth", False),
                        }
                    ],
                },
            )

            # Check that source type and identifier are valid
            source_type = temp_model._get_primary_source_type()
            source_identifier = temp_model._get_primary_source_identifier()

            if source_type == "unknown" or not source_identifier:
                return False

            return True
        except Exception:
            return False


@dataclass
class ModelFilterCriteria:
    """Data class for specifying model filter criteria."""

    maker: Optional[str] = None
    quantization: Optional[str] = None
    license: Optional[str] = None
    updated_since: Optional[datetime] = None
    # context_length: Optional[int] = None # Example: if you add this, update methods too

    # New fields for params_count comparisons
    params_count_eq: Optional[int] = None  # For exact match (replaces old params_count)
    params_count_gt: Optional[int] = None  # Greater than
    params_count_lt: Optional[int] = None  # Less than
    params_count_gte: Optional[int] = None  # Greater than or equal to
    params_count_lte: Optional[int] = None  # Less than or equal to

    # Backwards compatibility for params_count, will be mapped to params_count_eq
    # This is a property to handle a direct assignment to `params_count` if old code uses it.
    @property
    def params_count(self) -> Optional[int]:
        return self.params_count_eq

    @params_count.setter
    def params_count(self, value: Optional[int]):
        self.params_count_eq = value

    def to_dict(self) -> Dict[str, Any]:
        """Converts the filter criteria to a dictionary, excluding None values."""
        return {
            f.name: getattr(self, f.name)
            for f in dataclasses.fields(self)
            if getattr(self, f.name) is not None
        }

    def is_empty(self) -> bool:
        """Checks if any filter criteria are set."""
        return all(getattr(self, f.name) is None for f in dataclasses.fields(self))

    def to_sql_filters(
        self, table_alias: Optional[str] = None, placeholder_style: str = "?"
    ) -> Tuple[str, List[Any]]:
        """
        Converts filter criteria into SQL WHERE clause conditions and parameters.

        Args:
            table_alias: Optional alias for the table (e.g., 'm').
            placeholder_style: The placeholder style to use ('?' or '%s').

        Returns:
            Tuple containing:
            - SQL WHERE clause string with placeholders
            - List of parameter values to bind
        """
        conditions = []
        params = []

        prefix = f"{table_alias}." if table_alias else ""

        if self.maker:
            conditions.append(f"{prefix}model_maker = {placeholder_style}")
            params.append(self.maker)

        # Updated params_count filtering logic
        if self.params_count_eq is not None:
            conditions.append(f"{prefix}params_count = {placeholder_style}")
            params.append(self.params_count_eq)
        if self.params_count_gt is not None:
            conditions.append(f"{prefix}params_count > {placeholder_style}")
            params.append(self.params_count_gt)
        if self.params_count_lt is not None:
            conditions.append(f"{prefix}params_count < {placeholder_style}")
            params.append(self.params_count_lt)
        if self.params_count_gte is not None:
            conditions.append(f"{prefix}params_count >= {placeholder_style}")
            params.append(self.params_count_gte)
        if self.params_count_lte is not None:
            conditions.append(f"{prefix}params_count <= {placeholder_style}")
            params.append(self.params_count_lte)

        if self.quantization:
            conditions.append(f"{prefix}quantization = {placeholder_style}")
            params.append(self.quantization)

        if self.updated_since:
            conditions.append(f"{prefix}last_updated >= {placeholder_style}")
            params.append(self.updated_since)

        where_clause = " AND ".join(conditions) if conditions else "1=1"
        return where_clause, params

    def to_filter_string(self) -> str:
        """
        Generates a human-readable string of active filter criteria for logging.

        Returns:
            A string representing the active filters, or 'No filters applied'.
        """
        active_filters = []
        if self.maker:
            active_filters.append(f"maker='{self.maker}'")

        # Updated params_count string generation
        if self.params_count_eq is not None:
            active_filters.append(f"params_count={self.params_count_eq}")
        if self.params_count_gt is not None:
            active_filters.append(f"params_count>{self.params_count_gt}")
        if self.params_count_lt is not None:
            active_filters.append(f"params_count<{self.params_count_lt}")
        if self.params_count_gte is not None:
            active_filters.append(f"params_count>={self.params_count_gte}")
        if self.params_count_lte is not None:
            active_filters.append(f"params_count<={self.params_count_lte}")

        if self.quantization:
            active_filters.append(f"quantization='{self.quantization}'")
        if self.license:
            active_filters.append(f"license='{self.license}'")

        if self.updated_since:
            active_filters.append(
                f"updated_since>={self.updated_since.strftime('%Y-%m-%d %H:%M:%S')}"
            )

        if not active_filters:
            return "No filters applied"
        return ", ".join(active_filters)


# ============= Canonical Model ID Functions =============


def generate_canonical_id(model_name: str, global_registry_id: int) -> str:
    """
    Generate a canonical ID combining model name and global registry ID.

    Args:
        model_name: The model name (e.g., "bigcode/starcoderbase-1b")
        global_registry_id: The global registry ID (e.g., 161)

    Returns:
        Canonical ID in format "{model_name}_{global_registry_id}"

    Examples:
        >>> generate_canonical_id("bigcode/starcoderbase-1b", 161)
        "bigcode/starcoderbase-1b_161"
        >>> generate_canonical_id("microsoft/phi-3-mini", 42)
        "microsoft/phi-3-mini_42"
    """
    # Validate and clean model_name
    if not model_name or not str(model_name).strip():
        raise ValueError("model_name must be non-empty string")

    # Convert global_registry_id to int if possible
    try:
        global_id = int(global_registry_id)
    except (ValueError, TypeError):
        raise ValueError(
            f"global_registry_id must be convertible to integer, got: {global_registry_id!r}"
        )

    # Ensure the model name is clean for use as an identifier
    clean_model_name = str(model_name).strip()

    return f"{clean_model_name}_{global_id}"


def parse_canonical_id(canonical_id: str) -> tuple[str, int]:
    """
    Parse a canonical ID back into model name and global registry ID.

    Args:
        canonical_id: Canonical ID in format "{model_name}_{global_registry_id}"

    Returns:
        Tuple of (model_name, global_registry_id)

    Examples:
        >>> parse_canonical_id("bigcode/starcoderbase-1b_161")
        ("bigcode/starcoderbase-1b", 161)
        >>> parse_canonical_id("microsoft/phi-3-mini_42")
        ("microsoft/phi-3-mini", 42)
    """
    if not canonical_id or "_" not in canonical_id:
        raise ValueError(
            "Invalid canonical_id format. Expected: {model_name}_{global_registry_id}"
        )

    # Split on the last underscore to handle model names that might contain underscores
    parts = canonical_id.rsplit("_", 1)
    if len(parts) != 2:
        raise ValueError(
            "Invalid canonical_id format. Expected: {model_name}_{global_registry_id}"
        )

    model_name, global_id_str = parts

    try:
        global_registry_id = int(global_id_str)
    except ValueError:
        raise ValueError(f"Invalid global_registry_id in canonical_id: {global_id_str}")

    return model_name, global_registry_id
