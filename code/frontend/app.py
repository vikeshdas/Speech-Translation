from flask import Flask, render_template
# import app

app = Flask(__name__)


@app.route("/", methods=['POST','GET'])
def func():

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)  