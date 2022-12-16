from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import random
import smtplib, ssl
from getpass import getpass

# Details about the phone which we want
manufacturer_wanted = "samsung"
models_wanted = ["Galaxy S21 Ultra 5G"]
storages_wanted = ["256", "512"]
conditions_wanted = ["Ca nou", "Excelent"]
colors_wanted = [] # optional

# Who to inform
mail_account_sender = "helper.dga@gmail.com"
mail_account_sender_password = "" # will be asked for it at runtime
mail_account_receivers = ["danut.gavrus@gmail.com", "avram.vlad98@gmail.com"]
text_to_mail = 'Subject: {}\n\n{}'.format("FOUND your " + manufacturer_wanted + " phone at flip.ro", "")

# Global variables
port = 465  # for SSL
context = ssl.create_default_context()
phones_found = False
waiting_time_to_load_min = 4.844 # in seconds
waiting_time_to_load_max = 7.469
time_between_each_execution_min = 4 # in minutes
time_between_each_execution_max = 10

def get_page_driver(url):
    waiting_time_for_terms_conds = random.uniform(1.562, 2.874)
    waiting_time_to_load = random.uniform(waiting_time_to_load_min, waiting_time_to_load_max)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    driver.maximize_window()
    print("\nWaiting " + str(waiting_time_to_load) + "s for the first page to load...")
    sleep(waiting_time_for_terms_conds)
    driver.find_element(By.ID, "__BVID__28___BV_modal_body_").find_element(By.CLASS_NAME, "btn-green").click()
    sleep(waiting_time_to_load - waiting_time_for_terms_conds)
    print(str(waiting_time_to_load) + "s passed")
    return driver

def get_phones(driver):
    phone_details = []
    phone_conditions = []
    page_links = driver.find_elements(By.CLASS_NAME, "page-link")
    print("Found " + str(len(page_links)) + " page links, probably there are at least " + str(len(page_links) - 5) + " next pages.")
    while 1:
        # Load all phones from current page
        page_content = driver.page_source
        soup = BeautifulSoup(page_content, 'html.parser')
        phone_cards = soup.findAll("div", {"class": "card-body"})
        for phone_card in phone_cards:
            phone_detail = phone_card.find("h4", {"class": "card-title"})
            phone_details += [phone_detail.prettify()] if phone_detail is not None else []
            phone_condition = phone_card.find("div", {"class": "details"})
            phone_conditions += [phone_condition.prettify()] if phone_condition is not None else []
        # Try moving to next page
        try:
            page_links[-2].click()
            waiting_time_to_load = random.uniform(waiting_time_to_load_min, waiting_time_to_load_max)
            print("Waiting " + str(waiting_time_to_load) + "s for the next page to load...")
            sleep(waiting_time_to_load)
            print(str(waiting_time_to_load) + "s passed")    
        except:
            print("No more pages to load.\n")
            break
    return phone_details, phone_conditions

def check_for_phones_with_models(phone_details, phone_conditions, models):
    global text_to_mail
    phone_details_to_return = []
    phone_conditions_to_return = []
    for i, phone_detail in enumerate(phone_details):
        for model in models:
            if (len(model) == 0):
                print("Please specify at least 1 and only non-empty strings for the phone's model and try again.")
                return ""
            else:
                if model in phone_detail:
                    if ("Pro" in model or "Max" in model or "mini" in model or "Plus" in model or "Ultra" in model or "FE" in model or  "Lite" in model or " e" in model and ("Pro" in phone_detail or "Max" in phone_detail or "mini" in phone_detail or "Plus" in phone_detail or "Ultra" in phone_detail or "FE" in phone_detail or "Lite" in phone_detail or " e" in phone_detail)):
                        phone_details_to_return.append(phone_detail)
                        phone_conditions_to_return.append(phone_conditions[i])
                    if ("Pro" not in model and "Max" not in model and "mini" not in model and "Plus" not in model and "Ultra" not in model and "FE" not in model and "Lite" not in model and " e" not in model and ("Pro" not in phone_detail and "Max" not in phone_detail and "mini" not in phone_detail and "Plus" not in phone_detail and "Ultra" not in phone_detail and "FE" not in phone_detail and "Lite" not in phone_detail and " e" not in phone_detail)):
                        phone_details_to_return.append(phone_detail)
                        phone_conditions_to_return.append(phone_conditions[i])
    searched_for = "Searched for: manufacturer: " + manufacturer_wanted + ", models: " + str(models_wanted) + ", storages: " + str(storages_wanted) + ", conditions: " + str(conditions_wanted) + ", colors: " + (str(colors_wanted) if len(colors_wanted[0]) > 0 else "not specified") + ".\n"
    text = searched_for + "Found " + str(len(phone_details_to_return)) + " phones that match the MODEL(s)."
    print(text)
    text_to_mail += text + "\n"
    return phone_details_to_return, phone_conditions_to_return

