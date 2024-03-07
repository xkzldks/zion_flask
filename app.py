#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import json
import time
import os
import account
from random import *
from flask import Flask, url_for, render_template, request, redirect, session, jsonify, flash, send_file
from datetime import datetime
import model2
from model2 import db
from bson.objectid import ObjectId
# import music
import chulseck
import smtplib
from email.message import EmailMessage

now = datetime.now()
app = Flask(__name__)
# account app import
app.register_blueprint(account.blue_account)
app.secret_key = model2.appSecret
# 파일 업로드 위치
app.config['UPLOAD_FOLDER'] = 'static/upload/'

user_ip = request.remote_addr


@app.route('/kakao')
def kakao():
    print('ip - ',user_ip)
    return render_template('kaka.html')


@app.route('/indexC')
def indexC():
    print('ip - ',user_ip)
    return render_template('indexC.html')


@app.route('/kakao2')
def kakao2():
    print('ip - ',user_ip)
    return render_template('kaka2.html')


# H T M L을 주는 부분
@app.route('/')
def home():
    print('ip - ',user_ip)
    print('##home##')
    return render_template('index.html')

@app.route('/notitest')
def notitest():
    print('ip - ',user_ip)
    print('##notitest##')
    return render_template('notitest.html')


@app.route('/development')
def development():
    print('ip - ',user_ip)
    print('##development##')
    return render_template('development.html')


@app.route('/missions')
def missions():
    print('ip - ',user_ip)
    print('##missions##')
    return render_template('missions.html')


@app.route('/checkq')
def checkq():
    print('/print("##checkQ사이트##")')
    return render_template('checkq.html')


@app.route('/check')
def check():
    print('ip - ',user_ip)
    print("##check사이트##")
    print('/check')
    return render_template('check.html')




@app.route('/mission')
def mission():
    print('ip - ',user_ip)
    print("##mission##")
    peopleList = list(db.peopleList.find({}, {'_id': False}))
    global missionList
    missionList = []
    for _ in peopleList:
        if _['선교헌금'][0] != 0:
            missionList.append(_)
    chulseck.bubble_sort(missionList)
    print(missionList)
    c = list(db.mission.find({}, {'_id': False}))
    result = ''
    for i in c:
        for _ in i['헌금']:
            result += i['이름']+_+' '
    print(result)
    return jsonify({"all_reviews": missionList, "mM": result})


# def ageInt():
#     for _ in missionList:
#         doc = {
#             '이름': _['이름'],
#             '1월': 0,
#             '2월': 0,
#             '3월': 0,
#             '4월': 0,
#             '5월': 0,
#             '6월': 0,
#             '7월': 0,
#             '8월': 0,
#             '9월': 0,
#             '10월': 0,
#             '11월': 0,
#             '12월': 0
#         }
#         db.mission.insert_one(doc)

@app.route('/missionM', methods=["POST"])
def missionM():
    print('ip - ',user_ip)
    print("##missionM")
    print(request.form['mis'])
    a = request.form['mis'].strip().split(' ')
    print(a)

    m = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월']
    mList = []
    tName = ''
    cache = ''
    for el in range(len(a) - 1, -1, -1):
        if a[el] not in m:
            mList.append(a[el] + cache)
            cache = ''
        else:
            cache += " " + a[el]
        # print("이번 값 : ", a[el], ", cache: ", cache, cache == '', ", 리스트 : ", mList)

    for i in range(len(mList) - 1, -1, -1):
        b = mList[i].strip().split(' ')
        if len(mList[i]) != 3:
            print(b[0], b[1:])
            c = list(db.mission.find({'이름': b[0]}, {'id': False}))
            print(c)
            doc = {
                    '이름': b[0],
                    '헌금': b[1:]
                }
            if not c:
                db.mission.insert_one(doc)
            else:
                db.mission.update_one({'이름': b[0]}, {"$set": {'헌금': b[1:]}})
        else:
            db.mission.update_one({'이름': b[0]}, {"$set": {'헌금': ''}})
    return jsonify({"msg": '변경성공'})


@app.route('/dateLoad', methods=['GET'])
def dateLoad():
    print('ip - ',user_ip)
    print('/dateLoad')
    dayLoad = list(db.graphDate.find({}, {'_id': False}))
    print(dayLoad)
    return jsonify({'startDay': dayLoad[0]['startDay'], 'endDay': dayLoad[0]['endDay'], 'weekCompare': dayLoad[0]['weekCompare']})


@app.route('/dateSave', methods=["POST"])
def dateSave():
    print('ip - ',user_ip)
    print("/dateSave")
    startDay, endDay = request.form['from'], request.form['to']
    print(startDay, endDay)
    f = startDay.replace('-', '')
    e = endDay.replace('-', '')
    print(int(e[0:4]), int(f[0:4]))
    if int(e[0:4]) == int(f[0:4]):
        print(datetime(int(f[0:4]), int(f[4:6]), int(f[6:8])).isocalendar()[1], datetime(int(e[0:4]), int(e[4:6]), int(e[6:8])).isocalendar()[1])
        weekCompare = abs(datetime(int(e[0:4]), int(e[4:6]), int(e[6:8])).isocalendar()[1] - datetime(int(f[0:4]), int(f[4:6]), int(f[6:8])).isocalendar()[1])
        db.graphDate.update_one({'d': 'd'}, {"$set": {'startDay': startDay, 'endDay': endDay, 'weekCompare': weekCompare}})
        return jsonify({"msg": "날짜범위 " + startDay + ' ~ ' + endDay})
    else:
        w1 = datetime(int(e[0:4]), int(e[4:6]), int(e[6:8])).isocalendar()[1]
        wc = datetime(int(f[0:4]), 12, 31).isocalendar()[1]
        w2 = datetime(int(f[0:4]), int(f[4:6]), int(f[6:8])).isocalendar()[1]
        weekCompare = wc - w2 + w1 + 1
        db.graphDate.update_one({'d': 'd'}, {"$set": {'startDay': startDay, 'endDay': endDay, 'weekCompare': weekCompare}})
        return jsonify({"msg": "날짜범위 " + startDay + ' ~ ' + endDay})


