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
            '''
            test_pass = select(
                f'SELECT password FROM customers WHERE user_name="{user}";')
            if password == test_pass:
                return redirect(f'/customer?user={user}')
            '''
            return redirect(f'/customer?user={user}')

    return redirect('/')


@app.route('/insert_customer', methods=['POST'])
def insert_customer():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        customer_name = request.form.get('customer_name')
        phone = request.form.get('phone')
        password = request.form.get('password')
        # plan_type = request.form.get('plan_type')
        plan_type = 'Basic'

        '''
        
        cr = db.cursor()

        # check if new user_name is already exist or not
        cr.execute(f'SELECT user_name FROM customer WHERE user_name="{user_name}";')
        users = cr.fetchall()
        if users:  # if returned list has values that mean user already exist
            return redirect('/')

        # Insert Into customer table
        cr.execute(f"INSERT INTO customers(user_name,name ,phone, password)"
                   f" VALUES('{user_name}', '{customer_name}', '{phone}', '{password}' );")

        # Insert Into Plan Table
        cr.execute(f"INSERT INTO Plan(type, owner) VALUES('{plan_type}', '{user_name}');")

        # get id of this new plan
        cr.execute(f"SELECT plan_id FROM plan WHERE owner='{user_name}'")
        plan_id = cr.fetchone()

        # Insert Into Dependent Table
        cr.execute(f"INSERT INTO Plan(name, plan, relation) VALUES('{user_name}', '{plan_id}', {'owner'} );")

        cr.close()
        
        '''
    return redirect('/')


@app.route('/insert_hospital', methods=['POST', 'GET'])
def insert_hospital():
    if request.method == 'POST':
        hospital_name = request.form.get('hospital_name')
        location = request.form.get('location')
        phone = request.form.get('phone')
        plan_type_list = request.form.getlist('plan_type')

        '''
        
        cr = db.cursor()

        # check if new hospital is already exist or not
        cr.execute(f'SELECT user_name FROM customer WHERE user_name="{hospital_name}";')
        users = cr.fetchall()
        if users:  # if returned list has values that mean user already exist
            return redirect('/')

        # insert hospital data in hospital table
        cr.execute(f"INSERT INTO hospital (name, location, phone)"
                   f" values('{hospital_name}', '{location}', '{phone}');")

        # get hospital_id of new hospital
        cr.execute(f"SELECT id FROM hospital WHERE name='{hospital_name}';")
        hospital_id = cr.fetchone()

        # insert data to cover table
        for type in plan_type_list:
            cr.execute(f"INSERT INTO cover (hospital, plan)"
                       f" values('{hospital_id}', '{type}');")
        
        cr.close()
        
        '''

        return render_template('admin.html', plan_type=plan_type_list)

    return redirect('/')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/customer', methods=["GET"])
def customer():
    user = request.args.get('user')
    password = request.args.get('password')
    return render_template('customer.html', user=user, password=password)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
