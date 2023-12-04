from datetime import datetime
from flask import Flask, render_template,request,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = "yt%$#vg23657hKJj"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

class Form(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


@app.route("/",methods=["GET", "POST"])
def home():
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        date = request.form['date']
        dateobj = datetime.strptime(date,"%Y-%m-%d")
        occupation = request.form['occupation']

        form = Form(first_name=first_name,last_name=last_name,email=email,
                    occupation=occupation,date=dateobj)
        db.session.add(form)
        db.session.commit()
        flash(f"{first_name}, Your form submitted successfully!","success")
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