@app.route('/dbReset', methods=["POST"])
def dbReset():
    print('ip - ',user_ip)
    print('/dbReset')
    userAuthCheck = list(db.user.find({'username': session.get("username")}, {'_id': False}))
    if not session.get("username"):
        return jsonify({"False": "False"})
    elif userAuthCheck[0]['auth'] != 1:
        return jsonify({"False": "Auth"})
    else:
        autoSave()
        reviews = list(db.chulseck.find({}, {'_id': False})) # 191 ~ 194 날짜 데이터 뽑아내기
        dateList = []
        for i in reviews:
            dateList.append(i['title'])

        dbRemain = request.form['dbRemain'].strip().split(' ') # 유저가 설정한 날짜데이터 받아오기
        dbBackup = []

        if not dbRemain: #dbRemain이 빈칸일 경우
            db.chulseck.drop()
            db.create_collection("chulseck")
        else:            
            for i in range(len(dbRemain) - 1, 0, 1):
                for j in range(i):
                    if dbRemain[j] > dbRemain[j + 1]:
                        dbRemain[j], dbRemain[j + 1] = dbRemain[j + 1], dbRemain[j]
                        
            for i in dbRemain:
                if str(i) in dateList:
                    dbBackup.insert(0, list(db.chulseck.find({"title": str(i)})))
                    print(list(db.chulseck.find({"title": str(i)})))
            print(dbBackup)
            db.chulseck.drop()
            db.create_collection("chulseck")
            for i in dbBackup:
                db.chulseck.insert_one(i[0])
    return jsonify({"msg":"출석명단 삭제완료!!"})


# @app.route('/resetM', methods=["GET"])
# def resetM():
#     print('resetM')
#     userAuthCheck = list(db.user.find({'username': session.get("username")}, {'_id': False}))
#     if not session.get("username"):
#         return jsonify({"False": "False"})
#     elif userAuthCheck[0]['auth'] != 1:
#         return jsonify({"False": "Auth"})
#     db.mission.drop()
#     return jsonify({"msg":"삭제성공"})

# @app.route('missionGet', method=["GET"])
# def missionGet():
#     print("/missionGet")
#     reviews = list(db.chulseck.find({}, {'_id': False}))
#     re = []
#     for _ in range(len(reviews) - 1, -1, -1):
#         re.append(reviews[_])
#     return jsonify({'all_reviews': re})


@app.route('/missionSave', methods=["POST"])
def missionSave():
    print("##missionSave##")
    userAuthCheck = list(db.user.find({'username': session.get("username")}, {'_id': False}))
    if not session.get("username"):
        return jsonify({"False": "False"})
    elif userAuthCheck[0]['auth'] != 1:
        return jsonify({"False": "Auth"})
    name = request.form['name']
    mission = int(request.form['info'])
    db.peopleList.update_one({'이름': name}, {"$set": {'선교헌금': [mission]}})
    return jsonify({'msg': '변경성공'})



@app.route('/getInfo', methods=["POST"])
def info():
    print("##info##")
    url = request.form['url']
    yt = music.info(url)
    print("title : ", yt.title)
    print("length : ", yt.length)
    print("author : ", yt.author)
    print("publish_date : ", yt.publish_date)
    print("views : ", yt.views)
    # print("keywords : ", yt.keywords)
    # print("description : ", yt.description)
    # print("thumbnail_url : ", yt.thumbnail_url)
    return jsonify({'msg': yt.title})


@app.route('/downList', methods=["POST"])
def convert():
    print('/downList')
    url = request.form['url']
    mp = request.form['v']
    yt = music.cvt(url, mp)
    print(yt)
    if isinstance(yt, list):
        for i in yt:
            return send_file('/download/'+ i, as_attachment=True)
    else:
        return send_file('/download/' + yt, as_attachment=True)


@app.route('/chulCheck', methods=['POST'])
def chulCheck():
    print("##출석날짜존재확인##")
    print("/chulCheck")
    title_receive = request.form['title_give']
    print(title_receive)
    i = list(db.chulseck.find({'title': title_receive}, {'_id': False}))

    print("i", i)
    print(type(i))
    print(len(i))
    print('넘어온거 ', title_receive)


    try:  ## 저장된 명단 있을때
        if len(i) > 1: #년도가 다르고 일수가 같은 명단이 2개 있을때
            print("명단 두개", i)

        if str(i[0]['year']) == now.date().strftime("%Y"): #올해꺼
            print("저장된거 있음")
            return jsonify({'check': i[0]})
        else:
            print(i[0]['year'], now.date().strftime("%Y")) #올해꺼 아님
            print(type(i[0]['year']), type(now.date().strftime("%Y")))
    except IndexError: ## 저장명단 없을때
        print("저장된거 없음")
        return jsonify({'check': i})


#  저장된전체명단
@app.route('/review', methods=['GET'])
def readReviews():
    print("/review_GET")
    reviews = list(db.chulseck.find({}, {'_id': False}))
    re = []
    for _ in range(len(reviews) - 1, -1, -1):
        re.append(reviews[_])
    return jsonify({'all_reviews': re})


# API 역할을 하는 부분
@app.route('/review', methods=['POST'])
def writeReview():
    print("/review_POST")
    userAuthCheck = list(db.user.find({'username': session.get("username")}, {'_id': False}))
    if not session.get("username"):
        return jsonify({"False": "False"})
    elif userAuthCheck[0]['auth'] != 1:
        return jsonify({"False": "Auth"})

    title_receive = request.form['title_give']
    i = list(db.chulseck.find({'title': title_receive}, {'_id': False}))
    #  print(i)
    review_receive_list = list(map(str, request.form['review_give'].split()))
    review_receive_list = sorted(review_receive_list)
    print("확인 ", review_receive_list)
    review_receive_count = list(chulseck.people_calc(review_receive_list))
    list_people = str()
    list_result = str()
    for _ in review_receive_list:
        list_people += " " + _
        print("리스트 피플" + list_people)
    for _ in review_receive_count:
        list_result += " " + _
        print("리스트 결과" + list_result)
    doc = {
        'year': now.today().year,
        'title': title_receive,
        'review': list_people,
        'count': list_result  # 인원명단 + 밑에 남여합 출력하기위해
    }
    print(review_receive_list, review_receive_count)

    try:
        if str(i[0]['year']) == now.date().strftime("%Y"):
            print("저장된거 있음")
            db.chulseck.update_one({'title': title_receive}, {"$set": {'review': list_people, 'count': list_result}})
            autoSave()
            return jsonify({'msg': '저장성공!'})
    except IndexError:
        print("저장된거 없음")
        db.chulseck.insert_one(doc)
        autoSave()
        return jsonify({'msg': '저장성공!'})


#  명단삭제
@app.route('/dbDel', methods=['POST'])
def delReviews():
    print("/dbDel")
    userAuthCheck = list(db.user.find({'username': session.get("username")}, {'_id': False}))
    if not session.get("username"):
        return jsonify({"False": "False"})
    elif userAuthCheck[0]['auth'] != 1:
        return jsonify({"False": "Auth"})

    review = request.form['title_give']
    print("db del 시작")
    print(review)
    i = list(db.chulseck.find({'title': review}, {'_id': False}))
    # print(i)
    if not i:
        return jsonify({'msg': '해당하는 날짜에 저장된 데이터가 없습니다!'})
    else:
        db.chulseck.delete_one({'title': review})
    return jsonify({'msg': '삭제성공!'})


