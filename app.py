from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # request.args -> Dictionary(Immutable)
    # 클라이언트로 부터 받은 파라미터를 저장하고 있는 친구
    student = request.args.get('student')
    teacher = request.args.get('teacher')
    return { 'hello': student }

@app.route('/daum_webtoon')
def daum_toon_index():
    days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    return render_template('daum_webtoon_list.html', days=days)

@app.route('/daum_webtoon/<day>')
def daum_toon(day):
    url = f'http://webtoon.daum.net/data/pc/webtoon/list_serialized/{day}'
    data = request_json_data_from_url(url)
    return { 'data': parse_daum_webtoon_data(data) }



def request_json_data_from_url(url):
    # 3. 해당 url에 요청을 보낸다.
    response = requests.get(url)
    data = response.json()
    return data

def parse_daum_webtoon_data(data):
    toons = []
    for toon in data["data"]:
        # 제목의 key는 'title'
        title = toon["title"]

        # 설명의 key는 'introduction'
        desc = toon["introduction"]

        # 장르의 위치는 'cartoon' 안에 'genre'라는 리스트 안에 'name'이라는 key
        genres = []
        for genre in toon["cartoon"]["genres"]:
            genres.append(genre["name"])
        
        # 작가 이름의 위치는 'cartoon'안에 'artists'라는 리스트 안에 'name'이라는 key
        artists = []
        for artist in toon["cartoon"]["artists"]:
            artists.append(artist["name"])
        # 썸네일 이미지의 위치는 'pcThumbnailImage'안에 'url'이라는 키의 값으로 있음
        img_url = toon["pcThumbnailImage"]["url"]
        tmp = {
            title: {
                "desc": desc,
                "writer": artists,
                "img_url": img_url
            }
        }
        toons.append(tmp)
    return toons