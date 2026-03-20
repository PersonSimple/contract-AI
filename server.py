from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("contract-ai")

BASE_URL = "http://127.0.0.1:8000"


# ---------------- CREATE FULL PROJECT ----------------
@mcp.tool()
def create_full_project(name: str, email: str, skill: str, hourly_rate: float,
                        contract_name: str, budget: float, tasks: list):
    """
    Creates contractor, contract, and tasks in one flow
    """

    # 1. Create contractor
    contractor = requests.post(
        f"{BASE_URL}/contractors/",
        json={
            "name": name,
            "email": email,
            "skill": skill,
            "hourly_rate": hourly_rate
        }
    ).json()

    contractor_id = contractor["id"]

    # 2. Create contract
    contract = requests.post(
        f"{BASE_URL}/contracts/",
        json={
            "contract_name": contract_name,
            "contractor_id": contractor_id,
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "max_budget": budget,
            "status": "ACTIVE"
        }
    ).json()

    contract_id = contract["id"]

    # 3. Create tasks
    created_tasks = []
    for t in tasks:
        task = requests.post(
            f"{BASE_URL}/tasks/",
            json={
                "task_name": t["name"],
                "contract_id": contract_id,
                "estimated_hours": t["hours"]
            }
        ).json()
        created_tasks.append(task)

    return {
        "contractor": contractor,
        "contract": contract,
        "tasks": created_tasks
    }


# ---------------- COMPLETE TASK ----------------
@mcp.tool()
def complete_task(task_id: int):
    """
    Marks task as COMPLETED and triggers cost calculation
    """

    response = requests.patch(
        f"{BASE_URL}/tasks/{task_id}",
        params={"status": "COMPLETED"}
    )

    return response.json()


# ---------------- LOG WORK SAFELY ----------------
@mcp.tool()
def log_work(task_id: int, hours: float):
    """
    Logs hours with validation
    """

    response = requests.post(
        f"{BASE_URL}/costs/",
        params={
            "task_id": task_id,
            "hours": hours
        }
    )

    return response.json()


# ---------------- GET PROJECT HEALTH ----------------
@mcp.tool()
def get_project_health(contract_id: int):
    """
    Returns project insights
    """

    summary = requests.get(
        f"{BASE_URL}/contracts/{contract_id}/summary"
    ).json()

    total = summary["totalCost"]
    remaining = summary["remainingBudget"]

    used_percent = (total / (total + remaining)) * 100 if (total + remaining) > 0 else 0

    if used_percent > 80:
        risk = "HIGH"
    elif used_percent > 50:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "contract": summary["contractName"],
        "progress": summary["progress"],
        "budget_used_percent": round(used_percent, 2),
        "risk_level": risk
    }


# ---------------- CHECK BUDGET RISK ----------------
@mcp.tool()
def check_budget_risk(contract_id: int):
    """
    Warns if budget is close to limit
    """

    summary = requests.get(
        f"{BASE_URL}/contracts/{contract_id}/summary"
    ).json()

    total = summary["totalCost"]
    remaining = summary["remainingBudget"]

    if remaining <= 0:
        return {
            "status": "EXCEEDED",
            "message": "Budget exceeded!"
        }

    if remaining < total * 0.2:
        return {
            "status": "WARNING",
            "message": "Budget almost exhausted"
        }

    return {
        "status": "SAFE",
        "message": "Budget is under control"
    }


if __name__ == "__main__":
    mcp.run()