#db 인원수정
@app.route('/dbPersonChange', methods = ['POST'])
def changeDbPerson():
    print('/dbPersonChange')
    userAuthCheck = list(db.user.find({'username': session.get("username")}, {'_id': False}))
    try:
        print(userAuthCheck[0])
    except IndexError:
        print("권한 없음, 비로그인")
    if not session.get("username"):
        return jsonify({"False": "False"})
    elif userAuthCheck[0]['auth'] != 1:
        return jsonify({"False": "Auth"})

    name = request.form['name']
    group = request.form['group']
    s = request.form['sSelect']
    info = request.form['info']
    age = int(request.form['age'])

    i1 = list(db.peopleList.find({'이름': name}, {'_id': False}))

    if not i1:
        return jsonify({'no': "같은 이름의 사람이 없습니다!"})
    else:
        print(i1)
        db.peopleList.update_one({'이름': name}, {"$set": {'조': [str(group)], '나이': [age],'성별': [str(s)], '특이사항': [str(info)]}})
        return jsonify({'msg': "대상 : " + name + "\n" + str(group)+ "\n" + age + "\n" + str(s)+ "\n" + str(info)+ "\n"+'저장성공!'})


#  db 인원추가
@app.route('/dbPersonAdd', methods=['POST'])
def addDbPerson():
    print('/dbPersonAdd')
    userAuthCheck = list(db.user.find({'username': session.get("username")}, {'_id': False}))
    try:
        print(userAuthCheck[0])
    except IndexError:
        print("권한 없음, 비로그인")
    if not session.get("username"):
        return jsonify({"False": "False"})
    elif userAuthCheck[0]['auth'] != 1:
        return jsonify({"False": "Auth"})

    name = request.form['name']
    age = int(request.form['age'])
    group = request.form['group']
    s = request.form['sSelect']
    info = request.form['info']
    i1 = list(db.peopleList.find({'이름': name}, {'_id': False}))
    if not i1:
        doc = {
            '이름': name,
            '나이': [age],
            '조': [str(group)],
            '성별': [str(s)],
            '특이사항': [str(info)],
            '선교헌금': [int(0)]
        }
        print(doc)
        db.peopleList.insert_one(doc)
        return jsonify({'msg': name + " " + group + " " + s + ' 저장성공!'})
    else:
        return jsonify({'no': "같은 이름의 사람이 있습니다!"})

# db 다중인원삭제
@app.route('/delMultiPeople', methods=['POST'])
def delMultiPeople():
    print('/delMultiPeople')
    userAuthCheck = list(db.user.find({'username': session.get("username")}, {'_id': False}))
    if not session.get("username"):
        return jsonify({"False": "False"})
    elif userAuthCheck[0]['auth'] != 1:
        return jsonify({"False": "Auth"})

    name = list(request.form['name'].strip().split(' '))
    print(name)
    if not name:
        return jsonify({'no': '인원을 확인해주세요'})
    else:
        for i in name:
            print(i)
            i1 = list(db.peopleList.find({'이름': i}, {'_id': False}))
            if not i1:
                return jsonify({'no': '인원을 확인해주세요'})
            else:
                db.peopleList.delete_one({'이름': i})
        print(str(len(name)) + "명 삭제성공")
        return jsonify({'msg': str(len(name)) + "명 삭제성공"})


#  db 인원삭제
@app.route('/dbPersonDel', methods=['POST'])
def delDbPerson():
    print('/dbPersonDel')
    userAuthCheck = list(db.user.find({'username': session.get("username")}, {'_id': False}))

    if not session.get("username"):
        return jsonify({"False": "False"})
    elif userAuthCheck[0]['auth'] != 1:
        return jsonify({"False": "Auth"})

    print("#####출력#####")
    name = request.form['name']
    group = list(request.form['group'].strip().split())

    i1 = list(db.peopleList.find({'이름': name, '조': group}, {'_id': False}))
    if not i1:
        return jsonify({'no': 'DB에 저장된 인원이 없습니다!'})
    else:
        print(i1)
        print(i1[0]['조'][0])
        db.peopleList.delete_one({'이름': name, '조': group})
        print("msg: " + name + i1[0]['조'][0] + " " + ' 삭제성공!')
        return jsonify({'msg': name + " " + i1[0]['조'][0] + " " + '삭제성공!'})


@app.route('/ageAdd', methods=['POST'])
def ageAdd():
    print('/ageAdd')
    userAuthCheck = list(db.user.find({'username': session.get("username")}, {'_id': False}))

    if not session.get("username"):
        return jsonify({"False": "False"})
    elif userAuthCheck[0]['auth'] != 1:
        return jsonify({"False": "Auth"})

    i1 = list(db.peopleList.find({},{'_id': False}))

    for i in i1:
        print(i)
        print(i['이름'], i['나이'][0])
        a = int(i['나이'][0]) + 1
        print(i['이름'], i['나이'][0], "->", a)
        db.peopleList.update_one({'이름': i['이름']},{"$set": {'나이': [int(a)]}})
        #i['나이'] = i['나이'][0] + 1
    return jsonify({'msg': '전체인원 나이 증가!'})


@app.route('/ageDown', methods=['POST'])
def ageDown():
    print('/ageDown')
    userAuthCheck = list(db.user.find({'username': session.get("username")}, {'_id': False}))

    if not session.get("username"):
        return jsonify({"False": "False"})
    elif userAuthCheck[0]['auth'] != 1:
        return jsonify({"False": "Auth"})

    i1 = list(db.peopleList.find({}, {'_id': False}))

    for i in i1:
        print(i)
        print(i['이름'], i['나이'][0])
        a = int(i['나이'][0]) - 1
        print(i['이름'], i['나이'][0], "->", a)
        db.peopleList.update_one({'이름': i['이름']}, {"$set": {'나이': [int(a)]}})
    return jsonify({'msg': '전체인원 나이 감소!'})

#  인원추가
@app.route('/personAdd', methods=['POST'])
def addPerson():
    print('/personAdd')
    userAuthCheck = list(db.user.find({'username': session.get("username")}, {'_id': False}))

    if not session.get("username"):
        return jsonify({"False": "False"})
    elif userAuthCheck[0]['auth'] != 1:
        return jsonify({"False": "Auth"})

    review = request.form['title_give']
    addPersonList = request.form['new_give'].strip().split()
    print(addPersonList)
    print("personAdd 시작")
    i = list(db.chulseck.find({'title': review}, {'_id': False}))
    successList = ""
    failList = ""
    if not i:
        return jsonify({'msg': '해당하는 날짜에 저장된 데이터가 없습니다!'})
    else:
        print("삭제 후 db 업데이트")
        review_receive_list = list(i[0]['review'].strip().split())
        review_receive_list = sorted(review_receive_list)
        review_receive_list_copy = review_receive_list
        print(type(review_receive_list_copy))

        #addPersonList = addPersonList.split(" ")
        for _ in addPersonList:
            print(_)
            if _ == '':
                review_receive_list_copy.remove(_)
            if _ not in review_receive_list:
                review_receive_list_copy.append(_)
                successList += _ + " "
            else:
                failList += _ + " "
        print(review_receive_list)
        print(review_receive_list_copy)
        review_receive_count = chulseck.people_calc(review_receive_list_copy)
        list_people = str()
        list_result = str()
        for _ in review_receive_list_copy:
            list_people += " " + _
            print("리스트 피플" + list_people)
        for _ in review_receive_count:
            list_result += " " + _
            print("리스트 결과" + list_result)
        db.chulseck.update_one({'title': review}, {"$set": {'review': list_people, 'count': list_result}})
    return jsonify({'msg': '추가된 인원 : ' + successList + "\n" '추가안된 인원 : ' + failList})


