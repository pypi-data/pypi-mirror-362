from typing import Any, Dict, List

from openai import OpenAI


def oai(
    *,
    api_key: str,
    api_base: str,
    model: str,
    messages: List[Dict[str, str]],
    stream: bool = False,
    **kwargs: Any,
) -> str:
    client = OpenAI(
        api_key=api_key,
        base_url=api_base,
    )

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=stream,
            **kwargs,
        )

        if stream:
            content = ""
            for chunk in resp:
                if chunk.choices and chunk.choices[0].delta.content:
                    chunk_content = chunk.choices[0].delta.content
                    content += chunk_content
            return content
        else:
            return resp.choices[0].message.content

    except Exception as e:
        raise RuntimeError(f"Failed to send request: {e}") from e
