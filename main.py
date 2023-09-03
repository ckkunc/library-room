from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from datetime import datetime, timedelta


def main():
    global driver 
    driver = Edge()
    driver.get("https://calendar.lib.unc.edu/reserve/davis-study-rooms")

    # Get the current date
    current_date = datetime.now().date()

    # Calculate the date one week ahead
    two_weeks_ahead = current_date + timedelta(weeks=2)

    # Extract the month and date from the calculated date, fill in left side
    # with 0 if it is a single digit number
    month = f"{two_weeks_ahead.month:02d}"
    day = f"{two_weeks_ahead.day:02d}"

    select_date(month, day)
    reserve(month, day)
    driver.quit


def reserve(month: int, day: int):

    time.sleep(2)

    element = driver.find_element(By.CSS_SELECTOR, "div.fc-timeline-event-harness a.fc-timeline-event")
    element.click()

    time.sleep(2)

    drop_down = driver.find_element(By.CSS_SELECTOR, "select#bookingend_1")
    time.sleep(2)
    option = Select(drop_down)
    time.sleep(2)
    option.select_by_value(f"2023-{month}-{day} 12:30:00")
    time.sleep(2)

    button_element = driver.find_element(By.CSS_SELECTOR, "button#submit_times")
    button_element.click()
    time.sleep(5)


def select_date(month, day):
    # Locate the "Go To Date" button and click it
    go_to_date_button = driver.find_element(By.CSS_SELECTOR, '.fc-goToDate-button')
    go_to_date_button.click()

    # Click the month switch to open the month selection menu
    month_switch = driver.find_element(By.CSS_SELECTOR, '.datepicker-switch')
    month_switch.click()

    # Select the desired month
    months = driver.find_elements(By.CSS_SELECTOR, '.month')
    months[int(month) - 1].click()

    # Select the desired day
    days = driver.find_elements(By.CSS_SELECTOR, '.day')
    for d in days:
        if d.text == str(day):
            d.click()
            break
    time.sleep(5)

if __name__ == "__main__":
    main()