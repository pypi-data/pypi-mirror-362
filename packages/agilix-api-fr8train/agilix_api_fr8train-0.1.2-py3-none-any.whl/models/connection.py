from requests import Session
from urllib.parse import urlencode

class Connection:
    token: str
    session: Session
    base_url: str
    home_domain_id: str

    def __init__(self, token: str = "",
                 base_url: str = "",
                 home_domain_id: str = "",
                 session: Session = Session()):
        self.token = token
        self.base_url = base_url
        self.session = session
        self.home_domain_id = home_domain_id


    def get(self,
            cmd: str,
            params: dict = {}):
        query_string = urlencode({ 'cmd': cmd, '_token': self.token } | params, doseq=True)

        response = self.session.get(f"{self.base_url}?{query_string}")
        response.raise_for_status()

        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} - {response.text}")

        return response.json()

    def post(self,
             cmd: str,
             params: dict = {},
             payload: dict = {}):
        query_string = ""

        if cmd:
            query_string = urlencode({ 'cmd': cmd, '_token': self.token } | params, doseq=True)
        else:
            payload = {'_token': self.token} | payload
            if bool(params):
                query_string = urlencode(params, doseq=True)

        target_url = f"{self.base_url}?{query_string}" if query_string else self.base_url

        # NEED TO DO A POST PAYLOAD WITH THE TOKEN ADDED TO THE REQUESTS OBJECT

        response = self.session.post(target_url, json=payload)
        response.raise_for_status()

        return response.json()