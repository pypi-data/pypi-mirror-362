import logging
import torch
import torch.nn as nn
import os
import json
import sys
import pepe.utils
from pepe.embedders.base_embedder import BaseEmbedder
from transformers import AutoTokenizer

logger = logging.getLogger("src.embedders.custom_embedder")


class CustomEmbedder(BaseEmbedder):
    """
    CustomEmbedder for loading custom PyTorch models from .pt files.

    This embedder allows loading custom trained models saved as .pt files.
    It expects the model to have a specific structure and provides flexibility
    for different model architectures.
    """

    def __init__(self, args):
        super().__init__(args)

        # For custom models, we expect the model_name to be a path to a .pt file
        # or a directory containing model files
        model_path = args.model_name

        # Handle custom: prefix
        if model_path.startswith("custom:"):
            model_path = model_path[7:]  # Remove 'custom:' prefix

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Custom model path not found: {model_path}")

        # Store the actual model path
        self.model_path = model_path
        self.tokenizer_path = args.tokenizer_from

        # Load sequences from FASTA file
        self.sequences = pepe.utils.fasta_to_dict(args.fasta_path)
        self.num_sequences = len(self.sequences)

        # Initialize model and get model parameters
        (
            self.model,
            self.tokenizer,
            self.num_heads,
            self.num_layers,
            self.embedding_size,
        ) = self._initialize_model(self.model_path, self.tokenizer_path)

        # Set up tokenizer and validate tokens
        self.valid_tokens = self._get_valid_tokens()
        pepe.utils.check_input_tokens(
            self.valid_tokens, self.sequences, self.model_name
        )

        # Set up special tokens
        self.special_tokens = self._get_special_tokens()

        # Process layers
        self.layers = self._load_layers(self.layers)

        # Load and tokenize data
        self.data_loader, self.max_length = self._load_data(
            self.sequences, self.substring_dict
        )

        # Initialize output objects
        self._set_output_objects()

        logger.info(
            f"Custom embedder initialized with {self.num_layers} layers, "
            f"{self.num_heads} heads, embedding size {self.embedding_size}"
        )

    def _initialize_model(self, model_path, tokenizer_path=None):
        """Initialize the custom model from .pt file or directory."""
        logger.info(f"Loading custom model from: {model_path}")

        # Check if model_path is a directory or a file
        if os.path.isdir(model_path):
            # Directory: look for model files
            config_path = os.path.join(model_path, "config.json")
            model_file_path = os.path.join(model_path, "pytorch_model.pt")
            if not tokenizer_path:
                tokenizer_path = model_path

            # Alternative model file names
            if not os.path.exists(model_file_path):
                model_file_path = os.path.join(model_path, "model.pt")
            if not os.path.exists(model_file_path):
                model_file_path = os.path.join(model_path, "model.pth")

            if not os.path.exists(model_file_path):
                raise FileNotFoundError(
                    f"No model file found in {model_path}. "
                    f"Expected: pytorch_model.pt, model.pt, or model.pth"
                )
        else:
            # Single file: assume it's the model file
            model_file_path = model_path
            config_path = os.path.join(os.path.dirname(model_path), "config.json")
            if not tokenizer_path:
                tokenizer_path = os.path.dirname(model_path)

        # Load model
        model_data = torch.load(model_file_path, map_location="cpu")

        # Handle different model saving formats
        if isinstance(model_data, dict):
            if "model" in model_data:
                # Model saved with additional metadata
                model_state_dict = model_data["model"]
                config = model_data.get("config", {})
            elif "state_dict" in model_data:
                # Model saved with state_dict key
                model_state_dict = model_data["state_dict"]
                config = model_data.get("config", {})
            else:
                # Assume it's a state dict directly
                model_state_dict = model_data
                config = {}
        else:
            # Model saved directly
            model_state_dict = (
                model_data.state_dict() if hasattr(model_data, "state_dict") else None
            )
            config = {}

        # Load config if available
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                file_config = json.load(f)
                config.update(file_config)

        # Extract model parameters from config or infer from state_dict
        num_layers = config.get("num_layers", self._infer_num_layers(model_state_dict))
        num_heads = config.get(
            "num_attention_heads", self._infer_num_heads(model_state_dict)
        )
        embedding_size = config.get(
            "hidden_size", self._infer_embedding_size(model_state_dict)
        )

        # Initialize model architecture
        if isinstance(model_data, torch.nn.Module):
            model = model_data
        else:
            # Create a generic model wrapper
            model = CustomModelWrapper(model_state_dict, config)

        # Set model to evaluation mode
        model.eval()

        # Move model to appropriate device
        if torch.cuda.is_available() and self.device.type == "cuda":
            model = model.cuda()
            logger.info("Transferred custom model to GPU")
        else:
            logger.info("Running custom model on CPU")

        # Initialize tokenizer
        tokenizer = self._initialize_tokenizer(tokenizer_path, config)

        return model, tokenizer, num_heads, num_layers, embedding_size

    def _initialize_tokenizer(self, tokenizer_path, config):
        """Initialize tokenizer for custom model."""
        try:
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
            logger.info(f"Loaded tokenizer from {tokenizer_path}")
            return tokenizer
        except Exception as e:
            logger.warning(f"Could not load tokenizer from directory: {e}")

        # Use a default protein tokenizer if no custom tokenizer found
        logger.info("Using default protein tokenizer")
        return DefaultProteinTokenizer()

    def _infer_num_layers(self, state_dict):
        """Infer number of layers from state dict."""
        assert state_dict is not None, "State dict cannot be None for layer inference"

        layer_keys = [k for k in state_dict.keys() if "layer" in k.lower()]
        # Extract layer numbers and find the maximum
        layer_numbers = []
        for key in layer_keys:
            parts = key.split(".")
            for part in parts:
                if part.isdigit():
                    layer_numbers.append(int(part))
        return max(layer_numbers) + 1 if layer_numbers else 12

    def _infer_num_heads(self, state_dict):
        """Infer number of attention heads from state dict."""
        assert state_dict is not None, "State dict cannot be None for head inference"

        # Look for attention weight matrices
        attn_keys = [
            k
            for k in state_dict.keys()
            if "attention" in k.lower() and "weight" in k.lower()
        ]
        for key in attn_keys:
            tensor = state_dict[key]
            if len(tensor.shape) >= 2:
                # Assume the second dimension might be related to heads
                return tensor.shape[1] // 64 if tensor.shape[1] % 64 == 0 else 12

    def _infer_embedding_size(self, state_dict):
        """Infer embedding size from state dict."""
        assert (
            state_dict is not None
        ), "State dict cannot be None for embedding size inference"

        # Look for embedding layers
        emb_keys = [
            k
            for k in state_dict.keys()
            if "embed" in k.lower() and "weight" in k.lower()
        ]
        if emb_keys:
            # Get embedding dimension
            tensor = state_dict[emb_keys[0]]
            return tensor.shape[-1] if len(tensor.shape) >= 2 else 768

        # Look for output layers
        output_keys = [
            k
            for k in state_dict.keys()
            if "output" in k.lower() and "weight" in k.lower()
        ]
        if output_keys:
            tensor = state_dict[output_keys[0]]
            return tensor.shape[-1] if len(tensor.shape) >= 2 else 768

        return 768

    def _get_valid_tokens(self):
        """Get valid tokens for the tokenizer."""
        if hasattr(self.tokenizer, "get_vocab"):
            return set(self.tokenizer.get_vocab().keys())
        elif hasattr(self.tokenizer, "vocab"):
            return set(self.tokenizer.vocab.keys())
        else:
            # Return standard amino acid tokens
            return set(
                [
                    "A",
                    "R",
                    "N",
                    "D",
                    "C",
                    "Q",
                    "E",
                    "G",
                    "H",
                    "I",
                    "L",
                    "K",
                    "M",
                    "F",
                    "P",
                    "S",
                    "T",
                    "W",
                    "Y",
                    "V",
                ]
            )

    def _get_special_tokens(self):
        """Get special token IDs."""
        if hasattr(self.tokenizer, "all_special_ids"):
            return torch.tensor(
                self.tokenizer.all_special_ids, device=self.device, dtype=torch.int8
            )
        else:
            # Default special tokens (pad, cls, sep, unk)
            return torch.tensor([0, 1, 2, 3], device=self.device, dtype=torch.int8)

    def _load_layers(self, layers):
        """Process layer specification."""
        if not layers:
            layers = list(range(1, self.num_layers + 1))
            return layers

        # Validate layer indices
        assert all(
            -(self.num_layers + 1) <= i <= self.num_layers for i in layers
        ), f"Layer indices must be in range [{-(self.num_layers + 1)}, {self.num_layers}]"

        # Convert negative indices to positive
        layers = [(i + self.num_layers + 1) % (self.num_layers + 1) for i in layers]
        return layers

    def _load_data(self, sequences, substring_dict=None):
        """Load and tokenize sequences."""
        # Create dataset
        dataset = CustomDataset(
            sequences,
            substring_dict,
            self.context,
            self.tokenizer,
            self.max_length,
            add_special_tokens=not self.disable_special_tokens,
        )

        logger.info("Generating batches...")
        batch_sampler = pepe.utils.TokenBudgetBatchSampler(
            dataset=dataset, token_budget=self.batch_size
        )

        data_loader = torch.utils.data.DataLoader(
            dataset, batch_sampler=batch_sampler, collate_fn=dataset.safe_collate
        )

        max_length = dataset.get_max_encoded_length()
        logger.info("Data loaded and tokenized")

        return data_loader, max_length

    def _compute_outputs(
        self,
        model,
        toks,
        attention_mask,
        return_embeddings,
        return_contacts,
        return_logits,
    ):
        """Compute model outputs."""
        # Forward pass through the model
        outputs = model(
            input_ids=toks,
            attention_mask=attention_mask,
            output_hidden_states=return_embeddings,
            output_attentions=return_contacts,
            return_dict=True,
        )

        # Process logits
        logits = None
        if return_logits and hasattr(outputs, "logits"):
            logits = outputs.logits.to(
                dtype=self._precision_to_dtype(self.precision, "torch")  # type: ignore
            ).cpu()
            torch.cuda.empty_cache()

        # Process attention matrices
        attention_matrices = None
        if (
            return_contacts
            and hasattr(outputs, "attentions")
            and outputs.attentions is not None
        ):
            attention_matrices = (
                torch.stack(outputs.attentions)
                .to(self._precision_to_dtype(self.precision, "torch"))  # type: ignore
                .cpu()
            )
            torch.cuda.empty_cache()

        # Process representations
        representations = None
        if return_embeddings and hasattr(outputs, "hidden_states"):
            representations = {
                layer: outputs.hidden_states[layer - 1]
                .to(self._precision_to_dtype(self.precision, "torch"))  # type: ignore
                .cpu()
                for layer in self.layers
            }
            torch.cuda.empty_cache()

        return logits, representations, attention_matrices


