from realtimeTrafic import app, db
from flask import jsonify, request
from sqlalchemy import and_
from datetime import time


@app.route('/getstationtree')
def getStaionTree():
    pass
    # stationList = ChargeStation.query.all()
    # result = {}
    # for station in stationList:
    #     oneStation = {}
    #     oneStation["id"] = station.id
    #     oneStation["name"] = '{}({})'.format(station.stationName, station.gunTotalCount)
    #     if not (station.region in result):
    #         result[station.region] = []
    #     result[station.region].append(oneStation)
    
    # return jsonify(stationList=toArray(result))


@app.route('/querystatus_num', methods=['POST', 'GET'])
def queryStationStatus_ByNum():
    pass
    # data = request.get_json()
    # idList = data["ids"]
    
    # beginTime = data['beginTime']
    # endTime = data['endTime']
    # print(data)

    # result = {}
    # stationList = ChargeStation.query.filter(ChargeStation.id.in_(idList)).all()
    # for station in stationList:
    #     result[station.id] = {"name": station.stationName, "value": []}

    # statusList = ChargeStationStatus.query.filter(and_(ChargeStationStatus.stationId.in_(idList), ChargeStationStatus.queryTime>beginTime, ChargeStationStatus.queryTime < endTime)).all()
    # for item in statusList:
    #     oneStatus = [item.queryTime.strftime("%Y-%m-%d %H:%M"), item.usedGunCount]
    #     result[item.stationId]["value"].append(oneStatus)


    # return jsonify(stationList=result)
