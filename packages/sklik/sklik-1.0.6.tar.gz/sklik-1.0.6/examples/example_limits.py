import os

from dotenv import load_dotenv

import sklik

load_dotenv()

token = os.getenv("SKLIK_TOKEN")
sklik.SklikApi.init(token)

response = sklik.call("api", "limits")["batchCallLimits"]
print(response)
