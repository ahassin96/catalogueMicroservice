from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)


mongo_client = MongoClient("mongodb://ec2-54-221-90-30.compute-1.amazonaws.com:27017")
database = mongo_client.admin
genres = ['horror', 'military', 'action']

@app.route('/movies', methods=['GET'])
def get_movies():
    try:
        result = {}
        for genre in genres:
            videos = database.movies.find({'genre': genre})
            result[genre] = []

            for video in videos:
                result[genre].append({
                    'title': video['title'],
                    'url': video['url'],
                    '_id': str(video['_id']),
                    'watch_details': f'http://3.90.74.38:5000/watch.php/{str(video["_id"])}'
                })

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)
