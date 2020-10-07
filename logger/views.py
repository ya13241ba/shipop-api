from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bson.json_util import dumps

from pymongo import MongoClient, DESCENDING

SHIPOP_COLLECTIONS = [
"log_produce_result",
"log_event_result",
"log_answer_result",
"log_select_panel",
]

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
# Create your views here.

def getRawLog(request):
    response = JsonResponse({})
    
    # DB接続
    con = MongoClient("mongodb://127.0.0.1:27017")
    db = con.shipop
    
    # パラメータ展開
    collectname = request.GET.get(key="collectname")
    lessonIdolId = request.GET.get(key="idol")
    if not collectname or not lessonIdolId:
        return HttpResponseBadRequest()
    descFlag = request.GET.get(key="desc", default="0")

    result = {}
    if collectname in SHIPOP_COLLECTIONS:
        sort = None
        if descFlag == "1":
            sort = [("shipopUpdateTime", DESCENDING)]
        result = db[collectname].find(filter={"shipopLessonIdolId" : str(lessonIdolId)}, projection={'_id': False}, sort=sort)
    else:
        return HttpResponseBadRequest()

    response = JsonResponse(list(result), safe=False)
    response['Access-Control-Allow-Headers'] = "Content-Type, Accept, Access-Control-Allow-Origin"
    response['Access-Control-Allow-Methods'] = "GET"
    response['Access-Control-Allow-Origin'] = '*'
    return response

@csrf_exempt
def addRawLog(request):
    if request.method == 'GET':
        return JsonResponse({"response":"GET"})

    response = HttpResponse()
    response['Access-Control-Allow-Headers'] = "Content-Type, Accept, Access-Control-Allow-Origin"
    response['Access-Control-Allow-Methods'] = "POST, OPTIONS"
    response['Access-Control-Allow-Origin'] = '*'
    if request.method == 'OPTIONS':
        return response

    # DB接続
    con = MongoClient("mongodb://127.0.0.1:27017")
    db = con.shipop

    # リクエストパラメータ展開
    datas = json.loads(request.body) 

    result = None
    if datas["shipopLogTYpe"] == "ProduceResult":
        # ProduceResult
        result = db.log_produce_result.insert_one(datas)
    elif datas["shipopLogTYpe"] == "EventResult":
        # EventResult
        result = db.log_event_result.insert_one(datas)
    elif datas["shipopLogTYpe"] == "AnswerResult":
        # AnswerResult
        result = db.log_answer_result.insert_one(datas)
    elif datas["shipopLogTYpe"] == "SelectPanel":
        # SelectPanel
        result = db.log_select_panel.insert_one(datas)
    
    if result and result.inserted_id:
        print(" > insert success : [" + datas["shipopLogTYpe"] + "] " + str(result.inserted_id))
    else:
        print(" > insert failure")

    return response