import base64
import json
import requests
from urllib.parse import quote

class Codicent:
    def __init__(self, token, signalr_host=None, base_url=None, verify_https=True):
        self.token = token
        self.signalr_host = signalr_host
        self.base_url = base_url if base_url is not None else "https://codicent.com/"
        self.verify_https = verify_https

    def init(self):
        # No-op, initialization is done in the constructor
        pass

    def upload(self, file):
        url = f"{self.base_url}app/upload"
        files = {"file": file}
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(url, files=files, headers=headers, verify=self.verify_https)
        return response.json()["id"]

    def post_message(self, message, parent_id=None, type="info"):
        url = f"{self.base_url}app/AddChatMessage"
        data = {"content": message, "type": type, "isNew": False }
        if parent_id:
            data["parentId"] = parent_id
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        response = requests.post(url, json=data, headers=headers, verify=self.verify_https)
        return response.json()["id"]

    def _get_messages_deprecated(self, start=0, length=10, search="", after_timestamp=None, before_timestamp=None):
        url = f"{self.base_url}app/GetChatMessages"
        params = {"start": start, "length": length, "search": search}
        if after_timestamp:
            params["afterTimestamp"] = after_timestamp.isoformat()
        if before_timestamp:
            params["beforeTimestamp"] = before_timestamp.isoformat()
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, params=params, headers=headers, verify=self.verify_https)
        return response.json()
    
    def get_messages(self, start=0, length=10, tags=[], search="", after_timestamp=None, before_timestamp=None, no_tags=None):
        url = f"{self.base_url}api/GetMessages"
        params = {"start": start, "length": length, "search": search, "tags": tags}
        if after_timestamp:
            params["afterTimestamp"] = after_timestamp.isoformat()
        if before_timestamp:
            params["beforeTimestamp"] = before_timestamp.isoformat()
        if no_tags:
            params["noTags"] = no_tags
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(url, json=params, headers=headers, verify=self.verify_https)
        return response.json()
    
    def get_chat_reply(self, message):
        url = f"{self.base_url}api/GetChatReply2?message={quote(message)}"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers, verify=self.verify_https)
        return response.text, 

    def post_chat_reply(self, message, conversation_id=None):
        url = f"{self.base_url}app/GetAi2ChatReply"

        # extract project property from jwt token in this.token
        payload = self.token.split(".")[1]
        # Add padding if necessary
        payload += '=' * (-len(payload) % 4)
        decoded_payload = base64.urlsafe_b64decode(payload).decode('utf-8')
        jwt_token = json.loads(decoded_payload)
        codicent = jwt_token["project"]

        data = {"message": message, "project": codicent}
        if conversation_id:
            data["messageId"] = conversation_id
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        response = requests.post(url, json=data, headers=headers, verify=self.verify_https)
        message = response.json()
        return {"id": message["id"], "content": message["content"].replace("@" + codicent, "").strip()}
    
# Test...
# import os
# c = Codicent(os.getenv("CODICENT_TOKEN"))
# reply = c.post_chat_reply("Hello, my name is Johan")
# print(reply["content"])
# reply = c.post_chat_reply("What is my name?", reply["id"])
# print(reply["content"])