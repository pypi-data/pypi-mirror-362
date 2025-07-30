
import base64, json
import requests
from django.conf import settings


LOG_TYPE_GEN = "GEN"
LOG_TYPE_API = "API"
LOG_TYPE_IAM = "IAM"

LOG_TYPE_KEY = "xan"


class LoggingCommand:
    
    def __init__(self) -> None:
        user = settings.OPENOBSERVER_USER
        password = settings.OPENOBSERVER_PASSWORD
        self._bas64encoded_creds = base64.b64encode(bytes(user + ":" + password, "utf-8")).decode("utf-8")

        
    def send(self, stream: str, data: dict) -> requests.Response:
        headers = {"Content-type": "application/json", "Authorization": "Basic " + self._bas64encoded_creds}
        org = settings.OPENOBSERVER_ORGANIZATION
        stream = str(data[stream]).lower()
        openobserve_host = settings.OPENOBSERVER_HOST
        openobserve_url = openobserve_host + "/api/" + org + "/" + stream + "/_json"

        res = requests.post(openobserve_url, headers=headers, data=json.dumps(data))
        return res
       