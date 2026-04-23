# В crm_tools.py в классе CRMTools добавьте в get_definitions и execute
{
    "type": "function",
    "function": {
        "name": "get_churn_risk",
        "description": "Оценить риск оттока клиента по email",
        "parameters": {
            "type": "object",
            "properties": {"email": {"type": "string"}},
            "required": ["email"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "generate_retention_offer",
        "description": "Сгенерировать персональное предложение для удержания",
        "parameters": {
            "type": "object",
            "properties": {"customer_email": {"type": "string"}},
            "required": ["customer_email"]
        }
    }
}