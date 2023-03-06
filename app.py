import time
from flask import Flask, request, render_template
from datetime import datetime, timedelta
# from pytz import timezone
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

global driver

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        form_course = request.form.get("first_course")
        form_days = request.form.get("days_ahead")

        first_course = input_course(form_course)
        days_ahead = input_days(form_days)
        
        courses = order_courses(first_course)
        date = datetime.today() + timedelta(days=(days_ahead))

        # print("Scheduled for 7:00pm EST...")

        # while True:
        #     est_tz = timezone('US/Eastern')
        #     target_time = datetime.now(est_tz).replace(hour=19, minute=0, second=0, microsecond=0)

        #     if datetime.now(est_tz) >= target_time:
        #         break

        # print("It is 7:00pm EST, Running Golf-Bot Now!") 

        option = webdriver.ChromeOptions()

        option.add_argument("--disable-gpu")
        option.add_argument("--disable-extensions")
        option.add_argument("--disable-infobars")
        option.add_argument("--start-maximized")
        option.add_argument("--disable-notifications")
        option.add_argument('--headless')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=option)

        driver.get("https://foreupsoftware.com/index.php/booking/index/19765#/")

        assert "Bethpage State Park - Online Booking" in driver.title
        print("Browser Opened...")

        login(driver)
        # open_non_resident(driver)

        # end_script = time.time() + 22000
        end_script = time.time() + 600
        while time.time() < end_script:
            result = find_tee_time(driver, date, courses)
            if result == "Tee-Time Found!":
                break
            else:
                # time.sleep(60)
                time.sleep(5)

        print("Will close browser in 5 mins...")
        time.sleep(300)
        driver.close()

    return render_template('index.html')


def login(driver):
    button_resident = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='content']/div/button[1]")))
    button_resident.click()

    button_login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='teetime-login']/div/p[1]/button")))
    button_login.click()

    input_email = driver.find_element(By.XPATH, "//*[@id='login_email']")
    input_email.send_keys("jschwa19@binghamton.edu")

    input_password = driver.find_element(By.XPATH, "//*[@id='login_password']")
    input_password.send_keys("GolfBot12!")

    button_submit = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='login']/div/div[3]/div/button[1]")))
    button_submit.click()

    print("Login Successful!")

def open_non_resident(driver):
    button_non_resident = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='content']/div/button[2]")))
    button_non_resident.click()

def find_tee_time(driver, date, courses):
    select_course = Select(WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "schedule_select"))))
    select_course.select_by_visible_text(courses[0])

    input_date = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='date-field']")))
    input_date.send_keys(Keys.CONTROL + "a")
    input_date.send_keys(Keys.DELETE)
    input_date.send_keys(date.strftime("%m-%d-%Y"))
    input_date.send_keys(Keys.RETURN)

    # button_time_morning = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='nav']/div/div[4]/div[1]/div[1]/a[1]")))
    # button_time_morning.click()

    time.sleep(1)

    for course in courses:
        try:
            time_tile = driver.find_element(By.CLASS_NAME, "booking-start-time-label")
            time_tile.click()
            print("Tee-Time Found!")
            return "Tee-Time Found!"

        except NoSuchElementException:
            print("No Tee-Time: " + course)

            select_course = Select(WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "schedule_select"))))
            select_course.select_by_visible_text(course)
            time.sleep(1)

    print("Checked All Courses!")
    return "Checked All Courses!"

def input_course(first_course):
    if not first_course:
        return "Bethpage Yellow Course"
    else:
        course = first_course.lower()

    if course == 'y':
        return "Bethpage Yellow Course"
    if course == 'b':
        return "Bethpage Blue Course"     
    if course == 'r':
        return "Bethpage Red Course"    
    if course == 'g':
        return "Bethpage Green Course" 
    else:
        return "Bethpage Yellow Course"   

def input_days(days_ahead):
    try: 
        days_ahead = int(days_ahead)
        if 1 <= days_ahead <= 7:
            print(days_ahead)
            return days_ahead
        else: 
            return 1
    except:
        return 1

def order_courses(first_course):
    courses = ["Bethpage Blue Course", "Bethpage Yellow Course", "Bethpage Red Course", "Bethpage Green Course"]

    for course in courses:
        if course == first_course:
            courses.remove(course)      

    courses.insert(0, first_course) 
    print(courses)
    return courses