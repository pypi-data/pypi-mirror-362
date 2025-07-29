# walleot

Accept payments in your MCP agents in just two lines of code using [Walleot](https://walleot.com) — a drop-in payment provider built for the Model Context Protocol.

## Overview

This is a lightweight wrapper around [`paymcp`](https://pypi.org/project/paymcp/) that configures it to use **Walleot** as the payment backend, so you can start charging for tool usage with minimal effort.

## Installation

```bash
pip install walleot
```

## Usage

```python
from mcp.server.fastmcp import FastMCP
from walleot import Walleot, price, PaymentFlow
import os

mcp = FastMCP("My Server")

walleot = Walleot(
    mcp,
    api_key=os.getenv("WALLEOT_API_KEY"),
    payment_flow=PaymentFlow.ELICITATION
)

@walleot.price(0.99, currency="USD")
@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b
```

## Features

- Accept payments of any amount, including microtransactions as small as $0.01
- Add monetization to any tool with a simple decorator
- Supports multiple payment flows (elicit, confirm, progress)
- Secure API-key-based authentication

## Getting Started

1. Visit [https://walleot.com](https://walleot.com)
2. Create an account and register a new merchant
3. Generate your API key and use it in your MCP server

---
Built on top of [`paymcp`](https://pypi.org/project/paymcp/)