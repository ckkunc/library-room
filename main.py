from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime, timedelta


def main():
    global driver
    driver = Edge()
    driver.get("https://calendar.lib.unc.edu/reserve/davis-study-rooms")
    row_id = ['eid_29084', 'eid_29083', 'eid_29082', 'eid_29081', 'eid_29080', 'eid_29079']
    room_num = ['8052', '8051', '8049', '8048', '8047', '8046']
    
    # Get the current date
    current_date = datetime.now().date()

    # Calculate the date one week ahead
    two_weeks_ahead = current_date + timedelta(weeks=2)

    # Extract the month and date from the calculated date, fill in left side
    # with 0 if it is a single digit number
    month = f"{two_weeks_ahead.month:02d}"
    day = f"{two_weeks_ahead.day:02d}"
    year = f"{two_weeks_ahead.year:02d}"
    string_day = two_weeks_ahead.strftime('%A')
    string_month = two_weeks_ahead.strftime('%B')
    time.sleep(2)
    select_date(month, day)
    #reserve(month, day, year)
    time.sleep(1)

    for row_id, room_num in zip(row_id, room_num):
        try:
            select_time_slot(row_id, room_num, f'{string_day}, {string_month} {day}, {year}', '3:00pm', month, day, year)
            break  # If the function call was successful, break the loop
        except NoSuchElementException:
            continue  # If a NoSuchElementException was raised, continue with the next iteration
    input_box()
    driver.quit


def input_box():
    onyen = 'onyen'
    pw = 'pw'
    username_box = driver.find_element(By.CSS_SELECTOR, '#username')
    username_box.send_keys(onyen)
    time.sleep(1)
    next_button = driver.find_element(By.CSS_SELECTOR, '#nextBtn')
    next_button.click()
    password_box = driver.find_element(By.CSS_SELECTOR, '#password')
    password_box.send_keys(pw)


def select_time_slot(row, room, date, time_slot, month, day, year):
    # Locate the row for the desired room
    room_row = driver.find_element(By.XPATH, f"//td[@class='fc-timeline-lane fc-resource' and @data-resource-id='{row}']")

    # Locate the time slot within the row
    time_slot = room_row.find_element(By.XPATH, f".//a[@class='fc-timeline-event fc-h-event fc-event fc-event-start fc-event-end fc-event-future s-lc-eq-avail' and @title='{time_slot} {date} - Room {room} - Available']")

    # Click on the time slot to select it
    time_slot.click()

    time.sleep(3)
    
    # If the dropdown menu's ID isn't 58406914, try finding the menu with ID 1
    try:
        drop_down = driver.find_element(By.CSS_SELECTOR, 'select#bookingend_58406917')
    except NoSuchElementException:
        drop_down = driver.find_element(By.CSS_SELECTOR, 'select#bookingend_1')
    time.sleep(1)
    option = Select(drop_down)
    time.sleep(1)
    option.select_by_value(f'{year}-{month}-{day} 17:30:00')
    time.sleep(2)

    button_element = driver.find_element(By.CSS_SELECTOR, 'button#submit_times')
    button_element.click()
    time.sleep(2)


def select_date(month, day):
    # Locate the 'Go To Date' button and click it
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
    time.sleep(2)


if __name__ == '__main__':
   main()