class CustomModelWrapper(torch.nn.Module):
    """
    Generic wrapper for custom models loaded from state dict.
    """

    def __init__(self, state_dict, config):
        super().__init__()
        self.config = config
        self.state_dict_keys = list(state_dict.keys()) if state_dict else []

        # Get dimensions from config
        self.hidden_size = config.get("hidden_size", 768)
        self.num_layers = config.get("num_layers", 12)
        self.num_heads = config.get("num_attention_heads", 12)

        # Load state dict if provided
        if state_dict:
            self.load_state_dict(state_dict, strict=False)

    def forward(
        self,
        input_ids,
        attention_mask=None,
        output_hidden_states=True,
        output_attentions=False,
        return_dict=True,
    ):
        """
        Forward pass - this is a placeholder implementation.
        For actual custom models, this should be implemented based on the specific architecture.
        """
        # This is a basic implementation that returns dummy outputs
        # In practice, you would implement the actual forward pass of your model

        batch_size, seq_len = input_ids.shape

        # Use config values instead of hardcoded defaults
        hidden_size = self.hidden_size
        num_layers = self.num_layers
        num_heads = self.num_heads

        # Create dummy outputs for demonstration
        # In practice, these would be the actual model outputs
        dummy_hidden_states = []
        for _ in range(num_layers):
            dummy_hidden_states.append(
                torch.randn(batch_size, seq_len, hidden_size, device=input_ids.device)
            )

        dummy_attentions = []
        if output_attentions:
            for _ in range(num_layers):
                dummy_attentions.append(
                    torch.randn(
                        batch_size, num_heads, seq_len, seq_len, device=input_ids.device
                    )
                )

        # Create output object
        class ModelOutput:
            def __init__(self):
                self.hidden_states = (
                    dummy_hidden_states if output_hidden_states else None
                )
                self.attentions = dummy_attentions if output_attentions else None
                self.logits = torch.randn(
                    batch_size, seq_len, 21, device=input_ids.device
                )  # 21 for amino acids

        return ModelOutput()


