Util list:

 - count_tokens: GPT系列模型下，计算文本使用的token
 - calculate_total_tokens: GPT系列模型下，计算多轮对话使用的token
 - CommonGPTModel: 常见的 GPT 模型使用名称
 - os_environ_setting: API key 的环境变量设置，或者进行代理IP和端口设置（必须先于 chat_with_llm 进行调用；或者自己手动进行了 api key 的配置，就不用调用了）
 - chat_with_llm: 与 LLM 进行文本对话