from flask import Flask
from flask import request
from flask import render_template #幫助取出樣板檔案的內容，送到前端
from flask import session
from mysql.connector import pooling
from flask import jsonify 
import math
from mysql.connector import Error

connection_pool=pooling.MySQLConnectionPool(
                                            pool_name="mysqlpool",
                                            pool_size=5,
                                            pool_reset_session='True',
                                            host='localhost',
                                            database='taipei_day_trip',
                                            user='root',
                                            password='wh1999ne123')
app=Flask(__name__)
app.secret_key="any string but secret"


#Pages
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
    return render_template("attraction.html")
@app.route("/booking")
def booking():
    return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

@app.route("/error", methods=["GET"]) 
def error():
    massage=request.args.get("massage","")
    return render_template("error.html",massage=massage)

#取得景點資料
@app.route("/api/attractions",methods=["GET"]) 
def attractions():

    try:
        input_Page=request.args.get("page") 
        input_Page=int(input_Page)
        next_Page=int(input_Page)+1
        input_keyword=request.args.get("keyword")
        connection_object=connection_pool.get_connection()
        mycursor = connection_object.cursor(dictionary=True)
        mycursor.execute("SELECT COUNT(`id`) FROM `attractions` ")
        total_data = mycursor.fetchone()
        total_data= total_data["COUNT(`id`)"]
        total_Page=math.floor(total_data/12)
        if total_Page == input_Page:
            next_Page = None
        # print(total_Page)
        if input_keyword != None:
            mycursor.execute("SELECT * FROM attractions WHERE category=%s or LOCATE( %s ,`name`)  LIMIT %s,12 ", [input_keyword,input_keyword,(input_Page*12)])
            myresult = mycursor.fetchall()
            if len(myresult)<12:
                next_Page = None
            # print(myresult)
            result_all=[]
            for result in myresult:
                new_images=[]
                images=result["images"].split(",")
                for n in range(len(images)):
                    images_https=images[n]
                    new_images.append(images_https)
                result_all.append(
                    {
                        "id":result["id"],
                        "name":result["name"],
                        "category":result["category"],
                        "description":result["description"],
                        "address":result["address"],
                        "transport":result["transport"],
                        "lat":result["lat"],
                        "lng":result["lng"],
                        "images":new_images           
                    })
                if total_Page >= input_Page:        
                    result ={
                        "nextPage":next_Page,
                        "data": result_all
                    } 
                    ans=jsonify(result)
                else:
                    error ={
                        "error":True,
                        "message":"無此頁面"
                    }
                    ans=jsonify(error)
        else:
            mycursor.execute("SELECT * FROM attractions ORDER BY id LIMIT %s,12 ", [(input_Page*12)])  
            myresult = mycursor.fetchall()
            result_all=[]
            for result in myresult:
                new_images=[]
                images=result["images"].split(",")
                for n in range(len(images)):
                    images_https=images[n]
                    new_images.append(images_https)
                result_all.append(
                    {
                        "id":result["id"],
                        "name":result["name"],
                        "category":result["category"],
                        "description":result["description"],
                        "address":result["address"],
                        "transport":result["transport"],
                        "lat":result["lat"],
                        "lng":result["lng"],
                        "images":new_images           
                    })
                if total_Page >= input_Page:        
                    result ={
                        "nextPage":next_Page,
                        "data": result_all
                    } 
                    ans=jsonify(result)
                else:
                    error ={
                        "error":True,
                        "message":"無此頁面"
                    }
                    ans=jsonify(error)
        return ans
    except :
        return jsonify ({
                "error":True,
                "message":"伺服器內部錯誤"
            })
    finally:    
        mycursor.close()
        connection_object.close()
        print("DONE") 


#根據景點編號取得景點資料
@app.route("/api/attraction/<attractionId>",methods=["GET"]) 
def getattraction(attractionId):
    try:
        connection_object=connection_pool.get_connection()
        mycursor = connection_object.cursor(dictionary=True)
        mycursor.execute("SELECT COUNT(`id`) FROM `attractions` ")
        nums = mycursor.fetchone()
        nums= nums["COUNT(`id`)"]
        if int(nums)<int(attractionId):
            return  jsonify ({
                "error":True,
                "message":"景點編號不正確"
            }) 
        if int(nums)>=int(attractionId):
            mycursor.execute("SELECT * FROM attractions WHERE  id=%s", [attractionId])
            myresult=mycursor.fetchone()
            result_all=[]
            new_images=[]
            images=myresult["images"].split(",")
            # if '' in images:
            # images.remove('')
            for n in range(len(images)):
                images_https=images[n]
                new_images.append(images_https)

            result_all=(
                {
                    "id":myresult["id"],
                    "name":myresult["name"],
                    "category":myresult["category"],
                    "description":myresult["description"],
                    "address":myresult["address"],
                    "transport":myresult["transport"],
                    "lat":myresult["lat"],
                    "lng":myresult["lng"],
                    "images":new_images
                        
                    })
            return jsonify({
                "data": result_all
            })
    except :
        return  jsonify ({
                "error":True,
                "message":"伺服器內部錯誤"
            })
    finally:   
        mycursor.close()
        connection_object.close()
        print("DONE") 

#旅遊景點分類
@app.route("/api/categories",methods=["GET"]) 
def categories():
    try:
        connection_object=connection_pool.get_connection()
        mycursor = connection_object.cursor(dictionary=True)
        mycursor.execute("SELECT distinct category FROM `attractions` ")
        myresult = mycursor.fetchall()
        print(myresult)
        categories=[]

        for x in myresult:
            n = x['category']
            categories.append(n)
        return jsonify({
            "data":categories
            })

    except :
        return  jsonify ({
                "error":True,
                "message":"伺服器內部錯誤"
            })
    finally:   
        mycursor.close()
        connection_object.close()
        print("DONE") 


app.run(host='0.0.0.0',port=3000,debug=True)