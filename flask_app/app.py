from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database connection
def get_db_connection():
    return pymysql.connect(
        host="localhost",   # Use your PythonAnywhere MySQL host when deploying
        user="root",
        password="Jayesh@12345",
        database="jayesh"
    )

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        con_pass = request.form["con_pass"]

        if not (first_name and last_name and email and password and con_pass):
            flash("All fields are required!", "warning")
        elif password != con_pass:
            flash("Passwords do not match!", "danger")
        else:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                query = "INSERT INTO jay (first_name, last_name, email, passw, con_pass) VALUES (%s, %s, %s, %s, %s)"
                values = (first_name, last_name, email, password, con_pass)
                cursor.execute(query, values)
                conn.commit()
                flash("Registration successful!", "success")
                return redirect(url_for("success"))

            except pymysql.Error as e:
                flash(f"Database error: {e}", "danger")
            finally:
                cursor.close()
                conn.close()

    return render_template("index.html")

@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
