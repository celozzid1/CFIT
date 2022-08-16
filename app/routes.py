from app import app
from flask import render_template, redirect, url_for, flash, session, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from datetime import datetime
from app.models import user, section_a, section_b, section_c, section_d, section_e, admin, student, instructor, client
import sys

#################################################
#
# LOGIN
#
#################################################
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form.get("email")
        print(email, file=sys.stderr)
        password = request.form.get("password")
        print(password, file=sys.stderr)

        # Query DB for users by username
        users = db.session.query(user).filter_by(email=email).first()
        
        if users is None:
        #if users is None or not users.check_password(password):
        #if password is not users.password_hash:
            print('[EVENT] :::::: Login failed!!! ::::::', file=sys.stderr)
            flash('Invalid Username or Password provided', 'warning')
            return redirect(url_for('login'))
            
   
        # login_user is a flask_login function that starts a session
        else:
            login_user(users)
            print('[EVENT] :::::: user: ' + users.username + ' logged in on ' + str(datetime.utcnow()) + '::::::', file=sys.stderr)
       
        # Check user level
        if is_admin():
            return redirect(url_for('admin_dashboard'))
        if is_instructor():
            return redirect(url_for('instructor_dashboard'))
        if is_student():
            return redirect(url_for('student_dashboard'))
    return render_template('login.html')
    

#################################################
#
# GET SESSION - FUTURE
#
#################################################
@app.route('/getsession')
def getsession():
    if 'Username' in session:
        Username = session['Username']
        return f"Welcome {Username}"

#################################################
#
# LOGOUT
#
#################################################
@app.route('/logout')
@login_required
def logout():
    session.pop('Username',None)
    logout_user()
    return render_template('logout.html')


#################################################
#
# DASHBOARD
#    
#   This function redirects logged in user to the 
#   dashboard for their access level
#
#################################################
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    
    if is_admin():
        return redirect(url_for('admin_dashboard'))
        
    if is_instructor():
        return redirect(url_for('instructor_dashboard'))
       
    if is_student():
        return redirect(url_for('student_dashboard'))
    # Failure attempt to go to admin page which will redirect to login page
    # !!!!!!! may need to add a logout here !!!!!!!
    return render_template('admin.html')

#################################################
#
# ADMINISTRATOR DASHBOARD
#
#################################################
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    # verify user is an administrator    
    if is_admin():
        # get the data for new user
        if request.method=="POST":
            # create an administrator
            if 'addadmin' in request.form:
                id=request.form["id"]
                username=request.form["username"]
                email=request.form["email"]
                password_hash=request.form["password_hash"]
                # change so that id is automatically assigned to avoid duplication
                new_user=user(id=id, role='admin',username=username,email=email,password_hash=password_hash)
                new_admin=admin(id=id, username=username, email=email)
                # add user to the database
                db.session.add(new_user)
                db.session.add(new_admin)
                db.session.commit()
            
            # delete an administrator - only id is needed to delete         
            elif 'deleteadmin' in request.form:
                id=request.form["id"]
                new_admin=admin(id=id)
                new_user=user(id=id)
                delete_admin=new_admin.query.get_or_404(id)
                delete_user=new_user.query.get_or_404(id)
                # delete user from the database
                db.session.delete(delete_admin)
                db.session.delete(delete_user)
                db.session.commit()

        if request.method=="POST":
                # create an instructor
                if 'addinstructor' in request.form:
                    id=request.form["id"]
                    username=request.form["username"]
                    email=request.form["email"]
                    password_hash=request.form["password_hash"]
                    new_user=user(id=id,role='instructor', username=username,email=email,password_hash=password_hash)           
                    new_instructor=instructor(id=id, username=username,email=email)
                    # add user to the database  
                    db.session.add(new_user)
                    db.session.add(new_instructor)                        
                    db.session.commit()
                # delete an instructor - only id is needed to delete   
                elif 'deleteinstructor' in request.form:
                    id=request.form["id"]
                    new_instructor=instructor(id=id)
                    new_user=user(id=id)
                    delete_instructor=new_instructor.query.get_or_404(id)
                    delete_user=new_user.query.get_or_404(id)
                    db.session.delete(delete_instructor)
                    db.session.delete(delete_user)
                    db.session.commit()
                
        if request.method=="POST":
                # create a student
                if 'addstudent' in request.form: 
                    id=request.form["id"]
                    student_name=request.form["student_name"]
                    username=request.form["student_name"]
                    email=request.form["email"]
                    password_hash=request.form["password_hash"]
                    class_year=request.form["class_year"]
                    course=request.form["course"]
                    semester=request.form["semester"]
                    course_instructor=request.form["course_instructor"]
                    new_user=user(id=id,role='student',username=username,email=email,password_hash=password_hash)
                    new_student=student(id=id,student_id=id, class_year=class_year,course=course,semester=semester,student_name=student_name,course_instructor=course_instructor,email=email)
                    # add user to the database
                    db.session.add(new_user)
                    db.session.add(new_student)
                    db.session.commit()
                    
                # delete a student - only id is needed to delete    
                elif 'deletestudent' in request.form:
                    id=request.form["id"]
                    new_student=student(id=id)
                    new_user=user(id=id)
                    delete_student=new_student.query.get_or_404(id)
                    delete_user=new_user.query.get_or_404(id)
                    db.session.delete(delete_student)
                    db.session.delete(delete_user)
                    db.session.commit()

                return render_template("admin.html", 
                    admin=user.query.filter_by(role='admin').all(),
                    instructor=user.query.filter_by(role='instructor').all(),
                    student=student.query.all())

        return render_template("admin.html",
                    admin=user.query.filter_by(role='admin').all(),
                    instructor=user.query.filter_by(role='instructor').all(),
                    student=student.query.all())
    else:                
        return render_template("error.html")

