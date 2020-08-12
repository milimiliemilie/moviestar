import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request

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
    # 1. db에서 mystar 목록 전체를 검색합니다.
    # - ID는 제외하고 like 가 많은 순으로 정렬합니다.
    # - 참고) find({},{'_id':False}), sort()를 활용하면 굿!
    # - .sort([("field1", pymongo.ASCENDING), ("field2", pymongo.DESCENDING)])
    # - .sort("_id", 1)

    stars = list(db.mystar.find({}, {'_id': 0}).sort("like", pymongo.DESCENDING))
    # " db에서, mystar 를 찾아올(find) 건데.. _id 는 안 가져올꺼다. "
    # 그걸 list 화 해서 [['name': 머머, 'url': 머머머], '..', ...] stars 라고 부를 거다.
    # 애초에 db = client.dbsparta 라고 했고, client = MongoClient('localhost', 27017) 이라고 정했다는 걸 기억하자.
    # 결국 db = MongoClient('localhost', 27017).dbsparta 라는 뜻.

    # 2. articles 라는 키 값으로 articles 정보 보내주기
    result = {
        'result': 'success',
        'stars_list': stars,  # index.html 에서, " var stars_list = response['stars_list'] " 라고 하면서 db를 불러올 것이다.
    }

    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
    return jsonify(result)


@app.route('/api/like', methods=['POST'])
def like_star():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    name_receive = request.form['name_give']

    # 2. mystar 목록에서 find_one으로 name이 name_receive와 일치하는 star를 찾습니다.
    # - 결국 "검색"이당.
    # - 검색 조건을 걸어줄 때는, "'찾을 필드': 일치할 데이터 " 이런식으로 쓴당. (쉼표로 구분하고 여러 개 써도 됨)
    # - 그래서 그 document 를 python 에서 써먹기 위해 ... dict 형태의 자료로 만든다.
    mystar = dict(db.mystar.find_one({'name': name_receive}))

    # 3. star의 like 에 1을 더해준 new_like 변수를 만듭니다.
    like = mystar['like']
    newLike = like + 1

    # 4. mystar 목록에서 name이 name_receive인 문서의 like 를 new_like로 변경합니다.
    # - " 'name': 특정이름 " 인 항목을 찾아서,
    # - Dict 안에 Dict 가 있는 형태로 업뎃을 시켜준다. ('$set' 이라는걸 쓴다..)
    db.mystar.update_one({'name': name_receive}, {'$set': {'like': newLike}})

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
