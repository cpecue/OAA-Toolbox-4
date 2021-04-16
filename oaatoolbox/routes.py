import logging
import threading
from flask import render_template, url_for, flash, redirect, request
from selenium.webdriver.support.wait import WebDriverWait
import secrets
import os
from PIL import Image
from oaatoolbox import app, db, bcrypt
from oaatoolbox.forms import RegistrationForm, LoginForm, UpdateAccountForm
from oaatoolbox.models import User, Declarations, Majors, Minors
from flask_login import login_user, current_user, logout_user, login_required
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from rq import Queue
import redis
from worker import conn


q = Queue(connection=conn)

# my background threadf
class MyWorker():

  def __init__(self, message):
    self.message = message

    thread = threading.Thread(target=self.run, args=())
    thread.daemon = True
    thread.start()

  def run(self):
    logging.info(f'run MyWorker with parameter {self.message}')

    # do something


def to_background(e_ID, e_password, effective_term_text, studentFN, studentLN, studentID, studentEmail, studentPhone, requester, status_text, collegeCode, degreeCode, majorCode, majorConc, strippedName):
    time.sleep(3)
    print('It successfully grabs the queue')
    # Selenium setup
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.getenv("GOOGLE_CHROME_BIN")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=os.getenv('CHROMEDRIVER_PATH'), chrome_options=chrome_options)
    time.sleep(3)
    # This is the website form:
    driver.get('https://forms.office.com/Pages/ResponsePage.aspx?id=IX3zmVwL6kORA-FvAvWuzwdoWEcc_LNCksX8Xu0GatNUMFAwSDJONjZXUTBUN0NDRklTS1ZJRlpOSi4u')
    time.sleep(3)
    # Login Screen
    email_input = driver.find_element_by_xpath('//*[@id="i0116"]')  # email input
    email_input.send_keys(e_ID)
    email_input.send_keys(Keys.ENTER)
    time.sleep(3)
    # Password Screen
    password_input = driver.find_element_by_xpath('//*[@id="i0118"]')  # password input
    password_input.send_keys(e_password)
    password_input.send_keys(Keys.ENTER)
    time.sleep(3)
    # Reduce Sign-ins Page
    yes_btn = driver.find_element_by_xpath('//*[@id="idSIButton9"]')  # Yes button on reduced sign in page
    yes_btn.click()
    print(f'successfully logged in as {e_ID}.')
    time.sleep(4)
    #  Page 1
    # Primary Program
    primary_program = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div/div[2]/div/div[1]/div/label/input')  # Setting primary program to true for first declaration
    primary_program.click()
    print('Primary program clicked...')

    # Effective Term
    if effective_term_text == "This Semester":
        primary_program.send_keys(Keys.TAB, Keys.SPACE)
    else:
        primary_program.send_keys(Keys.TAB, Keys.TAB, Keys.SPACE)
    print(f'Effective term is set to {effective_term_text}.')

    # Student's Name
    student_name = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/div/div/input')
    student_name.send_keys(studentFN + ' ' + studentLN)
    print(f'Sending student\'s full name as {studentFN} {studentLN}. ')

    # Student's ID
    student_id = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[4]/div/div[2]/div/div/input')
    student_id.send_keys(studentID)
    print(f'Sending student\'s id as {studentID}.')

    # Student's Email
    student_email_input = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[5]/div/div[2]/div/div/input')
    student_email_input.send_keys(studentEmail)
    print(f'Sending student\'s email as {studentEmail}.')

    # Student's Phone
    student_phone_input = driver.find_element_by_xpath(
        '//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[6]/div/div[2]/div/div/input')
    student_phone_input.send_keys(studentPhone)
    print(f'Sending student\'s phone as {studentPhone}.')

    # Requester Name
    requester_input = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[7]/div/div[2]/div/div/input')
    requester_input.send_keys(requester)
    print(f'Form prepared by {requester}')

    if status_text == "Undeclared":
        print('from Undeclared')
        from_college_code = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[8]/div/div[2]/div/div[2]/div/label/input')
        from_college_code.click()
        from_degree_code = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[9]/div/div[2]/div/div/input')
        from_degree_code.send_keys('00')
        teacher_cert = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[21]/div/div[2]/div/div[2]/div/label/input')
        teacher_cert.click()
    else:
        pass

    print(f'Declaring student with College Code of {collegeCode}')
    if collegeCode == "AS":
        print('This is the AS option')
        college_to_btn = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[22]/div/div[2]/div/div[1]/div/label/input')
        college_to_btn.click()
    else:
        pass

    to_degree_code = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[23]/div/div[2]/div/div/input')
    to_degree_code.send_keys(degreeCode)
    print(f'Sending degree code of {degreeCode}')
    print(f'Sending majorCode of {majorCode}')
    print(f'Sending majorConc of {majorConc}')
    print(f'Sending strippedName of {strippedName}')

    driver.close()
    return



