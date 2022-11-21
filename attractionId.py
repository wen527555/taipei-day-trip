from flask import Flask
from mysql.connector import pooling
from flask import jsonify

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
app.config["JSON_AS_ASCII"] = False #把對象序列化為ASCII-encoded JSON 
app.config["TEMPLATES_AUTO_RELOAD"] = True #當模板改變時重載
app.config['JSON_SORT_KEYS'] = False



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

app.run(port=3000,debug=True)