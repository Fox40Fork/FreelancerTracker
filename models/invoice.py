from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import date

class InvoiceBase(BaseModel):
    amount: Decimal
    date: date
    status: str

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceResponse(InvoiceBase):
    invoice_number: int

class Invoice(InvoiceBase):
    invoice_number: int