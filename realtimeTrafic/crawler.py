import requests
from realtimeTrafic.models import ChargeStationStatus, GunStatus
from datetime import datetime


# 从粤易充抓取数据
def readGunStatusListFrom_yyc(stationId, stationCode):
    headers = {
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Referer': 'https://ev.gd.csg.cn/wp/charge.html?stationNo={0}&totalGunNum={1}&notUsedGunNum=9&dcTotalNum={1}&dcNotUsedNum=9'.format(stationCode, totalGunNum)
    }
    data = {
        'stationNo': stationCode,
        'hy_serviceName': 'chargeEquipInfo',
        'channel':2}
    cookie = {
        'Hm_lvt_618d27bb0b9954682270463c1f637561':'1555017354',
        'JSESSIONID': 'FnQVzbDphcKQkcro_19fvzTkOTV4GkzBu0CmcoKF8JEiMfVrGUwM!-500145939',
        'Secure': 'true'
    }

    try:
        r = requests.post('https://ev.gd.csg.cn/serviceInvoke.do', data = data, headers = headers, cookies = cookie, timeout=10)
        # print(r.status_code)
        # print(r.json())
        myObj = r.json()
        if myObj['code'] != 0:
            print('接口调用失败, ', myObj['code'], myObj['message'])
            return None

        gunList = []
        # stationStatus = ChargeStationStatus(stationId = stationId, queryTime = datetime.now(), usedGunCount = 0, fixedGunCount = 0, freeGunCount = 0) 
        # for item in myObj['content']['connectorList']:
        #     aGun = GunStatus(stationId = stationId, queryTime = datetime.now(), gunName = item['equipmentName'], power = int(item['power']), status = int(item['status']))
        #     gunList.append(aGun)
        #     # 只统计快充
        #     if aGun.power < 20:
        #         continue
        #     if aGun.status == 0 or aGun.status == 255:
        #         stationStatus.fixedGunCount = stationStatus.fixedGunCount + 1
        #     elif aGun.status == 1:
        #         stationStatus.freeGunCount = stationStatus.freeGunCount + 1
        #     else:
        #         stationStatus.usedGunCount = stationStatus.usedGunCount + 1

        # result = {
        #     "gunList": gunList,
        #     "status": stationStatus
        # }
        return result

    except Exception as e:
        print(str(e))
        return None