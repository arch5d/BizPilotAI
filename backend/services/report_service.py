"""
Report service functions for generating and managing reports.
"""
from typing import List
from bson import ObjectId

from database.db import get_database
from database.models import Report, ReportCreate


from agents.marketing_agent import MarketingAgent
from agents.finance_agent import FinanceAgent
from agents.operations_agent import OperationsAgent
from agents.sales_agent import SalesAgent
from agents.strategy_agent import StrategyAgent


_agent_map = {
    "marketing": MarketingAgent,
    "finance": FinanceAgent,
    "operations": OperationsAgent,
    "sales": SalesAgent,
    "strategy": StrategyAgent,
}


db = None

def get_db():
    global db
    if db is None:
        db = get_database()
    return db


async def list_reports() -> List[Report]:
    database = get_db()
    cursor = database["reports"].find().sort("created_at", -1)
    docs = await cursor.to_list(length=None)
    return [Report(**doc) for doc in docs]


async def list_reports_for_business(business_id: str) -> List[Report]:
    if not ObjectId.is_valid(business_id):
        raise ValueError("Invalid business ID")
    database = get_db()
    cursor = database["reports"].find({"business_id": ObjectId(business_id)})
    docs = await cursor.to_list(length=None)
    return [Report(**doc) for doc in docs]


async def get_report(report_id: str) -> Report:
    if not ObjectId.is_valid(report_id):
        raise ValueError("Invalid report ID")
    database = get_db()
    doc = await database["reports"].find_one({"_id": ObjectId(report_id)})
    if not doc:
        raise ValueError("Report not found")
    return Report(**doc)


async def delete_report(report_id: str) -> None:
    if not ObjectId.is_valid(report_id):
        raise ValueError("Invalid report ID")
    database = get_db()
    res = await database["reports"].delete_one({"_id": ObjectId(report_id)})
    if res.deleted_count == 0:
        raise ValueError("Report not found")


async def run_agent(agent_name: str, business_id: str) -> Report:
    """Run specified agent for business and save report."""
    if agent_name not in _agent_map:
        raise ValueError("Invalid agent name")
    business = await get_db()["businesses"].find_one({"_id": ObjectId(business_id)})
    if not business:
        raise ValueError("Business not found")

    agent_cls = _agent_map[agent_name]
    agent = agent_cls()
    # asynchronous call to agent
    content = await agent.run(business)

    report_doc = {
        "business_id": ObjectId(business_id),
        "agent_name": agent_name,
        "content": content,
        "created_at": __import__("datetime").datetime.utcnow(),
    }
    result = await get_db()["reports"].insert_one(report_doc)
    saved = await get_db()["reports"].find_one({"_id": result.inserted_id})
    return Report(**saved)
