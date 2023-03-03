import time
import sched
from datetime import datetime, timedelta
from pytz import timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

global driver

email = "jschwa19@binghamton.edu"
password = "GolfBot12!"
course_yellow = "Bethpage Yellow Course"
date = datetime.today()

service = Service("./chromedrive_py")
driver = webdriver.Chrome(service=service)


def open_browser():
  driver.get("https://foreupsoftware.com/index.php/booking/index/19765#/")

  assert "Bethpage State Park - Online Booking" in driver.title
  print("Browser Opened...")


def schedule_tee_time():
  print("Scheduled for 7:00pm EST...")

  while True:
    est_tz = timezone('US/Eastern')
    target_time = datetime.now(est_tz).replace(hour=3, minute=28, second=0, microsecond=0)

    if datetime.now(est_tz) >= target_time:
      break
  
  print("It is 7:00pm EST, Running Golf-Bot Now!") 

  open_browser()
  open_non_resident()
  find_tee_time(course_yellow)
  print("Finished Scheduling Tee-Time!")


def login():
  button_resident = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='content']/div/button[1]"))).click()
  time.sleep(1)

  button_login_first = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='teetime-login']/div/p[1]/button"))).click()
  time.sleep(1)

  input_email = driver.find_element(By.XPATH, "//*[@id='login_email']")
  input_email.send_keys(email)

  input_password =driver.find_element(By.XPATH, "//*[@id='login_password']")
  input_password.send_keys(password)

  button_login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='login']/div/div[3]/div/button[1]"))).click()
  time.sleep(1)

  print("Login Successful!")


def open_non_resident():
  button_non_resident = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='content']/div/button[2]"))).click()
  time.sleep(1)
 

def find_tee_time(course):
  select_course = Select(WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "schedule_select"))))
  select_course.select_by_visible_text(course)
  time.sleep(1)

  # button_time_morning = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='nav']/div/div[4]/div[1]/div[1]/a[1]"))).click()
  # time.sleep(1)

  button_time_midday = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='nav']/div/div[4]/div[1]/div[1]/a[2]"))).click()
  time.sleep(1)

  for i in range(7):
    try:
      time_tile = driver.find_element(By.CLASS_NAME, "booking-start-time-label")
      time_tile.click()
      print("Tee-Time Found!")
      break

    except NoSuchElementException:
      print("No Tee-Time: day " + str(i))

      input_date = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='date-field']")))
      input_date.send_keys(Keys.CONTROL + "a")
      input_date.send_keys(Keys.DELETE)
      input_date.send_keys((date + timedelta(days=(i+1))).strftime("%m-%d-%Y"))
      input_date.send_keys(Keys.RETURN)
      time.sleep(1)

  print("Checked: " + course)


def job():
  open_browser()
  open_non_resident()
  find_tee_time(course_yellow)

# sched.at("12:17").do(job())

schedule_tee_time()

print("Will close browser in 5 mins...")
time.sleep(300)
driver.close()
