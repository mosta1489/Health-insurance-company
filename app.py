from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    jsonify)
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
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('password')

        if (user, password) == ('admin', 'admin'):
            return redirect(url_for('admin'))

        else:
            # return jsonify({'data_user': data})
            return redirect(f'/customer?user={user}&password={password}')


@app.route('/insert_customer', methods=['POST'])
def insert_customer():

    return redirect('/')


@app.route('/insert_hospital', methods=['POST'])
def insert_hospital():

    return redirect('/')


@ app.route('/admin')
def admin():
    return render_template('admin.html')


@ app.route('/customer', methods=['POST', 'GIT'])
def customer():
    user = request.args.get('user')
    password = request.args.get('password')
    return render_template('customer.html', user=user, password=password)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
