from typing import Any, Dict, List, Type

import instructor
from openai import OpenAI

from wujing.llm.types import ResponseModelType

def oai_with_instructor(
    *,
    api_key: str,
    api_base: str,
    model: str,
    messages: List[Dict[str, str]],
    response_model: Type[ResponseModelType] | None = None,
    context: dict | None = None,
    **kwargs: Any,
) -> str:
    client = instructor.from_openai(
        client=OpenAI(api_key=api_key, base_url=api_base),
        mode=instructor.Mode.JSON,
    )

    try:
        return client.chat.completions.create(
            model=model,
            messages=messages,
            response_model=response_model,
            context=context,
            **kwargs,
        ).model_dump_json()

    except Exception as e:
        raise RuntimeError(f"Failed to send request: {e}") from e
