import asyncio
import platform
import random
from typing import Literal, Optional, Callable, AsyncIterator
from functools import partial
from abc import ABC, abstractmethod

import soundfile as sf
import torch
import numpy as np
from osc_data.text import TextNormalizer as ZhNormalizer

from ..llm import initialize_llm
from .utils import (
    split_text,
    parse_multi_speaker_text,
    limit_concurrency,
    contains_chinese,
    timer,
)
from ..logger import get_logger


logger = get_logger()


class Engine(ABC):
    _SUPPORT_CLONE = False
    _SUPPORT_SPEAK = False

    @abstractmethod
    def list_speakers(self) -> list[str]: ...

    @abstractmethod
    async def add_speaker(
        self, name: str, audio, reference_text: Optional[str] = None
    ): ...

    @abstractmethod
    async def delete_speaker(self, name: str): ...

    @abstractmethod
    async def get_speaker(self, name: str): ...

    @abstractmethod
    def save_speakers(self, save_path: str): ...

    @abstractmethod
    async def load_speakers(self, load_path: str): ...

    @abstractmethod
    async def speak_async(
        self,
        text: str,
        name: Optional[str] = None,
        pitch: Optional[
            Literal["very_low", "low", "moderate", "high", "very_high"]
        ] = None,
        speed: Optional[
            Literal["very_low", "low", "moderate", "high", "very_high"]
        ] = None,
        temperature: float = 0.9,
        top_k: int = 50,
        top_p: float = 0.95,
        repetition_penalty: float = 1.0,
        max_tokens: int = 4096,
        length_threshold: int = 50,
        window_size: int = 50,
        split_fn: Optional[Callable[[str], list[str]]] = None,
        **kwargs,
    ) -> np.ndarray: ...

    @abstractmethod
    async def speak_stream_async(
        self,
        text: str,
        name: Optional[str] = None,
        pitch: Optional[
            Literal["very_low", "low", "moderate", "high", "very_high"]
        ] = None,
        speed: Optional[
            Literal["very_low", "low", "moderate", "high", "very_high"]
        ] = None,
        temperature: float = 0.9,
        top_k: int = 50,
        top_p: float = 0.95,
        repetition_penalty: float = 1.0,
        max_tokens: int = 4096,
        length_threshold: int = 50,
        window_size: int = 50,
        split_fn: Optional[Callable[[str], list[str]]] = None,
        **kwargs,
    ) -> AsyncIterator[np.ndarray]:
        yield  # type: ignore

    @abstractmethod
    async def clone_voice_async(
        self,
        text: str,
        reference_audio,
        reference_text: Optional[str] = None,
        pitch: Optional[
            Literal["very_low", "low", "moderate", "high", "very_high"]
        ] = None,
        speed: Optional[
            Literal["very_low", "low", "moderate", "high", "very_high"]
        ] = None,
        temperature: float = 0.9,
        top_k: int = 50,
        top_p: float = 0.95,
        repetition_penalty: float = 1.0,
        max_tokens: int = 4096,
        length_threshold: int = 50,
        window_size: int = 50,
        split_fn: Optional[Callable[[str], list[str]]] = None,
        **kwargs,
    ) -> np.ndarray: ...

    @abstractmethod
    async def clone_voice_stream_async(
        self,
        text: str,
        reference_audio,
        reference_text: Optional[str] = None,
        pitch: Optional[
            Literal["very_low", "low", "moderate", "high", "very_high"]
        ] = None,
        speed: Optional[
            Literal["very_low", "low", "moderate", "high", "very_high"]
        ] = None,
        temperature: float = 0.9,
        top_k: int = 50,
        top_p: float = 0.95,
        repetition_penalty: float = 1.0,
        max_tokens: int = 4096,
        length_threshold: int = 50,
        window_size: int = 50,
        split_fn: Optional[Callable[[str], list[str]]] = None,
        **kwargs,
    ) -> AsyncIterator[np.ndarray]:
        yield  # type: ignore

    @abstractmethod
    async def multi_speak_async(
        self,
        text: str,
        temperature: float = 0.9,
        top_k: int = 50,
        top_p: float = 0.95,
        repetition_penalty: float = 1.0,
        max_tokens: int = 4096,
        length_threshold: int = 50,
        window_size: int = 50,
        split_fn: Optional[Callable[[str], list[str]]] = None,
        **kwargs,
    ) -> np.ndarray: ...

    @abstractmethod
    async def multi_speak_stream_async(
        self,
        text: str,
        temperature: float = 0.9,
        top_k: int = 50,
        top_p: float = 0.95,
        repetition_penalty: float = 1.0,
        max_tokens: int = 4096,
        length_threshold: int = 50,
        window_size: int = 50,
        split_fn: Optional[Callable[[str], list[str]]] = None,
        **kwargs,
    ) -> AsyncIterator[np.ndarray]:
        yield  # type: ignore


