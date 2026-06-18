from pydantic import BaseModel, Field


class CategorySpend(BaseModel):
    category_id: str | None
    category_name: str
    amount: int
    percentage: float = Field(ge=0, le=100)


class MonthlyInsight(BaseModel):
    month: str
    total_spent: int
    total_income: int
    currency: str = "UZS"
    by_category: list[CategorySpend]
