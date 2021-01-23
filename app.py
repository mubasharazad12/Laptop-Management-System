from flask import Flask , render_template , request , redirect , flash , session
import DBhelper
app = Flask(__name__)

app.config['SECRET_KEY'] = "abc"

is_logged_in = False
username = ""
@app.route("/")
def homePage():
    return render_template("index.html" , title="Home")

@app.route("/client")
def client_page():
    if session["loggedIn"]:
        return render_template("client.html" , title="Client" , logged_in=is_logged_in , username=username)
    else:
        return render_template("errorPage.html")

@app.route("/services")
def services_page():
    return render_template("services.html" , title="Services")

@app.route("/order", methods=['POST', 'GET'] )
def order_page():
    return render_template("order.html" , title="Order")

@app.route("/order-done", methods=['POST', 'GET'])
def order_done():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        city = request.form['city']
        address = request.form['address']
        code = request.form['code']
        state = request.form['state']
        price = request.form['price']
        subject = request.form['subject']
        product = request.form['product']
        country = request.form['country']
        return render_template("order-done.html" , title="Order-done", name=name, email=email, phone=phone, city=city, address= address, 
        code= code, state=state, price=price, subject=subject, product= product, country=country)

@app.route("/dell")
def dell_service_page():
    return render_template("subpages/dell.html" , title="Dell")

@app.route("/acer")
def acer_service_page():
    return render_template("subpages/acer.html" , title="Acer")

@app.route("/lenovo")
def lenovo_service_page():
    return render_template("subpages/lenovo.html" , title="Lenovo")

@app.route("/register" , methods=['GET' , 'POST'])
def register():
    return render_template("register.html" , title="Register")

@app.route("/process_login" , methods=['GET' , 'POST'])
def process_login():
    global username
    if request.method == "POST":
        username = request.form['username']
        password = request.form['pass']
        input_type = request.form['submit']
        if input_type == 'Login':
            hashed_password = DBhelper.get_password_From_database(username)
            if hashed_password is not None:
                check = DBhelper.varify_password(hashed_password , password)
                if check:
                    session["loggedIn"] = True
                    return redirect("/")
                else:
                    flash("password is incorrect")
                    return redirect("/register")
            else:
                flash("username is incorrect")
                return redirect("/register")
        else :
            DBhelper.Insert_into_database(username , password)
            flash("register sucessfull please login")
            return redirect("/register")


@app.route("/updateProfile" , methods=["GET" , "POST"])
def updateProfile():
    if request.method == "POST":
        old_username = request.form["old_username"]
        old_password = request.form["old_pass"]
        new_username = request.form["new_username"]
        new_password = request.form["new_pass"]
        DBhelper.update_user_to_database(old_username , old_password , new_username , new_password)
        flash("username and password has been updated please login")
        return redirect("/register")
    
@app.route("/logout")
def logout():
    session["loggedIn"] = False
    flash("logout successfull")
    return redirect("/register")


if __name__ == '__main__':
    app.run(debug=True)