import asyncio
from app.db.database import async_session_factory
from app.db.models import Customer, Lead, Deal

async def seed():
    async with async_session_factory() as session:
        from sqlalchemy import select
        res = await session.execute(select(Customer).limit(1))
        if res.scalar_one_or_none():
            return
        c1 = Customer(name="Иван Петров", email="ivan@example.com", company="Ромашка")
        c2 = Customer(name="Мария Сидорова", email="maria@example.com", company="Техно")
        session.add_all([c1, c2])
        await session.flush()
        session.add_all([
            Lead(customer_id=c1.id, source="website", status="new"),
            Deal(customer_id=c1.id, amount=150000, stage="proposal"),
            Deal(customer_id=c2.id, amount=75000, stage="qualification"),
        ])
        await session.commit()
        print("Data seeded")

if __name__ == "__main__":
    asyncio.run(seed())