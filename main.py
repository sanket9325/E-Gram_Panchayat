from flask import Flask, flash, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb
from urllib.parse import urlencode
import json
import os
import math
import random
import string
from datetime import date

app = Flask(__name__)
mysql = MySQL(app)

app.secret_key = os.urandom(24).hex()
app.tran_id = os.urandom(7).hex()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gram_panchayat'
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = 'static/upload'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def generate_id(col, table):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT " + col + " FROM " + table + " ORDER BY " + col + " DESC")
    id_data = cursor.fetchone()
    if id_data is None or id_data[col] is None:
        return "1"
    else:
        id = int(id_data[col]) + 1
        return str(id)



@app.route("/")
def index():
    return render_template('index.html')

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT ward_no FROM ward")
    ward_data = cursor.fetchall()
    if request.method == 'POST':
        name = request.form['txtname']
        email = request.form['txtemail']
        mobile = request.form['txtmobile']
        voter = request.form['txtvoter']
        aadhar = request.form['txtaadhar']
        ward_no = request.form['txtward']
        gender = request.form['gender']
        address = request.form['txtaddress']
        username = request.form['txtusername']
        password = request.form['txtpassword']
        photo = request.files['fuimage']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM registration WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        if user_data:
            alert_script = """
                <script>
                    function showAlert() {
                        Swal.fire({
                            title: 'Oops...',
                            text: 'Username already exists!',
                            icon: 'error'
                        });
                    }
                    showAlert();
                </script>
                """
            return render_template('registration.html', alert_script=alert_script, ward_data=ward_data)
        else:
            photo_name = photo.filename
            if not photo_name:
                photo_name = "profiledummy.png"
            else:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
                photo.save(image_path)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                "INSERT INTO registration(id,name,email,mobile,voter_id,aadhar,ward_no,gender,address,username,password,photo) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (generate_id("id", "registration"), name, email, mobile, voter, aadhar, ward_no, gender, address, username, password, photo_name)
            )
            mysql.connection.commit()

            alert_script = """
                            <script>
                                function showAlert() {
                                    Swal.fire({
                                        title: 'Thank You For Registration!',
                                        text: 'Click ok to Continue',
                                        icon: 'success'
                                    });
                                }
                                showAlert();
                            </script>
                            """
            return render_template('registration.html', alert_script=alert_script, ward_data=ward_data)
    return render_template('registration.html', ward_data=ward_data)