#  인원삭제
@app.route('/personDel', methods=['POST'])
def delPerson():
    print('/personDel')
    userAuthCheck = list(db.user.find({'username': session.get("username")}, {'_id': False}))

    if not session.get("username"):
        return jsonify({"False": "False"})
    elif userAuthCheck[0]['auth'] != 1:
        return jsonify({"False": "Auth"})

    review = request.form['title_give']
    delPersonList = request.form['new_give']
    print("personDel 시작")
    i = list(db.chulseck.find({'title': review}, {'_id': False}))
    successList = ""
    failList = ""
    if not i:
        return jsonify({'msg': '해당하는 날짜에 저장된 데이터가 없습니다!'})
    else:
        print("삭제 후 db 업데이트")
        review_receive_list = list(i[0]['review'].strip().split())
        review_receive_list = sorted(review_receive_list)
        review_receive_list_copy = review_receive_list
        print(type(review_receive_list_copy))

        delPersonList = delPersonList.split(" ")
        for _ in delPersonList:
            print(_)
            if _ == '':
                review_receive_list_copy.remove(_)
            if _ in review_receive_list:
                review_receive_list_copy.remove(_)
                successList += _ + " "
            else:
                failList += _ + " "
        print(review_receive_list)
        print(review_receive_list_copy)
        review_receive_count = chulseck.people_calc(review_receive_list_copy)
        list_people = str()
        list_result = str()
        for _ in review_receive_list_copy:
            list_people += " " + _
            print("리스트 피플" + list_people)
        for _ in review_receive_count:
            list_result += " " + _
            print("리스트 결과" + list_result)
        db.chulseck.update_one({'title': review}, {"$set": {'review': list_people, 'count': list_result}})
    return jsonify({'msg': '삭제된 인원 : ' + successList + "\n" '명단에 없는 인원 : ' + failList})


# 엑셀 데이터 표시
# @app.route('/review', methods=['GET'])
# def read_reviews():
#     reviews = list(db.chulseck.find({}, {'_id': False}))
#     re = []
#     for _ in reviews:
#         print(_)
#         print(_['title'])
#         for i in peo:
#             if i in _["review"]:
#                 print(1)
#             else:
#                 print("")
#     return jsonify({'all_reviews': re})



@app.route('/getCheckboxInfo', methods = ['POST'])
def getCheckboxInfo():
    print('/getCheckboxInfo')
    userAuthCheck = list(db.user.find({'username': session.get("username")}, {'_id': False}))
    if not session.get("username"):
        return jsonify({"False": "False"})
    elif userAuthCheck[0]['auth'] != 1:
        return jsonify({"False": "Auth"})

    name = request.form['name']
    print(name)
    group = request.form['group']
    print(group)
    i1 = list(db.peopleList.find({'이름': name, '조': group}, {'_id': False}))
    print(i1)
    se = ""
    try:
        se = i1[0]['성별'][0]
        print(se)
        info = i1[0]['특이사항'][0]
        print(info)
    except IndexError or ValueError:
        info = ""

    return jsonify({"se": se, "info": info})


@app.route('/getTDate', methods=['GET'])
def getTDate():
    print('/getTDate')
    reviews = list(db.chulseck.find({}, {'_id': False}))
    re = []
    for _ in reviews:
        re.append(str(_['year'])+" "+str(_['title']))
    print("tDate", re)
    return jsonify({"date": re})


@app.route('/getMissionDate', methods=['GET'])
def getMissionDate():
    print('/getMissionDate')
    re = []
    for i in range(1, 13):
        re.append(str(i)+'월')
    print("tDate", re)
    return jsonify({"date": re})


@app.route('/getGroupGraph', methods=['GET'])
def getGroupGraph():
    print('/getGroupGraph_월전체')
    reviews = list(db.chulseck.find({}, {'_id': False}))
    people = list(db.peopleList.find({}, {'_id': False}))
    dbGroup = list(db.Group.find({}, {'_id': False}))
    print(dbGroup)
    dbG = []

    group2 = ["" for i in range(len(dbGroup))]
    group3 = []

    for _ in dbGroup:
        dbG.append(_.get('조 이름'))
    print(dbGroup)
    print(dbG)

    try:
        for i in people:
            group2[dbG.index(i['조'][0])] += i['이름']+" "
    except ValueError:
        print('getGroupGraph2_월전체 에러')
        return jsonify({"error": 'error'})
    print("group2", group2)

    for _ in group2:
        _ = len(list(_.strip().split(" ")))
        print(_)

    dbGroup = list(dbG)
    month = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

    # dbG = [[] for i in range(len(dbGroup))]
    # print(dbG)

    chu = []
    result = []
    # chu.append('Group')

    for i in month:
        m = i
        for _ in reviews:
            if str(_['year']) == now.date().strftime("%Y"):
                if str(_['title'])[:2] == i:
                    m += _['review']
        chu.append(m)

    print(chu) ##월별 전체인원출석현황
    r = dbG
    r.insert(0, "조이름")
    print(r)
    # result.append(dbGroup)
    for _ in chu:
        # print(_[:2])
        m = _[:2]
        group = [0 for i in range(len(dbGroup))]
        if _ != '월별':
            for i in people:
                # print(i['조'][0], _.count(i['이름']), dbGroup.index(i['조'][0]))
                group[dbGroup.index(i['조'][0])] += _.count(i['이름'])
                # print(group[dbGroup.index(i['조'][0])])
        print(group)
        group.insert(0, m+'월')
        result.append(group)
    result.insert(0, r)
    chu = result
    print(chu)
    return jsonify({"chul": chu})


