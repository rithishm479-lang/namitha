from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

# Create DB
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/shop')
def shop():
    if "user" not in session:
        return redirect('/login')

    products = [

    {"name": "Necklace 1", "price": "₹499", "img": "necklace1.jpg"},
    {"name": "Necklace 2", "price": "₹456", "img": "necklace2.jpg"},
    {"name": "Necklace 3", "price": "₹560", "img": "necklace3.jpg"},
    {"name": "Necklace 4", "price": "₹599", "img": "necklace4.jpg"}

    ]
    return render_template("shop.html", products=products)

@app.route('/about')
def about():
    return render_template("about.html")

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template("register.html")

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user'] = username
            return redirect('/shop')
        else:
            return "Invalid login"

    return render_template("login.html")

# LOGOUT
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)