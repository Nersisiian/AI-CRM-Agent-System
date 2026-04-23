import json
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Customer, Lead, Deal
import structlog

logger = structlog.get_logger(__name__)

class CRMTools:
    def __init__(self, db: AsyncSession):
        self.db = db

    def get_definitions(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_customer_by_email",
                    "description": "Получить информацию о клиенте по email",
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
                    "name": "create_lead",
                    "description": "Создать новый лид",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "customer_email": {"type": "string"},
                            "name": {"type": "string"},
                            "source": {"type": "string"}
                        },
                        "required": ["customer_email", "name", "source"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_recent_deals",
                    "description": "Последние сделки",
                    "parameters": {
                        "type": "object",
                        "properties": {"limit": {"type": "integer"}}
                    }
                }
            }
        ]

    async def execute(self, func_name: str, arguments: str):
        args = json.loads(arguments)
        if func_name == "get_customer_by_email":
            return await self._get_customer(args["email"])
        elif func_name == "create_lead":
            return await self._create_lead(args["customer_email"], args["name"], args["source"])
        elif func_name == "list_recent_deals":
            limit = args.get("limit", 5)
            return await self._list_deals(limit)
        else:
            raise ValueError(f"Unknown function {func_name}")

    async def _get_customer(self, email: str) -> str:
        stmt = select(Customer).where(Customer.email == email)
        result = await self.db.execute(stmt)
        cust = result.scalar_one_or_none()
        if cust:
            return f"Клиент: {cust.name}, компания: {cust.company or '-'}, email: {cust.email}"
        return "Клиент не найден"

    async def _create_lead(self, email: str, name: str, source: str) -> str:
        stmt = select(Customer).where(Customer.email == email)
        result = await self.db.execute(stmt)
        cust = result.scalar_one_or_none()
        if not cust:
            return f"Ошибка: клиент с email {email} не найден"
        lead = Lead(customer_id=cust.id, source=source, notes=f"AI Lead for {name}")
        self.db.add(lead)
        await self.db.commit()
        return f"Лид создан, ID: {lead.id}"

    async def _list_deals(self, limit: int) -> str:
        stmt = select(Deal).join(Customer).order_by(desc(Deal.created_at)).limit(limit)
        result = await self.db.execute(stmt)
        deals = result.scalars().all()
        if not deals:
            return "Сделки не найдены"
        return "\n".join([f"Сделка {d.id}: сумма {d.amount}, стадия {d.stage}, клиент {d.customer.name}" for d in deals])