@app.route("/user_login", methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['txtusername']
        password = request.form.get('txtpassword')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM registration WHERE username = %s AND password = %s And status = %s", (username, password, "Active"))
        user_data = cursor.fetchone()

        if user_data is not None and user_data['username'] == username and user_data['password'] == password:
            session['username'] = username
            session['id'] = user_data['id']
            session['user_loggedin'] = True
            return redirect(url_for('user_home'))
        else:
            alert_script = """
                <script>
                    function showAlert() {
                        Swal.fire({
                            title: 'Oops...',
                            text: 'Invalid Username or Password or Inactive User!',
                            icon: 'error'
                        });
                    }
                    showAlert();
                </script>
            """
            return render_template('user_login.html', alert_script=alert_script)
    return render_template('user_login.html')

@app.route("/admin_login", methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['txtusername']
        password = request.form['txtpassword']
        if username == "Admin" and password == "Super":
            return redirect(url_for('admin_home'))
        else:
            alert_script = """
                <script>
                    function showAlert() {
                        Swal.fire({
                            title: 'Oops...',
                            text: 'Invalid Username or Password!',
                            icon: 'error'
                        });
                    }
                    showAlert();
                </script>
            """
            return render_template('admin_login.html', alert_script=alert_script)
    return render_template('admin_login.html')

@app.route("/about")
def about():
    return render_template('about.html')




################################################ Admin Side ##################################

@app.route("/admin_home")
def admin_home():
    return render_template('admin_home.html')

@app.route("/admin_addWard", methods=['GET', 'POST'])
def admin_addWard():
    if request.method == 'POST':
        ward_no = request.form['txtwardno']
        area_name = request.form['txtareaname']
        land_mark = request.form['txtlandmark']
        no_of_family = request.form['txtfamily']
        no_of_voter = request.form['txtvoter']
        councillor_name = request.form['txtcouncillorname']
        councillor_mobile = request.form['txtcouncillormob']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "INSERT INTO ward(wid,ward_no,area_name,land_mark,no_of_family,no_of_voter,councillor_name,councillor_mobile) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
            (generate_id("wid", "ward"), ward_no, area_name, land_mark, no_of_family, no_of_voter, councillor_name, councillor_mobile)
        )
        mysql.connection.commit()
        alert_script = """
                                    <script>
                                        function showAlert() {
                                            Swal.fire({
                                                title: 'Ward Added Successfully!',
                                                text: 'Click ok to Continue',
                                                icon: 'success'
                                            });
                                        }
                                        showAlert();
                                    </script>
                                    """
        return render_template('admin_addWard.html', alert_script=alert_script)
    return render_template('admin_addWard.html')

@app.route("/admin_wards")
def admin_wards():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""SELECT * FROM ward""")
    ward_data = cursor.fetchall()
    return render_template('admin_wards.html', ward_data=ward_data)

@app.route("/admin_userList")
def admin_userList():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM registration ORDER BY id DESC")
    user_data = cursor.fetchall()
    return render_template('admin_userList.html', user_data=user_data)

@app.route("/admin_changeStatus", methods=['GET', 'POST'])
def admin_changeStatus():
    if request.method == 'POST':
        status = request.args.get('status')
        id = request.args.get('id')
        if status == "Inactive":
            change_status = "Active"
        else:
            change_status = "Inactive"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE registration SET status=%s WHERE id=%s", (change_status, id))
        mysql.connection.commit()
        return redirect('/admin_userList')
    return redirect('/admin_userList')


@app.route("/admin_eleReq")
def admin_eleReq():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""SELECT * FROM electricity INNER JOIN registration ON registration.id=electricity.id""")
    ele_data = cursor.fetchall()
    return render_template('admin_eleReq.html', ele_data=ele_data)

@app.route("/admin_changeEleStatus")
def admin_changeEleStatus():
    eid = request.args.get('eid')
    status = request.args.get('status')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("UPDATE electricity SET status=%s WHERE eid=%s", (status, eid))
    mysql.connection.commit()
    return redirect("/admin_eleReq")

@app.route("/admin_downloadEleImg")
def admin_downloadEleImg():
    img_name = request.args.get('img')
    if img_name:
        directory = os.path.join(app.root_path, 'static/upload')
        return send_from_directory(directory, img_name, as_attachment=True)
    return redirect("/admin_eleReq")

@app.route("/admin_waterReq")
def admin_waterReq():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""SELECT * FROM water_pipe INNER JOIN registration ON registration.id=water_pipe.id""")
    water_data = cursor.fetchall()
    return render_template('admin_waterReq.html', water_data=water_data)

@app.route("/admin_changeWaterStatus")
def admin_changeWaterStatus():
    wpid = request.args.get('wpid')
    status = request.args.get('status')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("UPDATE water_pipe SET status=%s WHERE wpid=%s", (status, wpid))
    mysql.connection.commit()
    return redirect("/admin_waterReq")

@app.route("/admin_downloadWaterImg")
def admin_downloadWaterImg():
    img_name = request.args.get('img')
    if img_name:
        directory = os.path.join(app.root_path, 'static/upload')
        return send_from_directory(directory, img_name, as_attachment=True)
    return redirect("/admin_waterReq")

@app.route("/admin_complaints")
def admin_complaints():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""SELECT * FROM complaints INNER JOIN registration ON registration.id=complaints.id""")
    comp_data = cursor.fetchall()
    return render_template('admin_complaints.html', comp_data=comp_data)

