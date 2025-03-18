from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session handling

# Dummy user data (In a real application, you'd use a database)
users = {
    "testuser": "password123",  # username: password
    "admin": "adminpass"
}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            if users[username] == password:
                session["user"] = username  # Store user session
                return redirect(url_for("dashboard"))
            else:
                flash("Password incorrect", "error")
        else:
            flash("Unregistered user", "error")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html", username=session["user"])
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)

