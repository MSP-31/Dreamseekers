from django.http import HttpResponse
from django.shortcuts import render

# 네이버 검색 API 예제 - 블로그 검색
from django.conf import settings
from datetime import datetime
import re
import urllib.request
import json

def search_blog(request):
    client_id = settings.NAVER_CLIENT_ID
    client_secret = settings.NAVER_CLIENT_SECRET
    Blogger_name = '꿈을찾는사람들교육원' # 블로거 이름
    display = 100 # 출력 건수
    sort = 'date' # 날짜순 검색

    query = urllib.parse.quote("꿈을 찾는 사람들 교육원")
    url = "https://openapi.naver.com/v1/search/blog?query=" + query + \
          "&display=" + str(display) + \
          "&sort=" + sort

    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id",client_id)
    req.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(req)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        data = json.loads(response_body.decode('utf-8')) # JSON 데이터 파싱
        items = data["items"]

        filtered_items = []
        # 특정 블로그의 게시물만 필터링
        for item in items:
            if Blogger_name in item['bloggername']:
                # HTML태그 제거
                clean_text = re.sub('<.*?>', '', item['description'])
                item['description'] = clean_text

                # item.postdate를 datetime 객체로 변환
                date = datetime.strptime(item['postdate'], '%Y%m%d')
                # datetime 객체를 원하는 형식의 문자열로 변환
                formatted_date = date.strftime('%Y-%m-%d')
                item['postdate'] = formatted_date

                filtered_items.append(item)
        return render(request,'news.html',{'data':filtered_items}) # 데이터 전달
    else:
        return HttpResponse("Error Code:" + rescode)