#################################################
#
# INSTRUCTOR_DASHBOARD
#
#################################################
@app.route('/instructor', methods=['GET', 'POST'])
@login_required
def instructor_dashboard():
    # verify user level - instructor or admin/instructor
    if is_admin() or is_instructor():
        print('Instructor Dashboard', file=sys.stderr)
        role = current_user.role   
        current_instructor = current_user.username
        if request.method=="POST":
            id=request.form["id"]
            session_id = request.form["id"]
            session["id"] = id
            name=request.form["name"]
            date=request.form["date"]
            disorder=request.form["disorder"]
            new_client=client(id=id,name=name,date=date,disorder=disorder, session_id=session_id)
            # add a client    
            if 'addclient' in request.form:
                db.session.add(new_client)
                db.session.commit()
            # delete a client
            elif 'deleteclient' in request.form:
                delete_client=new_client.query.get_or_404(id)
                db.session.delete(delete_client)
                db.session.commit()
               
            return render_template("instructor.html", 
            values=student.query.filter_by(course_instructor=current_instructor).all(), 
            client=client.query.all(), role=role)

        return render_template("instructor.html", values=student.query.filter_by(course_instructor=current_instructor).all(), client=client.query.all(), role=role)
    else:                
        return render_template("error.html")

#################################################
#
# STUDENT_DASHBOARD
#
#################################################
@app.route('/student',  methods=['GET', 'POST'])
@login_required
def student_dashboard():
    # verify user is student. Only this students assessments will be available for viewing
    if is_student():
        print('Student Dashboard', file=sys.stderr)
        student_id=current_user.id
        session["student_id"] = student_id
        print(student_id, file=sys.stderr)
        if request.method=="POST":
            student_id=current_user.id
            session["student_id"] = student_id
            return render_template('student.html', values=db.session.query(section_a).filter_by(student_id=student_id).all())
        
        return render_template('student.html', values=db.session.query(section_a).filter_by(student_id=student_id).all())
    else:                
        return render_template("error.html")

