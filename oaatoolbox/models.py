from oaatoolbox import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(40), nullable=False)
    role = db.Column(db.String(40), nullable=False, default="False")
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    declarations = db.relationship('Declarations', backref='advisor', lazy="dynamic")

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Declarations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_fn = db.Column(db.String(60), nullable=False)
    student_ln = db.Column(db.String(60), nullable=False)
    student_ID = db.Column(db.Integer(), nullable=False)
    major_1 = db.Column(db.String(30), nullable=False)
    minor_1 = db.Column(db.String(30))
    major_2 = db.Column(db.String(30))
    minor_2 = db.Column(db.String(30))
    date_declared = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Declarations('{self.student_fn}', '{self.student_ln}', '{self.student_ID}', '{self.major_1}', " \
               f"'{self.minor_1}', '{self.major_2}', '{self.minor_2}', '{self.date_declared}')"


class Majors(db.Model):
    idmajors = db.Column(db.Integer, primary_key=True)
    majors = db.Column(db.String(100), nullable=False)
    majorRequirements = db.Column(db.String(60), nullable=False)
    majorPrimaryContact = db.Column(db.String(100), nullable=False)
    majorSecondaryContact = db.Column(db.String(100))
    majorCode = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Major('{self.majors}', '{self.majorRequirements}', '{self.majorPrimaryContact}', '{self.majorSecondaryContact}', '{self.majorCode}')"
