from math import isfinite
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

expenses = {}
next_id = 1


class Expense(BaseModel):
    description: str
    amount: float
    category: str


@app.get("/")
def home():
    return FileResponse(Path(__file__).parent / "index.html")


@app.get("/api/expenses")
def get_expenses():
    return list(expenses.values())


@app.post("/api/expenses")
def add_expense(expense: Expense):
    global next_id

    description = expense.description.strip()
    category = expense.category.strip()

    if not description:
        raise HTTPException(status_code=400, detail="Description cannot be empty.")
    if not isfinite(expense.amount) or expense.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero.")
    if not category:
        raise HTTPException(status_code=400, detail="Category cannot be empty.")

    new_expense = {
        "id": next_id,
        "description": description,
        "amount": expense.amount,
        "category": category,
    }
    expenses[next_id] = new_expense
    next_id += 1
    return new_expense


@app.put("/api/expenses/{expense_id}")
def update_expense(expense_id: int, expense: Expense):
    description = expense.description.strip()
    category = expense.category.strip()

    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    if not description:
        raise HTTPException(status_code=400, detail="Description cannot be empty.")
    if not isfinite(expense.amount) or expense.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero.")
    if not category:
        raise HTTPException(status_code=400, detail="Category cannot be empty.")

    updated_expense = {
        "id": expense_id,
        "description": description,
        "amount": expense.amount,
        "category": category,
    }
    expenses[expense_id] = updated_expense
    return updated_expense


@app.delete("/api/expenses/{expense_id}")
def delete_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")

    del expenses[expense_id]
    return {"message": "Expense deleted successfully"}
