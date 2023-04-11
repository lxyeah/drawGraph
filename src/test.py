import json
import os

import numpy as np
import pandas as pd

# l = [[1, 2, 7], [3, 4, 8], [5, 6, 9], [1, 10, 11]]
# p = pd.DataFrame(l).groupby([0, 1]).count()
# print(p)
# print(type(p))
# print("=========")
# print(p.index.tolist())
# print(p.at[(1, 11), 2])
# print(os.system("sleep 3s") == 0)
# # print(os.popen("ls"))
# print((3216+4878)*2.68)
# print((3216+5393)*2.5)
import requests

from src.const.WebConst import ALUrl

projName = "commons-bcel"
turnNum = "3"
post_url = ALUrl + "/turn/search"
bodys = {"projName": projName, "turn": turnNum}
res = requests.get(url=post_url, params=bodys)
# res = requests.get(url="http://localhost:8081/turn/search", params={"projName": "commons-bcel", "turn": "3"})
text = json.loads(res.text)
res.close()
print(text[0])
