import datetime
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy.sql.functions import current_timestamp
import json
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db = SQLAlchemy(app)

shop_name_list=["北海道商店","東北商店","関東商店","韓国商店","関西商店","四国商店","中国商店","九州商店","沖縄商店"]
coupon_list=["ビール","サワー","食べ放題","韓国商店","関西商店","四国商店","中国商店","九州商店","沖縄商店"]

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    sending=db.Column(db.Boolean, nullable=True, default=True)
    coupon_id = db.Column(db.Integer, nullable=True)
    type = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now,nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,nullable=False)

class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, nullable=True)
    text = db.Column(db.String(200), nullable=True)
    qr = db.Column(db.String(50), nullable=True)
    shopId = db.Column(db.Integer, nullable=True)
    used = db.Column(db.Integer, nullable=True)
    discountRate=db.Column(db.Integer, nullable=True)
    #あとで修正

    sheetNumber=db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now,nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,nullable=False)


#テスト用
@app.route("/",methods=["GET","POST"])
def index():
    return "お前、どこ園だ、バブゥ！？"

#テスト用にuserの作成
@app.route('/create_user',methods=["POST","GET","PATCH"])
def create_user():
    new_post = User(name="masatoshi",
                    age=30,
                    type=1,
        )

    db.session.add(new_post)
    db.session.commit()
    db.session.close()

    return jsonify({'message': 'Complete Coupon Create'}), 200

#ユーザの仮登録
@app.route('/create_users',methods=["POST","GET"])
def create_users():
    
    new_post = User(name=request.json["name"],
                    age=request.json["age"],
        )

    db.session.add(new_post)
    db.session.commit()

    return jsonify({'userId': new_post.id}), 200


'''
    if(not request.form["name"]): 
        print("No name")
        return jsonify({'message': 'No name'}), 500

    elif(not request.form["age"]):
        print("No age")
        return jsonify({'message': 'No age'}), 500

    new_post = User(name=request.form["name"],
                    age=request.form["age"],
        )

    db.session.add(new_post)
    db.session.commit()

    return jsonify({'userId': new_post.id}), 200
'''

#自分でクーポン作成
@app.route('/create_coupon',methods=["POST","GET"])
def self_create_coupon():
    
    if(not request.form["shopId"]): 
        print("No shopId")
        return jsonify({'message': 'No shopId'}), 500

    elif(not request.form["discountRate"]):
        print("No discountRate")
        return jsonify({'message': 'No discountRate'}), 500

    elif(not request.form["sheetNumber"]):
        print("No sheetNumber")
        return jsonify({'message': 'No sheetNumber'}), 500
    
    else:
        new_post = Coupon(shopId=int(request.form["shopId"]),
                            discountRate=int(request.form["discountRate"]),
                            sheetNumber=int(request.form["sheetNumber"]),
                            used=0,
            )

        db.session.add(new_post)
        db.session.commit()
        db.session.close()

        return jsonify({'message': 'Complete Coupon Create'}), 200



#店がクーポン作成
@app.route('/coupon',methods=["POST","GET"])
def create_coupon():
    
    '''
    if(not request.form["shopId"]): 
        print("No shopId")
        return jsonify({'message': 'No shopId'}), 500

    elif(not request.form["discountRate"]):
        print("No discountRate")
        return jsonify({'message': 'No discountRate'}), 500

    elif(not request.form["sheetNumber"]):
        print("No sheetNumber")
        return jsonify({'message': 'No sheetNumber'}), 500
    
    '''
    
    #else:
    new_post = Coupon(shopId=int(request.json["shopId"]),
                        discountRate=int(request.json["discountRate"]),
                        sheetNumber=int(request.json["sheetNumber"]),
                        used=0,
        )

    db.session.add(new_post)
    db.session.commit()
    db.session.close()

    return jsonify({'message': 'Complete Coupon Create'}), 200



#カスタマーが使用できるクーポンの一覧表示
@app.route('/coupons', methods=["GET"])
def customer_coupons():
    x= request.args.get("shopId")
    y= request.args.get("sheetNumber")

    #sheetNumber = request.args.get("sheetNumber")
    posts = Coupon.query.filter_by(shopId=x).filter_by(used=0)
    

    l=[]
    for post in posts:
        st={'id': post.id, 
        'shopId': post.shopId, 
        'shop_name':shop_name_list[post.shopId],
        'discountRate': post.discountRate,
        }
        
        l.append(st)
    

    res=json.dumps(l)
    return res

