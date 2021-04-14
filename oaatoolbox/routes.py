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
import time



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
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/_runSelenium", methods=['GET', 'POST'])
def selenium():
    # Toolbox Information
    print('Staring declaration process. Logging in...')
    e_ID = request.form['advisorEmail']
    e_password = request.form['advisorPw']
    effective_term_text = request.form['effective_term_text']
    # studentFN = request.form['studentFN']
    # studentLN = request.form['studentLN']
    # studentID = request.form['studentID']
    # studentEmail = request.form['studentEmail']
    # studentPhone = request.form['studentPhone']
    # studentMajor = request.form['studentMajor']
    # studentMinor = request.form['studentMinor']
    # majorCode = request.form['majorCode']
    # degreeCode = request.form['degreeCode']
    # collegeCode = request.form['collegeCode']
    # requester = current_user.username

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
    driver.get('https://forms.office.com/Pages/ResponsePage.aspx?id=IX3zmVwL6kORA-FvAvWuz-st4tjPcIRPvfsxXephpFpUQlhMMVpHQTRaRjA5MFIxWjJZUkc1SDE4Ny4u')
    driver.implicitly_wait(15)
    time.sleep(3)
    # Login Screen
    email_input = driver.find_element_by_xpath('//*[@id="i0116"]')  # email input
    email_input.send_keys(e_ID)
    next_btn = driver.find_element_by_xpath('//*[@id="idSIButton9"]')  # next button on log in page
    next_btn.click()
    time.sleep(3)
    # Password Screen
    password_input = driver.find_element_by_xpath('//*[@id="i0118"]')  # password input
    password_input.send_keys(e_password)
    sign_in = driver.find_element_by_xpath('//*[@id="idSIButton9"]')  # sign-in button on password page
    sign_in.click()
    time.sleep(3)
    # Reduce Sign-ins Page
    yes_btn = driver.find_element_by_xpath('//*[@id="idSIButton9"]')  # Yes button on reduced sign in page
    yes_btn.click()
    print(f'successfully logged in as {e_ID}.')
    time.sleep(2)

    #  Page 1
    # Primary Program
    primary_program = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div/div[1]/div/label/input')  # Setting primary program to true for first declaration
    primary_program.click()
    print('Primary program clicked...')

    # Effective Term
    current_term = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div/label/input')
    next_term = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div/label/input')
    if effective_term_text == "This Semester":
        current_term.click()  # if effective term is current term
    else:
        next_term.click()  # if effective term is next term
    print(f'Effective term is set to {effective_term_text}.')

    # # Student's Name
    # student_full_name = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div/div/input')
    # student_full_name.send_keys(studentFN + ' ' + studentLN)
    # print(f'Sending student\'s first name as {studentFN + studentLN}.')
    #
    # # Student's ID
    # student_id = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[4]/div/div[2]/div/div/input')
    # student_id.send_keys(studentID)
    # print(f'Sending student\'s id as {studentID}.')
    #
    # # Student's Email
    # student_email_input = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[5]/div/div[2]/div/div/input')
    # student_email_input.send_keys(studentEmail)
    # print(f'Sending student\'s email as {studentEmail}.')
    #
    # # Student's Phone
    # student_phone_input = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[6]/div/div[2]/div/div/input')
    # student_phone_input.send_keys(studentPhone)
    # print(f'Sending student\'s phone as {studentPhone}.')
    #
    # # Requester Name
    # requester_input = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[7]/div/div[2]/div/div/input')
    # requester_input.send_keys(requester)
    # print(f'Form prepared by {requester}')
    #
    # # Next Button
    # next_btn = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[3]/div[1]/button/div')
    # next_btn.click()
    # print('Clicking to next page...')
    # time.sleep(5)

    # # Second Page FROM Status
    # driver.close()
    # print(f'Information would have sent.')
    driver.close()
    return render_template('declare.html', cctitle="Declaration")


@app.route('/declare')
@login_required
def declare():
    majors = Majors.query.all()
    majors_list = []
    minors = Minors.query.all()
    minors_list = []
    for major in majors:
        majors_list.append({"name": major.majors, "Requirements": major.majorRequirements, "majorCode": major.majorCode, "degreeCode": major.degreeCode, "collegeCode": major.collegeCode})
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
