import hashlib
import json
from typing import Any, Literal, Type

from diskcache import FanoutCache as Cache
from pydantic import validate_call

from wujing.llm.internal.oai import oai
from wujing.llm.internal.oai_with_instructor import oai_with_instructor
from wujing.llm.types import ResponseModelType


class CacheManager:
    _instances: dict[str, Cache] = {}

    @classmethod
    def get_cache(cls, directory: str) -> Cache:
        if directory not in cls._instances:
            cls._instances[directory] = Cache(directory=directory)
        return cls._instances[directory]


def _generate_cache_key(
    api_key: str,
    api_base: str,
    model: str,
    messages: list[dict[str, str]],
    response_model: Type[ResponseModelType] | None = None,
    context: dict[str, Any] | None = None,
    guided_backend: Literal["instructor"] | None = None,
    **kwargs: dict[str, Any],
) -> str:
    cache_data = {
        "api_key_hash": hashlib.sha256(api_key.encode("utf-8")).hexdigest()[:16],
        "api_base": api_base,
        "model": model,
        "messages": messages,
        "response_model": str(response_model) if response_model else None,
        "context": context,
        "guided_backend": guided_backend,
        "kwargs": sorted(kwargs.items()) if kwargs else None,
    }

    cache_str = json.dumps(cache_data, sort_keys=True, ensure_ascii=False)
    return hashlib.md5(cache_str.encode("utf-8")).hexdigest()


@validate_call(config=dict(arbitrary_types_allowed=True, validate_assignment=False))
def llm_call(
    *,
    api_key: str,
    api_base: str,
    model: str,
    messages: list[dict[str, str]],
    context: dict[str, Any] | None = None,  # 仅用于 instructor 模式，用于传递额外上下文信息
    response_model: Type[ResponseModelType] | None = None,
    guided_backend: Literal["instructor", "vllm"] | None = None,
    cache_enabled: bool = True,
    cache_directory: str = "./.diskcache/llm_cache",
    **kwargs: Any,
) -> str:
    if (response_model is None) != (guided_backend is None):
        raise ValueError("Both response_model and guided_backend must be either set or unset.")

    try:
        cache = CacheManager.get_cache(cache_directory) if cache_enabled else None

        if cache is not None:
            cache_key = _generate_cache_key(
                api_key=api_key,
                api_base=api_base,
                model=model,
                messages=messages,
                response_model=response_model,
                context=context,
                guided_backend=guided_backend,
                **kwargs,
            )

            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

        match guided_backend:
            case "instructor":
                result = oai_with_instructor(
                    api_key=api_key,
                    api_base=api_base,
                    model=model,
                    messages=messages,
                    response_model=response_model,
                    context=context,
                    **kwargs,
                )
            case "vllm":
                kwargs.get("extra_body", {}).update(
                    {
                        "guided_json": response_model.model_json_schema(),
                        "chat_template_kwargs": {"enable_thinking": False},
                    }
                )

                result = oai(
                    api_key=api_key,
                    api_base=api_base,
                    model=model,
                    messages=messages,
                    **kwargs,
                )
            case _:
                result = oai(
                    api_key=api_key,
                    api_base=api_base,
                    model=model,
                    messages=messages,
                    **kwargs,
                )

        if cache is not None:
            cache.set(cache_key, result)

        return result

    except Exception:
        raise
