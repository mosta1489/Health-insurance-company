from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    flash)

from mysql.connector import connect

global db
db = connect(host='localhost',
             database='insurance company',
             user='root',
             password='mosta')

app = Flask(__name__)
app.secret_key = "super secret key"


# ---------------------------------------------------------------------------------------
# --------------------------- Main Page -------------------------------------------------

@app.route('/')
def main():
    return render_template('index.html')


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------
# ---------------------------- login part ----------------------------------------------->>>>>>> DONE <<<<<<<----------

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('password')

        if (user, password) == ('admin', 'admin'):
            return redirect('/admin')

        else:

            cr = db.cursor()

            cr.execute(f'SELECT user_name FROM customer WHERE user_name="{user}";')

            user_name = cr.fetchall()
            if not user_name:
                flash('username Is not exists', 'error')

            else:
                cr.execute(f'SELECT password FROM customer WHERE user_name="{user}";')

                test_pass = cr.fetchone()

                if password == test_pass[0]:
                    return redirect(f'/customer?user={user}')

                else:
                    flash('Incorrect username or password.. Try again', 'error')

            # return render_template('customer.html', user_name=user)

    return redirect('/')


# --------------------------------------------------------------------------------------->>>>>>> DONE <<<<<<<----------
# ---------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------
# -------------------------- Add New Customer ------------------------------------------->>>>>>> DONE <<<<<<<----------

@app.route('/insert_customer', methods=['POST'])
def insert_customer():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        phone = request.form.get('phone')
        plan_type = request.form.get('plan_type')

        cr = db.cursor()

        # check if new user_name is already exist or not
        cr.execute(f'SELECT user_name FROM customer WHERE user_name="{user_name}";')
        users = cr.fetchall()

        if users:  # if returned list has values that mean user already exist
            flash('This user name already exist', 'error')
            return redirect('/')

        # Insert Into customer table
        cr.execute(f"INSERT INTO customer(user_name,name ,phone, password)"
                   f" VALUES('{user_name}', '{customer_name}', '{phone}', '{password}' );")
        #
        #         # Insert Into Plan Table
        cr.execute(f"INSERT INTO plans(type, owner) VALUES('{plan_type}', '{user_name}');")

        # get id of this new plan
        cr.execute(f"SELECT plan_ID FROM plans WHERE owner='{user_name}'")
        plan_id = cr.fetchone()[0]

        # Insert Into Dependent Table
        cr.execute(f"INSERT INTO dependents (name, relationship, plan) VALUES('>{user_name}<' , 'owner', '{plan_id}');")

        db.commit()
        cr.close()

        flash('A new customer has been added successfully', 'success')

        return redirect('/')


# --------------------------------------------------------------------------------------->>>>>>> DONE <<<<<<<----------
# ---------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------
# -------------------------- Add New Hospital ------------------------------------------->>>>>>> DONE <<<<<<<----------

@app.route('/insert_hospital', methods=['POST', 'GET'])
def insert_hospital():
    if request.method == 'POST':
        hospital_name = request.form.get('hospital_name')
        location = request.form.get('location')
        phone = request.form.get('phone')
        plan_type_list = request.form.getlist('plan_type')

        if not plan_type_list:
            flash('Pleas choose type of plan', 'error')
            return redirect('/')

        cr = db.cursor()

        # check if new hospital is already exist or not
        cr.execute(f'SELECT name FROM hospital WHERE name="{hospital_name}";')
        users = cr.fetchall()

        if users:  # if returned list has values that mean hospital already exist
            flash('This Hospital already exist', 'error')
            return redirect('/')

        # insert hospital data in hospital table
        cr.execute(f"INSERT INTO hospital (name, location, phone)"
                   f" values('{hospital_name}', '{location}', '{phone}');")

        # insert data to cover table
        for type in plan_type_list:
            cr.execute(f"INSERT INTO covers (hospital, plan_type)"
                       f" values('{hospital_name}', '{type}');")

        db.commit()
        cr.close()

        flash('A new hospital has been added successfully', 'success')

        # return render_template('admin.html', plan_type=plan_type_list)

        return redirect('/')


