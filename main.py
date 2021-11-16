"""
Name: Donald Lee
Class: Computer Programming 12

Assignment 3: Do some other bot or scraper.
Examples: a bot that buys sneakers, a bot that does typeracer, a bot that downloads and pdfs chapters from a web novel or comic
"""

import os, time, json

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from datetime import datetime

from decouple import config # Used to get the .env variables

# A function that posts the post on Instagram
def upload_post(the_post):
    images = the_post['images']

    # The date on when the posts should be posted on
    the_date = the_post['post_date']
    the_time = the_post['post_time']

    images_post_list = []

    file_directory = os.getcwd()+"/scheduledposts/"

    for image in images:
        images_post_list.append(file_directory + image['file'])

    images_post_list.pop(0) # Removes the first image as it will be uploaded seperately
    images_to_post = "\n".join(images_post_list)

    username = config('instagram_username')
    password = config('instagram_password')

    path = "chromedriver.exe"
    driver = webdriver.Chrome(path)
    driver.get("https://www.instagram.com/") # Opens "https://www.instagram.com/"

    # Allows us to control the mouse position
    action = ActionChains(driver)

    def tag_users(image_index):
        image_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".civB6")))
        offset_x = 0
        offset_y = 0

        # Tag users
        for user_to_tag in images[image_index]['tags']:
            action.move_to_element_with_offset(image_element, offset_x, offset_y).click().perform()
            user_tag_form = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".RO68f")))
            user_tag_form.send_keys(user_to_tag)
            
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".IEk8l")))
            all_users = driver.find_elements_by_class_name("IEk8l")
            
            for user in all_users:
                if user.text.strip(" ") == user_to_tag.strip(" "):
                    user.click()

                    offset_x += 0
                    offset_y += 50
                    break

    username_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "username")))
    username_input.send_keys(username)

    password_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "password")))
    password_input.send_keys(password)

    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".y3zKF"))).click()

    # Clicks on "Not Now"
    save_login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".cmbtv"))).click()

    # Clicks on "Not Now"
    save_login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".HoLwm"))).click()

    # Click on new post button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='New Post']"))).click()

    # Gets all forms
    all_forms = driver.find_elements_by_class_name("tb_sK")

    for form in all_forms:
        if form.get_attribute('accept') == "image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime":
            form.send_keys(os.getcwd()+"/scheduledposts/" + images[0]['file'])

            # if mutiple photos in the folder
            if len(images) > 1:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Open Media Gallery']"))).click()
                
                all_forms = driver.find_elements_by_class_name("tb_sK")
                for form in all_forms:
                    if form.get_attribute('accept') == "image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime":
                        form.send_keys(images_to_post)
        
            # Clicks on the Next button
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".g6RW6"))).click()
            
            # Clicks on the Next button again to skip adding filters to the image
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".g6RW6"))).click()
            
            # Send a caption
            caption_form = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".lFzco")))
            caption_form.send_keys(the_post['caption'])
            
            if not the_post['commenting']:
                post_settings = driver.find_elements_by_class_name("C0Slf")
                for post_setting in post_settings:
                    if post_setting.text == "Advanced settings":
                        post_setting.click()
                        break
                
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".gZk2f"))).click()

            # if mutiple photos in the folder
            if len(images) > 0:
                for i in range(0, len(images)):
                    if len(images[i]['tags']) > 0:
                        # run a function to tag users   
                        tag_users(i)

                    if i+1 != len(images):
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Right chevron']"))).click()

            while True:
                today = str(datetime.today()).split(" ")
                current_time = datetime.now().strftime("%H:%M")
                current_date = today[0]

                if current_date > the_date:
                    print("Please add a date that as not passed yet!")

                    return

                if the_date == current_date:
                    print(str(the_time) + " " + str(current_time))
                    if str(the_time) == str(current_time):
                        # Post
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".g6RW6"))).click()
                        time.sleep(10)
                        return

                time.sleep(10)

file = open("posts_to_schedule.json", "r") # Opens the json file to get the post information
data = json.load(file)

posts = data["posts"]

for post in posts:
    the_post = {
        "caption": post["caption"],
        "commenting": post["allow_commenting"],
        "post_date": post["date"],
        "post_time": post["time"],
        "images": post["images"]
    }

    upload_post(the_post)