#################################################
#
# VIEW_ASSESSMENT
#
# The main assessment page
# this will load a previously completed assessment
# and display the ratings and comments    
#################################################
@app.route('/view', methods=['GET', 'POST'])
@login_required
def view_assessment():

    print('View assessment for:', file=sys.stderr)
   
    if request.method=="POST":
        assessment_id=request.form.get('session_id')
        student_id=request.form.get('student_id')

        #check for empty assessment
        if assessment_id == None:
            return render_template('invalid.html')
    else:
        student_id = session["student_id"]

    # grab the student data from the assessment.
    current_student = db.session.query(section_a).filter_by(student_id=student_id).first()
    student_name = current_student.student_name
    course = current_student.course
    semester = current_student.semester
    session_id=current_student.session_id

      # grab the session id from the assessment. they are all the same so section_a is fine
    client_name=db.session.query(section_a.client).filter_by(session_id=session_id).first()
    client_disorder=db.session.query(section_a.disorder).filter_by(session_id=session_id).first()
    course_instructor=db.session.query(section_a.course_instructor).filter_by(session_id=session_id).first()
    
    #############################
    # Section A
    #############################
    # Ratings
    a1_rating = db.session.query(section_a.a1_rating).filter_by(student_id=student_id).first()
    print('a1_rating', file=sys.stderr)
    print(a1_rating, file=sys.stderr)
    a2_rating = db.session.query(section_a.a2_rating).filter_by(student_id=student_id).first()
    a3_rating = db.session.query(section_a.a3_rating).filter_by(student_id=student_id).first()
    a4_rating = db.session.query(section_a.a4_rating).filter_by(student_id=student_id).first()
    a5_rating = db.session.query(section_a.a5_rating).filter_by(student_id=student_id).first()
   
    # Instructor Comments
    a1_instructor_comment = db.session.query(section_a.a1_instructor_comment).filter_by(student_id=student_id).first()
    a2_instructor_comment = db.session.query(section_a.a2_instructor_comment).filter_by(student_id=student_id).first()
    a3_instructor_comment = db.session.query(section_a.a3_instructor_comment).filter_by(student_id=student_id).first()
    a4_instructor_comment = db.session.query(section_a.a4_instructor_comment).filter_by(student_id=student_id).first()
    a5_instructor_comment = db.session.query(section_a.a5_instructor_comment).filter_by(student_id=student_id).first()

    # Student Comments
    a1_student_comment = db.session.query(section_a.a1_student_comment).filter_by(student_id=student_id).first()
    a2_student_comment = db.session.query(section_a.a2_student_comment).filter_by(student_id=student_id).first()
    a3_student_comment = db.session.query(section_a.a3_student_comment).filter_by(student_id=student_id).first()
    a4_student_comment = db.session.query(section_a.a4_student_comment).filter_by(student_id=student_id).first()
    a5_student_comment = db.session.query(section_a.a5_student_comment).filter_by(student_id=student_id).first()


    #############################
    # Section B
    #############################
    # Ratings
    b1_rating = db.session.query(section_b.b1_rating).filter_by(student_id=student_id).first()
    b2_rating = db.session.query(section_b.b2_rating).filter_by(student_id=student_id).first()
    b3_rating = db.session.query(section_b.b3_rating).filter_by(student_id=student_id).first()
    b4_rating = db.session.query(section_b.b4_rating).filter_by(student_id=student_id).first()

    # Instructor Comments
    b1_instructor_comment = db.session.query(section_b.b1_instructor_comment).filter_by(student_id=student_id).first()
    b2_instructor_comment = db.session.query(section_b.b2_instructor_comment).filter_by(student_id=student_id).first()
    b3_instructor_comment = db.session.query(section_b.b3_instructor_comment).filter_by(student_id=student_id).first()
    b4_instructor_comment = db.session.query(section_b.b4_instructor_comment).filter_by(student_id=student_id).first()

    # Student Comments
    b1_student_comment = db.session.query(section_b.b1_student_comment).filter_by(student_id=student_id).first()
    b2_student_comment = db.session.query(section_b.b2_student_comment).filter_by(student_id=student_id).first()
    b3_student_comment = db.session.query(section_b.b3_student_comment).filter_by(student_id=student_id).first()
    b4_student_comment = db.session.query(section_b.b4_student_comment).filter_by(student_id=student_id).first()


    #############################
    # Section C
    #############################
    # Ratings
    c1_rating = db.session.query(section_c.c1_rating).filter_by(student_id=student_id).first()
    c2_rating = db.session.query(section_c.c2_rating).filter_by(student_id=student_id).first()
    c3_rating = db.session.query(section_c.c3_rating).filter_by(student_id=student_id).first()
    c4_rating = db.session.query(section_c.c4_rating).filter_by(student_id=student_id).first()
    c5_rating = db.session.query(section_c.c5_rating).filter_by(student_id=student_id).first()
    c6_rating = db.session.query(section_c.c6_rating).filter_by(student_id=student_id).first()
    c7_rating = db.session.query(section_c.c7_rating).filter_by(student_id=student_id).first()
    c8_rating = db.session.query(section_c.c8_rating).filter_by(student_id=student_id).first()
    c9_rating = db.session.query(section_c.c9_rating).filter_by(student_id=student_id).first()
    c10_rating = db.session.query(section_c.c10_rating).filter_by(student_id=student_id).first()
    c11_rating = db.session.query(section_c.c11_rating).filter_by(student_id=student_id).first()
    c12_rating = db.session.query(section_c.c12_rating).filter_by(student_id=student_id).first()
    c13_rating = db.session.query(section_c.c13_rating).filter_by(student_id=student_id).first()

    # Instructor Comments
    c1_instructor_comment = db.session.query(section_c.c1_instructor_comment).filter_by(student_id=student_id).first()
    c2_instructor_comment = db.session.query(section_c.c2_instructor_comment).filter_by(student_id=student_id).first()
    c3_instructor_comment = db.session.query(section_c.c3_instructor_comment).filter_by(student_id=student_id).first()
    c4_instructor_comment = db.session.query(section_c.c4_instructor_comment).filter_by(student_id=student_id).first()
    c5_instructor_comment = db.session.query(section_c.c5_instructor_comment).filter_by(student_id=student_id).first()
    c6_instructor_comment = db.session.query(section_c.c6_instructor_comment).filter_by(student_id=student_id).first()
    c7_instructor_comment = db.session.query(section_c.c7_instructor_comment).filter_by(student_id=student_id).first()
    c8_instructor_comment = db.session.query(section_c.c8_instructor_comment).filter_by(student_id=student_id).first()
    c9_instructor_comment = db.session.query(section_c.c9_instructor_comment).filter_by(student_id=student_id).first()
    c10_instructor_comment = db.session.query(section_c.c10_instructor_comment).filter_by(student_id=student_id).first()
    c11_instructor_comment = db.session.query(section_c.c11_instructor_comment).filter_by(student_id=student_id).first()
    c12_instructor_comment = db.session.query(section_c.c12_instructor_comment).filter_by(student_id=student_id).first()
    c13_instructor_comment = db.session.query(section_c.c13_instructor_comment).filter_by(student_id=student_id).first()

    # Student Comments
    c1_student_comment = db.session.query(section_c.c1_student_comment).filter_by(student_id=student_id).first()
    c2_student_comment = db.session.query(section_c.c2_student_comment).filter_by(student_id=student_id).first()
    c3_student_comment = db.session.query(section_c.c3_student_comment).filter_by(student_id=student_id).first()
    c4_student_comment = db.session.query(section_c.c4_student_comment).filter_by(student_id=student_id).first()
    c5_student_comment = db.session.query(section_c.c5_student_comment).filter_by(student_id=student_id).first()
    c6_student_comment = db.session.query(section_c.c6_student_comment).filter_by(student_id=student_id).first()
    c7_student_comment = db.session.query(section_c.c7_student_comment).filter_by(student_id=student_id).first()
    c8_student_comment = db.session.query(section_c.c8_student_comment).filter_by(student_id=student_id).first()
    c9_student_comment = db.session.query(section_c.c9_student_comment).filter_by(student_id=student_id).first()
    c10_student_comment = db.session.query(section_c.c10_student_comment).filter_by(student_id=student_id).first()
    c11_student_comment = db.session.query(section_c.c11_student_comment).filter_by(student_id=student_id).first()
    c12_student_comment = db.session.query(section_c.c12_student_comment).filter_by(student_id=student_id).first()
    c13_student_comment = db.session.query(section_c.c13_student_comment).filter_by(student_id=student_id).first()


    #########################
    # Section D
    #############################
    # Ratings
    d1_rating = db.session.query(section_d.d1_rating).filter_by(student_id=student_id).first()
    d2_rating = db.session.query(section_d.d2_rating).filter_by(student_id=student_id).first()
    d3_rating = db.session.query(section_d.d3_rating).filter_by(student_id=student_id).first()

    # Instructor Comments
    d1_instructor_comment = db.session.query(section_d.d1_instructor_comment).filter_by(student_id=student_id).first()
    d2_instructor_comment = db.session.query(section_d.d2_instructor_comment).filter_by(student_id=student_id).first()
    d3_instructor_comment = db.session.query(section_d.d3_instructor_comment).filter_by(student_id=student_id).first()

    # Student Comments
    d1_student_comment = db.session.query(section_d.d1_student_comment).filter_by(student_id=student_id).first()
    d2_student_comment = db.session.query(section_d.d2_student_comment).filter_by(student_id=student_id).first()
    d3_student_comment = db.session.query(section_d.d3_student_comment).filter_by(student_id=student_id).first()


    #############################
    # Section E
    #############################
    # Ratings
    e1_rating = db.session.query(section_e.e1_rating).filter_by(student_id=student_id).first()
    e2_rating = db.session.query(section_e.e2_rating).filter_by(student_id=student_id).first()

    # Instructor Comments
    e1_instructor_comment = db.session.query(section_e.e1_instructor_comment).filter_by(student_id=student_id).first()
    e2_instructor_comment = db.session.query(section_e.e2_instructor_comment).filter_by(student_id=student_id).first()

    # Student Comments
    e1_student_comment = db.session.query(section_e.e1_student_comment).filter_by(student_id=student_id).first()
    e2_student_comment = db.session.query(section_e.e2_student_comment).filter_by(student_id=student_id).first()

    return render_template('assessment.html',  
                            a1_rating=a1_rating[0], a1_instructor_comment=a1_instructor_comment[0], a1_student_comment=a1_student_comment[0],
                            a2_rating=a2_rating[0], a2_instructor_comment=a2_instructor_comment[0], a2_student_comment=a2_student_comment[0],
                            a3_rating=a3_rating[0], a3_instructor_comment=a3_instructor_comment[0], a3_student_comment=a3_student_comment[0],
                            a4_rating=a4_rating[0], a4_instructor_comment=a4_instructor_comment[0], a4_student_comment=a4_student_comment[0],
                            a5_rating=a5_rating[0], a5_instructor_comment=a5_instructor_comment[0], a5_student_comment=a5_student_comment[0],
                            b1_rating=b1_rating[0], b1_instructor_comment=b1_instructor_comment[0], b1_student_comment=b1_student_comment[0],
                            b2_rating=b2_rating[0], b2_instructor_comment=b2_instructor_comment[0], b2_student_comment=b2_student_comment[0],
                            b3_rating=b3_rating[0], b3_instructor_comment=b3_instructor_comment[0], b3_student_comment=b3_student_comment[0],
                            b4_rating=b4_rating[0], b4_instructor_comment=b4_instructor_comment[0], b4_student_comment=b4_student_comment[0],
                            c1_rating=c1_rating[0], c1_instructor_comment=c1_instructor_comment[0], ca1_student_comment=c1_student_comment[0],
                            c2_rating=c2_rating[0], c2_instructor_comment=c2_instructor_comment[0], ca2_student_comment=c2_student_comment[0],
                            c3_rating=c3_rating[0], c3_instructor_comment=c3_instructor_comment[0], ca3_student_comment=c3_student_comment[0],
                            c4_rating=c4_rating[0], c4_instructor_comment=c4_instructor_comment[0], ca4_student_comment=c4_student_comment[0],
                            c5_rating=c5_rating[0], c5_instructor_comment=c5_instructor_comment[0], ca5_student_comment=c5_student_comment[0],
                            c6_rating=c6_rating[0], c6_instructor_comment=c6_instructor_comment[0], c6_student_comment=c6_student_comment[0],
                            c7_rating=c7_rating[0], c7_instructor_comment=c7_instructor_comment[0], c7_student_comment=c7_student_comment[0],
                            c8_rating=c8_rating[0], c8_instructor_comment=c8_instructor_comment[0], c8_student_comment=c8_student_comment[0],
                            c9_rating=c9_rating[0], c9_instructor_comment=c9_instructor_comment[0], c9_student_comment=c9_student_comment[0],
                            c10_rating=c10_rating[0], c10_instructor_comment=c10_instructor_comment[0], c10_student_comment=c10_student_comment[0],
                            c11_rating=c11_rating[0], c11_instructor_comment=c11_instructor_comment[0], c11_student_comment=c11_student_comment[0],
                            c12_rating=c12_rating[0], c12_instructor_comment=c12_instructor_comment[0], c12_student_comment=c12_student_comment[0],
                            c13_rating=c13_rating[0], c13_instructor_comment=c13_instructor_comment[0], c13_student_comment=c13_student_comment[0],
                            d1_rating=d1_rating[0], d1_instructor_comment=d1_instructor_comment[0], d1_student_comment=d1_student_comment[0],
                            d2_rating=d2_rating[0], d2_instructor_comment=d2_instructor_comment[0], d2_student_comment=d2_student_comment[0],
                            d3_rating=d3_rating[0], d3_instructor_comment=d3_instructor_comment[0], d3_student_comment=d3_student_comment[0],
                            e1_rating=e1_rating[0], e1_instructor_comment=e1_instructor_comment[0], e1_student_comment=e1_student_comment[0],
                            e2_rating=e2_rating[0], e2_instructor_comment=e2_instructor_comment[0], e2_student_comment=e2_student_comment[0],
                            id=student_id, student_name=student_name, course=course, semester=semester,  course_instructor=course_instructor[0], client_name=client_name[0], client_disorder=client_disorder[0]) 

