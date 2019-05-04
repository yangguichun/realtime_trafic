import requests
from realtimeTrafic.models import DrivePath, Traffic
from datetime import datetime


# 从百度地图上读取指定路径的路径规划
def readTrafficFromBaidu(path):
    headers = {
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    params = {
        'origin': path.origin,
        'destination': path.dest,
        'alternatives': 1,
        'ak':'OYQbSTxotG4vWIu7Gtzx7GdK3btn1hyB'
    }

    try:
        r = requests.get('http://api.map.baidu.com/direction/v2/driving', headers = headers, params = params, timeout=10)
        # print(r.status_code)
        # print(r.json())
        resp = r.json()
        if resp['status'] != 0:
            print('接口调用失败, ', resp['status'], resp['message'])
            return None
        
        # 默认的距离给10万公里
        rtPath = Traffic(pathId = path.id, queryTime = datetime.now(), distance = 100000000)
        
        for route in resp['result']['routes']:
            dist = float(route['distance'])
            if rtPath.distance > dist:
                rtPath.distance = float(route['distance'])
                rtPath.duration = float(route['duration'])
        return rtPath

    except Exception as e:
        print(str(e))
        return None