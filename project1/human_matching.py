from lib2to3.pgen2 import token
import os
import json
import base64
import requests
import numpy as np

def get_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=HLeB6tlQqrnzZO6le9m2qz8T&client_secret=VaOCT9NvEkW9vxYfudDmWFaGu48B8fxQ'
    response = requests.get(host)
    access_token = response.json()['access_token']
    return access_token

def get_match(input_img):
    # input: 捕捉到的的現場圖片路徑
    access_token = get_token()
    _codes, scores = [], []
    usrs = os.listdir('./usr')
    for usr in usrs:
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"
        f = open(os.path.join('./usr', usr), 'rb')
        f2 = open(input_img, 'rb')

        raw_face = str(base64.b64encode(f.read()), 'utf-8')
        input_face = str(base64.b64encode(f2.read()), 'utf-8')

        params = [{'image': raw_face,
                    'image_type': 'BASE64',
                    'face_type': 'LIVE',
                    'quality_control': 'LOW',
                    'liveness_control': 'NORMAL'
                },
                {'image': input_face,
                    'image_type': 'BASE64',
                    'face_type': 'LIVE',
                    'quality_control': 'LOW',
                    'liveness_control': 'NORMAL'
                }]

        params = json.dumps(params, ensure_ascii=False)
        params = json.loads(params)
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, json=params, headers=headers)
        if response:
            response = response.json()
            _code = response['error_code']
            _codes.append(_code)
            if _code != 0:
                continue
            res = response['result']
            scores.append(res['score'])
    if scores == []:
        return 'API ERROR', str(_codes)

    match_res = np.argsort(np.array(scores))
    tmp = scores[match_res[-1]]
    if scores[match_res[-1]] >= 75.:
        return 'Success', usrs[match_res[0]].split('.')[0]
    else:
        return 'No Match', -1

if __name__ == '__main__':
    msg, usr_token = get_match('./__cache__/input1.jpg')
    print()