#################################################
#
# SELECT_CLIENT
#
# This will select a client for a new assessment
#
#################################################
@app.route('/select_client', methods=['GET', 'POST'])
@login_required
def select_client():
    if request.method=="POST":  
        student_id=request.form["student_id"]

        print('Assigned Client for: ',file=sys.stderr)
        print(student_id,file=sys.stderr )
        student_name=request.form["student_name"]
        print('student_name: ',file=sys.stderr )
        print(student_name ,file=sys.stderr )
     
        course=request.form["course"]
        semester=request.form["semester"]
        current_student = db.session.query(student).filter_by(id=student_id).first()
        student_name = current_student.student_name
        course = current_student.course
        semester = current_student.semester
        session['student_id'] = student_id
       
    return render_template("client.html", values=client.query.all(),id=student_id)
    
#################################################
#
# NEW_ASSESSMENT
#
# This will create a new assessment and load all
# relevant student, client and instructor data 
# into the form
#
#################################################  
@app.route('/new', methods=['GET', 'POST'])
@login_required
def new_assessment():

    if request.method=="POST":  
   
        student_id = session['student_id']
        print(student_id, file=sys.stderr )

        current_student = db.session.query(student).filter_by(id=student_id).first()
        client_id=request.form.get("id")
        current_client=db.session.query(client).filter_by(id=client_id).first()
        print('New Assessment for Client: ',file=sys.stderr )
        print(student_id,file=sys.stderr )
       
        course_instructor = current_user.username
        session['course_instructor'] = current_user.username
        session['date'] = request.form.get("date")
        student_name = current_student.student_name
        course = current_student.course
        session['course'] = current_student.course
        semester = current_student.semester
        session['semester'] = current_student.semester  
        client_name = current_client.name
        session['client_name'] = current_client.name
        client_disorder = current_client.disorder
        session['client_disorder'] = current_client.disorder

    else:
        print("ERROR", file=sys.stderr)


    # Start an assessment with all ratings at N/A (rating = 0)
    assessment_a = section_a(
                           a1_rating=0,                  
                           a2_rating=0,  
                           a3_rating=0,
                           a4_rating=0,
                           a5_rating=0, 
                           student_id=student_id, student_name=student_name)
    
    assessment_b = section_b(
                           b1_rating=0,                  
                           b2_rating=0,  
                           b3_rating=0,
                           b4_rating=0,
                           student_id=student_id, student_name=student_name)
    
    assessment_c = section_c(
                           c1_rating=0,                  
                           c2_rating=0,  
                           c3_rating=0,
                           c4_rating=0,
                           c5_rating=0, 
                           c6_rating=0, 
                           c7_rating=0, 
                           c8_rating=0, 
                           c9_rating=0, 
                           c10_rating=0, 
                           c11_rating=0, 
                           c12_rating=0, 
                           c13_rating=0, 
                           student_id=student_id, student_name=student_name)
   
    assessment_d = section_d(
                           d1_rating=0,                  
                           d2_rating=0,  
                           d3_rating=0,
                           student_id=student_id, student_name=student_name)

    
    assessment_e = section_e(
                           e1_rating=0,                  
                           e2_rating=0,  
                           student_id=student_id, student_name=student_name)

    # add assessement with the blank ratings in case a save occurs before all ratings have been edited
    db.session.add(assessment_a)
    db.session.add(assessment_b)
    db.session.add(assessment_c)
    db.session.add(assessment_d)
    db.session.add(assessment_e)

    return render_template('assessment.html',  
                            a1_rating=0,
                            a2_rating=0,  
                            a3_rating=0,
                            a4_rating=0,
                            a5_rating=0,
                            b1_rating=0,
                            b2_rating=0,
                            b3_rating=0,
                            b4_rating=0,
                            c1_rating=0,
                            c2_rating=0,
                            c3_rating=0,
                            c4_rating=0,
                            c5_rating=0,
                            c6_rating=0,
                            c7_rating=0,
                            c8_rating=0,
                            c9_rating=0,
                            c10_rating=0,
                            c11_rating=0,
                            c12_rating=0,
                            c13_rating=0,
                            d1_rating=0,
                            d2_rating=0,
                            d3_rating=0,
                            e1_rating=0,
                            e2_rating=0,
                            id=student_id, student_name=student_name, course=course, semester=semester, 
                            course_instructor=course_instructor, 
                            client_name=client_name, client_disorder=client_disorder) 


