import time
from datetime import datetime, timedelta
from inputs import input_course, input_days, order_courses
from script import login, open_non_resident, find_tee_time
from pytz import timezone
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

global driver

first_course = input_course()
courses = order_courses(first_course)

days_ahead = input_days()
date = datetime.today() + timedelta(days=(days_ahead))

print("Scheduled for 7:00pm EST...")

while True:
  est_tz = timezone('US/Eastern')
  target_time = datetime.now(est_tz).replace(hour=19, minute=20, second=0, microsecond=0)

  if datetime.now(est_tz) >= target_time:
    break

print("It is 7:00pm EST, Running Golf-Bot Now!") 

service = Service("./chromedrive_py")
driver = webdriver.Chrome(service=service)

driver.get("https://foreupsoftware.com/index.php/booking/index/19765#/")

assert "Bethpage State Park - Online Booking" in driver.title
print("Browser Opened...")

login(driver)
# open_non_resident(driver)
find_tee_time(driver, date, courses)

print("Will close browser in 5 mins...")
time.sleep(300)
driver.close()
