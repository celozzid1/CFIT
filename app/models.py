import flask
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# The mySQL Database contains a table for each of the 5 sections in the feedback form
# They all share the same structure and some common elements while the 
# ratings, instructor and student comments are unigue to each section_x table
# The common data in each section is mirrored in all 5 sections. 
# Since all sections are tied together in one Assessment form, it could be done
# by using section_a as the anchor point, but for unkwown scope of future expansion 
# it was added to each table.

# Section A - 5 questions and common data
class section_a(db.Model):
    __tablename__ = 'section_a'   
    id = db.Column(db.Integer, primary_key = True)
    a1_rating = db.Column(db.Numeric(10,1), default = 1)
    a1_instructor_comment = db.Column(db.String(256))
    a1_student_comment = db.Column(db.String(256))  
    a2_rating = db.Column(db.Numeric(10,1), default = 1)
    a2_instructor_comment = db.Column(db.String(256))
    a2_student_comment = db.Column(db.String(256)) 
    a3_rating = db.Column(db.Numeric(10,1), default = 1)
    a3_instructor_comment = db.Column(db.String(256))
    a3_student_comment = db.Column(db.String(256)) 
    a4_rating = db.Column(db.Numeric(10,1), default = 1)
    a4_instructor_comment = db.Column(db.String(256))
    a4_student_comment = db.Column(db.String(256)) 
    a5_rating = db.Column(db.Numeric(10,1), default = 1)
    a5_instructor_comment = db.Column(db.String(256))
    a5_student_comment = db.Column(db.String(256)) 
    session_id = db.Column(db.Integer, default = 1)
    instructor_id = db.Column(db.Integer, default = 1)
    student_id = db.Column(db.Integer, default = 1)
    student_name = db.Column(db.String(256))
    course = db.Column(db.String(256))
    semester = db.Column(db.String(256))
    client = db.Column(db.String(256))
    disorder = db.Column(db.String(256))
    client_id = db.Column(db.Integer, default = 1)
    date = db.Column(db.String(256))
    course_instructor = db.Column(db.String(256))
    class_year = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return self.a1_rating + ': ' + self.a2_rating + ': ' + self.a3_rating + ': ' + self.a4_rating + ': ' + self.a5_rating

# Section B - 4 questions and common data
class section_b(db.Model):
    __tablename__ = 'section_b'   
    id = db.Column(db.Integer, primary_key = True)
    b1_rating = db.Column(db.Numeric(10,1), default = 1)
    b1_instructor_comment = db.Column(db.String(256))
    b1_student_comment = db.Column(db.String(256))  
    b2_rating = db.Column(db.Numeric(10,1), default = 1)
    b2_instructor_comment = db.Column(db.String(256))
    b2_student_comment = db.Column(db.String(256)) 
    b3_rating = db.Column(db.Numeric(10,1), default = 1)
    b3_instructor_comment = db.Column(db.String(256))
    b3_student_comment = db.Column(db.String(256)) 
    b4_rating = db.Column(db.Numeric(10,1), default = 1)
    b4_instructor_comment = db.Column(db.String(256))
    b4_student_comment = db.Column(db.String(256)) 
    session_id = db.Column(db.Integer, default = 1)
    instructor_id = db.Column(db.Integer, default = 1)
    student_id = db.Column(db.Integer, default = 1)
    student_name = db.Column(db.String(256))
    course = db.Column(db.String(256))
    semester = db.Column(db.String(256))
    client = db.Column(db.String(256))
    disorder = db.Column(db.String(256))
    client_id = db.Column(db.Integer, default = 1)
    date = db.Column(db.String(256))
    course_instructor = db.Column(db.String(256))
          
    def __repr__(self):
        return self.b1_rating + ': ' + self.b2_rating + ': ' + self.b3_rating + ': ' + self.b4_rating