@app.route('/getGroupGraph2', methods=['GET'])
def getGroupGraph2():
    print('/getGroupGraph2_월 평균')
    reviews = list(db.chulseck.find({}, {'_id': False}))
    people = list(db.peopleList.find({}, {'_id': False}))
    dbGroup = list(db.Group.find({}, {'_id': False}))
    print(dbGroup)
    dbG = []

    group2 = ["" for i in range(len(dbGroup))]
    group3 = [] #각 그룹에 속한 사람 수
    for _ in dbGroup:
        dbG.append(_.get('조 이름'))
    print(dbGroup)
    print(dbG)

    try:
        for i in people:
            group2[dbG.index(i['조'][0])] += i['이름']+" "
    except ValueError:
        print('getGroupGraph2_월평균 에러')
        return jsonify({"error": 'error'})
    print("group2", group2)

    for _ in group2:
        _ = len(list(_.strip().split(" ")))
        print(_)
        group3.append(_)
    print("group3", group3)
    dbGroup = list(dbG)
    month = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    month2 = [0 for i in range(len(month))]

    # dbG = [[] for i in range(len(dbGroup))]
    # print(dbG)

    chu = []
    result = []
    # chu.append('Group')

    for i in month:
        m = i
        for _ in reviews:
            if str(_['year']) == now.date().strftime("%Y"):
                if str(_['title'])[:2] == i:
                    m += _['review']
                    month2[month.index(i)] += 1
        chu.append(m)
    print("m2",month2)
    print(chu) ##월별 전체인원출석현황
    r = dbG
    r.insert(0, "조이름")
    print(r)
    # result.append(dbGroup)
    a = 0
    for _ in chu:
        a += 1
        # print(_[:2])
        m = _[:2]
        group = [0 for i in range(len(dbGroup))]
        for i in people:
            # print(i['조'][0], _.count(i['이름']), dbGroup.index(i['조'][0]))
            group[dbGroup.index(i['조'][0])] += _.count(i['이름'])
            # print(group[dbGroup.index(i['조'][0])])
            if i == people[-1]:
                print(a, group, sum(group))
                gSum = sum(group)
                for k in range(len(group)):
                    # group[k] /= group3[k] * month2[k] #각 월별 조 출석인원 / 그 조의 전체 인원 * 해당 월의 출석주차수
                    print("group", dbGroup[k], group[k], gSum)
                    try:
                        group[k] /= gSum # 해당 월의 조 출석인원 / 전체 출석인원
                    except ZeroDivisionError:
                        group[k] = 0
                    group[k] *= 100
                # group[dbGroup.index(i['조'][0])] = (group[dbGroup.index(i['조'][0])]/group3[dbGroup.index(i['조'][0])])
        print(group)
        group.insert(0, m+'월')
        result.append(group)
    result.insert(0, r)
    chu = result
    print(chu)
    return jsonify({"chul": chu})

@app.route('/getAgeGraph', methods=['GET'])
def getAgeGraph():
    print('/getAgeGraph')
    reviews = list(db.chulseck.find({}, {'_id': False}))
    people = list(db.peopleList.find({}, {'_id': False}))
    ageGroup = []
    month = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    month2 = [0 for i in range(len(month))]

    for i in people:
        ageGroup.append(i['나이'][0])

    ageGroupS = set(ageGroup)
    #print(ageGroupS)
    ageGroupS = list(sorted(ageGroupS))
    #print(type(ageGroupS))

    r = ageGroup
    r.insert(0, "나이")

    a = 0
    chu = []
    result = []

    for i in month:
        m = i
        for _ in reviews:
            #print(_['year'], now.date().strftime("%Y"))
            if str(_['year']) == now.date().strftime("%Y"):
                if str(_['title'])[:2] == i:
                    m += _['review']
                    month2[month.index(i)] += 1
        chu.append(m)
        #print(m)

    for _ in chu:
        a += 1
        # print(_[:2])
        m = _[:2]
        group = [0 for i in range(len(ageGroupS))]
        for i in people:
            # print(i['조'][0], _.count(i['이름']), dbGroup.index(i['조'][0]))
            group[ageGroupS.index(i['나이'][0])] += _.count(i['이름'])
            # print(group[dbGroup.index(i['조'][0])])
            if i == people[-1]:
                print(a, group, sum(group))
                gSum = sum(group)
                for k in range(len(group)):
                    # group[k] /= group3[k] * month2[k] #각 월별 조 출석인원 / 그 조의 전체 인원 * 해당 월의 출석주차수
                    print("group", ageGroupS[k], group[k], gSum)
                    try:
                        group[k] /= gSum  # 해당 월의 조 출석인원 / 전체 출석인원
                    except ZeroDivisionError:
                        group[k] = 0
                    group[k] *= 100
                # group[dbGroup.index(i['조'][0])] = (group[dbGroup.index(i['조'][0])]/group3[dbGroup.index(i['조'][0])])
        print(group)
        group.insert(0, m + '월')
        result.append(group)
    print("re",result)
    for i in range(len(ageGroupS)):
        ageGroupS[i] = str(ageGroupS[i])
        print(type(i))
    ageGroupS.insert(0,'나이')
    result.insert(0, ageGroupS)
    chu = result
    print(chu)
    return jsonify({"chul": chu})


@app.route('/getAttendanceGraph', methods=['GET'])
def getAttendanceGraph():
    print('/getAttendanceGraph')
    dayBound = list(db.graphDate.find({}, {'_id': False}))
    reviews = list(db.chulseck.find({}, {'_id': False}))
    people = list(db.peopleList.find({}, {'_id': False}))
    str = ""
    chul = {}
    chu = []
    # f = dayBound[0]['startDay'].replace('-', '')
    # e = dayBound[0]['endDay'].replace('-', '')
    # print(f, e)
    # print(f, e)
    # print(int(e[0:4]), int(e[4:6]), int(e[6:8]))
    # print(datetime(int(f[0:4]), int(f[4:6]), int(f[6:8])).isocalendar()[1]) #startDay 주차
    # print(datetime(int(e[0:4]), int(e[4:6]), int(e[6:8])).isocalendar()[1]) #endDay 주차

    # for i in review:
    #     # print(int(f"{i['year']}{i['title']}") - int(f) >= 0 and int(e) - int(f"{i['year']}{i['title']}") >= 0)
    #     # print(int("{}{}".format(i['year'], i['title'])), int(f))
    #     if int(f"{i['year']}{i['title']}") - int(f) >= 0 and int(e) - int(f"{i['year']}{i['title']}") >= 0:  #from <= compareDay
    #         # print(f, ("{}{}".format(i['year'], i['title'])), e)
    #         reviews.append(i)

    for i in reviews:
        str += i['review']

    str = list(str.strip().split(" "))

    for _ in people:
        try:
            if str.count(_['이름']) > 0:
                chu.append([_['이름'], str.count(_['이름'])])
                chul[_['이름']] = str.count(_['이름'])
        except KeyError:
            print("x")

    chulseck.bubble_sort_chul(chu)
    chul2 = dict(sorted(chul.items(), key=lambda x: x[1], reverse=True)) #람다정렬
    print(chul2)
    print(chu)
    # return jsonify({"chul": chu, "weekCompare": dayBound[0]['weekCompare']})
    return jsonify({"chul": chu})


