import requests
import json
from fastapi import FastAPI
import sched, time
import threading    


client_id =  "05xrp9ocuea41axl"
client_secret = "MiI00fTz"

app = FastAPI()
token = ""



class BackgroundTasks(threading.Thread):
    def run(self,*args,**kwargs):
        global token
        while True:
            token = get_access_token(client_id=client_id, client_secret=client_secret)
            time.sleep(3000)

@app.on_event("startup")
async def startup_event():
    global token
    token = get_access_token(client_id=client_id, client_secret=client_secret)
    t = BackgroundTasks()
    t.start()


def get_access_token(client_id, client_secret):
    """
    Generate a access token with the help of client id and client secret
    """
    
    url = "https://auth.emsicloud.com/connect/token"
    payload = f"client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials&scope=emsi_open"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.request("POST", url, data=payload, headers=headers)

    return json.loads(response.text)['access_token']

def get_skills(JD, token):
    """
    Get the skills fromt he Job description
    """
    skills = []
    url = "https://emsiservices.com/skills/versions/latest/extract/trace"
    querystring = {"language":"en"}

    payload = {"text": JD}
    payload = json.dumps(payload)

    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': "application/json"
        }
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    try:
        for i in json.loads(response.text)['data']['skills']:
            if i['confidence'] > 0.90:
                skills.append(i['skill']['name'])
    except Exception as e:
        return {"error" : e}
    return {"skills":skills}




@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/extract-skills/{jd}")
def read_item(jd: str):
    global token
    print(token)
    return get_skills(jd, token)