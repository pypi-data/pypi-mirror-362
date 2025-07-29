import os
import json
import time
import httpx

class KandinskyAPI:
    def __init__(self):
        self.URL = "https://api-key.fusionbrain.ai/"
        self.api_key = os.getenv("KANDINSKY_API_KEY")
        self.secret_key = os.getenv("KANDINSKY_SECRET_KEY")
        if not self.api_key or not self.secret_key:
            raise ValueError("KANDINSKY_API_KEY и/или KANDINSKY_SECRET_KEY не заданы в окружении")
        self.AUTH_HEADERS = {
            'X-Key': f'Key {self.api_key}',
            'X-Secret': f'Secret {self.secret_key}',
        }
        self._pipeline_id = None

    def get_pipeline(self):
        if self._pipeline_id:
            return self._pipeline_id
        resp = httpx.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        resp.raise_for_status()
        data = resp.json()
        self._pipeline_id = data[0]['id']
        return self._pipeline_id

    def generate(self, prompt, width=1024, height=1024, style="DEFAULT", negative_prompt=""):
        pipeline = self.get_pipeline()
        params = {
            "type": "GENERATE",
            "style": style,
            "width": width,
            "height": height,
            "numImages": 1,
            "generateParams": {
                "query": prompt
            }
        }
        if negative_prompt:
            params["negativePromptDecoder"] = negative_prompt
        data = {
            'pipeline_id': (None, pipeline),
            'params': (None, json.dumps(params), 'application/json')
        }
        resp = httpx.post(self.URL + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        resp.raise_for_status()
        uuid = resp.json()['uuid']
        return uuid

    def check_generation(self, request_id, attempts=10, delay=5):
        while attempts > 0:
            resp = httpx.get(self.URL + f'key/api/v1/pipeline/status/{request_id}', headers=self.AUTH_HEADERS)
            resp.raise_for_status()
            data = resp.json()
            if data['status'] == 'DONE':
                return data['result']['files']
            elif data['status'] == 'FAIL':
                raise RuntimeError(f"Kandinsky generation failed: {data.get('errorDescription', 'Unknown error')}")
            attempts -= 1
            time.sleep(delay)
        raise TimeoutError("Kandinsky generation timed out")

    def generate_and_get_image(self, prompt, width=1024, height=1024, style="DEFAULT", negative_prompt=""):
        uuid = self.generate(prompt, width, height, style, negative_prompt)
        files = self.check_generation(uuid)
        return files 