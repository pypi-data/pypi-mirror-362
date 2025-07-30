import re
from typing import Literal, Optional
from .base_llm import BaseLLM
from ..utils import (
    is_llama_cpp_available,
    is_sglang_available,
    is_mlx_lm_available,
    is_trtllm_available,
)
from ..logger import get_logger

logger = get_logger()


def initialize_llm(
    model_path: str,
    tensorrt_path: Optional[str] = None,
    backend: Literal[
        "vllm", "llama-cpp", "sglang", "torch", "mlx-lm", "tensorrt-llm"
    ] = "torch",
    max_length: int = 32768,
    device: Literal["cpu", "cuda", "auto"] | str = "auto",
    attn_implementation: Optional[Literal["sdpa", "flash_attention_2", "eager"]] = None,
    torch_dtype: Literal["float16", "bfloat16", "float32", "auto"] = "auto",
    gpu_memory_utilization: Optional[float] = 0.6,
    cache_implementation: Optional[str] = None,
    batch_size: int = 32,
    seed: int = 0,
    stop_tokens: Optional[list[str]] = None,
    stop_token_ids: Optional[list[int]] = None,
    **kwargs,
) -> BaseLLM:
    if backend == "vllm":
        # if not is_vllm_available():
        #     raise ImportError("vllm is not installed. Please install it with `pip install vllm`.")

        from .vllm_generator import VllmGenerator

        return VllmGenerator(
            model_path=model_path,
            max_length=max_length,
            device=device,
            max_num_seqs=batch_size,
            gpu_memory_utilization=gpu_memory_utilization,
            dtype=torch_dtype,
            seed=seed,
            stop_tokens=stop_tokens,
            stop_token_ids=stop_token_ids,
            **kwargs,
        )
    elif backend == "llama-cpp":
        if not is_llama_cpp_available():
            raise ImportError(
                "llama-cpp is not installed. Please install it with `pip install llama-cpp-python`."
            )

        from .llama_cpp_generator import LlamaCppGenerator

        return LlamaCppGenerator(
            model_path=model_path,
            max_length=max_length,
            device=device,
            stop_tokens=stop_tokens,
            stop_token_ids=stop_token_ids,
            **kwargs,
        )

    elif backend == "sglang":
        if not is_sglang_available():
            raise ImportError(
                "sglang is not installed. Please install it : https://docs.sglang.ai/start/install.html."
            )
        from .sglang_generator import SglangGenerator

        if re.match(r"cuda:\d+", device):
            logger.warning(
                "sglang目前不支持指定GPU ID，将默认使用第一个GPU。您可以通过设置环境变量CUDA_VISIBLE_DEVICES=0 来指定GPU。"
            )
            device = "cuda"
        return SglangGenerator(
            model_path=model_path,
            max_length=max_length,
            device=device,
            gpu_memory_utilization=gpu_memory_utilization,
            max_running_requests=batch_size,
            dtype=torch_dtype,
            random_seed=seed,
            stop_tokens=stop_tokens,
            stop_token_ids=stop_token_ids,
            **kwargs,
        )

    elif backend == "torch":
        from .torch_generator import TorchGenerator

        return TorchGenerator(
            model_path=model_path,
            max_length=max_length,
            device=device,
            attn_implementation=attn_implementation,
            torch_dtype=torch_dtype,
            cache_implementation=cache_implementation,
            stop_tokens=stop_tokens,
            stop_token_ids=stop_token_ids,
            **kwargs,
        )

    elif backend == "mlx-lm":
        if not is_mlx_lm_available():
            raise ImportError(
                "mlx-lm is not installed. Please install it with `pip install mlx-lm`."
            )
        from .mlx_lm_generator import MlxLmGenerator

        return MlxLmGenerator(
            model_path=model_path,
            max_length=max_length,
            stop_tokens=stop_tokens,
            stop_token_ids=stop_token_ids,
            **kwargs,
        )

    elif backend == "tensorrt-llm":
        if not is_trtllm_available():
            raise NotImplementedError(
                "tensorrt-llm is not installed. Please install it with `pip install tensorrt-llm --extra-index-url https://pypi.nvidia.com`."
            )
        from .trtllm_generator import TrtLLMGenerator

        return TrtLLMGenerator(
            model_path=model_path,
            tensorrt_path=tensorrt_path,
            max_length=max_length,
            device=device,
            stop_tokens=stop_tokens,
            stop_token_ids=stop_token_ids,
            batch_size=batch_size,
            **kwargs,
        )
    else:
        raise ValueError(f"Unknown backend: {backend}")
