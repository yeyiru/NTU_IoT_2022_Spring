import http.server as SimpleHTTPServer
import pandas as pd
import socketserver
import base64
import json
import time

def base2jpg(data, mode):
    image_data = base64.b64decode(data)
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    if 'success' not in mode:
        file = open(f"./error_img/{t}.jpg", 'wb')
        file.write(image_data)
        file.close()
    else:
        file = open(f"./success_img/{t}.jpg", 'wb')
        file.write(image_data)
        file.close()
    return t

class myHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    # def get_heading(self, pano_id, h_id):
    #     df = pd.read_csv('./2021_04_21_full.csv')
    #     row = df[df['pano_id'] == pano_id]
    #     heading = str(row[f'HEADING{h_id}'].iloc[0])
    #     return heading

    def do_GET(self):
        self.post = self.path[1:].replace('%20', ' ')
        j_post = json.loads(self.post)
        t = base2jpg(j_post['image'], j_post['mode'])

        print('-'*50)
        print(f'Saved to {t}!')
        print('-'*50)
        df = pd.read_csv('./log/root.csv')
        df = df.append({'time': t,
                        'machine': 1,
                        'log': j_post['mode']}, ignore_index=True)
        df.to_csv('./log/root.csv', index=0)
        # pano_id, h_id = self.path[1:].split('$')[:2]
        # heading = self.get_heading(pano_id, h_id)
        self.send_response(200)
        self.end_headers()

PORT = 8001
handler = socketserver.TCPServer(("", PORT), myHandler)
print(f"serving at port {PORT}")
handler.serve_forever()

# import base64
# import socket
# import threading
# import os, time
# from loguru import logger
# from io import BytesIO
# import socketserver
# import json, types, string
# from PIL import Image
 
# ip_port = ("0.0.0.0", 8001)
 
 
# class Model:
#     network: int
#     class_names: list
#     class_colors: dict
 
 
# def base2jpg(data):
#     image_data = base64.b64decode(data)
#     file = open("./app/test_img/0.jpg", 'wb')
#     file.write(image_data)
#     file.close()
#     i = Image.open('./app/test_img/0.jpg')
#     return i

# class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
#     def handle(self):
#         print('accept new connection from %s:%s...' % self.client_address)
#         data1 = self.request.recv(1310720)
#         data2 = self.request.recv(1310720)
#         data = data1 + data2
#         print(data)
#         jdata = json.loads(data1)
#         print(jdata)
#         method = jdata[0]['method']
#         global res_bytes
#         if method == 'post':
#             res_bytes = post(jdata)
#             self.request.sendall(b'200ok')
#             print(res_bytes)
#         elif method == 'get':
#             time.sleep(10)
#             self.request.sendall(res_bytes)
#             print("succeed send:", res_bytes)
 
 
# def post(jdata):
#     token = jdata[0]['token']
#     image_name = jdata[0]['imgtype']
#     model = jdata[0]['model']
#     data = jdata[0]['data']
#     if token != 'bonccvlab':
#         logger.error('400--token验证失败！，token值为{}'.format(token))
#         # raise HTTPException(status_code=400, detail="token验证失败！")
#         res = {'success': 400, 'message': "token验证失败", "flag": None, "icon": ""}
#         return res
 
#     if not image_name.endswith('jpg') and not image_name.endswith('png'):
#         logger.error('400--请求字段imgtype有误')
#         # raise HTTPException(status_code=400, detail="imgtype数据传输有误！")
#         res = {'success': 400, 'message': "图片后缀名不是.jpg或者.png结尾", "flag": None, "icon": ""}
#         return res
 
#     da = str(data)
#     i = base2jpg(da)
#     i.save(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}.jpg')
 
# def get(connect, res_bytes):
#     connect.sendall(res_bytes)
#     print("succeed send:", res_bytes)
 
 
# class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
#     pass
 
 
# if __name__ == "__main__":
#     s = socketserver.ThreadingTCPServer(ip_port, ThreadedTCPRequestHandler)
#     s.serve_forever()