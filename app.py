from pymongo import MongoClient
from flask import Flask, render_template, jsonify

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.dbsparta


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# API 역할을 하는 부분 --> 성공하면 .../api/list 쳤을 때, JSON 형태가 뜬다.
@app.route('/api/list', methods=['GET'])
def show_stars():
    # 1. db에서 mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
    # 참고) find({},{'_id':False}), sort()를 활용하면 굿!

    stars = list(db.mystar.find({}, {'_id': 0}))  # pymongo 의 db 중에서, mystar 를 찾아올(find) 건데.. _id 는 안 가져올꺼다.
                                                  # 그걸 list 화 해서 [['name': 머머, 'url': 머머머], '..', ...] stars 라고 부를 거다.

    # 2. articles라는 키 값으로 articles 정보 보내주기
    result = {
        'result': 'success',
        'stars_list': stars,  # index.html 에서, " var stars_list = response['stars_list'] " 라고 하면서 db를 불러올 것이다.
    }

    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
    return jsonify(result)


@app.route('/api/like', methods=['POST'])
def like_star():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    # 2. mystar 목록에서 find_one으로 name이 name_receive와 일치하는 star를 찾습니다.
    # 3. star의 like 에 1을 더해준 new_like 변수를 만듭니다.
    # 4. mystar 목록에서 name이 name_receive인 문서의 like 를 new_like로 변경합니다.
    # 참고: '$set' 활용하기!
    # 5. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success', 'msg': 'like 연결되었습니다!'})


@app.route('/api/delete', methods=['POST'])
def delete_star():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    # 2. mystar 목록에서 delete_one으로 name이 name_receive와 일치하는 star를 제거합니다.
    # 3. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success', 'msg': 'delete 연결되었습니다!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
