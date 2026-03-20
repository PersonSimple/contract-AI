def calculate_cost(hours_worked, hourly_rate):

    if hours_worked <= 0:
        raise ValueError("hours_worked must be positive")

    if hourly_rate <= 0:
        raise ValueError("hourly_rate must be positive")

    total_cost = hours_worked * hourly_rate

    return total_cost