#################################################
#
# SAVE_ASSESSMENT
#
# This will save the assessment and all
# ratings, comments, relevant student, client and 
# instructor data into the database
#
#################################################  
@app.route('/save', methods=['GET', 'POST'])
@login_required
def save_assessment():

    print('Saving Assessment.....', file=sys.stderr) 
    # get the ratings and comment data from the assessment form 
    if request.method == "POST":
        #get the current student data
        student_id = session['student_id']
        print(student_id, file=sys.stderr)
        current_student = db.session.query(user).filter_by(id=student_id).first()
        student_name = current_student.username
        print(current_student.username, file=sys.stderr)
        # get the data saved to the session to ensure it gets saved to the assessment
        date = session['date']
        course = session['course'] 
        semester = session['semester'] 
        client = session['client_name']
        disorder= session['client_disorder'] 
        course_instructor = session['course_instructor'] 

        # SECTION A
        # get the section ratings and comments from the form
        a1_rating = request.form.get("a1_rating")
        a2_rating = request.form.get("a2_rating")
        a3_rating = request.form.get("a3_rating")
        a4_rating = request.form.get("a4_rating")
        a5_rating = request.form.get("a5_rating")
                
        a1_instructor_comment = request.form.get("a1_instructor_comment")
        a2_instructor_comment = request.form.get("a2_instructor_comment")
        a3_instructor_comment = request.form.get("a3_instructor_comment")
        a4_instructor_comment = request.form.get("a4_instructor_comment")
        a5_instructor_comment = request.form.get("a5_instructor_comment")

        a1_student_comment = request.form.get("a1_student_comment")
        a2_student_comment = request.form.get("a2_student_comment")
        a3_student_comment = request.form.get("a3_student_comment")
        a4_student_comment = request.form.get("a4_student_comment")
        a5_student_comment = request.form.get("a5_student_comment")
      
        # save it in a new assessment object
        assessment_a = section_a(
                            a1_rating=a1_rating, a1_instructor_comment=a1_instructor_comment, a1_student_comment=a1_student_comment,
                            a2_rating=a2_rating, a2_instructor_comment=a2_instructor_comment, a2_student_comment=a2_student_comment,
                            a3_rating=a3_rating, a3_instructor_comment=a3_instructor_comment, a3_student_comment=a3_student_comment,
                            a4_rating=a4_rating, a4_instructor_comment=a4_instructor_comment, a4_student_comment=a4_student_comment,
                            a5_rating=a5_rating, a5_instructor_comment=a5_instructor_comment, a5_student_comment=a5_student_comment,
                            student_id=student_id, student_name=student_name, course_instructor=course_instructor, course=course, semester=semester, date=date, client=client, disorder=disorder)

   
        # SECTION B
        # get the section ratings and comments from the form
        b1_rating = request.form.get("b1_rating")
        b2_rating = request.form.get("b2_rating")
        b3_rating = request.form.get("b3_rating")
        b4_rating = request.form.get("b4_rating")
 
        b1_instructor_comment = request.form.get("b1_instructor_comment")
        b2_instructor_comment = request.form.get("b2_instructor_comment")
        b3_instructor_comment = request.form.get("b3_instructor_comment")
        b4_instructor_comment = request.form.get("b4_instructor_comment")

        b1_student_comment = request.form.get("b1_student_comment")
        b2_student_comment = request.form.get("b2_student_comment")
        b3_student_comment = request.form.get("b3_student_comment")
        b4_student_comment = request.form.get("b4_student_comment")

        # save it in a new assessment object
        assessment_b = section_b(
                            b1_rating=b1_rating, b1_instructor_comment=b1_instructor_comment, b1_student_comment=b1_student_comment,
                            b2_rating=b2_rating, b2_instructor_comment=b2_instructor_comment, b2_student_comment=b2_student_comment,
                            b3_rating=b3_rating, b3_instructor_comment=b3_instructor_comment, b3_student_comment=b3_student_comment,
                            b4_rating=b4_rating, b4_instructor_comment=b4_instructor_comment, b4_student_comment=b4_student_comment,
                            student_id=student_id, student_name=student_name, course_instructor=course_instructor, course=course, semester=semester, date=date, client=client, disorder=disorder)

   
        # SECTION C
        # get the section ratings and comments from the form
        c1_rating = request.form.get("c1_rating")
        c2_rating = request.form.get("c2_rating")
        c3_rating = request.form.get("c3_rating")
        c4_rating = request.form.get("c4_rating")
        c5_rating = request.form.get("c5_rating")
        c6_rating = request.form.get("c6_rating")
        c7_rating = request.form.get("c7_rating")
        c8_rating = request.form.get("c8_rating")
        c9_rating = request.form.get("c9_rating")
        c10_rating = request.form.get("c10_rating")
        c11_rating = request.form.get("c11_rating")
        c12_rating = request.form.get("c12_rating")
        c13_rating = request.form.get("c13_rating")

        c1_instructor_comment = request.form.get("c1_instructor_comment")
        c2_instructor_comment = request.form.get("c2_instructor_comment")
        c3_instructor_comment = request.form.get("c3_instructor_comment")
        c4_instructor_comment = request.form.get("c4_instructor_comment")
        c5_instructor_comment = request.form.get("c5_instructor_comment")
        c6_instructor_comment = request.form.get("c6_instructor_comment")
        c7_instructor_comment = request.form.get("c7_instructor_comment")
        c8_instructor_comment = request.form.get("c8_instructor_comment")
        c9_instructor_comment = request.form.get("c9_instructor_comment")
        c10_instructor_comment = request.form.get("c10_instructor_comment")
        c11_instructor_comment = request.form.get("c11_instructor_comment")
        c12_instructor_comment = request.form.get("c12_instructor_comment")
        c13_instructor_comment = request.form.get("c13_instructor_comment")

        c1_student_comment = request.form.get("c1_student_comment")
        c2_student_comment = request.form.get("c2_student_comment")
        c3_student_comment = request.form.get("c3_student_comment")
        c4_student_comment = request.form.get("c4_student_comment")
        c5_student_comment = request.form.get("c5_student_comment")
        c6_student_comment = request.form.get("c6_student_comment")
        c7_student_comment = request.form.get("c7_student_comment")
        c8_student_comment = request.form.get("c8_student_comment")
        c9_student_comment = request.form.get("c9_student_comment")
        c10_student_comment = request.form.get("c10_student_comment")
        c11_student_comment = request.form.get("c11_student_comment")
        c12_student_comment = request.form.get("c12_student_comment")
        c13_student_comment = request.form.get("c13_student_comment")
        
        # save it in a new assessment object
        assessment_c = section_c(
                            c1_rating=c1_rating, c1_instructor_comment=c1_instructor_comment, c1_student_comment=c1_student_comment,
                            c2_rating=c2_rating, c2_instructor_comment=c2_instructor_comment, c2_student_comment=c2_student_comment,
                            c3_rating=c3_rating, c3_instructor_comment=c3_instructor_comment, c3_student_comment=c3_student_comment,
                            c4_rating=c4_rating, c4_instructor_comment=c4_instructor_comment, c4_student_comment=c4_student_comment,
                            c5_rating=c5_rating, c5_instructor_comment=c5_instructor_comment, c5_student_comment=c5_student_comment,
                            c6_rating=c6_rating, c6_instructor_comment=c6_instructor_comment, c6_student_comment=c6_student_comment,
                            c7_rating=c7_rating, c7_instructor_comment=c7_instructor_comment, c7_student_comment=c7_student_comment,
                            c8_rating=c8_rating, c8_instructor_comment=c8_instructor_comment, c8_student_comment=c8_student_comment,
                            c9_rating=c9_rating, c9_instructor_comment=c9_instructor_comment, c9_student_comment=c9_student_comment,
                            c10_rating=c10_rating, c10_instructor_comment=c10_instructor_comment, c10_student_comment=c10_student_comment,
                            c11_rating=c11_rating, c11_instructor_comment=c11_instructor_comment, c11_student_comment=c11_student_comment,
                            c12_rating=c12_rating, c12_instructor_comment=c12_instructor_comment, c12_student_comment=c12_student_comment,
                            c13_rating=c13_rating, c13_instructor_comment=c13_instructor_comment, c13_student_comment=c13_student_comment,
                            student_id=student_id, student_name=student_name, course_instructor=course_instructor, course=course, semester=semester, date=date, client=client, disorder=disorder)

        # SECTION D
        # get the section ratings and comments from the form
        d1_rating = request.form.get("d1_rating")
        d2_rating = request.form.get("d2_rating")
        d3_rating = request.form.get("d3_rating")

        d1_instructor_comment = request.form.get("d1_instructor_comment")
        d2_instructor_comment = request.form.get("d2_instructor_comment")
        d3_instructor_comment = request.form.get("d3_instructor_comment")
        
        d1_student_comment = request.form.get("d1_student_comment")
        d2_student_comment = request.form.get("d2_student_comment")
        d3_student_comment = request.form.get("d3_student_comment")

        # save it in a new assessment object
        assessment_d = section_d(
                            d1_rating=d1_rating, d1_instructor_comment=d1_instructor_comment, d1_student_comment=d1_student_comment,
                            d2_rating=d2_rating, d2_instructor_comment=d2_instructor_comment, d2_student_comment=d2_student_comment,
                            d3_rating=d3_rating, d3_instructor_comment=d3_instructor_comment, d3_student_comment=d3_student_comment,
                            student_id=student_id, student_name=student_name, course_instructor=course_instructor, course=course, semester=semester, date=date, client=client, disorder=disorder)


        # SECTION E
        # get the section ratings and comments from the form
        e1_rating = request.form.get("e1_rating")
        e2_rating = request.form.get("e2_rating")
        
        e1_instructor_comment = request.form.get("e1_instructor_comment")
        e2_instructor_comment = request.form.get("e2_instructor_comment")
        
        e1_student_comment = request.form.get("e1_student_comment")
        e2_student_comment = request.form.get("e2_student_comment")

        # save it in a new assessment object
        assessment_e = section_e(
                            e1_rating=e1_rating, e1_instructor_comment=e1_instructor_comment, e1_student_comment=e1_student_comment,
                            e2_rating=e2_rating, e2_instructor_comment=e2_instructor_comment, e2_student_comment=e2_student_comment,
                            student_id=student_id, student_name=student_name, course_instructor=course_instructor, course=course, semester=semester, date=date, client=client, disorder=disorder)

        # add record to DB and commit changes
        db.session.add(assessment_a)
        db.session.add(assessment_b)
        db.session.add(assessment_c)
        db.session.add(assessment_d)
        db.session.add(assessment_e)
        db.session.add(assessment_e)
        db.session.flush()
        
        # get the assessment id just created from the db
        # this is the 'session_id' used in the other database tables to 
        # tie everything together
        id_= assessment_a.id
        print(id_, file=sys.stderr)
       
        current_assessment_a = assessment_a.query.get(id_)
        current_assessment_a.session_id = id_
        
        # append the assessment objects with the session id
        assessment_b.session_id = id_
        assessment_c.session_id = id_
        assessment_d.session_id = id_
        assessment_e.session_id = id_
       
        # append the current student record with the session id
        usr = student.query.filter_by(id=student_id).first()
        usr.session_id = id_
        
        # store the assessment data in the DB
        db.session.commit()
        
    print('saving all sections and redirecting', file=sys.stderr)
    return redirect(url_for('dashboard'))


#################################################
#
# IS_ADMIN
#
# Helper function to determine if authenticated 
# user is an administrator
#################################################
def is_admin():

    if current_user:
        if current_user.role == 'admin':
            return True
        else:
            return False
    else:
        print('User not authenticated.', file=sys.stderr)

#################################################
#
# IS_INSTRUCTOR
#
# Helper function to determine if authenticated 
# user is an instructor.
#################################################
def is_instructor():
    
    if current_user:
        if current_user.role == 'instructor':
            return True
        else:
            return False
    else:
        print('User not authenticated.', file=sys.stderr)        

#################################################
#
# IS_STUDENT
#
# Helper function to determine if authenticated 
# user is a student.
#################################################
def is_student():
    
    if current_user:
        if current_user.role == 'student':
            return True
        else:
            return False
    else:
        print('User not authenticated.', file=sys.stderr)    