# Section C - 13 questions and common data
class section_c(db.Model):
    __tablename__ = 'section_c'   
    id = db.Column(db.Integer, primary_key = True)
    c1_rating = db.Column(db.Numeric(10,1), default = 1)
    c1_instructor_comment = db.Column(db.String(256))
    c1_student_comment = db.Column(db.String(256))  
    c2_rating = db.Column(db.Numeric(10,1), default = 1)
    c2_instructor_comment = db.Column(db.String(256))
    c2_student_comment = db.Column(db.String(256)) 
    c3_rating = db.Column(db.Numeric(10,1), default = 1)
    c3_instructor_comment = db.Column(db.String(256))
    c3_student_comment = db.Column(db.String(256)) 
    c4_rating = db.Column(db.Numeric(10,1), default = 1)
    c4_instructor_comment = db.Column(db.String(256))
    c4_student_comment = db.Column(db.String(256)) 
    c5_rating = db.Column(db.Numeric(10,1), default = 1)
    c5_instructor_comment = db.Column(db.String(256))
    c5_student_comment = db.Column(db.String(256)) 
    c6_rating = db.Column(db.Numeric(10,1), default = 1)
    c6_instructor_comment = db.Column(db.String(256))
    c6_student_comment = db.Column(db.String(256))  
    c7_rating = db.Column(db.Numeric(10,1), default = 1)
    c7_instructor_comment = db.Column(db.String(256))
    c7_student_comment = db.Column(db.String(256))  
    c8_rating = db.Column(db.Numeric(10,1), default = 1)
    c8_instructor_comment = db.Column(db.String(256))
    c8_student_comment = db.Column(db.String(256))  
    c9_rating = db.Column(db.Numeric(10,1), default = 1)
    c9_instructor_comment = db.Column(db.String(256))
    c9_student_comment = db.Column(db.String(256))  
    c10_rating = db.Column(db.Numeric(10,1), default = 1)
    c10_instructor_comment = db.Column(db.String(256))
    c10_student_comment = db.Column(db.String(256))  
    c11_rating = db.Column(db.Numeric(10,1), default = 1)
    c11_instructor_comment = db.Column(db.String(256))
    c11_student_comment = db.Column(db.String(256))  
    c12_rating = db.Column(db.Numeric(10,1), default = 1)
    c12_instructor_comment = db.Column(db.String(256))
    c12_student_comment = db.Column(db.String(256))  
    c13_rating = db.Column(db.Numeric(10,1), default = 1)
    c13_instructor_comment = db.Column(db.String(256))
    c13_student_comment = db.Column(db.String(256))  
    session_id = db.Column(db.Integer, default = 1)
    instructor_id = db.Column(db.Integer, default = 1)
    student_id = db.Column(db.Integer, default = 1)
    student_name = db.Column(db.String(256))
    course = db.Column(db.String(256))
    semester = db.Column(db.String(256))
    client = db.Column(db.String(256))
    disorder = db.Column(db.String(256))
    client_id = db.Column(db.Integer, default = 1)
    date = db.Column(db.String(256))
    course_instructor = db.Column(db.String(256))       

    def __repr__(self):
        return (self.c1_rating + ': ' + self.c2_rating + ': ' + self.c3_rating + ': ' + self.c4_rating + ': ' + self.c5_rating
                              + ': ' + self.c6_rating + ': ' + self.c7_rating + ': ' + self.c8_rating + ': ' + self.c9_rating
                              + ': ' + self.c10_rating + ': ' + self.c11_rating + ': ' + self.c12_rating + ': ' + self.c13_rating)

