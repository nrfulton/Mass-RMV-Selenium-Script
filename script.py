# MA RMV is appointment only and appointments are released sporadically throughout the day (eg due to cancellations).
# This script continuously searches all/some (toggle nearby_only) RMV offices for a license transfer appointment in October.
# An appointment is not actually booked. The script will just beep and print out the options, leaving a window open on the selection page.
# ten second wait between checks; there's no acceptable use policy or robots.txt on the website so choosing an excessively good-citizeny wait time.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

print("\a\a\a")

def print_appt_dates(all_appt_dates):
    for location_name in all_appt_dates.keys():
        print(location_name.replace("\n", ""))
        for date in all_appt_dates[location_name]:
            print(f"\t{date}")


nearby_only = True
driver = webdriver.Firefox()
found_desired_appt = False

try:
    while not found_desired_appt:
        print("retarting...")
        time.sleep(10)
        driver.quit()
        driver = webdriver.Firefox()
        driver.get("https://rmvmassdotappt.cxmflow.com/Appointment/Index/2c052fc7-571f-4b76-9790-7e91f103c408")

        # Find the LICENSING/ID APPOINTMENT button and click it.
        id_appt_btn = None
        elems = driver.find_elements(By.TAG_NAME, "button")
        for elem in elems:
            if elem.text == "LICENSING/ID APPOINTMENT":
                id_appt_btn = elem
        assert id_appt_btn is not None, f"could not find the LICENSING/ID APPOINTMENT button."
        id_appt_btn.click()

        # Find the TRANSFER MY OUT OF STATE LICENSE TO MASS button and click it.
        xfer_license_button = None
        for elem in driver.find_elements(By.TAG_NAME, "button"):
            if elem.text == "TRANSFER MY OUT OF STATE LICENSE TO MASS":
                xfer_license_button = elem
        assert xfer_license_button is not None, "could not find 'TRANSFER MY OUT OF STATE LICENSE TO MASS' button"
        xfer_license_button.click()

        # Click every relevant appointment location button.
        all_appt_dates = {}

        all_service_center_names = list(map(lambda button: button.text, driver.find_elements(By.TAG_NAME, "button")))
        if nearby_only:
            all_service_center_names = list(filter(lambda name: 'LEONMINSTER' in name or 'WATERTOWN' in name or 'MILFORD' in name or 'WORCESTER' in name or 'NATICK' in name or 'HAYMARKET' in name, all_service_center_names))
            print("only considering nearby appointments:")
        print(all_service_center_names)

        for service_center_name in all_service_center_names:
            if service_center_name == 'BACK' or service_center_name == '':
                continue
            service_center_button = None
            for button in driver.find_elements(By.TAG_NAME, "button"):
                if button.text == service_center_name:
                    service_center_button = button
                    break
            if service_center_button is None:
                print(f"couldn't find a button for {service_center_name}")
                continue

            all_appt_dates[service_center_name] = []
            service_center_button.click()

            # Check if there's an appointment at this service center in October.
            dates = driver.find_elements(By.CLASS_NAME, "DateTimeGrid-Day")
            for date in dates:
                date_text = date.text.replace("\n", "")
                all_appt_dates[service_center_name].append(date_text)
                if 'Oct' in date.text:
                    found_desired_appt = True
                    print("FOUND!")
                    print(service_center_name)
                    print(date.text)
            driver.back()
        
        print_appt_dates(all_appt_dates)
        if found_desired_appt:
            print("\a\a\a\a")
except Exception as e:
    print("\a\a\a\a")
