from typing import List

import tiktoken

'''
tiktoken是由OpenAI开发的一个用于文本处理的Python库。它的主要功能是将文本编码为数字序列(称为"tokens"),或将数字序列解码为文本。这个过程被称为"tokenization"(分词)。
可以说它是专门为OpenAI的语言模型(如GPT系列)设计的。这意味着它使用的编码方式与这些模型的训练数据一致,从而可以最大限度地发挥模型的性能。
纯本地计算 的，不会调用任何外部接口。
'''


def count_tokens(text: str, model: str):
    """
    计算文本的 token 数量
    :param text: 要计算 token 的文本
    :param model: llm model name, e.g. 'gpt-4o-mini'
    """
    # 获取编码器
    enc = tiktoken.encoding_for_model(model)

    # 获取文本的 tokens 列表
    tokens = enc.encode(text)

    # 返回 token 数量
    return len(tokens)


def calculate_total_tokens(messages: List[dict], model: str):
    """
    计算一系列消息的总 token 数量
    :param messages: 消息, list of message, message format:
        {
            'role': 'system' or 'user' or 'assistant',
            'content': {
                'type': 'text' or 'image_url',
                'text': str,
                # or
                'image_url': str,
            }
        }
    :param model: llm model name, e.g. 'gpt-4o-mini'
    """
    total_tokens = 0

    for message in messages:
        for content in message["content"]:
            content_type = content["type"]
            if content_type == "image_url":
                continue
            content_xxx = content[content_type]
            # 统计每条消息的 token 数量
            total_tokens += count_tokens(content_xxx, model)

    return total_tokens