class DefaultProteinTokenizer:
    """
    Default tokenizer for protein sequences.
    """

    def __init__(self):
        # Standard amino acid vocabulary
        self.vocab = {
            "<pad>": 0,
            "<cls>": 1,
            "<sep>": 2,
            "<unk>": 3,
            "A": 4,
            "R": 5,
            "N": 6,
            "D": 7,
            "C": 8,
            "Q": 9,
            "E": 10,
            "G": 11,
            "H": 12,
            "I": 13,
            "L": 14,
            "K": 15,
            "M": 16,
            "F": 17,
            "P": 18,
            "S": 19,
            "T": 20,
            "W": 21,
            "Y": 22,
            "V": 23,
        }
        self.id_to_token = {v: k for k, v in self.vocab.items()}
        self.pad_token_id = 0
        self.cls_token_id = 1
        self.sep_token_id = 2
        self.unk_token_id = 3
        self.all_special_ids = [0, 1, 2, 3]

    def get_vocab(self):
        return self.vocab

    def __call__(
        self,
        text,
        truncation=True,
        padding="max_length",
        max_length=512,
        add_special_tokens=True,
        return_tensors=None,
    ):
        """Tokenize protein sequence."""
        if isinstance(text, str):
            sequences = [text]
        else:
            sequences = text

        tokenized = []
        for seq in sequences:
            tokens = []
            if add_special_tokens:
                tokens.append(self.cls_token_id)

            for aa in seq:
                tokens.append(self.vocab.get(aa.upper(), self.unk_token_id))

            if add_special_tokens:
                tokens.append(self.sep_token_id)

            if truncation and len(tokens) > max_length:
                tokens = tokens[:max_length]

            # Create attention mask
            attention_mask = [1] * len(tokens)

            # Pad if necessary
            if padding == "max_length":
                while len(tokens) < max_length:
                    tokens.append(self.pad_token_id)
                    attention_mask.append(0)

            tokenized.append({"input_ids": tokens, "attention_mask": attention_mask})

        if return_tensors == "pt":
            return {
                "input_ids": torch.tensor([t["input_ids"] for t in tokenized]),
                "attention_mask": torch.tensor(
                    [t["attention_mask"] for t in tokenized]
                ),
            }

        return tokenized[0] if len(tokenized) == 1 else tokenized