@app.route('/getTChul', methods= ['GET'])
def getTChul():
    print('/getTChul')
    reviews = list(db.chulseck.find({}, {'_id': False}))
    people = list(db.peopleList.find({}, {'_id': False}))
    weekC = list(db.graphDate.find({}, {'_id': False}))
    chulseck.bubble_sort(people)
    chul = []

    for i in people:
        re = []
        cnt = 0
        re.append(i['이름'])
        for _ in reviews:
            if i['이름'] in _['review']:
                re.append("1")
                cnt += 1
            else:
                re.append(".")
        per = str(int(cnt/len(reviews)*100)) + str("%")
        re.insert(1, per)
        chul.append(re)
    return jsonify({'chul': chul})

@app.route('/getTMission', methods= ['GET'])
def getTMssion():
    print("/getTMssion")



@app.route('/getGroup', methods=['GET'])
def getGroup():
    print('/getGroup')
    dbGroup = list(db.Group.find({}, {'_id': False}))
    print(dbGroup)
    return jsonify({'dbG': dbGroup})


@app.route('/getTxtGroup', methods=['GET'])
def getGroup2():
    print('/getTxtGroup')
    dbGroup = list(db.Group.find({}, {'_id': False}))
    print(dbGroup)
    return jsonify({'dbG': dbGroup})


#  명단체크박스출력
@app.route('/getDB', methods=['GET'])
def readPeopleDB():
    print('/getDB')
    dbGroup = list(db.Group.find({}, {'_id': False}))
    dbPeople = list(db.peopleList.find({}, {'_id': False}))
    l = []
    for _ in range(len(dbGroup)):
        s = []
        for i in dbPeople:
            #  print(list(dbGroup[_ ].values()))
            if i['조'] == list(dbGroup[_].values()):
                s.append(i)
            if i == dbPeople[-1]:
                chulseck.bubble_sort(s)
                l.extend(s)
                s = []

    global n
    n = []
    for _ in dbPeople:
        if _ not in l:
            n.append(_)
    chulseck.bubble_sort(n)
    print("n ",len(n))
    #print("소속 x ", n)
    #print("소속 o ", l)
    return jsonify({'dbP': l, 'dbG': dbGroup})


#  명단체크박스출력_미분류그룹
@app.route('/getNotsetGroup', methods=['GET'])
def readNotSetPeopleDB():
    print("/getNotsetGroup")
    print("넘어옴!")
    print("소속 x ", n)
    return jsonify({'dbP': n})


#  결과복사_데이터확인
@app.route('/copyResult', methods=['POST'])
def copyResultPOST():
    print("/copyResultPost")
    review = request.form['title_give']
    global sendResult
    sendResult = list(db.chulseck.find({'title': review}, {'_id': False}))
    print(sendResult)
    if not sendResult:
        return jsonify({'msg': '해당하는 날짜에 저장된 데이터가 없습니다!'})
    else:
        print(sendResult[0]['title'])
        print(sendResult[0]['review'])
        print(sendResult[0]['count'])
        return jsonify({'review': sendResult})


@app.route('/changeGroupU', methods=['POST'])
def changeGroup():
    print("/changeGroupU")
    userAuthCheck = list(db.user.find({'username': session.get("username")}, {'_id': False}))

    if not session.get("username"):
        return jsonify({"False": "False"})
    elif userAuthCheck[0]['auth'] != 1:
        return jsonify({"False": "Auth"})

    peopleList = list(request.form['peopleList'].strip().split(' '))
    print(peopleList)
    print(len(peopleList))
    nextGroup = request.form['new_give']
    print(nextGroup)
    for _ in peopleList:
        print(_, nextGroup)
        db.peopleList.update_one({'이름': _}, {"$set": {'조': [nextGroup]}})
    return jsonify({'msg': 'txt'})


@app.route('/setGroup', methods=['POST'])
def setGroup():
    print("/setGroup")
    userAuthCheck = list(db.user.find({'username': session.get("username")}, {'_id': False}))

    if not session.get("username"):
        return jsonify({"False": "False"})
    elif userAuthCheck[0]['auth'] != 1:
        return jsonify({"False": "Auth"})

    g = list(db.Group.find({}, {'_id': False}))
    la = []
    for i in g:
        la.append(i['조 이름'])
    print(la)
    # a = g.values()
    # print(a)
    groupList = list(request.form['strGroup'].strip().split(' '))
    groupList = [v for v in groupList if v]
    strGroupList = str()
    print(groupList)
    print(len(groupList))
    c = set(la) - set(groupList)
    u = set(groupList) - set(la)
    db.Group.drop()
    # txt = "조 변경 성공!"
    for _ in groupList:
        doc = {
            "조 이름": _
        }
        db.Group.insert_one(doc)
        strGroupList += _ + "\n"
    print("c", c)
    if len(c) == 1:
        print(list(c)[0])
        return jsonify({'one': 'one', 'b': list(c)[0], 'a': list(u)[0]})
    return jsonify({'msg': strGroupList + "그룹 변환 성공"})


@app.route('/setGroupOne', methods=['POST'])
def setGroupOne():
    print('/setGroupOne')
    a = request.form['a']
    b = request.form['b']
    print(a, b)
    person = list(db.peopleList.find({"조": b}, {'_id': False}))
    print(person)
    for i in person:
        db.peopleList.update_one({'이름': i['이름']}, {"$set": {'조': [str(a)]}})
    return jsonify({'msg': "완료"})

#  결과복사_데이터전송
@app.route('/copyResult', methods=['GET'])
def copyResultGet():
    print('/copyResultGet')
    try:
        r = str(sendResult[0]['year']) + " " + str(sendResult[0]['title']) + '\n' + str(sendResult[0]['review']) \
            + '\n' + str(sendResult[0]['count'])
        r = r.replace("      ", " ")
        print(r)
        return jsonify({'review': r})
    except IndexError:
        r = "날짜를 확인해주세요."
        return jsonify({'review': r})


