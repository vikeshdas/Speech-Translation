from flask import Flask, render_template
import app

app1 = Flask(__name__)


@app1.route("/", methods=['POST','GET'])
def func():
    return render_template('new.html')

if __name__ == '__main__':
    app1.run(debug=True)  