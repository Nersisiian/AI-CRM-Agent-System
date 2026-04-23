import json
from app.integrations.crm_connector import CRMConnector

class ExternalAPITools:
    def __init__(self, crm_connector: CRMConnector):
        self.crm = crm_connector

    def get_definitions(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "crm_get_customer",
                    "description": "Найти клиента в CRM через API",
                    "parameters": {"type": "object", "properties": {"email": {"type": "string"}}, "required": ["email"]}
                }
            }
        ]

    async def execute(self, func_name: str, arguments: str):
        args = json.loads(arguments)
        if func_name == "crm_get_customer":
            return await self.crm.get_customer(args["email"])
        raise ValueError("Unknown tool")
