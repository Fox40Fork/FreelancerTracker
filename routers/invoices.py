#Invoices CRUD

import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from models.invoice import Invoice, InvoiceCreate
from database import getDBConnection

router = APIRouter()

@router.get('/', response_model = List[Invoice])

def getInvoices():
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT invoice_number, amount, date, status FROM invoices")
    invoices = cursor.fetchall()
    return [{
        "invoice_number": invoice[0],
        "client_id": invoice[1],
        "amount": invoice[2],
        "date": invoice[3],
        "status": invoice[4]
    } for invoice in invoices]

@router.post("/", response_model = Invoice)
def createInvoice(invoice: InvoiceCreate):
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO invoices (invoice_number, client_id, amount, date, status)"
                "VALUES (?, ?, ?, ?, ?)",
                (invoice.invoice_number, invoice.client_id, invoice.amount, invoice.date, invoice.status))


@router.put("/{invoice_number}", response_model=Invoice)
def updateInvoice(invoice_number: int, invoice: InvoiceCreate):
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE invoices SET invoice_number = ?, client_id = ?, amount = ?, date = ?, status = ?"
        "WHERE invoice_number = ?",
        (invoice.invoice_number, invoice.client_id, invoice.amount, invoice.date, invoice.status))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Invoice not found")
    conn.commit()
    conn.close()
    return Invoice(id=invoice_number, **invoice.dict())

@router.delete("/{invoice_number}", response_model=dict)
def deleteInvoice(invoice_number: int):
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM invoices WHERE id = ?", (invoice_number,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Invoice not found")
    conn.commit()
    conn.close()
    return {"detail": "Invoice deleted"}