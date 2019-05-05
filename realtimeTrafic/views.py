from realtimeTrafic import app, db
from realtimeTrafic.models import DrivePath, Traffic
from flask import jsonify, request, render_template
from sqlalchemy import and_
from datetime import time



def toArray(aDict):
    aList = list(map(lambda item: {'id': None, 'name': item}, list(aDict.keys())))
    for item in aList:
        item['children'] = aDict[item['name']]
    return aList

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/getpathtree')
def getPathTree():
    paths = DrivePath.query.all()
    result = {}
    for path in paths:
        onePath = {}
        onePath["id"] = path.id
        onePath["name"] = path.name
        if not (path.subType in result):
            result[path.subType] = []
        result[path.subType].append(onePath)
    
    return jsonify(pathList=toArray(result))


@app.route('/querytraffic', methods=['POST', 'GET'])
def queryTraffic():
    data = request.get_json()
    idList = data["ids"]
    
    beginTime = data['beginTime']
    endTime = data['endTime']
    print(data)


    result = {}
    pathes = DrivePath.query.filter(DrivePath.id.in_(idList)).all()
    for path in pathes:
        result[path.id] = {"name": path.name, "value": []}

    traffics = Traffic.query.filter(and_(Traffic.pathId.in_(idList), Traffic.queryTime>beginTime, Traffic.queryTime < endTime)).all()
    for item in traffics:
        traffic = [item.queryTime.strftime("%Y-%m-%d %H:%M"), round(item.duration/60.0,1)]
        result[item.pathId]["value"].append(traffic)


    return jsonify(stationList=result)
