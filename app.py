from fastapi import FastAPI, Request, HTTPException,Depends,Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import cx_Oracle
app=FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="template")
@app.get("/{path:path}", response_class=HTMLResponse)
async def read_item(request: Request, path: str):
    if path == "" or path == "index.html":
        return templates.TemplateResponse("index.html", {"request": request})
    elif path == "login.html":
        return templates.TemplateResponse("login.html", {"request": request})
    elif path == "signup.html":
        return templates.TemplateResponse("signup.html", {"request": request})
    return templates.TemplateResponse("index.html", {"request": request})
@app.post("/submit_contact_form")
async def submit_contact_form(request: Request, FullName: str = Form(...), email: str = Form(...), Subject: str = Form(...), Message: str = Form(...)):
    conn = cx_Oracle.connect('admin/admin@localhost:1521/XEXDB')
    cursor = conn.cursor()

    # Define the SQL query
    query = """
    INSERT INTO contactform (FULLNAME, EMAIL, SUBJECT, MESSAGE)
    VALUES (:1, :2, :3, :4)
    """

    # Define the values to insert
    values = (FullName, email, Subject, Message)

    # Execute the query
    cursor.execute(query, values)

    # Commit the transaction
    conn.commit()

    cursor.close()
    conn.close()

    return templates.TemplateResponse("index.html", {"request": request})
@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    conn = cx_Oracle.connect('admin/admin@localhost:1521/XEXDB')
    cursor = conn.cursor()

    # Define the SQL query
    query = """
    SELECT * FROM users
    WHERE email = :1 AND password = :2
    """
    
    # Define the values to insert
    values = (email, password)
    print(email, password)
    # Execute the query
    cursor.execute(query, values)
    print(f"Executing query: {query} with values: {values}")
    user = cursor.fetchone()
    print(user)
    cursor.close()
    conn.close()

    
    if user is None:
        return {"status": "error", "message": "Invalid credentials"}

    return {"status": "success", "message": "Login successful"}