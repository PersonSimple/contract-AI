from app.services.cost_service import calculate_cost
from app.services.contract_service import validate_budget
from app.exceptions.custom_exceptions import BudgetExceededException


# Test cost calculation
def test_cost_calculation():
    assert calculate_cost(10, 50) == 500


# Dummy objects for testing
class DummyCost:
    def __init__(self, total_cost):
        self.total_cost = total_cost


class DummyTask:
    def __init__(self, costs):
        self.costs = costs


class DummyContract:
    def __init__(self, max_budget, tasks):
        self.max_budget = max_budget
        self.tasks = tasks


# Test budget exceeded
def test_budget_exceeded():
    contract = DummyContract(
        max_budget=1000,
        tasks=[
            DummyTask([DummyCost(900)])
        ]
    )

    try:
        validate_budget(contract, 200)
        assert False  # should not reach here
    except BudgetExceededException:
        assert True