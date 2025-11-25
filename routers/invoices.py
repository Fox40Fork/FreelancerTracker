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
    cursor.execute("SELECT id, invoice_number, client_id, amount, date, status FROM invoices")
    invoices = cursor.fetchall()
    return [{
        "id": invoice[0],
        "invoice_number": invoice[1],
        "client_id": invoice[2],
        "amount": invoice[3],
        "date": invoice[4],
        "status": invoice[5]
    } for invoice in invoices]

@router.post("/", response_model = Invoice)
def createInvoice(invoice: InvoiceCreate):
    conn = getDBConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO invoices (invoice_number, client_id, amount, date, status) VALUES (?, ?, ?, ?, ?)",
            (invoice.invoice_number, invoice.client_id, invoice.amount, invoice.date, invoice.status)
        )
        conn.commit()

        invoice_id = cursor.lastrowid
        cursor.execute("SELECT * FROM invoices WHERE id = ?", (invoice_id,))
        row = cursor.fetchone()

        return Invoice(
            id=row[0],
            invoice_number=row[1],
            client_id=row[2],
            amount=row[3],
            date=row[4],
            status=row[5]
        )

    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{e}"
        )
    finally:
        conn.close()


@router.put("/{invoice_number}", response_model=Invoice)
def updateInvoice(invoice_id: int, invoice: InvoiceCreate):
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE invoices SET invoice_number = ?, client_id = ?, amount = ?, date = ?, status = ?"
        "WHERE id = ?",
        (invoice.invoice_number, invoice.client_id, invoice.amount, invoice.date, invoice.status, invoice_id))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Invoice not found")
    conn.commit()
    conn.close()
    return Invoice(id=invoice_id, **invoice.model_dump())

@router.delete("/{invoice_number}", response_model=dict)
def deleteInvoice(invoice_id: int):
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM invoices WHERE id = ?", (invoice_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Invoice not found")
    conn.commit()
    conn.close()
    return {"detail": "Invoice deleted"}