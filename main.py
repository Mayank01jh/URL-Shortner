import json
from fastapi import FastAPI, Header, Depends, HTTPException
from pydantic import BaseModel
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pymongo.mongo_client import MongoClient
from database import urls
from qrcode import qr_code

connection_string = "mongodb+srv://Mayank1234:mayank1234@mydata.ezd5wcv.mongodb.net/"

mongo_db = MongoClient(connection_string)

database = mongo_db.UrlShortner
collection = database.urls

qr_obj = qr_code()
base_url = "https://url-shortner-axwl.onrender.com/"

url_obj = urls(collection)
class addURL(BaseModel):
    special_key: str
    url: str

app = FastAPI()  # http://127.0.0.1:8000/


@app.get("/")  # http://127.0.0.1:8000/docs
async def hello():
    return "Hello World"


#@app.get("/hello")  # http://127.0.0.1:8000/hello
#async def new():
#    return RedirectResponse("https://9ai.in", status_code=302)

@app.get("/{specialkey}")#http://127.0.0.1:8000/hello
async def new(specialkey:str):
    url = url_obj.fetch_url(specialkey)
    return RedirectResponse(url, status_code=302)


    #if specialkey == "hi":
    #    return RedirectResponse("https://9ai.in",status_code=302)
    #elif specialkey == "hello":
    #    return RedirectResponse("https://www.google.com",status_code=302)
    #else:
    #    return RedirectResponse("http://127.0.0.1:8000/",status_code=302)
    
#http://127.0.0.1:8000/9ai

@app.post("/addURL")
async def addurl(json: addURL):
    insert = url_obj.insert_url(json.url,json.special_key)
    if insert:
        return{"shprtened URL": base_url + json.special_key}
    return {"Shortening of URL": insert}

@app.get("/count/{specialkey}")
async def count_click(specialkey:str):
    return url_obj.count(specialkey)

@app.get("/qrcode/{specialkey}")
async def make_qr(specialkey:str):
    qr_obj.make_qr(base_url + specialkey , specialkey)
    return FileResponse(specialkey + ".png")
