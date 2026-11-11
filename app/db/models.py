from sqlalchemy import Integer
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, String , CheckConstraint,UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Expenses(Base):
    __tablename__ = "expenses"
     
    id : Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    spent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)



class MonthlyBudget(Base):
    __tablename__ = "monthly_budgets"
     
    id : Mapped[int] = mapped_column(primary_key=True)
    month : Mapped[int] = mapped_column(Integer,CheckConstraint("month >= 1 AND month <= 12", name="check_valid_month"),nullable=False)
    year : Mapped[int] = mapped_column()
    monthly_budget : Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    __table_args__ = (
        UniqueConstraint("month", "year", name="unq_month_budget"),
    )