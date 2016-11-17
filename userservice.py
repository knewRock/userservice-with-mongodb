from flask import Flask, jsonify, url_for, redirect, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource
from flask import Response
from flask_cors import CORS, cross_origin
from bson import json_util
from bson import ObjectId
import json
import bcrypt

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "usertest"
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = 27020
mongo = PyMongo(app, config_prefix='MONGO')
# APP_URL = "http://127.0.0.1:1024"

#input the other domain in this command
cors = CORS(app, resources={r"/*": {"origins": "*"}})

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def oldToNewJson(obj):
    # obj['userId'] = obj['_id']
    # obj['userId'] = JSONEncoder().encode(obj['_id'])
    obj['userId'] = str(obj['_id'])
    del obj['_id'];
    obj['userStatus'] = obj['status']['userStatusName']
    del obj['status']
    del obj['_class']

def serializer(obj):
    # obj['userId'] = obj['_id']
    # obj['userId'] = JSONEncoder().encode(obj['_id'])
    obj['userId'] = str(obj['_id'])
    del obj['_id'];
    # obj['userStatus'] = obj['status']['userStatusName']
    # del obj['status']
    # del obj['_class']
    return obj

def serializerList(users):
    # obj['userId'] = obj['_id']
    # obj['userId'] = JSONEncoder().encode(obj['_id'])
    data = []
    for user in users:
        user = serializer(user)
        data.append(user)
    return data;
# def passwordTohash(password){
#     password = b+password
#     hashed = bcrypt.hashpw(password, bcrypt.gensalt())
#     if bcrypt.hashpw(password, hashed) == hashed:
#         print("It Matches!")
#     else:
#         print("It Does not Match :(")
# }

class Users(Resource):
    def get(self):
        data = []
        users = mongo.db.usertestonly.find()
        print users.count()
        users = serializerList(users)
        return Response( json_util.dumps(users, sort_keys=True),mimetype='application/json')

class User(Resource):
    def get(self, id):
        user = mongo.db.usertestonly.find_one({'_id': ObjectId(id)})
        # oldToNewJson(user)
        user = serializer(user)
        return Response( json_util.dumps(user, sort_keys=True),mimetype='application/json')

    def post(self, id =None):
        user = request.get_json()
        user['password'] = bcrypt.hashpw(str(officer['password']), bcrypt.gensalt())
        if not user:
            user = {"response": "Don't have data"}
            return jsonify(user)
        mongo.db.usertestonly.insert(user)
        return Response( json_util.dumps({"response": "add new officer"}, sort_keys=True),mimetype='application/json')

class deleteUser(Resource):
    def get(self, id):
        user = mongo.db.usertestonly.remove({'_id': ObjectId(id)})
        return Response( json_util.dumps({"response": "This user was deleted."}, sort_keys=True),mimetype='application/json')

class getBosses(Resource):
    def get(self):
        bosses = mongo.db.usertestonly.find({'status.userStatusName': 'Boss'})
        bosses = serializerList(bosses)
        return Response( json_util.dumps(bosses, sort_keys=True),mimetype='application/json')

# class getOfficers(Resource):
#     def get(self):
#         officers = mongo.db.usertestonly.find({'status.userStatusName': 'Officer'})
#         officers = serializerList(officers)
#         return Response( json_util.dumps(officers, sort_keys=True),mimetype='application/json')

# class newBoss(Resource):
#     def post(self):
#         boss = request.get_json()
#         boss['status'] = {}
#         boss['status']['_class'] = "main.rest.userstatus.Boss"
#         boss['status']['userStatusName'] = "Boss"
#         boss['_class'] = "main.model.User"
#         boss['password'] = bcrypt.hashpw(str(boss['password']), bcrypt.gensalt())
#         if not boss:
#             boss = {"response": "Don't have data"}
#             return jsonify(boss)
#         mongo.db.usertestonly.insert(boss)
#         return Response( json_util.dumps({"response": "add new boss"}, sort_keys=True),mimetype='application/json')

# class newOfficer(Resource):
#     def post(self):
#         officer = request.get_json()
#         officer['status'] = {}
#         officer['status']['_class'] = "main.rest.userstatus.Officer"
#         officer['status']['userStatusName'] = "Officer"
#         officer['_class'] = "main.model.User"
#         officer['password'] = bcrypt.hashpw(str(officer['password']), bcrypt.gensalt())
#         if not officer:
#             officer = {"response": "Don't have data"}
#             return jsonify(officer)
#         mongo.db.usertestonly.insert(officer)
#         return Response( json_util.dumps({"response": "add new officer"}, sort_keys=True),mimetype='application/json')

class newUser(Resource):
    def post(self):
        user = request.get_json()
        user['password'] = bcrypt.hashpw(str(user['password']), bcrypt.gensalt())
        # if user['bossId'] is not None:
        #     user['bossId'] = ObjectId(user['bossId'])
        if not user:
            user = {"response": "Don't have data"}
            return jsonify(user)
        mongo.db.usertestonly.insert(user)
        return Response( json_util.dumps({"response": "add new officer"}, sort_keys=True),mimetype='application/json')