class BaseEngine(Engine):
    SAMPLE_RATE = 16000

    def __init__(
        self,
        llm_model_path: str,
        max_length: int = 32768,
        llm_device: Literal["cpu", "cuda", "mps", "auto"] | str = "auto",
        llm_tensorrt_path: Optional[str] = None,
        backend: Literal[
            "vllm", "llama-cpp", "sglang", "torch", "mlx-lm", "tensorrt-llm"
        ] = "torch",
        llm_attn_implementation: Optional[
            Literal["sdpa", "flash_attention_2", "eager"]
        ] = None,
        torch_dtype: Literal["float16", "bfloat16", "float32", "auto"] = "auto",
        llm_gpu_memory_utilization: Optional[float] = 0.6,
        cache_implementation: Optional[str] = None,
        llm_batch_size: int = 8,
        seed: int = 0,
        stop_tokens: Optional[list[str]] = None,
        stop_token_ids: Optional[list[int]] = None,
        **kwargs,
    ):
        self.generator = initialize_llm(
            model_path=llm_model_path,
            tensorrt_path=llm_tensorrt_path,
            backend=backend,
            max_length=max_length,
            device=self._auto_detect_device(llm_device),
            attn_implementation=llm_attn_implementation,
            torch_dtype=torch_dtype,
            gpu_memory_utilization=llm_gpu_memory_utilization,
            cache_implementation=cache_implementation,
            batch_size=llm_batch_size,
            seed=seed,
            stop_tokens=stop_tokens,
            stop_token_ids=stop_token_ids,
            **kwargs,
        )
        self._batch_size = llm_batch_size
        self.zh_normalizer = ZhNormalizer(
            overwrite_cache=False, remove_erhua=False, remove_interjections=False
        )
        # self.en_normalizer = EnNormalizer(overwrite_cache=False)
        self.speakers = {}
        self._lock = asyncio.Lock()

    def list_speakers(self) -> list[str]:
        names = []
        for name in self.speakers:
            if name not in names:
                names.append(name)
        return names

    async def _add_speaker(
        self, name: str, audio, reference_text: Optional[str] = None
    ):
        raise NotImplementedError(
            f"_add_speaker not implemented for {self.__class__.__name__}"
        )

    async def add_speaker(self, name: str, audio, reference_text: Optional[str] = None):
        async with self._lock:
            if name in self.speakers:
                logger.warning(
                    f"The audio role '{name}' already exists and will be overwritten."
                )
            await self._add_speaker(name, audio, reference_text=reference_text)

    async def delete_speaker(self, name: str):
        async with self._lock:
            if name not in self.speakers:
                logger.warning(f"The role '{name}' does not exist.")
            del self.speakers[name]

    async def get_speaker(self, name: str):
        async with self._lock:
            if name not in self.speakers:
                logger.warning(f"The audio role '{name}' does not exist.")
                return None
            data = self.speakers[name]
        return data

    def save_speakers(self, save_path: str):
        save_data = {
            "class": self.__class__.__name__,
            "speakers": self.speakers,
        }
        torch.save(save_data, save_path)

    async def load_speakers(self, load_path: str):
        speakers = torch.load(load_path, map_location="cpu")
        speaker_class = speakers.get("class", None)
        if speaker_class is None or speaker_class != self.__class__.__name__:
            logger.warning(
                f"The given speaker file does not belong to the current engine and will not be loaded. "
                f"File's engine: {speaker_class}, current engine: {self.__class__.__name__}"
            )
        async with self._lock:
            self.speakers.update(speakers.get("speakers", {}))

    def shutdown(self):
        self.generator.shutdown()

    def __del__(self):
        self.shutdown()

    @classmethod
    def set_seed(cls, seed: int):
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

    @classmethod
    def _auto_detect_device(cls, device: str):
        if device in ["cpu", "cuda", "mps"] or device.startswith("cuda"):
            return device
        if torch.cuda.is_available():
            return "cuda"
        elif platform.system() == "Darwin" and torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"

    def write_audio(self, audio: np.ndarray, filepath: str):
        sf.write(filepath, audio, self.SAMPLE_RATE, "PCM_16")

    @timer(tag="preprocess")
    def preprocess_text(
        self,
        text: str,
        length_threshold: int = 50,
        window_size: int = 50,
        split_fn: Optional[Callable[[str], list[str]]] = None,
    ) -> list[str]:
        if contains_chinese(text):
            text = self.zh_normalizer.normalize(text)
        else:
            text = self.en_normalizer.normalize(text)

        tokenize_fn = partial(
            self.generator.tokenizer.encode,
            add_special_tokens=False,
            truncation=False,
            padding=False,
        )
        return split_text(
            text,
            window_size,
            tokenize_fn=tokenize_fn,
            split_fn=split_fn,
            length_threshold=length_threshold,
        )

    def _parse_multi_speak_text(self, text: str) -> list[dict[str, str]]:
        if len(self.list_speakers()) == 0:
            msg = f"The role library in {self.__class__.__name__} is empty, making multi-role speech synthesis impossible."
            logger.error(msg)
            raise RuntimeError(msg)

        segments = parse_multi_speaker_text(text, self.list_speakers())
        if len(segments) == 0:
            msg = f"The multi-role text parsing result is empty. Please check the input text format: {text}"
            logger.error(msg)
            raise RuntimeError(msg)

        return segments

    async def speak_async(
        self,
        text: str,
        name: Optional[str] = None,
        pitch: Optional[
            Literal["very_low", "low", "moderate", "high", "very_high"]
        ] = None,
        speed: Optional[
            Literal["very_low", "low", "moderate", "high", "very_high"]
        ] = None,
        temperature: float = 0.9,
        top_k: int = 50,
        top_p: float = 0.95,
        repetition_penalty: float = 1.0,
        max_tokens: int = 4096,
        length_threshold: int = 50,
        window_size: int = 50,
        split_fn: Optional[Callable[[str], list[str]]] = None,
        **kwargs,
    ) -> np.ndarray:
        raise NotImplementedError(
            f"Speak_async not implemented for {self.__class__.__name__}"
        )

    async def speak_stream_async(
        self,
        text: str,
        name: Optional[str] = None,
        pitch: Optional[
            Literal["very_low", "low", "moderate", "high", "very_high"]
        ] = None,
        speed: Optional[
            Literal["very_low", "low", "moderate", "high", "very_high"]
        ] = None,
        temperature: float = 0.9,
        top_k: int = 50,
        top_p: float = 0.95,
        repetition_penalty: float = 1.0,
        max_tokens: int = 4096,
        length_threshold: int = 50,
        window_size: int = 50,
        split_fn: Optional[Callable[[str], list[str]]] = None,
        **kwargs,
    ) -> AsyncIterator[np.ndarray]:
        yield NotImplementedError(
            f"speak_stream_async not implemented for {self.__class__.__name__}"
        )

    async def clone_voice_async(
        self,
        text: str,
        reference_audio,
        reference_text: Optional[str] = None,
        pitch: Optional[
            Literal["very_low", "low", "moderate", "high", "very_high"]
        ] = None,
        speed: Optional[
            Literal["very_low", "low", "moderate", "high", "very_high"]
        ] = None,
        temperature: float = 0.9,
        top_k: int = 50,
        top_p: float = 0.95,
        repetition_penalty: float = 1.0,
        max_tokens: int = 4096,
        length_threshold: int = 50,
        window_size: int = 50,
        split_fn: Optional[Callable[[str], list[str]]] = None,
        **kwargs,
    ) -> np.ndarray:
        raise NotImplementedError(
            f"Clone_voice_async not implemented for {self.__class__.__name__}"
        )

    async def clone_voice_stream_async(
        self,
        text: str,
        reference_audio,
        reference_text: Optional[str] = None,
        pitch: Optional[
            Literal["very_low", "low", "moderate", "high", "very_high"]
        ] = None,
        speed: Optional[
            Literal["very_low", "low", "moderate", "high", "very_high"]
        ] = None,
        temperature: float = 0.9,
        top_k: int = 50,
        top_p: float = 0.95,
        repetition_penalty: float = 1.0,
        max_tokens: int = 4096,
        length_threshold: int = 50,
        window_size: int = 50,
        split_fn: Optional[Callable[[str], list[str]]] = None,
        **kwargs,
    ) -> AsyncIterator[np.ndarray]:
        yield NotImplementedError(
            f"clone_voice_stream_async not implemented for {self.__class__.__name__}"
        )

    async def multi_speak_async(
        self,
        text: str,
        temperature: float = 0.9,
        top_k: int = 50,
        top_p: float = 0.95,
        repetition_penalty: float = 1.0,
        max_tokens: int = 4096,
        length_threshold: int = 50,
        window_size: int = 50,
        split_fn: Optional[Callable[[str], list[str]]] = None,
        **kwargs,
    ) -> np.ndarray:
        """
        调用多角色共同合成语音。
        text (str): 待解析的文本，文本中各段台词前以 <role:角色名> 标识。
        如：<role:角色1>你好，欢迎来到我们的节目。<role:角色2>谢谢，我很高兴在这里。<role:角色3>大家好！
        """
        segments = self._parse_multi_speak_text(text)
        semaphore = asyncio.Semaphore(self._batch_size)  # 限制并发数，避免超长文本卡死
        limit_speak = limit_concurrency(semaphore)(self.speak_async)
        tasks = [
            asyncio.create_task(
                limit_speak(
                    name=segment["name"],
                    text=segment["text"],
                    pitch=segment["pitch"],
                    speed=segment["speed"],
                    temperature=temperature,
                    top_k=top_k,
                    top_p=top_p,
                    repetition_penalty=repetition_penalty,
                    max_tokens=max_tokens,
                    length_threshold=length_threshold,
                    window_size=window_size,
                    split_fn=split_fn,
                    **kwargs,
                )
            )
            for segment in segments
        ]
        # 并发执行所有任务
        audios = await asyncio.gather(*tasks)
        audio = np.concatenate(audios, axis=0)
        return audio

    async def multi_speak_stream_async(
        self,
        text: str,
        temperature: float = 0.9,
        top_k: int = 50,
        top_p: float = 0.95,
        repetition_penalty: float = 1.0,
        max_tokens: int = 4096,
        length_threshold: int = 50,
        window_size: int = 50,
        split_fn: Optional[Callable[[str], list[str]]] = None,
        **kwargs,
    ) -> AsyncIterator[np.ndarray]:
        segments = self._parse_multi_speak_text(text)

        for segment in segments:
            async for chunk in self.speak_stream_async(
                name=segment["name"],
                text=segment["text"],
                pitch=segment["pitch"],
                speed=segment["speed"],
                temperature=temperature,
                top_k=top_k,
                top_p=top_p,
                repetition_penalty=repetition_penalty,
                max_tokens=max_tokens,
                length_threshold=length_threshold,
                window_size=window_size,
                split_fn=split_fn,
                **kwargs,
            ):
                yield chunk
