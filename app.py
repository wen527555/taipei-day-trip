from flask import Flask
from flask import request
from flask import render_template #幫助取出樣板檔案的內容，送到前端
from flask import session
from mysql.connector import pooling
from mysql.connector import Error
from flask import jsonify #使用jsonify模块来让网页直接显示json数据

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
#取得景點資料列表
# @app.route("/api/attractions",methods=["GET"]) 
# def attractions():

#根據景點編號取得景點資料
@app.route("/api/attraction/{attractionId}",methods=["GET"]) 
def attractionId():
    attractionId = request.args.get("id"," ")
    connection_object=connection_pool.get_connection()
    mycursor = connection_object.cursor
    sql = " SELECT (id, name, category, description, address, transport, mrt, lat, lng, images_image FROM attractions WHERE `attractionId`=%s"
    val = (attractionId,)
    mycursor.execute(sql,val)
    myresult=mycursor.fetchall()
    print(myresult)
    try:
    #     connection_object=connection_pool.get_connection() 
    #     cursor=connection_object.cursor()
    #     cursor.execute(sql,val)
    #     connection_object.commit()
      #使用jsonify来讲定义好的数据转换成json格式，并且返回给前端
        return jsonify({
                "data":{
                    "id":myresult["id"],
                    "name":myresult["name"],
                    "category":myresult["category"],
                    "description":myresult["description"],
                    "address":myresult["address"],
                    "transport":myresult["transport"],
                    "lat":myresult["lat"],
                    "lng":myresult["lng"],
                    "images":myresult["images_image"],
                }
            })
    except Error as e:
        return  jsonify ({"error":True},e)
    finally:
        # closing database connection.    
        mycursor.close()
        connection_object.close()
        print("DONE!") 
        return jsonify({
                "data":{
                    "id":myresult["id"],
                    "name":myresult["name"],
                    "category":myresult["category"],
                    "description":myresult["description"],
                    "address":myresult["address"],
                    "transport":myresult["transport"],
                    "lat":myresult["lat"],
                    "lng":myresult["lng"],
                    "images":myresult["images_image"],
                }
            })

    # sql = "INSERT INTO attractions (id, name, category, description, address, transport, mrt, lat, lng) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    # val = (id, name, category, description, address, transport, mrt, lat, lng)

    # try:
    # #  get the connection object from a connection pool
    #     connection_object=connection_pool.get_connection() 
    #     cursor=connection_object.cursor() #open MySQL
    #     cursor.execute(sql,val)
    #     connection_object.commit()
    # except Error as e:
    #     print("Error while connecting to MySQL using Connection pool ", e)
    # finally:
    # # closing database connection.    
    #     cursor.close()
    #     connection_object.close()
    # print("DONE") 


app.run(port=3000,debug=True)