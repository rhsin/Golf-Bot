from flask import Flask, request, render_template
from script import schedule_tee_times

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        schedule_tee_times()

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