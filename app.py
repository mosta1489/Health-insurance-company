from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request)
from mysql.connector import connect

global db
db = connect(host='localhost',
             database='project_1',
             user='root',
             password='mosta')


def select(quary):
    cr = db.cursor()
    cr.execute(quary)
    data = cr.fetchall()
    cr.close()
    return data


app = Flask(__name__)


@app.route('/')
def main():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
