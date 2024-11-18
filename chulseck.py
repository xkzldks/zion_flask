from flask import Flask, url_for, render_template, request, redirect, session, jsonify, flash, send_file
from datetime import datetime
from model2 import db
# from python_arptable import get_arp_table

now = datetime.now()


def user_info():
    user_agent = request.user_agent.string
    # if "Linux" in user_agent:
    #     user_agent = user_agent.replace('(', '')
    #     user_agent = user_agent.replace(')', '')
    #     user_agent = user_agent.split(';')
    #     print(user_agent)
    #     user_agent[2] = user_agent[2].split(",")
    # else:
    #     user_agent = user_agent.replace('(', '')
    #     user_agent = user_agent.replace(')', '')
    #     print(user_agent)
    # print(user_agent)
    # print(type(user_agent_nama))
    # print('브라우저',user_agent_nama.browser)
    # print('플랫폼',user_agent_nama.platform)
    # print('버전',user_agent_nama.version)
    # print('언어', user_agent_nama.language)
    return user_agent[user_agent.find("(")+1:user_agent.find(")")]


def people_calc(n):
    print("#####people_calc#####")
    print(n)  # 저장하려는 명단

    ManCount = 0
    WomanCount = 0

    for _ in n:
        person = list(db.peopleList.find({"이름": _}, {'_id': False}))
        print(person)
        if person[0]['성별'] == list('여'):
            WomanCount += 1
        elif person[0]['성별'] == list('남'):
            ManCount += 1
    result = "남 : ", str(ManCount), "<br>여 : ", str(WomanCount), "<br>합 : ", str(ManCount + WomanCount)
    print("result ", result)

    return result


def writeReviewQ(dic):
    print("/review_QR")
    title_receive = dic['title']
    #  print(i)
    ManCount = 0
    WomanCount = 0

    person = list(db.peopleList.find({"이름": dic['이름']}, {'_id': False}))
    print(person)
    if person[0]['성별'] == list('여'):
        WomanCount += 1
    elif person[0]['성별'] == list('남'):
        ManCount += 1
    result = "남 : ", str(ManCount), "<br>여 : ", str(WomanCount), "<br>합 : ", str(ManCount + WomanCount)
    print("result ", result)

    review_receive_count = result
    list_people = str()
    list_result = str()
    for _ in review_receive_count:
        list_result += " " + _
        print("리스트 결과" + list_result)
    doc = {
        'year': now.today().year,
        'title': dic['title'],
        'review': list_people,
        'count': list_result  # 인원명단 + 밑에 남여합 출력하기위해
    }
    print(review_receive_count)

    db.chulseck.insert_one(doc)
    return jsonify({'msg': '저장성공!'})


def bubble_sort(arr):
    for i in range(len(arr) - 1, 0, -1):
        for j in range(i):
            if arr[j]['이름'] > arr[j + 1]['이름']:
                arr[j]['이름'], arr[j + 1]['이름'] = arr[j + 1]['이름'], arr[j]['이름']
                arr[j]['나이'], arr[j + 1]['나이'] = arr[j + 1]['나이'], arr[j]['나이']
                arr[j]['조'], arr[j + 1]['조'] = arr[j + 1]['조'], arr[j]['조']
                arr[j]['성별'], arr[j + 1]['성별'] = arr[j + 1]['성별'], arr[j]['성별']
                arr[j]['특이사항'], arr[j + 1]['특이사항'] = arr[j + 1]['특이사항'], arr[j]['특이사항']
                arr[j]['선교헌금'], arr[j + 1]['선교헌금'] = arr[j + 1]['선교헌금'], arr[j]['선교헌금']

def bubble_sort_chul(arr):
    for i in range(len(arr) - 1, 0, -1):
        for j in range(i):
            if arr[j][1] < arr[j + 1][1]:
                arr[j][0], arr[j + 1][0] = arr[j + 1][0], arr[j][0]
                arr[j][1], arr[j + 1][1] = arr[j + 1][1], arr[j][1]


def mac_for_ip(ip):
    # arp_table = get_arp_table()
    #
    # for entry in arp_table:
    #     if entry['IP address'] == ip:
    #         return entry['HW address']
    return None
