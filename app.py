from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import cx_Oracle
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="template")
sn_tns = cx_Oracle.makedsn('Host_Name', 'Port_Number', service_name='Service_Name') 
conn = cx_Oracle.connect(user='Username', password='Password', dsn=sn_tns) 

class ContactForm(BaseModel):
    name: str 
    email: str
    message: str

@app.post("/submit_form", response_class=HTMLResponse)
async def submit_form(form: ContactForm):
    # Use the connection
    c = conn.cursor()
    c.execute(f"INSERT INTO admin.contact_form (email, message) VALUES ('{form.email}', '{form.message}')") 
    conn.commit()
    return {"message": "Form submitted successfully"}

@app.get("/{path:path}", response_class=HTMLResponse)
async def read_item(request: Request, path: str):
    if path == "" or path == "index.html":
        return templates.TemplateResponse("index.html", {"request": request})
    return templates.TemplateResponse("index.html", {"request": request})
@app.get("/login.html", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
@app.get("/signup.html", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})