class CustomDataset(pepe.utils.SequenceDictDataset):
    """
    Dataset class for custom embedder.
    """

    def __init__(
        self,
        sequences,
        substring_dict,
        context,
        tokenizer,
        max_length,
        add_special_tokens=True,
    ):
        super().__init__(sequences, substring_dict, context)
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.add_special_tokens = add_special_tokens
        self.pad_token_id = getattr(tokenizer, "pad_token_id", 0)

        # Encode sequences
        self.encoded_data = self._encode_sequences(
            self.data, tokenizer, max_length, add_special_tokens
        )

        # Handle substring sequences if provided
        if self.substring_dict:
            logger.info("Tokenizing substrings...")
            self.encoded_substring_data = self._encode_sequences(
                self.filtered_substring_data,
                tokenizer,
                "max_length",
                add_special_tokens=False,
            )
            self.substring_masks = self._get_substring_masks()

    def _encode_sequences(self, data, tokenizer, max_length, add_special_tokens):
        """Encode sequences using the tokenizer."""
        labels, strs = zip(*data)

        # Convert max_length to int if needed
        if max_length == "max_length":
            max_length = max(len(s) for s in strs) + (2 if add_special_tokens else 0)

        encoded_sequences = []
        for label, seq in zip(labels, strs):
            # Tokenize the sequence
            tokens = tokenizer(
                seq,
                truncation=True,
                padding="max_length",
                max_length=max_length,
                add_special_tokens=add_special_tokens,
                return_tensors="pt",
            )

            encoded_sequences.append(
                (
                    label,
                    seq,
                    tokens["input_ids"].squeeze(0),
                    tokens["attention_mask"].squeeze(0),
                )
            )

        return encoded_sequences

    def get_max_encoded_length(self):
        """Get maximum encoded sequence length."""
        return max(len(toks) for _, _, toks, _ in self.encoded_data)

    def safe_collate(self, batch):
        """Collate function for data loader."""
        if self.substring_dict:
            labels, seqs, toks, attn_masks, substring_masks = zip(*batch)
            return (
                list(labels),
                list(seqs),
                torch.stack(toks),
                torch.stack(attn_masks),
                torch.stack(substring_masks),
            )
        else:
            labels, seqs, toks, attn_masks = zip(*batch)
            return (
                list(labels),
                list(seqs),
                torch.stack(toks),
                torch.stack(attn_masks),
                None,
            )

    def __getitem__(self, idx):
        """Get item from dataset."""
        labels, seqs, toks, attn_mask = self.encoded_data[idx]
        if self.substring_dict:
            substring_masks = self.substring_masks[idx]
            return labels, seqs, toks, attn_mask, substring_masks
        else:
            return labels, seqs, toks, attn_mask
