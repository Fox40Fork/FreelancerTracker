from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import date

class InvoiceBase(BaseModel):
    invoice_number: int
    client_id: int
    amount: float
    date: date
    status: str

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceResponse(InvoiceBase):
    id: int

class Invoice(InvoiceBase):
    id: int