from app.exceptions.custom_exceptions import BudgetExceededException


def validate_budget(contract, new_cost):

    if new_cost <= 0:
        raise ValueError("New cost must be positive")

    current_cost = sum(
        cost.total_cost
        for task in contract.tasks
        for cost in task.costs
    )

    if current_cost + new_cost > contract.max_budget:
        raise BudgetExceededException("Contract budget limit exceeded")

    return True


def calculate_progress(contract):

    total_tasks = len(contract.tasks)

    if total_tasks == 0:
        return 0.0

    completed_tasks = sum(
        1 for task in contract.tasks if task.status == "COMPLETED"
    )

    return completed_tasks / total_tasks