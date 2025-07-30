import instructor
import logging
import colorlog
from openai import OpenAI
from pydantic import BaseModel


handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)s:%(name)s:%(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )
)
logging.basicConfig(level=logging.DEBUG, handlers=[handler])

client = instructor.from_openai(
    client=OpenAI(api_key="<api_key>", base_url="https://ark.cn-beijing.volces.com/api/v3"),
    mode=instructor.Mode.MD_JSON,
)


class UserDetail(BaseModel):
    name: str
    age: int


user = client.chat.completions.create(
    model="deepseek-v3-250324",
    response_model=UserDetail,
    messages=[
        {"role": "user", "content": "Extract Jason is 25 years old"},
    ],
)

logging.info("User detail: %s", user)
