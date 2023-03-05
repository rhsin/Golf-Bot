import time
from datetime import datetime, timedelta
from inputs import input_course, input_days, order_courses
from script import login, open_non_resident, find_tee_time
from pytz import timezone
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

global driver

first_course = input_course()
courses = order_courses(first_course)

days_ahead = input_days()
date = datetime.today() + timedelta(days=(days_ahead))

print("Scheduled for 7:00pm EST...")

# while True:
#   est_tz = timezone('US/Eastern')
#   target_time = datetime.now(est_tz).replace(hour=19, minute=0, second=0, microsecond=0)

#   if datetime.now(est_tz) >= target_time:
#     break

print("It is 7:00pm EST, Running Golf-Bot Now!") 

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(
  service= Service(ChromeDriverManager().install()), 
  options=options,
)

driver.get("https://foreupsoftware.com/index.php/booking/index/19765#/")

assert "Bethpage State Park - Online Booking" in driver.title
print("Browser Opened...")

open_non_resident(driver)
# login(driver)

end_script = time.time() + 86400
while time.time() < end_script:
  result = find_tee_time(driver, date, courses)
  if result == "Tee-Time Found!":
    break
  else:
    time.sleep(5)

print("Will close browser in 5 mins...")
time.sleep(300)
driver.close()
