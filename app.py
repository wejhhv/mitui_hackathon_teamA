##flaskを扱った大まかな流れと方法
# -*- coding: utf-8 -*-
import datetime
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy.sql.functions import current_timestamp

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cooking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


#setting database
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    making_time = db.Column(db.String(50), nullable=False)
    serves = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now,nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,nullable=False)

@app.route('/recipes',methods=["POST"])
def create():
    
    if("title" not in request.json): 
        print("titleが存在しない")
        return jsonify({"message": "Recipe creation failed!","required": "title, making_time, serves, ingredients, cost"})
    if("making_time" not in request.json):
        print("making_timeが存在しない")
        return jsonify({"message": "Recipe creation failed!","required": "title, making_time, serves, ingredients, cost"}) 
    if("serves" not in request.json):
        return jsonify({"message": "Recipe creation failed!","required": "title, making_time, serves, ingredients, cost"}) 
    if("ingredients" not in request.json):
        return jsonify({"message": "Recipe creation failed!","required": "title, making_time, serves, ingredients, cost"}) 
    if("cost" not in request.json):
        return jsonify({"message": "Recipe creation failed!","required": "title, making_time, serves, ingredients, cost"}) 
    
    print("完璧な処理")
    new_post = Post(title=request.json["title"], making_time=request.json["making_time"], serves=request.json["serves"],ingredients=request.json["ingredients"],cost=request.json["cost"])

    db.session.add(new_post)
    db.session.commit()
            
    return jsonify({"message": 'Recipe successfully created!',"recipe": [{"id": new_post.id,"title": new_post.title,"making_time": new_post.making_time,\
    "serves": new_post.serves,"ingredients": new_post.ingredients,"cost": new_post.cost,"created_at": new_post.created_at,"updated_at": new_post.updated_at}]})



@app.route('/recipes', methods=["GET"]) 
def allselect():
    posts = Post.query.all()
    #リストを作ってそれをそのまま辞書に入れる
    l=[]
    for i in range(0,len(posts)):
        st={'id': posts[i].id, 'title': posts[i].title, 'making_time': posts[i].making_time, 'serves': posts[i].serves, 'ingredients': posts[i].ingredients, 'cost': posts[i].cost}
        l.append(st)
    
    res={"recipes":l}
    return res

@app.route('/recipes/<int:id>', methods=["GET"]) 
def oneselect(id):
    
    post = Post.query.get(id)
    """
    if post==None:
        id=1
        post = Post.query.get(id)
    
    if post==None:
        return jsonify({"message": "No Recipe found"})
    """
    return jsonify({\
    "message": "Recipe details by id",\
    "recipe": [\
    {\
    "id": id,\
    "title": post.title,\
    "making_time": post.making_time,\
    "serves": post.serves,\
    "ingredients": post.ingredients,\
    "cost": post.cost,\
    }]})

@app.route('/recipes/<int:id>', methods=["PATCH"]) 
def update(id):
    
    post = Post.query.get(id)
    if post==None:
        id=1
        post = Post.query.get(id)    
    
    if post==None:
        return jsonify({"message": "Recipe details by id","recipe":[]})


    if("title" in request.form): 
        post.title=request.form.get("title")
    
    if("making_time" in request.form): 
        post.making_time=request.form.get("making_time")

    if("serves" in request.form): 
        post.serves=request.form.get("serves")

    if("ingredients" in request.form): 
        post.ingredients=request.form.get("ingredients")
    
    if("cost" in request.form): 
        post.const=request.form.get("cost")
    
    db.session.commit()

    return jsonify({\
    "message": "Recipe details by id",\
    "recipe": [\
    {\
    "id": id,\
    "title": post.title,\
    "making_time": post.making_time,\
    "serves": post.serves,\
    "ingredients": post.ingredients,\
    "cost": post.cost,\
    }]})

@app.route('/recipes/<int:id>', methods=["DELETE"]) # こちらに変更
def delete(id):
    
       
    if Post.query.get(id)==None:
        id=1
    
    post = Post.query.get(id)
    if post==None:
        return jsonify({"message": "No Recipe found"})

    else:
        db.session.delete(post)
        db.session.commit()
    
        return jsonify({"message": "Recipe successfully removed!"})


if __name__=="__main__":
    app.run(debug=True)