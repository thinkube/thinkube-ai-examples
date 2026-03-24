#!/usr/bin/env python3
"""
Convert openai/gpt-oss-20b from MXFP4 format to a trainable BF16 format.

This script leverages HuggingFace transformers' built-in Mxfp4Config(dequantize=True)
to automatically dequantize MXFP4 weights to BF16.

The output model can be used with:
- Unsloth + BitsAndBytes for QLoRA fine-tuning
- Any standard HuggingFace training pipeline

Usage:
    python convert_gptoss_to_trainable.py --input /path/to/mlflow/model --output /path/to/output

Example:
    python convert_gptoss_to_trainable.py \
        --input /home/thinkube/mlflow/artifacts/1/5f7e5b0abf8e4c1db0e7f8e6c0f2a1b3/artifacts/model/data/model \
        --output /home/thinkube/models/gpt-oss-20b-bf16
"""

import argparse
import gc
import os
import sys
from pathlib import Path

import torch


def convert_model(input_path: str, output_path: str, dtype: str = "bfloat16"):
    """
    Convert MXFP4 GPT-OSS model to dequantized BF16 format.

    Args:
        input_path: Path to the MXFP4 model (local path or HF repo)
        output_path: Path to save the converted model
        dtype: Output dtype (bfloat16, float16, or float32)
    """
    from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig
    from transformers.utils.quantization_config import Mxfp4Config

    dtype_map = {
        "bfloat16": torch.bfloat16,
        "float16": torch.float16,
        "float32": torch.float32,
    }
    torch_dtype = dtype_map[dtype]

    print(f"=" * 60)
    print(f"GPT-OSS MXFP4 to BF16 Converter")
    print(f"=" * 60)
    print(f"Input path:  {input_path}")
    print(f"Output path: {output_path}")
    print(f"Output dtype: {dtype}")
    print(f"=" * 60)

    # Check input path exists
    if not os.path.exists(input_path):
        print(f"ERROR: Input path does not exist: {input_path}")
        sys.exit(1)

    # Load config first to verify it's an MXFP4 model
    print("\n[1/5] Loading model config...")
    config = AutoConfig.from_pretrained(input_path, trust_remote_code=True)

    if hasattr(config, 'quantization_config'):
        quant_config = config.quantization_config
        print(f"  Quantization method: {quant_config.get('quant_method', 'unknown')}")
    else:
        print("  Warning: No quantization_config found. Model may already be dequantized.")

    print(f"  Model type: {config.model_type}")
    print(f"  Hidden size: {config.hidden_size}")
    print(f"  Num layers: {config.num_hidden_layers}")
    if hasattr(config, 'num_local_experts'):
        print(f"  Num experts: {config.num_local_experts}")

    # Create Mxfp4Config with dequantize=True
    print("\n[2/5] Configuring dequantization...")
    dequant_config = Mxfp4Config(dequantize=True)
    print(f"  Using Mxfp4Config(dequantize=True)")

    # Load model with dequantization
    print("\n[3/5] Loading and dequantizing model (this may take a while)...")
    print("  Loading model to CPU with automatic dequantization...")

    model = AutoModelForCausalLM.from_pretrained(
        input_path,
        quantization_config=dequant_config,
        torch_dtype=torch_dtype,
        device_map="cpu",  # Load to CPU to save GPU memory
        trust_remote_code=True,
        low_cpu_mem_usage=True,
    )

    # Verify model is dequantized
    print("\n  Verifying model structure...")
    param_count = sum(p.numel() for p in model.parameters())
    trainable_count = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"  Total parameters: {param_count:,}")
    print(f"  Trainable parameters: {trainable_count:,}")

    # Check dtypes
    dtypes = set()
    for name, param in model.named_parameters():
        dtypes.add(str(param.dtype))
    print(f"  Parameter dtypes: {', '.join(dtypes)}")

    # Load tokenizer
    print("\n[4/5] Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(input_path, trust_remote_code=True)
    print(f"  Tokenizer type: {type(tokenizer).__name__}")
    print(f"  Vocab size: {len(tokenizer)}")

    # Save the converted model
    print(f"\n[5/5] Saving converted model to {output_path}...")
    os.makedirs(output_path, exist_ok=True)

    # Save model
    model.save_pretrained(
        output_path,
        safe_serialization=True,  # Use safetensors format
        max_shard_size="5GB",     # Split into manageable chunks
    )

    # Save tokenizer
    tokenizer.save_pretrained(output_path)

    # Clean up quantization config from saved config
    config_path = Path(output_path) / "config.json"
    if config_path.exists():
        import json
        with open(config_path) as f:
            config_dict = json.load(f)

        # Remove quantization config since model is now dequantized
        if "quantization_config" in config_dict:
            del config_dict["quantization_config"]
            with open(config_path, "w") as f:
                json.dump(config_dict, f, indent=2)
            print("  Removed quantization_config from saved config")

    # Free memory
    del model
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    print("\n" + "=" * 60)
    print("CONVERSION COMPLETE!")
    print("=" * 60)
    print(f"Model saved to: {output_path}")
    print(f"\nTo use with Unsloth:")
    print(f"  model, tokenizer = FastLanguageModel.from_pretrained(")
    print(f"      model_name='{output_path}',")
    print(f"      load_in_4bit=True,  # Now works with BitsAndBytes!")
    print(f"      dtype=None,")
    print(f"      max_seq_length=2048,")
    print(f"  )")
    print("=" * 60)

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Convert GPT-OSS from MXFP4 to trainable BF16 format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert from local MLflow path
  python convert_gptoss_to_trainable.py \\
      --input /home/thinkube/mlflow/artifacts/.../model/data/model \\
      --output /home/thinkube/models/gpt-oss-20b-bf16

  # Convert with float16 instead of bfloat16
  python convert_gptoss_to_trainable.py \\
      --input /path/to/model \\
      --output /path/to/output \\
      --dtype float16
        """
    )
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to input MXFP4 model"
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Path to save converted BF16 model"
    )
    parser.add_argument(
        "--dtype",
        type=str,
        default="bfloat16",
        choices=["bfloat16", "float16", "float32"],
        help="Output dtype (default: bfloat16)"
    )

    args = parser.parse_args()

    convert_model(
        input_path=args.input,
        output_path=args.output,
        dtype=args.dtype
    )


if __name__ == "__main__":
    main()
