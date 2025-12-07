from flask import Flask
from flask import request
from flask import jsonify
import json
import redis

app = Flask(__name__)


redisDB = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

class Note:
    def __init__(self, id, title, content):
        self.id = id
        self.title = title
        self.content = content

    def __repr__(self):
        return f"id: {self.id} - title: {self.title} - content: {self.content}"
    
    def to_json(self):
            return {"id": self.id, "title": self.title, "content": self.content}
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["title"], data["content"])

notes = [Note(id=0,title="fefe",content="ssssss"), Note(id=1,title="fefe",content="ssssss")]

@app.route("/")
def test():
    return "<p>Hello from notes server!!</p>"

# GET /notes → list all # POST /notes → create
@app.route("/notes", methods=['GET', 'POST'])
def noteWork():
    if request.method == 'POST':

        id = request.json.get("id") 
        title = request.json.get("title")
        content = request.json.get("content") 

        print("post: ", str(title), str(content), id)

        noteToPost = Note(id, title, content)
        try:
            redisDB.hset("id", int(id), json.dumps(noteToPost.to_json()))
        except Exception as e:
            print(f"🚨 Radis error occurred: {e}")
            return jsonify({"error": str(e)}), 500


        return jsonify({'note': noteToPost.to_json()}), 201
    else:
        try:
            listAllValues = redisDB.hgetall('id')
        except Exception as e:
            print(f"🚨 Radis error occurred: {e}")
            return jsonify({"error": str(e)}), 500

        print("resp", listAllValues)
        print("resp items", listAllValues.items())
        print("resp values", listAllValues.values())

        notes_list = [json.loads(v) for v in listAllValues.values()]
        return jsonify(notes_list), 200

# GET /notes/:id → retrieve one
@app.route("/notes/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def findNote(id):
    if request.method == 'GET':
        res = []
        noteFromSearch = redisDB.hget('id', id)
        return noteFromSearch

    elif request.method == 'PUT':
        id = request.json.get("id") 
        title = request.json.get("title") 
        content = request.json.get("content") 
        newNote = Note(id, title, content)
        redisDB.hset('id', id, json.dumps(newNote.to_json()))

        return redisDB.hget('id', id), 200

    elif request.method == 'DELETE':
        numberOfDeletedItems = redisDB.hdel('id', id)
        if numberOfDeletedItems == 0:
            return "Resource not found", 404
        else:
            return "No Content", 204
    else:
        return f"<p>id: {id} not found</p>", 404