# @app.route('/autoSave', methods=['GET'])
def autoSave():
    print('/autoSave')
    userAuthCheck = list(db.user.find({'username': session.get("username")}, {'_id': False}))
    if not session.get("username"):
        return jsonify({"False": "False"})
    elif userAuthCheck[0]['auth'] != 1:
        return jsonify({"False": "Auth"})

    reviews = list(db.chulseck.find({}, {'_id': False}))
    mailList = list(db.mail.find({}, {'_id': False}))
    # mail = mailName.split('/')
    print(reviews)
    result = ''
    for i in reviews:
        result += str(i['year']) + '년 ' + str(i['title'][:2]) + "월 " + str(i['title'][2:]) + "일 출석 " + i[
            'count'].replace('<br>', '').replace('  ', ' ') + "\n" + i['review'][1:] + "\n\n"
    # print(result)
    now = datetime.now()

    eList = ['naochugu@gmail.com', 'xkzldks@naver.com']
    # STMP 서버의 url과 port 번호
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 465

    # 1. SMTP 서버 연결
    smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)

    EMAIL_ADDR = 'naochugu@gmail.com'
    EMAIL_PASSWORD = 'bead jpye ahpz sfjn'  # 구글 앱 비밀번호

    # 2. SMTP 서버에 로그인
    smtp.login(EMAIL_ADDR, EMAIL_PASSWORD)
    # 3. MIME 형태의 이메일 메세지 작성

    for i in mailList:
        print(i)
        message = EmailMessage()
        message.set_content(result + '\n\n\nhttp://zion' + now.date().strftime("%Y") + ".site\n")  # 내용
        message["Subject"] = str("[진주교회 시온청년부] " + now.date().strftime("%Y/%m/%d") + " 출석백업")  # 제목
        message["From"] = EMAIL_ADDR  # 보내는 사람의 이메일 계정
        message["To"] = i['메일주소']  # 받는 사람
        smtp.send_message(message)  # 4. 서버로 메일 보내기

    # 5. 메일을 보내면 서버와의 연결 끊기
    smtp.quit()
    return jsonify({'msg': "메일전송!"})


@app.route('/getUserAuth', methods=['GET'])
def getUserAuth():
    print('/getUserAuth')
    userAuthCheck = list(db.user.find({'username': session.get("username")}, {'_id': False}))

    # if not i:
    #     i = 0
    # else:
    #     i = userAuthCheck[0]['auth']
    i = 0
    try:
        i = userAuthCheck[0]['auth']

    except IndexError:
        i = 0
    print("권한 ", i)
    return jsonify({'msg': i})


#  그래프출력
@app.route("/graph")
def graph():
    return render_template('graph3.html')


@app.route("/login")
def login():
    return render_template('login.html')



#########게시판#############
def filesave(file):
    d_num = 1
    filename = file.filename
    file_path = app.config['UPLOAD_FOLDER'] + filename

    # 중복파일이 없을때 까지 파일명 수정
    print(file_path, os.path.isfile(file_path))
    while os.path.isfile(file_path):
        filename = str(d_num) + "_" + file.filename
        d_num += 1
        file_path = app.config['UPLOAD_FOLDER'] + filename

    file.save(file_path)
    return filename


