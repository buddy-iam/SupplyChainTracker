from flask import Flask, render_template, request, redirect, session, url_for, flash
from blockchain import Blockchain
from roles import CREDENTIALS, ROLES
from utils import generate_qr_code
from datetime import datetime
from collections import OrderedDict

app = Flask(__name__)
app.secret_key = 'secret_key_for_session'
bc = Blockchain()

# audit_logs for every new login
audit_logs = []

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form["role"]
        username = request.form["username"]
        password = request.form["password"]
        if role in CREDENTIALS and username == CREDENTIALS[role]["username"] and password == CREDENTIALS[role]["password"]:
            session["role"] = role

            audit_logs.append({
            "role": role,
            "action": "login",
            "product_id": None,
            "timestamp": datetime.now().timestamp()
            })

            flash("Logged in successfully.") 

            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials")
    return render_template("login.html", roles=ROLES)

@app.route("/dashboard")
def dashboard():
    if "role" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", role=session["role"])

@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if "role" not in session:
        return redirect(url_for("login"))

    role = session["role"]

    if request.method == "POST":
        product_id = request.form["product_id"]
        details = request.form["description"]

        # Role-specific logic
        if role.lower() == "manufacturer":
            description = f"Manufactured Product: {details}"
        elif role.lower() == "distributor":
            description = f"Shipped from warehouse or in transit: {details}"
        elif role.lower() == "retailer":
            description = f"Received and marked for sale: {details}"
        else:
            description = details  # fallback (shouldn't happen)

        # Add to blockchain
        bc.add_block({
            "product_id": product_id,
            "description": description,
            "by": role
        })

        audit_logs.append({
            "role": role,
            "action": "add_product",
            "product_id": product_id,
            "timestamp": datetime.now().timestamp()
        })


        flash(f"{role.title()} update recorded for Product ID {product_id}.")
        return redirect(url_for("dashboard"))

    return render_template("product_form.html", role=role)

@app.route("/track", methods=["GET", "POST"])
def track():
    if "role" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        pid = request.form["product_id"]
        history = bc.get_product_history(pid)

        # Detect if product is recalled by scanning blocks
        is_recalled = any(block.data.get("recall") for block in history)

        audit_logs.append({
            "role": session["role"],
            "action": "track",
            "product_id": pid,
            "timestamp": datetime.now().timestamp()
        })        

        qr = generate_qr_code(f"Product ID: {pid}")
        return render_template("view_history.html", history=history, pid=pid, qr=qr, is_recalled=is_recalled)

    return render_template("track_product.html")

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value).strftime(format)
    return value

@app.route("/recall", methods=["GET", "POST"])
def recall():
    if "role" not in session:
        return redirect(url_for("login"))
    role = session["role"]
    if role != "Manufacturer":
        flash("Only manufacturers can issue product recalls.")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        product_id = request.form["product_id"]
        recall_reason = request.form["recall_reason"]

        # Check if product exists in blockchain (at least one block)
        history = bc.get_product_history(product_id)
        if not history:
            flash("Product ID not found.")
            return redirect(url_for("recall"))

        # Append recall block on blockchain
        recall_description = f"⚠️ PRODUCT RECALLED: {recall_reason}"
        bc.add_block({
            "product_id": product_id,
            "description": recall_description,
            "by": role,
            "recall": True  # flag indicating this block is a recall notice
        })

        # Add to audit log
        audit_logs.append({
            "role": role,
            "action": "recall_product",
            "product_id": product_id,
            "timestamp": datetime.now().timestamp()
        })

        flash(f"Recall issued for Product ID {product_id}.")
        return redirect(url_for("dashboard"))

    return render_template("recall_form.html")


@app.route("/logout")
def logout():
    session.clear()

    flash("Logged out successfully.")
    return redirect(url_for("login"))

@app.route("/catalog")
def catalog():
    products = OrderedDict()
    for block in bc.chain[1:]:  # skip genesis block
        pid = block.data["product_id"]
        products[pid] = {
            "index": block.index,
            "by": block.data["by"],
            "description": block.data["description"],
            "timestamp": block.timestamp
        }
    # Log audit for viewing the catalog
    audit_logs.append({
        "role": session.get("role"),
        "action": "view_catalog",
        "product_id": None,
        "timestamp": datetime.now().timestamp()
    })

    flash("Loaded public product catalog.")
    return render_template("catalog.html", products=products)


@app.route("/audit")
def audit():
    # Log audit for viewing the audit log
    audit_logs.append({
        "role": session.get("role"),
        "action": "view_audit",
        "product_id": None,
        "timestamp": datetime.now().timestamp()
    })

    flash("Loaded audit log.")
    return render_template("audit.html", logs=audit_logs)


if __name__ == "__main__":
    app.run(debug=True)
