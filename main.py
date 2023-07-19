import requests
import json
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

def get_current_weather(ip):
    url =  "http://api.weatherapi.com/v1/current.json"
    par = {
        "key" : "08b6a02118ec4f68a52213450231107",
        "q"  :   f"{ip}"
    }
    result = requests.get(url=url,params=par)
    print(result.text)
    result_json = json.loads(result.text)
    current_weather = result_json["current"]
    print(current_weather)
    return current_weather

# template_str = """
# Current Weather:
# Temperature: {{ current.temp_c }}°C
# Feels Like: {{ current.feelslike_c }}°C
# Weather Condition: {{ current.condition.text }}
# """
# template = result(template_str)
# rendered_template = template.render(current=result_json["current"])
# print(rendered_template)
app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})

@app.post('/', response_class=HTMLResponse)
async def root(request: Request, mytxtinput: str = Form(...)):
    current_weather = get_current_weather(mytxtinput)
    locaion = ["mytxtinput"]
    is_day = current_weather["is_day"]
    temp_c = current_weather["temp_c"]
    temp_f = current_weather["temp_f"]
    last_updated = current_weather["last_updated"]
    return templates.TemplateResponse('index1.html', {"request": request, "Location": mytxtinput, "last_update": last_updated, "temp_c":temp_c,"temp_f":temp_f,"is_day":is_day})