#カスタマーのクーポンを使用・発行usedは0→1
@app.route('/coupons/user_id',methods=["PATCH"])
def customer_use_coupon():

    
    '''
    if(not request.form["coupon_id"]):
        print("No coupon_id")
        return jsonify({'message': 'No coupon_id'}), 500
    
    elif(not request.form["state"]):
        print("No state")
        return jsonify({'message': 'No state'}), 500

    elif(not request.form["userId"]):
        print("No userId")
        return jsonify({'message': 'No userId'}), 500

    elif(not request.form["text"]):
        print("No text")
        return jsonify({'message': 'No text'}), 500
    '''
    
    #else:
        #DB入力
    post = Coupon.query.get(int(request.json["coupon_id"]))
    post.used=1
    post.user_id=int(request.json["userId"])
    post.text=request.json["text"]

    db.session.commit()
        

    return jsonify({'message': 'Used Coustomer_cuupon'}), 200

#レシーバーのクーポン一覧表示
@app.route('/receiver/coupons',methods=["GET"])
def receiver_coupon():
    
    posts = Coupon.query.filter_by(used=1)
     
    l=[]
    for post in posts:
        id=post.user_id
        #user_post = User.query.filter_by(id=post.user_id)
        user_post = User.query.get(id)  
    
        print((user_post.id))

        st={'id': post.id, 
        'text': post.text, 
        'sheetNumber': post.sheetNumber,
        'shopId':post.shopId,
        'shop_name':shop_name_list[post.shopId],
        'user':{"name":user_post.name,
                "age":user_post.age

        }
        }
        
        l.append(st)
    

    res=json.dumps(l)
    return res


#レシーバーのクーポン利用後1→2
@app.route('/coupons/used',methods=["PATCH"])
def use_receiver_coupon():
    
    '''
    if(not request.json["coupon_id"]):
        print("No coupon_id")
        return jsonify({'message': 'No coupon_id'}), 500
    
    elif(not request.json["state"]):
        print("No state")
        return jsonify({'message': 'No state'}), 500
    
    
    '''
    #else:
    print(request.json["coupon_id"])
    post = Coupon.query.get(int(request.json["coupon_id"]))
    post.used=2

    db.session.commit()

    return jsonify({'message': 'Complete Coupon Use'}), 200



#レシーバが客のQRを読み取った2→3
@app.route('/coupons/read',methods=["PATCH"])
def read_coupon():
    
    '''
    if(not request.form["state"]):
        print("No state")
        return jsonify({'message': 'No state'}), 500

    elif(not request.form["coupon_id"]):
        print("No coupon_id")
        return jsonify({'message': 'No coupon_id'}), 500
    '''
    #else:
    post = Coupon.query.get(int(request.json["coupon_id"]))
    post.used=3

    db.session.commit()

    return jsonify({'message': 'Complete Coupon Use'}), 200



#全てのDBの値を確認する
@app.route('/all_viwe_coupon', methods=["GET","POST"]) 
def all_view_coupon():
    posts = Coupon.query.all()
    l=[]
    for i in range(0,len(posts)):
        st={'id': posts[i].id, 
        'user_id': posts[i].user_id, 
        'text': posts[i].text, 
        'shopId': posts[i].shopId,
        'shop_name':shop_name_list[posts[i].shopId],
        'used': posts[i].used,
        'qr':posts[i].qr,
        'discountRate':posts[i].discountRate,
        'sheetNumber':posts[i].sheetNumber
        }

        l.append(st)

    #これでリストをjsonに変換
    res=json.dumps(l)

    return res

#全てのUSERtableの値を確認する
@app.route('/all_viwe_user', methods=["GET","POST"]) 
def all_view_user():
    posts = User.query.all()
    l=[]
    for i in range(0,len(posts)):
        st={'id': posts[i].id, 
        'name': posts[i].name, 
        'age': posts[i].age, 
        'sending': posts[i].sending,
        'coupon_id': posts[i].coupon_id,
        'type':posts[i].type,
        }

        l.append(st)

    #これでリストをjsonに変換
    res=json.dumps(l)

    return res


#最終的には"debug=False"に変更
if __name__=="__main__":
    app.run(debug=True)