@app.route("/admin_changeCompStatus")
def admin_changeCompStatus():
    cid = request.args.get('cid')
    status = request.args.get('status')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("UPDATE complaints SET status=%s WHERE cid=%s", (status, cid))
    mysql.connection.commit()
    return redirect("/admin_complaints")

@app.route("/admin_downloadCompImg")
def admin_downloadCompImg():
    img_name = request.args.get('img')
    if img_name:
        directory = os.path.join(app.root_path, 'static/upload')
        return send_from_directory(directory, img_name, as_attachment=True)
    return redirect("/admin_complaints")

@app.route("/admin_editWard", methods=['GET', 'POST'])
def admin_editWard():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""SELECT * FROM ward WHERE wid = %s""", (request.args.get("wid"),))
    ward_data = cursor.fetchone()
    if request.method == 'POST':
        ward_no = request.form['txtwardno']
        area_name = request.form['txtareaname']
        land_mark = request.form['txtlandmark']
        no_of_family = request.form['txtnooffamily']
        no_of_voter = request.form['txtnoofvoter']
        councillor_name = request.form['txtcounname']
        councillor_mobile = request.form['txtcounmobile']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE ward SET ward_no=%s,area_name=%s,land_mark=%s,no_of_family=%s,no_of_voter=%s,councillor_name=%s,councillor_mobile=%s WHERE wid=%s", (ward_no,area_name,land_mark,no_of_family,no_of_voter,councillor_name,councillor_mobile,request.args.get("wid")))
        mysql.connection.commit()
        alert_script = """
            <script>
                function showAlert() {
                    Swal.fire({
                    title: 'Ward Edited Successfully!',
                    text: 'Click ok to Continue',
                    icon: 'success'
                    });
                }
                showAlert();
            </script>
            """
        return render_template('admin_editWard.html', alert_script=alert_script, ward_data=ward_data)
    return render_template('admin_editWard.html', ward_data=ward_data)

@app.route("/admin_deleteWard")
def admin_deleteWard():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM ward WHERE wid=%s", request.args.get("wid"))
    mysql.connection.commit()
    return redirect("/admin_wards")



############################################## User Side #####################################

@app.route("/user_home")
def user_home():
    id = session["id"]
    return render_template('user_home.html', id=id)

@app.route("/user_wardDetail")
def user_wardDetail():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""SELECT ward.ward_no, area_name, land_mark, no_of_family, 
    no_of_voter, councillor_name, councillor_mobile FROM ward 
    INNER JOIN registration ON registration.ward_no = ward.ward_no 
    WHERE registration.id = %s""", str(session["id"]))
    ward_data = cursor.fetchone()
    return render_template('user_wardDetail.html', ward_data=ward_data)

@app.route("/user_electricityReq", methods=['GET', 'POST'])
def user_electricityReq():
    if request.method == 'POST':
        doc_type = request.form['ddldoctype']
        id_proof_img = request.files['fuidproof']
        type = request.form['ddltype']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "INSERT INTO electricity(eid,id,document_type,doc_img,type) VALUES(%s, %s, %s, %s, %s)",
            (generate_id("eid", "electricity"), str(session["id"]), doc_type, id_proof_img.filename, type)
        )
        mysql.connection.commit()
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], id_proof_img.filename)
        id_proof_img.save(image_path)
        alert_script = """
                                            <script>
                                                function showAlert() {
                                                    Swal.fire({
                                                        title: 'Electricity Request Sent Successfully!',
                                                        text: 'Click ok to Continue',
                                                        icon: 'success'
                                                    });
                                                }
                                                showAlert();
                                            </script>
                                            """
        return render_template('user_electricityReq.html', alert_script=alert_script)
    return render_template('user_electricityReq.html')

