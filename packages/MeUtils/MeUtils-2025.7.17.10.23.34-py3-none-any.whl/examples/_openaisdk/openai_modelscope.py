#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_siliconflow
# @Time         : 2024/6/26 10:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
"""
Qwen/Qwen2.5-Coder-32B-InstructQwen/Qwen2.5-Coder-14B-InstructQwen/Qwen2.5-Coder-7B-InstructQwen/Qwen2.5-72B-InstructQwen/Qwen2.5-32B-InstructQwen/Qwen2.5-14B-InstructQwen/Qwen2.5-7B-Instruct

Qwen/QVQ-72B-Preview
"""
import os

from meutils.pipe import *
from openai import OpenAI
from openai import OpenAI, APIStatusError

client = OpenAI(
    # api_key=os.getenv("STEP_API_KEY"),
    # base_url="https://api.stepfun.com/v1",
    base_url=os.getenv("MODELSCOPE_BASE_URL"),
    # api_key=os.getenv("MODELSCOPE_API_KEY"),
    api_key="81ccebd2-1933-4996-8c65-8e170d4f4264"
)

# print(client.models.list().model_dump_json(indent=4))

models = client.models.list().data

print(','.join([m.id for m in models]))

qwen = {m.id.removeprefix("Qwen/").lower(): m.id for m in models if m.id.startswith('Qwen')}

print(','.join(qwen))
print(bjson(qwen))

"""
LLM-Research/c4ai-command-r-plus-08-2024, mistralai/Mistral-Small-Instruct-2409, mistralai/Ministral-8B-Instruct-2410, mistralai/Mistral-Large-Instruct-2407, Qwen/Qwen2.5-Coder-32B-Instruct, Qwen/Qwen2.5-Coder-14B-Instruct, Qwen/Qwen2.5-Coder-7B-Instruct, Qwen/Qwen2.5-72B-Instruct, Qwen/Qwen2.5-32B-Instruct, Qwen/Qwen2.5-14B-Instruct, Qwen/Qwen2.5-7B-Instruct, Qwen/QwQ-32B-Preview, LLM-Research/Llama-3.3-70B-Instruct, opencompass/CompassJudger-1-32B-Instruct, Qwen/QVQ-72B-Preview, LLM-Research/Meta-Llama-3.1-405B-Instruct, LLM-Research/Meta-Llama-3.1-8B-Instruct, Qwen/Qwen2-VL-7B-Instruct, LLM-Research/Meta-Llama-3.1-70B-Instruct, Qwen/Qwen2.5-14B-Instruct-1M, Qwen/Qwen2.5-7B-Instruct-1M, Qwen/Qwen2.5-VL-3B-Instruct, Qwen/Qwen2.5-VL-7B-Instruct, Qwen/Qwen2.5-VL-72B-Instruct, deepseek-ai/DeepSeek-R1-Distill-Llama-70B, deepseek-ai/DeepSeek-R1-Distill-Llama-8B, deepseek-ai/DeepSeek-R1-Distill-Qwen-32B, deepseek-ai/DeepSeek-R1-Distill-Qwen-14B, deepseek-ai/DeepSeek-R1-Distill-Qwen-7B, deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B, deepseek-ai/DeepSeek-R1, deepseek-ai/DeepSeek-V3, Qwen/QwQ-32B, XGenerationLab/XiYanSQL-QwenCoder-32B-2412, Qwen/Qwen2.5-VL-32B-Instruct, deepseek-ai/DeepSeek-V3-0324, Wan-AI/Wan2.1-T2V-1.3B, LLM-Research/Llama-4-Scout-17B-16E-Instruct, LLM-Research/Llama-4-Maverick-17B-128E-Instruct, Qwen/Qwen3-0.6B, Qwen/Qwen3-1.7B, Qwen/Qwen3-4B, Qwen/Qwen3-8B, Qwen/Qwen3-14B, Qwen/Qwen3-30B-A3B, Qwen/Qwen3-32B, Qwen/Qwen3-235B-A22B, XGenerationLab/XiYanSQL-QwenCoder-32B-2504, deepseek-ai/DeepSeek-R1-0528

"""


# client.images.generate(
#     model="DiffSynth-Studio/FLUX.1-Kontext-dev-lora-SuperOutpainting",
#     prompt='a dog'
# )

def main():
    try:
        completion = client.chat.completions.create(
            # model="step-1-8k",
            model="deepseek-ai/DeepSeek-R1-0528",

            # model="Qwen/QVQ-72B-Preview",
            # model="qwen/qvq-72b-preview",

            messages=[
                {"role": "user", "content": "你是谁"}
            ],
            # top_p=0.7,
            top_p=None,
            temperature=None,
            stream=True,
            max_tokens=1
        )
    except APIStatusError as e:
        print(e.status_code)

        print(e.response)
        print(e.message)
        print(e.code)

    for chunk in completion:
        content = chunk.choices[0].delta.content
        reasoning_content = chunk.choices[0].delta.reasoning_content
        print(content or reasoning_content)
    print(chunk)


# if __name__ == '__main__':
#     for i in tqdm(range(1)):
#         # break
#         main()

