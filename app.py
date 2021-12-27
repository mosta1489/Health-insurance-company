from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request, )
from mysql.connector import connect

global db
db = connect(host='localhost',
             database='Insurance Company',
             user='root',
             password='mosta')


def select(quary):
    cr = db.cursor()
    cr.execute(quary)
    data = cr.fetchall()
    return data


app = Flask(__name__)


# ---------------------------------------------------------------------------------------
# --------------------------- Main Page -------------------------------------------------

@app.route('/')
def main():
    return render_template('index.html')


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------
# ---------------------------- login part -----------------------------------------------

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('password')

        if (user, password) == ('admin', 'admin'):
            return redirect('/admin')

        else:
            # cr = db.cursor()
            # cr.execute(f'SELECT password FROM customers WHERE user_name="{user}";')
            # test_pass = cr.fetchall()

            '''
            test_pass = select(
                f'SELECT password FROM customers WHERE user_name="{user}";')
            if password == test_pass:
                return redirect(f'/customer?user={user}')
            '''

            return redirect(f'/customer?user={user}')

            # return render_template('customer.html', user_name=user)

    return redirect('/')


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------
# -------------------------- Add New Customer -------------------------------------------

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
        cr.commit()
        
        # Insert Into Plan Table
        cr.execute(f"INSERT INTO Plan(type, owner) VALUES('{plan_type}', '{user_name}');")
        cr.commit()

        # get id of this new plan
        cr.execute(f"SELECT plan_id FROM plan WHERE owner='{user_name}'")
        plan_id = cr.fetchone()

        # Insert Into Dependent Table
        cr.execute(f"INSERT INTO Plan(name, plan, relation) VALUES('{user_name}', '{plan_id}', {'owner'} );")
        cr.commit()
        

        cr.close()
        
        '''
    return redirect('/')


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------
# -------------------------- Add New Hospital -------------------------------------------

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
        cr.execute(f'SELECT name FROM hospital WHERE name="{hospital_name}";')
        users = cr.fetchall()
        if users:  # if returned list has values that mean user already exist
            return redirect('/')

        # insert hospital data in hospital table
        cr.execute(f"INSERT INTO hospital (name, location, phone)"
                   f" values('{hospital_name}', '{location}', '{phone}');")
        
        cr.commit()
        
        # get hospital_id of new hospital
        cr.execute(f"SELECT id FROM hospital WHERE name='{hospital_name}';")
        hospital_id = cr.fetchone()

        # insert data to cover table
        for type in plan_type_list:
            cr.execute(f"INSERT INTO cover (hospital, plan)"
                       f" values('{hospital_id}', '{type}');")
        
        cr.commit()
        
        
        cr.close()

        '''

        # return render_template('admin.html', plan_type=plan_type_list)

    return redirect('/')


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------
# ------------------------------ Admin Page ---------------------------------------------

@app.route('/admin')
def admin():
    return render_template('admin.html')


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# -------------------------- Customer Page ----------------------------------------------

@app.route('/customer', methods=["GET"])
def customer():
    user = request.args.get('user')

    '''
    cr = db.cursor()
    cr.execute(f"SELECT plan_id FORM plan WHERE owner='{user}'")
    plans_list = cr.fetchall()
    plans = [plan[0] for plan in plans_list]


    cr.execute(f"")
    
    available_hospital_list = cr.fetchall()

    '''

    return render_template('customer.html',
                           user=user)  # , plans_list=plans, available_hospital= available_hospital_list)


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------
# ------------- Purchase Plan in Customer Page ------------------------------------------

@app.route('/customer/purchase_plan', methods=["POST"])
def customer_purchase_plan():
    if request.method == "POST":
        plan_type = request.form.get('plan_type')
        user = request.form.get('user')

        '''
        cr = db.cursor()
        cr.execute(f"INSERT INTO plan (type, owner) VALUES('{plan_type}', '{user}')")
        
        cr.commit()
        cr.close()
        '''

    return redirect('/customer')


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------
# ------------- Add Dependent in Customer Page ------------------------------------------


@app.route('/customer/add_dependent', methods=["POST"])
def add_dependent():
    if request.method == "POST":
        dependent_name = request.form.get('dependent_name')
        plan_id = request.form.get('plan_id')
        relationship = request.form.get('relationship')

        '''
        cr = db.cursor()
        cr.execute(
            f"INSERT INTO dependent (name, plan, relationship) VALUES('{dependent_name}', '{plan_id}', '{relationship}')")
            
            cr.commit()
            cr.close()
        '''

    return redirect('/customer')


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

@app.route('/customer/file_claim', methods=["POST"])
def file_claim():
    if request.method == "POST":
        description = request.form.get('description')
        plan_id = request.form.get('plan_id')
        solved = 'False'

        '''
        cr = db.cursor()
        cr.execute(f"INSERT INTO claim (plan, solved, description) VALUES ('{description}', '{plan_id}', '{solved}')")

        cr.commit()

        cr.close()
        '''
    return redirect('/customer')


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True, port=8000)
