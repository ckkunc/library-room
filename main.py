from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

driver = Edge()
driver.get("https://calendar.lib.unc.edu/reserve/davis-study-rooms")

time.sleep(2)

date = driver.find_element(By.CSS_SELECTOR, "button.fc-goToNextAvailable-button")
date.click()

time.sleep(2)

element = driver.find_element(By.CSS_SELECTOR, "div.fc-timeline-event-harness a.fc-timeline-event")
element.click()

time.sleep(2)

drop_down = driver.find_element(By.CSS_SELECTOR, "select#bookingend_1")
time.sleep(2)
option = Select(drop_down)
time.sleep(2)
option.select_by_value("2023-08-30 09:30:00")
time.sleep(2)

button_element = driver.find_element(By.CSS_SELECTOR, "button#submit_times")
button_element.click()
time.sleep(5)

print("Success")

driver.quit
