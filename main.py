from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime


# Initialize FastAPI app
app = FastAPI()

# Setup templates
templates = Jinja2Templates(directory="templates")

# In-memory storage for demonstration purposes
data_storage = []

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "data": data_storage})


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
