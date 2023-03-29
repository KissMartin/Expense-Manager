def yearly_i_to_monthly(yearly: float) -> float:
    return (yearly / 12)


def monthly_i_to_yearly(monthly: float) -> float:
    return (monthly * 12)


def state(income: float, expenditure: float) -> float:
    return income - expenditure

