from textwrap import dedent
from typing import Type
from enum import Enum as _Enum
import os

import openai
from pydantic import BaseModel

from count_tokens import calculate_total_tokens


class CommonGPTModel(_Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo-0125"
    GPT_4_0314 = "gpt-4-0314"
    GPT_4_32k_0314 = "gpt-4-32k-0314"
    GPT_4_0613 = "gpt-4-0613"
    GPT_4_32k_0613 = "gpt-4-32k-0613"
    GPT_4o_MINI = "gpt-4o-mini"
    GPT_4o_240806 = "gpt-4o-2024-08-06"


# 获取特定环境变量的值
_client = None


def _get_client():
    global _client
    if _client is None:
        _client = openai.OpenAI()
    return _client


def os_environ_setting(api_key_file_path: str, proxy_ip: str = None, proxy_port: int = None):
    """
    进行环境变量配置，必须先于 chat_with_llm 进行调用；或者自己手动进行了 api key 的配置，就不用调用了
    :param api_key_file_path: 存放 API Key 的文件路径(文件内容仅有 api key)
    :param proxy_ip: 如果需要设置代理，可以填写；如本地代理 '127.0.0.1'，或者外部代理'外部服务商IP'
    :param proxy_port: 如果需要设置代理，可以填写；对应的代理服务端口
    :return:
    """
    with open(api_key_file_path, 'r') as f:  # 临时设置 api_key 为环境变量
        api_key = f.read().strip()
        os.environ['OPENAI_API_KEY'] = api_key

    if proxy_ip is not None and proxy_port is not None:
        os.environ['HTTP_PROXY'] = f'http://{proxy_ip}:{proxy_port}'
        os.environ['HTTPS_PROXY'] = f'https://{proxy_ip}:{proxy_port}'


def chat_with_llm(model: str, instruction: str, prompt: str, response_format: Type[BaseModel], print_token: bool) \
        -> Type[BaseModel]:
    """
    与 LLM 进行聊天。
    :param model: llm model name, e.g. 'gpt-4o-mini'
    :param instruction: 指令，让大模型扮演具体身份角色，并且指明讨论的详细具体的场景描述
    :param prompt: 提示词，具体要询问大模型的输入内容，
        要求：问题直接明确，有结构性(可以使用制表符、换行符或 MD 格式)；输出要求也得讲明(内容量，大致格式(具体格式由 response_format 指出))；可以有少样本提示(几个输入输出案例)
        instruction 和 prompt 要直接、具体、明确。
    :param response_format: 输出的具体格式，为继承 BaseModel 的类, e.g.
        class Category(str, Enum):
            shoes = "shoes"
            jackets = "jackets"
            tops = "tops"
            bottoms = "bottoms"
        class ProductSearchParameters(BaseModel):
            category: Category
            subcategory: str
            color: str

        class ArticleSummary(BaseModel):
            class Concept(BaseModel):
                title: str
                description: str

            invented_year: int
            summary: str
            inventors: list[str]
            description: str
            concepts: list[Concept]
    :param print_token: 是否打印使用的 token
    :return: the response, the subclass of BaseModel, usage:
        re: ArticleSummary = response
        re.concepts[0].title
    """
    client = _get_client()
    messages = [
        {
            "role": "system",
            "content": [
                {"type": "text", "text": dedent(instruction)},
                # {
                #     "type": "image_url",
                #     "image_url": {
                #         "url": "https://example.com/gui_image.jpg"
                #     }
                # }
            ]
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": dedent(prompt)}
            ]
        },
    ]
    if print_token:
        t = calculate_total_tokens(messages, model)
        print('total input tokens: %d.' % t)
    response = client.beta.chat.completions.parse(
        model=model,
        messages=messages,
        response_format=response_format
    )
    return response.choices[0].message.parsed
