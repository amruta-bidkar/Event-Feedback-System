from flask import *
from flask import jsonify
import sqlite3
app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/events")
def events():
    return render_template("events.html")


@app.route("/feedback")
def feedback():
    return render_template("feedback.html")



@app.route("/saveform" , methods=["POST"])
def saveform():
    
        n=request.form["name"]
        en=request.form["event_name"]
        r=request.form["rating"]
        co=request.form["comments"]

        con=sqlite3.connect("database.db", timeout=5)
        c=con.cursor()

        c.execute("insert into feedback(name,event_name,rating,comments) values (?,?,?,?) ",(n,en,r,co))
        con.commit()
        con.close()
        return render_template("index.html")



@app.route("/view")
def view():
    con=sqlite3.connect("database.db")
    c=con.cursor()
    c.execute("select * from feedback")
    data=c.fetchall()

    con.commit()
    con.close()

    return render_template("view.html",data=data)




@app.route("/deletefeedback/<int:id>")
def deletefeedback(id):
     con=sqlite3.connect("database.db")
     c=con.cursor()
     c.execute("DELETE FROM feedback WHERE id=?",[id])
    
     con.commit()
     con.close()
     return redirect(url_for("view"))





@app.route("/update/<int:id>")
def updatepage(id):
    con = sqlite3.connect("database.db")
    c = con.cursor()

    c.execute("SELECT * FROM feedback WHERE id=?", (id,))
    data = c.fetchone()

    con.close()
    return render_template("update.html", data=data)


# @app.route("/update", methods=["POST"])
@app.route("/update", methods=["POST"])
def update():
    if request.method == "POST":
        id = request.form["id"]
        n = request.form["name"]
        en = request.form["event_name"]
        r = request.form["rating"]
        co = request.form["comments"]

        con = sqlite3.connect("database.db")
        c = con.cursor()

        c.execute("UPDATE feedback SET  name=?,event_name=?,rating=?,comments=? WHERE id=?", ( n, en, r, co,id))

        con.commit()
        con.close()

    return redirect(url_for("view"))



# API connectivity to get all data

@app.route("/api/feedback",methods=["GET"])
def getfeedback():
    con=sqlite3.connect("database.db")
    c=con.cursor()

    c.execute("select * from feedback")
    row=c.fetchall()

    feedback_list=[]

    for i in row:
        feedback_list.append({
            "id":i[0],
            "name":i[1],
            "event_name":i[2],
            "rating":i[3],
            "comments":i[4],

        })

    con.close()
    return jsonify(feedback_list)

# api to insert feedback(create data)

@app.route("/api/feedback",methods=["POST"])
def insertedfeedback():

    data=request.json

    name=data["name"]
    event_name=data["event_name"]
    rating=data["rating"]
    comments=data["comments"]

    con=sqlite3.connect("database.db")
    c=con.cursor()

    c.execute("INSERT INTO feedback(name,event_name,rating,comments) VALUES(?,?,?,?)",(name, event_name, rating, comments))

    con.commit()
    con.close()

    return jsonify({"message":"feedback added successfully"})


#api update

@app.route("/api/feedback/<int:id>", methods=["PUT"])
def update_feedback(id):
    data = request.json

    con = sqlite3.connect("database.db")
    c = con.cursor()

    c.execute(
        "UPDATE feedback SET name=?, event_name=?, rating=?, comments=? WHERE id=?",
        (data["name"], data["event_name"], data["rating"], data["comments"], id)
    )
    con.commit()
    con.close()

    return jsonify({"message": "Feedback updated"})

# delete
@app.route("/api/feedback/<int:id>", methods=["DELETE"])
def delete_feedback(id):

    con = sqlite3.connect("database.db")
    c = con.cursor()

    c.execute("DELETE FROM feedback WHERE id=?", (id,))

    con.commit()
    con.close()

    return jsonify({"message": "Feedback deleted"})




if __name__=='__main__':
    app.run(debug=True)