# --------------------------------------------------------------------------------------->>>>>>> DONE <<<<<<<----------
# ---------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------>>>>>>> DONE <<<<<<<-------------
# ------------------------------ Admin Page ---------------------------------------------

@app.route('/admin')
def admin():
    cr = db.cursor()
    cr.execute("SELECT user_name, name, phone FROM customer;")
    customers_list = cr.fetchall()

    return render_template('admin.html', customers_list=customers_list)


# -------------------------------------------------------------------------------->>>>>>> DONE <<<<<<<-----------------
# ----------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------->>>>>>> DONE <<<<<<<---------------
# ----------------------- show_all_claims -------------------------------------------------

@app.route('/admin/show_all_claims', methods=['GET'])
def show_all_claims():
    user = request.args.get('user')

    cr = db.cursor()

    cr.execute(
        "SELECT claim_ID, beneficiary, CONVERT(cost, CHAR), date_of_claim, state, description FROM claims WHERE plan "
        f"IN (SELECT plan_ID FROM plans WHERE owner='{user}');")

    claims_list = cr.fetchall()

    cr.close()

    return render_template('claims.html', claims_list=claims_list, user=user)


# ------------------------------------------------------------------  >>>>>>> DONE <<<<<<<-----------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------ >>>>>>> DONE <<<<<<<------------------------------------
# ---------------------- show_unresolved_claims -----------------------------------------------------------------------

@app.route('/admin/show_unresolved_claims', methods=['GET'])
def show_unresolved_claims():
    user = request.args.get('user')

    cr = db.cursor()
    cr.execute(
        "SELECT claim_ID, beneficiary, CONVERT(cost, CHAR), date_of_claim, state, description  FROM claims WHERE plan "
        f"IN (SELECT plan_ID FROM plans WHERE owner='{user}') and state='unresolved' ;")

    claims_list = cr.fetchall()

    cr.close()

    return render_template('claims.html', claims_list=claims_list, user=user)


# ------------------------------------------------------------ >>>>>>> DONE <<<<<<<---------------------------------
# -------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------- >>>>>>> DONE <<<<<<<---------------------------------
# -----------------------  make_claim_resolved ---------------------------------------------------------------------

@app.route('/make_claim_resolved', methods=['GET'])
def make_claim_resolved():
    user = request.args.get('user')
    claim_id = request.args.get('claim_id')

    cr = db.cursor()

    cr.execute(f"UPDATE claims SET state='resolved' WHERE claim_ID='{claim_id}';")

    db.commit()
    cr.close()

    flash("Status of Claims Has Been Edited Successfully", 'success')
    return redirect(f"/admin/show_all_claims?user={user}")


# --------------------------------------------------------------------------------------->>>>>>> DONE <<<<<<<----------
# --------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------
# -------------------------- Customer Page ---------------------------------------------->>>>>>> DONE <<<<<<<----------

@app.route('/customer', methods=["GET"])
def customer():
    user = request.args.get('user')

    cr = db.cursor()
    # Get all plans purchased by this customer
    cr.execute(f"SELECT plan_ID FROM plans WHERE owner='{user}';")
    plans_list_tuple = cr.fetchall()
    plans_list = [plan[0] for plan in plans_list_tuple]

    # Get all Hospital Available to this customer
    cr.execute(f"SELECT * FROM hospital WHERE name"
               f" IN (SELECT hospital FROM covers WHERE plan_type "
               f" IN (SELECT DISTINCT type FROM plans WHERE owner='{user}'));")

    available_hospital_list = cr.fetchall()

    # user = 'mosta148'

    # Get all Dependants for this customer
    cr.execute(f"SELECT name FROM dependents WHERE plan in( SELECT plan_ID FROM plans WHERE owner='{user}');")
    dependents_tuple = cr.fetchall()
    dependents_list = [depend[0] for depend in dependents_tuple]

    # get name of this customer to print in page
    cr.execute(f"SELECT name FROM customer WHERE user_name='{user}';")
    customer_tuple = cr.fetchall()
    customer_name = customer_tuple[0][0]

    cr.close()

    return render_template('customer.html',
                           customer_name=customer_name, user=user, plans_list=plans_list,
                           available_hospital=available_hospital_list, dependents_list=dependents_list)


