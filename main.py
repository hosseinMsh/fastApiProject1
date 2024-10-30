from datetime import datetime
from fastapi import FastAPI, Form, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Initialize FastAPI app
app = FastAPI()

# Setup templates
templates = Jinja2Templates(directory="templates")

# In-memory storage for demonstration purposes
data_storage = []
users = {
    "user1": "password1",
    "user2": "password2"
}
current_user = None


@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})

@app.get("/forget", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "data": data_storage})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    global current_user
    if username in users and users[username] == password:
        current_user = username  # Set the current user
        return templates.TemplateResponse("home.html", {"request": request})
    else:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid username or password"
        })

@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    if current_user:
        return templates.TemplateResponse("home.html", {"request": request})
    else:
        raise HTTPException(status_code=403, detail="Not authorized")

@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    global current_user
    current_user = None  # Clear the current user
    return templates.TemplateResponse("landing.html", {"request": request})
@app.get("/view-repo")
async def view_repo(request: Request, period: str):
    # Here you can implement logic to view the repository based on the period
    return f"Viewing repository for the {period}."

# Other routes...
@app.post("/add-event")

async def add_data(request: Request):
    from sabtFaramoshi import addDataToDb
    data = await request.json()
    name = data.get('name')
    job_id = data.get('job_id')
    time_event = data.get('time_event')
    type_event = data.get('type')
    door_id = data.get('door_id')

    # Parse the datetime string to extract date and time
    datetime_obj = datetime.fromisoformat(time_event)
    day = datetime_obj.date()
    time = datetime_obj.time()
    registration_type = 'manual'
    # Call addDataToDb with all required parameters
    insertion_made = addDataToDb(name, job_id, day, time, type_event, door_id, registration_type)

    if insertion_made:
        return {"message": "Data added successfully"}
    else:
        return {"message": "Data already exists or an error occurred"}

@app.get("/get-event")
async def get_data(request: Request):
    from getDataFromServer import getDataFromServer
    getDataFromServer()
    return 0

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)