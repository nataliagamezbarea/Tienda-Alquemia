from flask import render_template, redirect, url_for, session

def pagar():
    if "user" not in session or not session.get("user"):
        return redirect(url_for('login'))  
    return render_template("user/pagar/pagar.html")
