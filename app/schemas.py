from unicodedata import category
from sqlalchemy.util.typing import Literal
from pydantic import BaseModel , ValidationError
from datetime import datetime

class ExpensePydantic(BaseModel):
    # id : Mapped[int] = mapped_column(primary_key=True)
    # amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    # category: Mapped[str] = mapped_column(String(50), nullable=False)
    # spent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    amount : int | None = None
    category: str| None = None
    spent_at : datetime | None = None


# raw = {"amount":10}

# try:
#     res = ExpensePydantic(**raw)
#     print(res)
#     print(res.model_fields_set)
# except ValidationError as e:
#     print(e.errors())

