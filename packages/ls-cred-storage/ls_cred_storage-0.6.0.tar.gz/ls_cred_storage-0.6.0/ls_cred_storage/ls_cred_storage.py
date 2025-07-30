
import keyring
import time
import json
import os


class LSCredStorage():
    USER_KEY = 'userToken'
    TIMESTAMP_KEY = 'timestamp'
    USER_ID_KEY = 'userId'
    SESSION_TOKEN_KEY = 'sessionToken'
    ACCESS_TOKEN_KEY = 'accessToken'
    MAX_TOKEN_RETENTION_TIME_SECS = 3500
    APP_SERVICE_NAME = 'LightSolverClient'
    CHUNK_SIZE = 1000  # max bytes per chunk


    def __init__(self,token = None):
        self.currentTokenDic = token

    def is_cached_user(self, userName):
        return self.currentTokenDic[self.USER_KEY] == userName

    def update_current_token(self,token):
        self.currentTokenDic = token

    def store_token(self, username, token):
        self.update_current_token(token)
        if os.name == "nt":
            # Serialize token
            data = json.dumps(token)
            # Split into chunks
            chunks = [data[i:i+self.CHUNK_SIZE] for i in range(0, len(data), self.CHUNK_SIZE)]
            total = len(chunks)
            chunk_keys = []
            for idx, chunk in enumerate(chunks):
                key = f"{username}_{idx+1}_{total}"
                keyring.set_password(self.APP_SERVICE_NAME, key, chunk)
                chunk_keys.append(key)
            # Store index as json list
            keyring.set_password(self.APP_SERVICE_NAME, username, json.dumps(chunk_keys))
            return
        # fallback: file
        with open("tokens.data", "w") as f:
            f.write(json.dumps(token))

    def remove_token(self, username):
        if os.name == "nt":
            # Remove all chunked keys
            index = keyring.get_password(self.APP_SERVICE_NAME, username)
            if not index:
                return
            chunk_keys = json.loads(index)
            for key in chunk_keys:
                keyring.delete_password(self.APP_SERVICE_NAME, key)
            keyring.delete_password(self.APP_SERVICE_NAME, username)
            return
        raise Exception("Removing cached tokens is not supported for this OS.")

    def get_stored_token(self, username):
        if os.name == "nt":
            index = keyring.get_password(self.APP_SERVICE_NAME, username)
            if not index:
                return None
            chunk_keys = json.loads(index)
            # Reassemble chunks
            chunks = []
            for key in chunk_keys:
                chunk = keyring.get_password(self.APP_SERVICE_NAME, key)
                if chunk is None:
                    return None
                chunks.append(chunk)
            data = ''.join(chunks)
            token = json.loads(data.replace("'", '"'))
            self.update_current_token(token)
            return token
        # fallback: file
        filename = f"tokens.data"
        if not os.path.isfile(filename):
            return None
        with open(filename, "r") as f:
            data = f.readline()
            token =  json.loads(data.replace("'", '"'))
            if token[self.USER_KEY] == username:
                self.update_current_token(token)
                return token
            return None


    def is_token_valid(self):
        if self.currentTokenDic != None:
          return time.time() - self.currentTokenDic[self.TIMESTAMP_KEY] < self.MAX_TOKEN_RETENTION_TIME_SECS
        return False