# Section D - 3 questions and common data
class section_d(db.Model):
    __tablename__ = 'section_d'   
    id = db.Column(db.Integer, primary_key = True)
    d1_rating = db.Column(db.Numeric(10,1), default = 1)
    d1_instructor_comment = db.Column(db.String(256))
    d1_student_comment = db.Column(db.String(256))  
    d2_rating = db.Column(db.Numeric(10,1), default = 1)
    d2_instructor_comment = db.Column(db.String(256))
    d2_student_comment = db.Column(db.String(256)) 
    d3_rating = db.Column(db.Numeric(10,1), default = 1)
    d3_instructor_comment = db.Column(db.String(256))
    d3_student_comment = db.Column(db.String(256)) 
    session_id = db.Column(db.Integer, default = 1)
    instructor_id = db.Column(db.Integer, default = 1)
    student_id = db.Column(db.Integer, default = 1)
    student_name = db.Column(db.String(256))
    course = db.Column(db.String(256))
    semester = db.Column(db.String(256))
    client = db.Column(db.String(256))
    disorder = db.Column(db.String(256))
    client_id = db.Column(db.Integer, default = 1)
    date = db.Column(db.String(256))
    course_instructor = db.Column(db.String(256))
            
    def __repr__(self):
        return self.d1_rating + ': ' + self.d2_rating + ': ' + self.d3_rating

# Section E - 2 questions and common data
class section_e(db.Model):
    __tablename__ = 'section_e'   
    id = db.Column(db.Integer, primary_key = True)
    e1_rating = db.Column(db.Numeric(10,1), default = 1)
    e1_instructor_comment = db.Column(db.String(256))
    e1_student_comment = db.Column(db.String(256))  
    e2_rating = db.Column(db.Numeric(10,1), default = 1)
    e2_instructor_comment = db.Column(db.String(256))
    e2_student_comment = db.Column(db.String(256)) 
    session_id = db.Column(db.Integer, default = 1)
    instructor_id = db.Column(db.Integer, default = 1)
    student_id = db.Column(db.Integer, default = 1)
    student_name = db.Column(db.String(256))
    course = db.Column(db.String(256))
    semester = db.Column(db.String(256))
    client = db.Column(db.String(256))
    disorder = db.Column(db.String(256))
    client_id = db.Column(db.Integer, default = 1)
    date = db.Column(db.String(256))
    course_instructor = db.Column(db.String(256))
    
    def __repr__(self):
        return self.e1_rating + ': ' + self.e2_rating

# The Admin user data
# this is also stored in the 'user' table but again
# may have future use.
class admin(db.Model):
    __tablename__ = 'admin'   
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64))
    session_id = db.Column(db.Integer)
    email = db.Column(db.String(64), unique=True)

# The Instructor user data
# this is also stored in the 'user' table but again
# may have future use.        
class instructor(db.Model):
    __tablename__ = 'instructor'   
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64))
    session_id = db.Column(db.Integer) 
    email = db.Column(db.String(64), unique=True)

# The Student user data
# Elements of this table are also stored in the 'user' table
# This table is used when the instructor or admin access students
class student(db.Model):
    __tablename__ = 'student'   
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer)
    student_name = db.Column(db.String(64))
    session_id = db.Column(db.Integer)
    class_year = db.Column(db.String(64))
    course = db.Column(db.String(64))
    semester = db.Column(db.String(64))
    course_instructor = db.Column(db.String(256))
    email = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return self.student_name + ': ' + str(self.session_id) + ': ' + str(self.class_year) 
        + ': ' + str(self.course_num) + ': ' + str(self.semester) + ': ' + str(self.course_instructor) + ': ' + str(self.email)

 
# The Client user data
# Elements of this table are also stored in the 'section_x' tables
# Due to HIPPA/FRPA this table currently has limited use but is here for future expansion    
class client(db.Model):
    __tablename__ = 'client'   
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256))
    date = db.Column(db.String(256))
    disorder = db.Column(db.String(256))
    session_id = db.Column(db.Integer)

# User extends the flask_login defined UserMixin class.  UserMixin
# provides default functionality that allows us to keep track of
# authenticated user
class user(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    role = db.Column(db.String(64))
    password_hash = db.Column(db.String(256), unique=True)

    def __repr__(self):
        return self.username + ': ' + str(self.email) + ': ' + str(self.password_hash) + ': ' + str(self.role)
        
    # Store hashed (encrypted) password in database        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Compare hashed (encrypted) password in database to entered password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# load_user is a function that's used by flask_login to manage the session.
# It simply returns the object associated with the authenticated user.
@login.user_loader
def load_user(id):
    return db.session.query(user).get(int(id))