def check_for_models_with_storages(phone_details, phone_conditions, storages):
    global text_to_mail
    phone_details_to_return = []
    phone_conditions_to_return = []
    for i, phone_detail in enumerate(phone_details):
        for storage in storages:
            if (len(storage) == 0):
                print("Please specify at least 1 and only non-empty strings for phone's storage and try again.")
                return ""
            else:
                if storage in phone_detail:
                    phone_details_to_return.append(phone_detail)
                    phone_conditions_to_return.append(phone_conditions[i])
    text = "Found " + str(len(phone_details_to_return)) + " phones that match the MODEL(s) and the STORAGE(s)."
    print(text)
    text_to_mail += text + "\n"
    return phone_details_to_return, phone_conditions_to_return

def check_for_models_with_storages_and_conditions(phone_details, phone_conditions, conditions):
    global text_to_mail
    phone_details_to_return = []
    phone_conditions_to_return = []
    for i, phone_condition in enumerate(phone_conditions):
        for condition in conditions:
            if (len(condition) == 0):
                print("Please specify at least 1 and only non-empty strings for phone's condition and try again.")
                return ""
            else:
                if condition in phone_condition:
                    phone_details_to_return.append(phone_details[i])
                    phone_conditions_to_return.append(phone_condition)
    text = "Found " + str(len(phone_details_to_return)) + " phones that match the MODEL(s) and the STORAGE(s) and the CONDITION(s)."
    print(text)
    text_to_mail += text + "\n"
    return phone_details_to_return, phone_conditions_to_return

def check_for_models_with_storages_and_conditions_and_colors(phone_details, phone_conditions, colors):
    global text_to_mail
    phone_details_to_return = []
    phone_conditions_to_return = []
    for i, phone_detail in enumerate(phone_details):
        for color in colors:
            if (len(color) == 0):
                text = "INFO No color specified, returning any color." + "\n" + "Found " + str(len(phone_details)) + " phones that match the MODEL(s) and the STORAGE(s) and the CONDITION(s) and the COLOR(s)."
                print(text)
                text_to_mail += text + "\n"
                return phone_details, phone_conditions
            else:
                if color in phone_detail:
                    phone_details_to_return.append(phone_detail)
                    phone_conditions_to_return.append(phone_conditions[i])
    text = "Found " + str(len(phone_details_to_return)) + " phones that match the MODEL(s) and the STORAGE(s) and the CONDITION(s) and the COLOR(s)."
    print(text)
    text_to_mail += text + "\n"
    return phone_details_to_return, phone_conditions_to_return

def check_for_phone_with_specs(manufacturer, models, storages, conditions, colors):
    global text_to_mail, phones_found
    url = "https://flip.ro/magazin/" + manufacturer + "/"
    driver = get_page_driver(url)
    phones = get_phones(driver)
    driver.quit()
    phones = check_for_phones_with_models(phones[0], phones[1], models)
    if (len(phones) != 0):
        phones = check_for_models_with_storages(phones[0], phones[1], storages)
    if (len(phones) != 0):
        phones = check_for_models_with_storages_and_conditions(phones[0], phones[1], conditions)
    if (len(phones) != 0):
        phones = check_for_models_with_storages_and_conditions_and_colors(phones[0], phones[1], colors)
    if (len(phones[0]) != 0):
        phones_found = True
        text = "\nThe phones may be found at: https://flip.ro/magazin/" + manufacturer_wanted + "/" + " and are:"
        print(text)
        text_to_mail += text + "\n"
        for i, phone_detail in enumerate(phones[0]):
            text = str(i + 1) + ')' + str(phone_detail) + str(phones[1][i])
            print(text)
            text_to_mail += text + "\n"

def email_user_about_phone():
    global text_to_mail, mail_account_receivers
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(mail_account_sender, mail_account_sender_password)
        server.sendmail(mail_account_sender, mail_account_receivers, text_to_mail)

def connect_to_the_email_server():
    global mail_account_sender, mail_account_sender_password, server
    mail_account_sender_password = getpass('Type your gmail\'s account "' + mail_account_sender + '" password and press enter: ')
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(mail_account_sender, mail_account_sender_password)
            print("Successfully connected to the mail server.")
            return True
    except Exception as e:
        if isinstance(e, smtplib.SMTPAuthenticationError):
            print("Invalid password or email.")
        else:
            print("Unknown exception when trying to connect to the mail server.")
        return False

connection_established = connect_to_the_email_server()
while connection_established == True:
    check_for_phone_with_specs(manufacturer_wanted, models_wanted, storages_wanted, conditions_wanted, colors_wanted)
    if (phones_found == True):
        print('Mail(s) sent to: ' + str(mail_account_receivers))
        print("Script STOPPED until manually started again to prevent spam!")
        text_to_mail += "You won't receive another email until the scipt is started manually again in order to prevent spam!"
        email_user_about_phone()
        break
    else:
        time_between_each_execution = random.uniform(time_between_each_execution_min * 60, time_between_each_execution_max * 60)
        minutes = str(time_between_each_execution / 60)
        print("Waiting " + minutes + "m before searching again...")
        sleep(time_between_each_execution)
        print(minutes + "m passed")
