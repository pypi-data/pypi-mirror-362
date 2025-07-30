from langchain.tools import BaseTool
from typing import Dict, Any
from gokite import KiteClient
import os


class KitePaymentTool(BaseTool):
    name = "KiteAgentPayment"
    description = "Use this tool to make on-chain payments via the Kite Network. Input should be a dictionary like {'to': '0x...', 'amount': 1.5}."

    def __init__(self, client: KiteClient):
        super().__init__()
        self.client = client

    @classmethod
    def from_env(cls):
        api_key = os.environ.get("KITE_API_KEY")
        if not api_key:
            raise ValueError("Missing KITE_API_KEY in environment.")
        client = KiteClient(api_key=api_key)
        return cls(client=client)

    def _run(self, payment_details: Dict[str, Any]) -> str:
        try:
            tx_hash = self.client.make_payment(
                to_address=payment_details.get("to"),
                amount=payment_details.get("amount")
            )
            return f"Payment successful. Transaction hash: {tx_hash}"
        except Exception as e:
            return f"Payment failed: {str(e)}"

    async def _arun(self, payment_details: Dict[str, Any]) -> str:
        return self._run(payment_details)
