def declaration_login():
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
    requester = current_user.name
    # Selenium setup
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.getenv("GOOGLE_CHROME_BIN")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=os.getenv('CHROMEDRIVER_PATH'), chrome_options=chrome_options)

    print('Staring declaration process. Logging in...')
    time.sleep(3)
    # This is the website form:
    driver.get(
        'https://forms.office.com/Pages/ResponsePage.aspx?id=IX3zmVwL6kORA-FvAvWuz-st4tjPcIRPvfsxXephpFpUQlhMMVpHQTRaRjA5MFIxWjJZUkc1SDE4Ny4u')
    driver.implicitly_wait(60)
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
    time.sleep(3)

    #  Page 1
    # Primary Program
    primary_program = driver.find_element_by_xpath(
        '//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div/div[1]/div/label/input')  # Setting primary program to true for first declaration
    primary_program.click()
    print('Primary program clicked...')

    # Effective Term
    current_term = driver.find_element_by_xpath(
        '//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div/label/input')
    next_term = driver.find_element_by_xpath(
        '//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div/label/input')
    if effective_term_text == "This Semester":
        current_term.click()  # if effective term is current term
    else:
        next_term.click()  # if effective term is next term
    print(f'Effective term is set to {effective_term_text}.')

    # Student's Name
    student_name = driver.find_element_by_xpath(
        '//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div/div/input')
    student_name.send_keys(studentFN + ' ' + studentLN)
    print(f'Sending student\'s full name as {studentFN} {studentLN}. ')

    # Student's ID
    student_id = driver.find_element_by_xpath(
        '//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[4]/div/div[2]/div/div/input')
    student_id.send_keys(studentID)
    print(f'Sending student\'s id as {studentID}.')

    # Student's Email
    student_email_input = driver.find_element_by_xpath(
        '//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[5]/div/div[2]/div/div/input')
    student_email_input.send_keys(studentEmail)
    print(f'Sending student\'s email as {studentEmail}.')

    # Student's Phone
    student_phone_input = driver.find_element_by_xpath(
        '//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[6]/div/div[2]/div/div/input')
    student_phone_input.send_keys(studentPhone)
    print(f'Sending student\'s phone as {studentPhone}.')

    # Requester Name
    requester_input = driver.find_element_by_xpath(
        '//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[7]/div/div[2]/div/div/input')
    requester_input.send_keys(requester)
    print(f'Form prepared by {requester}')
    time.sleep(2)

    # Next Button
    next_btn = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div[1]/div[2]/div[3]/div[1]/button/div')
    next_btn.click()
    print('Clicking to next page...')
    time.sleep(3)

    print('Second page loaded...Ending...')

    if status_text == "Undeclared":
        print('from Undeclared')
        time.sleep(3)
        from_college_code = driver.find_element_by_xpath(
            '//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div/div[2]/div/label/input')
        from_college_code.click()
        from_degree_code = driver.find_element_by_xpath(
            '//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[2]/div/div[2]/div/div/input')
        from_degree_code.send_keys('00')
        teacher_cert = driver.find_element_by_xpath(
            '//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[14]/div/div[2]/div/div[2]/div/label/input')
        teacher_cert.click()
        next_btn = driver.find_element_by_xpath(
            '/html/body/div/div/div/div/div/div/div[1]/div[2]/div[3]/div[1]/button[2]/div')
        next_btn.click()
        time.sleep(4)
    else:
        pass

    # Page 3 // To
    print(f'Declaring student with College Code of {collegeCode}')
    if collegeCode == "AS":
        print('This is the AS option')
        college_to_btn = driver.find_element_by_xpath(
            '//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div/div[1]/div/label/input')
        college_to_btn.click()
    else:
        pass

    to_degree_code = driver.find_element_by_xpath(
        '//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[2]/div/div[2]/div/div/input')
    to_degree_code.send_keys(degreeCode)
    print(f'Sending degree code of {degreeCode}')
    print(f'Sending majorCode of {majorCode}')

    time.sleep(3)
    driver.close()
    return