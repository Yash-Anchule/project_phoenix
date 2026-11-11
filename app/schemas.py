from unicodedata import category
from typing import Literal
from pydantic import BaseModel, Field , ValidationError
from datetime import datetime

class ExpensePydantic(BaseModel):   
    # id : Mapped[int] = mapped_column(primary_key=True)
    # amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    # category: Mapped[str] = mapped_column(String(50), nullable=False)
    # spent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    amount : int | None = None
    category: Literal["restaurant","groceries",
    "transportation",
    "shopping",
    "entertainment",
    "health",
    "utilities",
    "rent",
    "travel",
    "subscriptions",
    "other"
] | None = None
    spent_at : datetime | None = None


class MonthlyBudgetPydantic(BaseModel):
    month: int = Field(..., ge=1, le=12, description="Month must be between 1 and 12")
    year: int  = Field(..., ge=2026, le=9999, description="Year must be between 2026 and 9999")
    monthly_budget: int = Field(..., gt=0, description="Monthly Budget must be a non-negative value")

# raw = {"amount":10}

# try:
#     res = ExpensePydantic(**raw)
#     print(res)
#     print(res.model_fields_set)
# except ValidationError as e:
#     print(e.errors())