# --------------------------------------------------------------------------------------->>>>>>> DONE <<<<<<<----------
# ---------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------
# ------------- Purchase Plan in Customer Page ------------------------------------------>>>>>>> DONE <<<<<<<----------

@app.route('/customer/purchase_plan', methods=["POST"])
def customer_purchase_plan():
    if request.method == "POST":
        plan_type = request.form.get('plan_type')

        user = request.form.get('user')  # this is a hidden input sent with plan type input

        cr = db.cursor()

        # Insert Into Plan Table
        cr.execute(f"INSERT INTO plans(type, owner) VALUES('{plan_type}', '{user}');")

        db.commit()
        cr.close()

        flash('Successfully purchased a new plan', 'success')
        return redirect(f"/customer?user={user}")


# --------------------------------------------------------------------------------------->>>>>>> DONE <<<<<<<----------
# ---------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------
# ------------- Add Dependent in Customer Page ------------------------------------------>>>>>>> DONE <<<<<<<----------

@app.route('/customer/add_dependent', methods=["POST"])
def add_dependent():
    if request.method == "POST":
        new_dependent_name = request.form.get('dependent_name')
        relationship = request.form.get('relationship')
        plan_id = request.form.get('plan_id')

        user = request.form.get('user')  # this is a hidden input sent with plan type input

        cr = db.cursor()

        # Get all Dependants for this customer
        cr.execute(f"SELECT name FROM dependents WHERE plan in( SELECT plan_ID FROM plans WHERE owner='{user}');")
        dependents_tuple = cr.fetchall()
        dependents_list = [depend[0] for depend in dependents_tuple]

        if new_dependent_name in dependents_list:
            flash('This dependent name already exists', 'error')
            return redirect(f'/customer?user={user}')

        else:
            cr.execute(
                f"INSERT INTO dependents (name, relationship, plan)"
                f" VALUES('{new_dependent_name}', '{relationship}', '{plan_id}');")

            db.commit()
            cr.close()

            flash('A new dependent has been added successfully', 'success')
            return redirect(f'/customer?user={user}')


# --------------------------------------------------------------------------------------->>>>>>> DONE <<<<<<<----------
# ---------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------
# --------------------- File New Claim -------------------------------------------------- >>>>>>> DONE <<<<<<<----------

@app.route('/customer/file_claim', methods=["POST"])
def file_claim():
    if request.method == "POST":

        user = request.form.get('user')  # this is a hidden input sent with plan type input
        cost = request.form.get('cost')

        for i in cost:
            if i.islower() or i.isupper():
                flash('Invalid data entry ', 'error')
                return redirect(f'/customer?user={user}')

        str_cost = str(cost)
        if len(str_cost) > 4:
            if ('.' in str_cost) and not (str_cost.index('.') > 4):
                pass
            else:
                flash('The cost value is rejected', 'error')
                return redirect(f'/customer?user={user}')


        description = request.form.get('description')
        beneficiary = request.form.get('beneficiary')
        user = request.form.get('user')  # this is a hidden input sent with plan type input

        cr = db.cursor()

        # get plan_id of this beneficiary
        cr.execute(f"SELECT plan_ID FROM plans"
                   f" WHERE owner='{user}'"
                   f" AND plan_ID IN ( SELECT plan FROM dependents WHERE name='{beneficiary}');")

        plan_id = cr.fetchall()[0][0]

        cr.execute(f"INSERT INTO claims (plan,  description, cost, beneficiary)"
                   f" VALUES ('{plan_id}', '{description}', '{cost}', '{beneficiary}')")

        db.commit()
        cr.close()

        flash('A new Claim has been added successfully', 'success')
        return redirect(f'/customer?user={user}')


# --------------------------------------------------------------------------------------- >>>>>>> DONE <<<<<<<---------
# ---------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True, port=8000)
