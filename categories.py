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

#取得所有的景點分類名稱列表
@app.route("/api/categories",methods=["GET"]) 
def categories():

    try:
        connection_object=connection_pool.get_connection()
        mycursor = connection_object.cursor()
        mycursor.execute("SELECT category FROM attractions")
        categories = mycursor.fetchall()
        results=[]
        for category in categories:
            category=category[0]
            if(category in results):
                continue
            else:
                results.append(category)
                print(results)
        return jsonify({
            "data": results
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