class Login(Resource):
    def post(self):
        data = request.get_json()
        data['check'] = "not check"
        user = mongo.db.usertestonly.find_one({'email': data['email']})
        if bcrypt.hashpw(str(data['password']), str(user['password'])) == str(user['password']):
            # data['check'] = "It Matches!"
            return Response( json_util.dumps({"response": True}, sort_keys=True),mimetype='application/json')
        else:
            # data['check'] = "It Does not Match"
            return Response( json_util.dumps({"response": False}, sort_keys=True),mimetype='application/json')
        # return Response( json_util.dumps(data, sort_keys=True),mimetype='application/json')

# class getBossesOfUser(Resource):
#     def get(self, id):
#         bosses = []
#         user = mongo.db.usertestonly.find_one({'_id': ObjectId(id)})
#         while(user["bossId"] != None):
#             user = mongo.db.usertestonly.find_one({'_id': ObjectId(user["bossId"])})
#             bosses.append(user) 

#         bosses = serializerList(bosses)
#         return Response( json_util.dumps(bosses, sort_keys=True),mimetype='application/json')
class Relationship(Resource):
    def post(self):
        relation = request.get_json()
        if not relation:
            return jsonify({"response": "Don't have data"})
        mongo.db.relationship.insert(relation)
        return Response( json_util.dumps({"response": "add new relation"}, sort_keys=True),mimetype='application/json')

class getBossesOfUser(Resource):
    # bosses = []
    # a= "12345"
    def findBoss(self, subordinateId, bosses):
        # while(bosses != None):
        bossList = mongo.db.relationship.find({'subordinateId': subordinateId})
        # print len(bossList)
        if(bosses != None):
            for boss in bossList:
                if boss['bossId'] in bosses:
                    continue
                else:
                    bosses.append(boss['bossId'])
                    self.findBoss(boss['bossId'], bosses)
        
    def get(self, id):
        bossesId = []
        self.findBoss(id, bossesId)
        bosses = []
        for bossId in bossesId:
            bosses.append(mongo.db.usertestonly.find_one({'_id': ObjectId(bossId)}))
        # user = mongo.db.usertestonly.find_one({'_id': ObjectId(id)})
        # while(user["bossId"] != None):
        #     user = mongo.db.usertestonly.find_one({'_id': ObjectId(user["bossId"])})
        #     bosses.append(user) 

        bosses = serializerList(bosses)
        return Response( json_util.dumps(bosses, sort_keys=True),mimetype='application/json')

class getTree(Resource):
    def createTree(self,bossId):
        tree = {}
        tree['name'] = mongo.db.usertestonly.find_one({'_id': ObjectId(bossId)})
        tree['name'] = serializer(tree['name'])
        subordinateList = mongo.db.relationship.find({'bossId': bossId})
        if subordinateList.count() >0:
            tree['children'] = []
            for subordinate in subordinateList:
                childTree = self.createTree(subordinate['subordinateId'])
                tree['children'].append(childTree)
        return tree

    def get(self):
        root = mongo.db.usertestonly.find_one({'firstname':'boss0'})
        tree = self.createTree(str(root['_id']))
        return Response( json_util.dumps(tree),mimetype='application/json')        
                        
class Test(Resource):
    def post(self):
        data = request.get_json()
        # data['bpassword'] = b"super secret password"
        # data['hashed'] = bcrypt.hashpw(data['bpassword'], bcrypt.gensalt())
        # data['check'] = "not check"
        # if bcrypt.hashpw("super secret password", data['hashed']) == data['hashed']:
        #     data['check'] = "It Matches!"
        # else:
        #     data['check'] = "It Does not Match"
        # return Response( json_util.dumps(data, sort_keys=True),mimetype='application/json')
        return data['test'] != None


api = Api(app)
api.add_resource(Users, "/users", endpoint="users")
api.add_resource(User, "/user/<string:id>", endpoint="user")
api.add_resource(deleteUser, "/deleteUser/<string:id>", endpoint="deleteUser")
# api.add_resource(getBosses, "/getBosses", endpoint="bosses")
api.add_resource(getBossesOfUser, "/user/<string:id>/getBosses", endpoint="bossesOfUser")
api.add_resource(getTree, "/tree", endpoint="tree")
# api.add_resource(getOfficers, "/getOfficers", endpoint="officers")
# api.add_resource(newBoss, "/newBoss", endpoint="newBoss")
# api.add_resource(newOfficer, "/newOfficer", endpoint="newOfficer")
api.add_resource(newUser, "/newUser", endpoint="newUser")
api.add_resource(Relationship, "/newRelationship", endpoint="newRelationship")
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(Test, "/test", endpoint="test")

if __name__ == "__main__":
    app.run(port =5001, debug=True)