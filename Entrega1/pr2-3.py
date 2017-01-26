from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/user/")
@app.route("/user/<name>")

def hello(name=None):
	return render_template("user.html",name=name)

if __name__ == "__main__":
	app.run(host='0.0.0.0')