@app.route("/user_waterPipeReq", methods=['GET', 'POST'])
def user_waterPipeReq():
    if request.method == 'POST':
        doc_type = request.form['ddldoctype']
        id_proof_img = request.files['fuidproof']
        type = request.form['ddltype']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "INSERT INTO water_pipe(wpid,id,document_type,doc_img,type) VALUES(%s, %s, %s, %s, %s)",
            (generate_id("wpid", "water_pipe"), str(session["id"]), doc_type, id_proof_img.filename, type)
        )
        mysql.connection.commit()
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], id_proof_img.filename)
        id_proof_img.save(image_path)
        alert_script = """
                                            <script>
                                                function showAlert() {
                                                    Swal.fire({
                                                        title: 'Water Pipe Request Sent Successfully!',
                                                        text: 'Click ok to Continue',
                                                        icon: 'success'
                                                    });
                                                }
                                                showAlert();
                                            </script>
                                            """
        return render_template('user_waterPipeReq.html', alert_script=alert_script)
    return render_template('user_waterPipeReq.html')

@app.route("/user_myRequest")
def user_myRequest():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""SELECT * FROM electricity WHERE id = %s""", str(session["id"]))
    ele_data = cursor.fetchall()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""SELECT * FROM water_pipe WHERE id = %s""", str(session["id"]))
    water_data = cursor.fetchall()
    return render_template('user_myRequest.html', ele_data=ele_data, water_data=water_data)

@app.route("/user_deleteEleReq")
def user_deleteEleReq():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM electricity WHERE eid=%s", request.args.get("eid"))
    mysql.connection.commit()
    return redirect("/user_myRequest")

@app.route("/user_deleteWaterReq")
def user_deleteWaterReq():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM water_pipe WHERE wpid=%s", request.args.get("wpid"))
    mysql.connection.commit()
    return redirect("/user_myRequest")

@app.route("/user_complaint", methods=['GET', 'POST'])
def user_complaint():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""SELECT * FROM complaints WHERE id = %s""", str(session["id"]))
    complaints_data = cursor.fetchall()
    if request.method == 'POST':
        title = request.form['txttitle']
        msg = request.form['txtmsg']
        image = request.files['fuimg']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "INSERT INTO complaints(cid,id,title,message,image) VALUES(%s, %s, %s, %s, %s)",
            (generate_id("cid", "complaints"), str(session["id"]), title, msg, image.filename)
        )
        mysql.connection.commit()
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_path)
        alert_script = """
                                            <script>
                                                function showAlert() {
                                                    Swal.fire({
                                                        title: 'Complaint Sent Successfully!',
                                                        text: 'Click ok to Continue',
                                                        icon: 'success'
                                                    });
                                                }
                                                showAlert();
                                            </script>
                                            """
        return render_template('user_complaint.html', alert_script=alert_script, complaints_data=complaints_data)
    return render_template('user_complaint.html', complaints_data=complaints_data)

@app.route("/user_deleteComp")
def user_deleteComp():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM complaints WHERE cid=%s", request.args.get("cid"))
    mysql.connection.commit()
    return redirect("/user_complaint")

@app.route("/user_editProfile", methods=['GET', 'POST'])
def user_editProfile():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""SELECT * FROM registration WHERE id = %s""", str(session["id"]))
    user_data = cursor.fetchone()
    if request.method == 'POST':
        name = request.form['txtname']
        email = request.form['txtemail']
        mobile = request.form['txtmobile']
        voter = request.form['txtvoter']
        aadhar = request.form['txtaadhar']
        username = request.form['txtusername']
        address = request.form['txtaddress']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE registration SET name=%s,email=%s,mobile=%s,voter_id=%s,aadhar=%s,username=%s,address=%s WHERE id=%s", (name,email,mobile,voter,aadhar,username,address,str(session["id"])))
        mysql.connection.commit()
        alert_script = """
            <script>
                function showAlert() {
                    Swal.fire({
                    title: 'Profile Edited Successfully!',
                    text: 'Click ok to Continue',
                    icon: 'success'
                    });
                }
                showAlert();
            </script>
            """
        return render_template('user_editProfile.html', alert_script=alert_script, user_data=user_data)
    return render_template('user_editProfile.html', user_data=user_data)



##############################################################################################


if __name__ == '__main__':
    app.run(debug=True)