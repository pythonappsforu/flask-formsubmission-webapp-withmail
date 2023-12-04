from datetime import datetime
from flask import Flask, render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = "yt%$#vg23657hKJj"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_ECHO"] = True
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.getenv("EMAIL")
app.config["MAIL_PASSWORD"] = os.getenv("PASSWORD")

db = SQLAlchemy(app)

mail = Mail(app)

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

        message_body = f"Thank you for your submission, {first_name}."\
                        f"Here are your data,\n"\
                        f"{first_name}\n"\
                        f"{last_name}\n"\
                        f"{date}"

        message = Message(subject="New from submission!",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=message_body)

        mail.send(message)
        flash(f"{first_name}, Your form submitted successfully!","success")
        return redirect(url_for('home'))

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
