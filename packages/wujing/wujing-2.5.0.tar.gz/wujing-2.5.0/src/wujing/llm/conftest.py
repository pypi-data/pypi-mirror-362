from typing import Self

import pytest
from pydantic import BaseModel, ValidationInfo, model_validator

from rich import print as rprint


@pytest.fixture(scope="session")
def volces():
    return ("https://ark.cn-beijing.volces.com/api/v3", "<api_key>", "deepseek-v3-250324")


@pytest.fixture(scope="session")
def vllm():
    return ("http://127.0.0.1:8001/v1", "sk-xylx1.t!@#", "Qwen3-32B")


@pytest.fixture(scope="session")
def model():
    return "deepseek-v3-250324"


@pytest.fixture(scope="session")
def messages():
    return [{"role": "user", "content": "Hello, how are you?"}]


class ResponseModel(BaseModel):
    content: str

    @model_validator(mode="after")
    def check_info(self, info: ValidationInfo) -> Self:
        if info.context is None:
            rprint("[red]No context provided[/red]")
        else:
            rprint(f"[red]{info.context=}[/red]")
        return self


@pytest.fixture(scope="session")
def context():
    return {"test": "context"}


@pytest.fixture(scope="session", params=[ResponseModel])
def response_model(request):
    return request.param
