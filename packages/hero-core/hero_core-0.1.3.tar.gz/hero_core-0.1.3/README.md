[English](README.md) | [中文](README.zh-CN.md)

## Installation

1. Install package:

```sh

pip install hero-core

```

2. Quickly Start

```python

import asyncio
from hero import Hero, Model

model = Model(model_name="your-model",
              api_base="api_base",
              api_key="api_key")

hero = Hero(model=model, search_api="api-key") # https://serper.dev

async def test_init():
    result = await hero.run("hello")
    print(result)

if __name__ == "__main__":
    asyncio.run(test_init())

```