@app.route('/write', methods=['GET', 'POST'])
def write():
    username = session.get("username")
    if not username:
        flash("로그인부터 해주세요")
        return redirect(url_for('account.login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form.get('content')
        create_date = str(time.strftime("%Y.%m.%d", time.localtime()))

        if title and content:
            print(title)
            print(content)
            # 파일 업로드
            files = request.files.getlist("file[]")
            images = []
            # 파일 유무 확인
            print("filename", files[0].filename)
            if not files[0].filename == "":
                # upload 폴더 생성(기존에 있으면 생성x)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

                for file in files:
                    filename = filesave(file)
                    print(filename)
                    images.append({"filename": filename})

            board = {
                "title": title,
                "content": content,
                "create_date": create_date,
                "username": username,
                "hit": 0,
                "good": [],
                "bad": [],
                "images": images
            }
            board_id = db.board.insert_one(board).inserted_id
            print(board)
            flash('작성 완료!')
            return redirect(url_for('detail', board_id=board_id))

        else:
            flash('제목과 내용을 빈칸없이 입력해주세요')
            # return render_template('board_in.html')
    return render_template('board_in.html')


@app.route('/mailBackup', methods = ['POST'])
def mailBackup():
    print('/mailBackup')
    userAuthCheck = list(db.user.find({'username': session.get("username")}, {'_id': False}))
    if not session.get("username"):
        return jsonify({"False": "False"})
    elif userAuthCheck[0]['auth'] != 1:
        return jsonify({"False": "Auth"})

    mailName = request.form['mail'] #메일주소/이름
    mail = mailName.split('/')
    mailList = list(db.mail.find({'메일주소' : mail[0]}, {'_id': False}))
    print("중복 : ", mailList)

    try:
        if not mailList:
            doc = {
                '메일주소': mail[0],
                '이름': mail[1]
            }
            db.mail.insert_one(doc)
            return jsonify({'success': '메일저장완료! 명단 저장후 입력하신 메일로 보내드립니다!'})
        else:
            return jsonify({'msg': '이미 추가된 메일입니다!'})
    except:
        return jsonify({'msg': '취소되었거나 잘못된 형식의 메일입니다!'})

@app.route('/board')
def board():
    boards = list(db.board.find({}).sort([("_id", -1)]))
    max_page = len(boards) // 10 + 1
    # 한 페이지에 들어가는 게시글 개수
    page_block = 10

    # 현재 페이지
    num = request.args.get('page')
    print("num", num)
    # 만약 처음 게시판 접속했을땐 페이지번호 = 1
    num = int(num) if num else 1

    # 이전 페이지 접속(페이지번호가 1보다 작을때) 했을때 페이지 번호 조정
    if num < 1: num = 1
    # 페이지 번호는 5개씩 보여줌
    start_page = ((num - 1) // 5) * 5 + 1  # 페이지 시작 번호
    end_page = start_page + 4 if (start_page + 4) < max_page else max_page  # 페이지 끝번호
    # 다음 페이지 접속(페이지 번호가 페이지 끝번호보다 클때)
    if num > end_page: num = end_page
    board_num = len(boards) - (page_block * (num - 1))
    return render_template('board.html', boards=boards[page_block * (num - 1): page_block * num], page=num,
                           board_num=board_num, start_page=start_page, end_page=end_page)


@app.route('/modify/<board_id>', methods=['GET', 'POST'])
def modify(board_id):
    username = session.get("username")
    if not username:
        flash("로그인부터 해주세요")
        return redirect(url_for('account.login'))

    board = db.board.find_one({'_id': ObjectId(board_id)})
    if request.method == 'POST':
        title = request.form['title']
        content = request.form.get('content')

        if title and content:
            print(title)
            print(content)

            # 기존 파일 삭제
            print("product images : ", board['images'])
            for image in board['images']:
                print("iamge: ", image)
                file_path = app.config['UPLOAD_FOLDER'] + image['filename']
                if os.path.isfile(file_path):
                    os.remove(file_path)

            # 파일 업로드
            files = request.files.getlist("file[]")
            images = []
            # 파일 유무 확인
            print("filename", files[0].filename)
            if not files[0].filename == "":
                # upload 폴더 생성(기존에 있으면 생성x)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

                for file in files:
                    filename = filesave(file)
                    print(filename)
                    images.append({"filename": filename})

            board = {
                "title": title,
                "content": content,
                "images": images
            }
            db.board.update_one({'_id': ObjectId(board_id)}, {"$set": board})
            flash('수정 완료!')
            return redirect(url_for('detail', board_id=board_id))
        else:
            flash('다시 입력해주세요')
            return render_template('modify.html', board=board)
    print(board)
    return render_template('modify.html', board=board)


@app.route('/detail/<board_id>')
def detail(board_id):
    # board_id = request.args.get('board')
    print("detail board id", board_id)

    db.board.update_one({'_id': ObjectId(board_id)}, {"$inc": {"hit": 1}})
    board = db.board.find_one({'_id': ObjectId(board_id)})

    print("detail", board)
    return render_template('detail.html', board=board)


@app.route('/delete/<board_id>')
def delete(board_id):
    board = db.board.find_one({'_id': ObjectId(board_id)})
    # 기존 파일 삭제
    print("product images : ", board['images'])
    for image in board['images']:
        print("iamge: ", image)
        file_path = app.config['UPLOAD_FOLDER'] + image['filename']
        if os.path.isfile(file_path):
            os.remove(file_path)
    db.board.delete_one({'_id': ObjectId(board_id)})

    flash('삭제 완료!')
    return redirect(url_for('board'))

@app.template_filter("formatdatetime")
def format_datetime(value):
    if value is None:
        return ""

    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    value = datetime.fromtimestamp(int(value / 1000)) + offset
    return value.strftime('%Y-%m-%d %H:%M:%S')


@app.route('/filedown/<filename>')
def filedown(filename):
    file_path = app.config['UPLOAD_FOLDER'] + filename
    return send_file(file_path, as_attachment=True)


@app.route('/good/<board_id>')
def good(board_id):
    username = session.get("username")
    if not username:
        return jsonify({"success": False, "msg": "로그인 후 이용가능합니다."})

    try:
        board = db.board.find_one({"$and": [{'good': username}, {'_id': ObjectId(board_id)}]})
        print(board)
        print("good board", board)
        if board:
            db.board.update_one({'_id': ObjectId(board_id)}, {"$pull": {"good": username}})
            # print(board)
            return jsonify({"success": True, "is_good": False})
        else:
            db.board.update_one({'_id': ObjectId(board_id)}, {"$push": {"good": username}})
            # print(board['good'])
            return jsonify({"success": True, "is_good": True})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "msg": "잘못된 요청입니다."})


@app.route('/bad/<board_id>')
def bad(board_id):
    username = session.get("username")
    if not username:
        return jsonify({"success": False, "msg": "로그인 후 이용가능합니다."})

    try:
        board = db.board.find_one({"$and": [{'bad': username}, {'_id': ObjectId(board_id)}]})

        if board:
            db.board.update_one({'_id': ObjectId(board_id)}, {"$pull": {"bad": username}})
            return jsonify({"success": True, "is_bad": False})
        else:
            db.board.update_one({'_id': ObjectId(board_id)}, {"$push": {"bad": username}})
            return jsonify({"success": True, "is_bad": True})
    except:
        return jsonify({"success": False, "msg": "잘못된 요청입니다."})


@app.route('/qr', methods=["POST"])
def qrCode():
    name = request.form['name']
    gender = request.form['gender']
    birthday = request.form['birthday']
    peopleList2 = list(db.peopleList.find({}, {'_id': False}))
    person = ""

    if len(name) > 3:# 이름이 네글자 이상인 경우
        print(name)
        if name[:3] in peopleList2:
            print()
    else:

        person = list(db.peopleList.find({"이름": name}, {'_id': False}))
        if peopleList2.count(name[:3]) >= 2:#이름 중복
            print(len(person))
        else:
            print(person)
            dM = str(datetime.today().month)
            dD = str(datetime.today().day)
            if int(dM) < 10:
                dM = "0" + str(datetime.today().month)

            if int(dD) < 10:
                dD = "0" + str(datetime.today().day)
            try:
                r = randint(1,100)
                qr = {
                    "year": now.date().strftime("%Y"),
                    "title": dM+dD,
                    "이름": name,
                    "조": person[0]['조'][0],
                    "r": r
                }
                qr2 = "year : " + str(now.date().strftime("%Y")) + "\ntitle : " + dM+dD + "\n이름 : " + name + "\n조 : " + person[0]['조'][0] + "\nr : " + str(randint(1, 100))
                db.peopleList.update_one({'이름': name}, {"$set": {'r': r}})
                print("qr", qr, "qr2", qr2)
            except IndexError:
                return jsonify({"msg": "명단에 이름이 없습니다. 서기나 임원들에게 문의부탁드립니다."})

            return jsonify({"msg": qr, "qr2": str(qr2)})


@app.route('/qrChul', methods= ["POST"])
def qrChul():
    userAuthCheck = list(db.user.find({'username': session.get("username")}, {'_id': False}))
    if not session.get("username"):
        return jsonify({"False": "False"})
    elif userAuthCheck[0]['auth'] != 1:
        return jsonify({"False": "Auth"})

    re = request.form['title_give']
    result = {}
    key = []
    val = []
    re = list(re.strip().split("\n"))
    print(re)
    for _ in re:
        a = _.strip().split(":")
        key.append(a[0].replace(" ", ""))
        val.append(a[1].replace(" ", ""))
    dic = dict(zip(key, val))
    print(dic)
    try:
        a = dic['이름']
        print(a)
    except:
        return jsonify({"msg": "추가안됨"})

    i = list(db.chulseck.find({'title': dic['title']}, {'_id': False}))
    print('i', i)
    successList = ""
    failList = ""

    if not i:
        # return jsonify({'msg': '해당하는 날짜에 저장된 데이터가 없습니다!'})
        chulseck.writeReviewQ(dic)
    else:
        print('else')
        print(i[0]['review'])
        print(addPerson)
        addPersonList = dic['이름']
        print("삭제 후 db 업데이트")
        review_receive_list = list(i[0]['review'].strip().split())
        review_receive_list = sorted(review_receive_list)
        review_receive_list_copy = review_receive_list
        print(type(review_receive_list_copy))

        # addPersonList = addPersonList.split(" ")
        # addPersonList = dic['이름']
        print("apl",addPersonList)
        if addPersonList == '':
            review_receive_list_copy.remove(addPersonList)
        if addPersonList not in review_receive_list:
            review_receive_list_copy.append(addPersonList)
            successList += addPersonList + " "
        else:
            failList += addPersonList + " "
            print(failList)
            return jsonify({"msg": "추가안됨"})

        print(review_receive_list)
        print(review_receive_list_copy)
        review_receive_count = chulseck.people_calc(review_receive_list_copy)
        list_people = str()
        list_result = str()
        for _ in review_receive_list_copy:
            list_people += " " + _
            print("리스트 피플" + list_people)
        for _ in review_receive_count:
            list_result += " " + _
            print("리스트 결과" + list_result)
        db.chulseck.update_one({'title': dic['title']}, {"$set": {'review': list_people, 'count': list_result}})
        return jsonify({"msg": "good"})




if __name__ == '__main__':
    app.secret_key = "123"
    app.run('0.0.0.0', debug=True)
