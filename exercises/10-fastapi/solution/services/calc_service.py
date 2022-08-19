from models.db.calculator_result import CalculatorResult


async def record_calculation(x: int, y: int, action: str, result: float) -> CalculatorResult:
    calc = CalculatorResult(
        x=x,
        y=y,
        action=action,
        result=result
    )

    await calc.save()
    return calc
