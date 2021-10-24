import datetime
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy.sql.functions import current_timestamp
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=False)
    sending=db.Column(db.Boolean, nullable=False, default=True)
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
    sheetNumber=db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now,nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,nullable=False)


#テスト用
@app.route("/")
def index():
    return "お前、どこ園だ、バブゥ！？"

#クーポン作成
@app.route('/create_coupon',methods=["POST"])
def create_coupon():
    print(int(request.form["shopId"]))
    
    
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



#カスタマーが使用できるクーポンの一覧表示
@app.route('/coupons/<int:shopId>/<int:sheetNumber>', methods=["GET"])
def customer_coupons(shopId,sheetNumber):
    x=shopId

    posts = Coupon.query.filter_by(shopId=x).filter_by(used=0)
    

    l=[]
    for post in posts:
        st={'id': post.id, 
        'shopId': post.shopId, 
        'discountRate': post.discountRate,}
        
        l.append(st)
    

    res=json.dumps(l)
    return res

#カスタマーのクーポンを使用・発行
@app.route('/coupons/user_id',methods=["PATCH"])
def customer_use_coupon():

    
    
    if(not request.form["coupon_id"]):
        print("No coupon_id")
        return jsonify({'message': 'No coupon_id'}), 500
    
    if(not request.form["state"]):
        print("No state")
        return jsonify({'message': 'No state'}), 500

    elif(not request.form["userId"]):
        print("No userid")
        return jsonify({'message': 'No userid'}), 500

    elif(not request.form["text"]):
        print("No text")
        return jsonify({'message': 'No text'}), 500
    
    else:
        #DB入力
        post = Coupon.query.get(int(request.form["coupon_id"]))
        post.used=int(request.form["state"])
        post.user_id=int(request.form["userId"])
        post.text=request.form["text"]

        db.session.commit()
        

        return jsonify({'message': 'Used Coustomer_cuupon'}), 200

#レシーバーのクーポン一覧表示
@app.route('/receiver/coupons',methods=["GET"])
def receiver_coupon():
    
    posts = Coupon.query.filter_by(used=1)
    for post in posts:
        print(post)
    
    l=[]
    for post in posts:
        print(type(post.user_id))
        user_post = User.query.filter_by(id=post.user_id)
        user_post1 = User.query.get(post.user_id)  
        print(type(user_post))
        print(type(user_post1))

        st={'id': post.id, 
        'text': post.text, 
        'sheetNumber': post.sheetNumber,
        'shopId':post.shopId,
        'user':{"name":user_post.name,
                "age":user_post.age

        }
        }
        
        l.append(st)
    

    res=json.dumps(l)
    return res


#レシーバーのクーポン利用後で治す#############
@app.route('/coupons/used',methods=["PATCH"])
def use_receiver_coupon():
    
    if(not request.form["coupon_id"]):
        print("No coupon_id")
        return jsonify({'message': 'No coupon_id'}), 500
    
    elif(not request.form["state"]):
        print("No state")
        return jsonify({'message': 'No state'}), 500
    
    
    else:
        post = Coupon.query.get(int(request.form["state"]))
        post.used=int(request.form["state"])

        db.session.commit()

        return jsonify({'message': 'Complete Coupon Use'}), 200



#レシーバが客のQRを読み取った
@app.route('/coupons/used',methods=["PATCH"])
def read_coupon():

    if("couponId" not in request.json):
        print("No couponId")
        return jsonify({'message': 'No couponId'}), 500

    elif("state" not in request.json):
        print("No state")
        return jsonify({'message': 'No state'}), 500
    
    else:
        post = Coupon.query.get(int(request.json["couponId"]))
        post.used=int(request.json["state"])

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
def all_view_coupon():
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


@app.route('/coupon', methods=["POST"])
def coupon():
    return "asd"


if __name__=="__main__":
    app.run(debug=True)