"""

UPSTREAM_BASE_URL=https://api.chatfire.cn
UPSTREAM_API_KEY=

API_KEY=https://xchatllm.feishu.cn/sheets/MekfsfVuohfUf1tsWV0cCvTmn3c?sheet=305f17[:20]
BASE_URL=https://api-inference.modelscope.cn


curl -X 'POST' http://openai-dev.chatfire.cn/oneapi/channel \
    -H "Authorization: Bearer $API_KEY" \
    -H "UPSTREAM-BASE-URL: $UPSTREAM_BASE_URL" \
    -H "UPSTREAM-API-KEY: $UPSTREAM_API_KEY" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
      -d '{
        "id": "1:20",
        "name": "modelscope",
        "tag": "modelscope",
        "key": "$KEY",
        "type": 0,

        "base_url": "'$BASE_URL'",
        "group": "default,china",

        "models": "deepseek-r1-distill-qwen-14b,deepseek-r1-distill-llama-70b,deepseek-r1,deepseek-r1-0528,deepseek-r1-250528,deepseek-chat,deepseek-v3,deepseek-v3-0324,deepseek-v3-250324,PaddlePaddle/ERNIE-4.5-21B-A3B-PT,PaddlePaddle/ERNIE-4.5-0.3B-PT,PaddlePaddle/ERNIE-4.5-VL-28B-A3B-PT,PaddlePaddle/ERNIE-4.5-300B-A47B-PT,qwen2.5-coder-32b-instruct,qwen2.5-coder-14b-instruct,qwen2.5-coder-7b-instruct,qwen2.5-72b-instruct,qwen2.5-32b-instruct,qwen2.5-14b-instruct,qwen2.5-7b-instruct,qwq-32b-preview,qvq-72b-preview,qwen2-vl-7b-instruct,qwen2.5-14b-instruct-1m,qwen2.5-7b-instruct-1m,qwen2.5-vl-3b-instruct,qwen2.5-vl-7b-instruct,qwen2.5-vl-72b-instruct,qwq-32b,qwen2.5-vl-32b-instruct,qwen3-0.6b,qwen3-1.7b,qwen3-4b,qwen3-8b,qwen3-14b,qwen3-30b-a3b,qwen3-32b,qwen3-235b-a22b",
        "model_mapping": {
            "deepseek-reasoner": "deepseek-ai/DeepSeek-R1-0528",
            "deepseek-r1": "deepseek-ai/DeepSeek-R1-0528",
            "deepseek-r1-0528": "deepseek-ai/DeepSeek-R1-0528",
            "deepseek-r1-250528": "deepseek-ai/DeepSeek-R1-0528",
        
            "deepseek-chat": "deepseek-ai/DeepSeek-V3",
            "deepseek-v3": "deepseek-ai/DeepSeek-V3",
            "deepseek-v3-0324": "deepseek-ai/DeepSeek-V3-0324",
            "deepseek-v3-250324": "deepseek-ai/DeepSeek-V3-0324",
            
            "deepseek-r1-distill-qwen-14b": "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B",
            "deepseek-r1-distill-llama-70b": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
        
            "majicflus_v1": "MAILAND/majicflus_v1",
            
            "qwen2.5-coder-32b-instruct": "Qwen/Qwen2.5-Coder-32B-Instruct",
            "qwen2.5-coder-14b-instruct": "Qwen/Qwen2.5-Coder-14B-Instruct",
            "qwen2.5-coder-7b-instruct": "Qwen/Qwen2.5-Coder-7B-Instruct",
            "qwen2.5-72b-instruct": "Qwen/Qwen2.5-72B-Instruct",
            "qwen2.5-32b-instruct": "Qwen/Qwen2.5-32B-Instruct",
            "qwen2.5-14b-instruct": "Qwen/Qwen2.5-14B-Instruct",
            "qwen2.5-7b-instruct": "Qwen/Qwen2.5-7B-Instruct",
            "qwq-32b-preview": "Qwen/QwQ-32B-Preview",
            "qvq-72b-preview": "Qwen/QVQ-72B-Preview",
            "qwen2-vl-7b-instruct": "Qwen/Qwen2-VL-7B-Instruct",
            "qwen2.5-14b-instruct-1m": "Qwen/Qwen2.5-14B-Instruct-1M",
            "qwen2.5-7b-instruct-1m": "Qwen/Qwen2.5-7B-Instruct-1M",
            "qwen2.5-vl-3b-instruct": "Qwen/Qwen2.5-VL-3B-Instruct",
            "qwen2.5-vl-7b-instruct": "Qwen/Qwen2.5-VL-7B-Instruct",
            "qwen2.5-vl-72b-instruct": "Qwen/Qwen2.5-VL-72B-Instruct",
            "qwq-32b": "Qwen/QwQ-32B",
            "qwen2.5-vl-32b-instruct": "Qwen/Qwen2.5-VL-32B-Instruct",
            "qwen3-0.6b": "Qwen/Qwen3-0.6B",
            "qwen3-1.7b": "Qwen/Qwen3-1.7B",
            "qwen3-4b": "Qwen/Qwen3-4B",
            "qwen3-8b": "Qwen/Qwen3-8B",
            "qwen3-14b": "Qwen/Qwen3-14B",
            "qwen3-30b-a3b": "Qwen/Qwen3-30B-A3B",
            "qwen3-32b": "Qwen/Qwen3-32B",
            "qwen3-235b-a22b": "Qwen/Qwen3-235B-A22B"

        } 

    }'

"""
