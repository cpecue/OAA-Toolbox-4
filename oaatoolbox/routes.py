from flask import render_template, url_for, flash, redirect, request
import secrets
import os
from PIL import Image
from oaatoolbox import app, db, bcrypt
from oaatoolbox.forms import RegistrationForm, LoginForm, UpdateAccountForm
from oaatoolbox.models import User, Declarations, Majors
from flask_login import login_user, current_user, logout_user, login_required
from selenium import webdriver
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
    e_ID = request.form['advisorEmail']
    e_password = request.form['advisorPw']
    studentFN = request.form['studentFN']
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROME_DRIVER_PATH"), chrome_options=chrome_options)

    driver.get(
        'https://forms.office.com/Pages/ResponsePage.aspx?id=IX3zmVwL6kORA-FvAvWuzwdoWEcc_LNCksX8Xu0GatNURThSMDBZQ01QS082SUpESE5QTlZQTEkwVi4u')
    time.sleep(5)
    email = driver.find_element_by_xpath('//*[@id="i0116"]')
    email.send_keys(e_ID)
    next = driver.find_element_by_xpath('//*[@id="idSIButton9"]')
    time.sleep(1)
    next.click()
    time.sleep(2)
    password = driver.find_element_by_xpath(
        '/html/body/div/form[1]/div/div/div[2]/div/div/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div/div[2]/input')
    password.send_keys(e_password)
    time.sleep(3)
    next = driver.find_element_by_xpath(
        '/html/body/div/form[1]/div/div/div[2]/div/div/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div/div/div/div/input')
    next.click()
    time.sleep(3)
    yes = driver.find_element_by_xpath(
        '/html/body/div/form/div/div/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div/div/div[2]/input')
    yes.click()

    major = driver.find_element_by_xpath(
        '/html/body/div/div/div/div/div/div/div[1]/div[2]/div[2]/div/div/div[2]/div/div/input')
    major.send_keys(studentFN)

    minor = driver.find_element_by_xpath(
        '//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div/input')
    minor.send_keys('CHEM')

    student = driver.find_element_by_xpath(
        '/html/body/div/div/div/div/div/div/div[1]/div[2]/div[2]/div[3]/div/div[2]/div/div/input')
    student.send_keys('Caleb Pecue')
    time.sleep(2)
    button = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div[1]/div[2]/div[3]/div[1]/button/div')
    time.sleep(2)
    driver.close()


@app.route('/declare')
@login_required
def declare():
    majors = Majors.query.all()
    majors_list = []
    for major in majors:
        majors_list.append({"name": major.majors, "Requirements": major.majorRequirements, "MajorPrimaryContact": major.majorPrimaryContact, "majorCode": major.majorCode})


    return render_template('declare.html', cctitle="Declaration", majors_list=majors_list)


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