@app.route('/')
@login_required
def home():
    return render_template('home.html', cctitle="Dashboard")


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if current_user.role == "1":
        if current_user.is_authenticated:
            # return redirect('/')
            form = RegistrationForm()
            if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = User(username=form.username.data, email=form.email.data, password=hashed_password, name=form.name.data, role=form.role.data)
                db.session.add(user)
                db.session.commit()
                flash(f'Your account has been created!', 'success')
                return redirect(url_for('login'))
            return render_template('register.html', cctitle="Register", form=form)
    else:
        return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/')
        else:
            flash('Login Unsuccessful', 'danger')
    return render_template('login.html', cctitle="Login", form=form)

@app.route('/major-management')
def majorManagement():
    return render_template('major-management.html', title='Major Management')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


def save_picture(form_picture):
    random_hex = secrets.token_bytes(16)
    # random_hex = "12312h345h2j34"
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    # i.thumbnail(output_size)
    i = i.resize((125,125), Image.ANTIALIAS)
    i.save(picture_path)
    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/_runSelenium", methods=['GET', 'POST'])
def selenium():
    MyWorker('param_value')
    # Toolbox Information
    print('Staring declaration process. Logging in...')
    e_ID = request.form['advisorEmail']
    e_password = request.form['advisorPw']
    effective_term_text = request.form['effective_term_text']
    studentFN = request.form['studentFN']
    studentLN = request.form['studentLN']
    studentID = request.form['studentID']
    studentEmail = request.form['studentEmail']
    studentPhone = request.form['studentPhone']
    status_text = request.form['status_text']
    collegeCode = request.form['collegeCode']
    degreeCode = request.form['degreeCode']
    majorCode = request.form['majorCode']
    majorConc = request.form['majorConc']
    strippedName = request.form['strippedName']
    requester = current_user.name
    print(majorConc)
    result = q.enqueue(to_background, e_ID, e_password, effective_term_text, studentFN, studentLN, studentID, studentEmail, studentPhone, requester, status_text, collegeCode, degreeCode, majorCode, majorConc, strippedName)
    return render_template('declare.html', title='Declaration Success')


@app.route('/declare')
@login_required
def declare():
    majors = Majors.query.all()
    majors_list = []
    minors = Minors.query.all()
    minors_list = []
    for major in majors:
        majors_list.append({"name": major.majors, "Requirements": major.majorRequirements, "majorCode": major.majorCode, "degreeCode": major.degreeCode, "collegeCode": major.collegeCode, "majorConc": major.majorConc, "strippedName": major.strippedName})
    for minor in minors:
        minors_list.append({"name": minor.minors, "minorCode": minor.minorCode, "minorCollegeCode": minor.minorCollegeCode})
    return render_template('declare.html', cctitle="Declaration", majors_list=majors_list, minors_list=minors_list)


@app.route('/finaid')
@login_required
def finaid():
    return render_template('finaid.html', cctitle="Financial Aid")


@app.route('/test')
@login_required
def test():
    return render_template('test.html', cctitle="Test Environ")


@app.route('/layout')
@login_required
def layout():
    return render_template('layout.html', cctitle="Layout")

@app.route('/success')
@login_required
def success():
    return render_template('success.html', cctitle="Success")

@app.route('/about', methods=['GET', 'POST'])
@login_required
def about():
    return render_template('about.html', cctitle="About")


@app.route('/quick-notes')
@login_required
def quick_notes():
    return render_template('quick-notes.html', cctitle="Quick Notes")


@app.route('/password')
@login_required
def password():
    return render_template('password.html', cctitle="Password")


@app.route('/gpa-calc')
@login_required
def gpa():
    return render_template('gpa-calc.html', cctitle="GPA Calculation")