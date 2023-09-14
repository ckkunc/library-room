from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time, os
from dotenv import load_dotenv
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
    time.sleep(1)

    # If the room is already booked at 3:30, try the next room above it
    for row_id, room_num in zip(row_id, room_num):
        success = select_time_slot(row_id, room_num, f'{string_day}, {string_month} {day}, {year}', '3:30pm', month, day, year)
        if success:
            break  # If the function call was successful, break the loop
        
    input_box()
    driver.quit


def input_box():
    load_dotenv()
    onyen = os.getenv('ONYEN')
    pw = os.getenv('PW')
    username_box = driver.find_element(By.CSS_SELECTOR, '#username')
    username_box.send_keys(onyen)
    time.sleep(1)
    next_button = driver.find_element(By.CSS_SELECTOR, '#nextBtn')
    next_button.click()
    time.sleep(3)
    password_box = driver.find_element(By.CSS_SELECTOR, '#password')
    password_box.send_keys(pw)
    submit_button = driver.find_element(By.CSS_SELECTOR, '#submitBtn')
    submit_button.click()
    time.sleep(3)
    complete_booking = driver.find_element(By.CSS_SELECTOR, '#terms_accept')
    complete_booking.click()
    time.sleep(3)
    input_box = driver.find_element(By.CSS_SELECTOR, '#nick')
    input_box.send_keys('Studying')
    submit_booking = driver.find_element(By.CSS_SELECTOR, '#btn-form-submit')
    submit_booking.click()
    time.sleep(3)


def select_time_slot(row, room, date, time_slot, month, day, year) -> bool:
    try:
        # Locate the row for the desired room
        room_row = driver.find_element(By.XPATH, f"//td[@class='fc-timeline-lane fc-resource' and @data-resource-id='{row}']")

        # Locate the time slot within the row
        time_slot = room_row.find_element(By.XPATH, f".//a[@class='fc-timeline-event fc-h-event fc-event fc-event-start fc-event-end fc-event-future s-lc-eq-avail' and @title='{time_slot} {date} - Room {room} - Available']")

        # Click on the time slot to select it
        time_slot.click()

        time.sleep(2)
        
        # If the dropdown menu's ID isn't 58406914, try finding the menu with ID 1
        try:
            drop_down = driver.find_element(By.CSS_SELECTOR, 'select#bookingend_58406917')
        except NoSuchElementException:
            drop_down = driver.find_element(By.CSS_SELECTOR, 'select#bookingend_1')
        time.sleep(1)   
        option = Select(drop_down)
        time.sleep(1)

        times = ['18:30:00', '18:00:00', '1:730:00', '17:00:00', '16:30:00', '16:00:00',]
        for slot in times:
            try:
                option.select_by_value(f'{year}-{month}-{day} {slot}')
                break
            except NoSuchElementException:
                continue
                
        time.sleep(2)

        button_element = driver.find_element(By.CSS_SELECTOR, 'button#submit_times')
        button_element.click()
        time.sleep(2)
        return True
    except NoSuchElementException:
        return False

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
    days = driver.find_elements(By.CSS_SELECTOR, 'td.day:not(.old):not(.disabled)')
    for d in days:
        if d.text == str(day):
            d.click()
            break
    time.sleep(2)


if __name__ == '__main__':
   main()