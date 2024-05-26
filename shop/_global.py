from flask import session,flash,redirect,url_for

def checkuser():
    if 'email' not in session:
        flash(f"Please Login first","danger")
        return redirect(url_for('login'))
    else:
        return True