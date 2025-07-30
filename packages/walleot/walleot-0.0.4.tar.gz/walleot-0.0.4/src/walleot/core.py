# walleot/core.py
from paymcp import PayMCP, PaymentFlow, price 

class Walleot:
    def __init__(self, mcp_instance, api_key=None, apiKey=None,  payment_flow: PaymentFlow = PaymentFlow.ELICITATION):
        effective_api_key = api_key if api_key is not None else apiKey
        self._paymcp = PayMCP(
            mcp_instance,
            providers={"walleot": {"api_key": effective_api_key}},
            payment_flow=payment_flow
        )

    def __getattr__(self, item):
        return getattr(self._paymcp, item)
        

