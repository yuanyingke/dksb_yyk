# -*- coding: utf-8 -*-
import requests
import http.client
import random
import time

def get_token():
    token_list = []
    conn = http.client.HTTPSConnection("www.chinastock.com.cn")

    headers = {
        'Host': "www.chinastock.com.cn",
        'Connection': "keep-alive",
        'Accept': "*/*",
        'Access-Control-Request-Method': "POST",
        'Access-Control-Request-Headers': "content-type",
        'Origin': "https://cdns.chinastock.com.cn",
        'User-Agent': "Mozilla/5.0 (Linux; Android 12; Mi 10 Pro Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/107.0.5304.141 Mobile Safari/537.36 XWEB/5023 MMWEBSDK/20230202 MMWEBID/818 MicroMessenger/8.0.33.2320(0x28002151) WeChat/arm64 Weixin NetType/5G Language/zh_CN ABI/arm64",
        'Sec-Fetch-Mode': "cors",
        'X-Requested-With': "com.tencent.mm",
        'Sec-Fetch-Site': "same-site",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://cdns.chinastock.com.cn/",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    try:
        conn.request("OPTIONS", "/h5_gateway/userVerify/outWorker/signinout", headers=headers)
        res = conn.getresponse().headers.items()

        for res_i in res:
            if res_i[0] == 'Set-Cookie':
                token = res_i[1].split(';')[0].split('=')
                token_head = token[0]
                if token_head == 'aliyungf_tc':
                    token_list.append(token[1])
                if token_head == 'acw_tc':
                    token_list.append(token[1])
        
        if len(token_list) < 2 or '' in token_list[:2]:
            print('没有获取到完整的token')
            return None
        print(f"获取到token: {token_list}")
        return token_list
    except Exception as e:
        print(f"获取token失败：{str(e)}")
        return None

def qd(aliyungf_tc, acw_tc, para_list):
    cookie = 'aliyungf_tc=' + aliyungf_tc + '; ' + 'acw_tc=' + acw_tc
    url = "https://www.chinastock.com.cn/h5_gateway/userVerify/outWorker/signinout"

    payload = {
        "phoneNum": para_list[0],
        "name": para_list[1],
        "flag": para_list[2],
        "buildingNum": para_list[3],
        "floorNum": para_list[4],
        "seatNum": para_list[5]
    }
    headers = {
        "Host": "www.chinastock.com.cn",
        "Connection": "keep-alive",
        "Content-Length": "103",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; Mi 10 Pro Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/107.0.5304.141 Mobile Safari/537.36 XWEB/5023 MMWEBSDK/20230202 MMWEBID/818 MicroMessenger/8.0.33.2320(0x28002151) WeChat/arm64 Weixin NetType/5G Language/zh_CN ABI/arm64",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://cdns.chinastock.com.cn",
        "X-Requested-With": "com.tencent.mm",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://cdns.chinastock.com.cn/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": cookie,
        "content-type": "application/json"
    }

    try:
        response = requests.request("POST", url, json=payload, headers=headers)
        print(f"请求返回结果：{response.text}")
        print(f"请求状态码：{response.status_code}")
    except Exception as e:
        print(f"签到/签退请求失败：{str(e)}")

if __name__ == "__main__":
    token = get_token()
    if token is None:
        print("token获取失败，终止执行")
    else:
        para_list = ["15718867696", '范少龙', '2', '6', '6', 'A129']
        qd(token[0], token[1], para_list)