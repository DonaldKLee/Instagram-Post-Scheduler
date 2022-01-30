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

    # A list containing all the posts
    images_post_list = []

    # Initializes the folder of all the images
    file_directory = os.getcwd()+"/scheduledposts/"

    # Loops through each image in the json file and add their path to the list "images_post_list"
    for image in images:
        images_post_list.append(file_directory + image['file'])

    images_post_list.pop(0) # Removes the first image as it will be uploaded seperately
    images_to_post = "\n".join(images_post_list) # Combines all the rest of the images into 1 string

    # Collects the login information from the .env file
    username = config('instagram_username')
    password = config('instagram_password')

    # Opens "https://www.instagram.com/" with the Chrome Driver 
    path = "chromedriver.exe"
    driver = webdriver.Chrome(path)
    driver.get("https://www.instagram.com/")

    # Allows us to control the mouse position
    action = ActionChains(driver)

    # A function to tag users
    def tag_users(image_index):
        image_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".civB6")))
        offset_x = 0
        offset_y = 0

        # For each user in the tags list
        for user_to_tag in images[image_index]['tags']:
            action.move_to_element_with_offset(image_element, offset_x, offset_y).click().perform()
            
            # Adds the user to the tags
            user_tag_form = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".RO68f")))
            user_tag_form.send_keys(user_to_tag)

            # Finds all the users that we can possibly tag, and click on the one with the matching username
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".IEk8l")))
            all_users = driver.find_elements_by_class_name("IEk8l")
            for user in all_users:
                if user.text.strip(" ") == user_to_tag.strip(" "):
                    user.click()

                    # Moves the mouse for the next user
                    offset_x += 0
                    offset_y += 50
                    break # Stops looking for the other users, because we already found the one

    # Sends the login information to the login form, and clicks on login                
    username_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "username")))
    username_input.send_keys(username)

    password_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "password")))
    password_input.send_keys(password)

    # Clicks on the login button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".y3zKF"))).click()

    # Clicks on "Not Now" for saving login info
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".cmbtv"))).click()

    # Clicks on "Not Now" for notifications
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".HoLwm"))).click()

    # Click on new post button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='New Post']"))).click()

    # Gets all the upload image forms and loops through all the upload files option, and finds the one that allows images         
    all_forms = driver.find_elements_by_class_name("tb_sK")
    for form in all_forms:
        if form.get_attribute('accept') == "image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime":
            form.send_keys(os.getcwd()+"/scheduledposts/" + images[0]['file']) # Uploads the first image

            # if there are mutiple photos in the list "images" file, then add upload those images as well
            if len(images) > 1:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Open Media Gallery']"))).click()
                
                # Gets all the upload image forms and loops through all the upload files option, and finds the one that allows images
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
            
            # If "allow_commenting" is set to false, disable commenting
            if not the_post['commenting']:
                post_settings = driver.find_elements_by_class_name("C0Slf")
                for post_setting in post_settings:
                    if post_setting.text == "Advanced settings":
                        post_setting.click()
                        break
                
                # Clicks on the toggle to disable commenting
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".gZk2f"))).click()

            # For each image, if there are users to tag, tag them
            for i in range(0, len(images)):
                if len(images[i]['tags']) > 0:
                    # run a function to tag users   
                    tag_users(i)

                # If we are not at the last image, clicks on the next button to go to the next image
                if i+1 != len(images):
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Right chevron']"))).click()

            # Runs a loop to see if it is time to post the post
            while True:
                today = str(datetime.today()).split(" ") # Gets the current date
                current_date = today[0] # Only gets the date (Removes the time)
                current_time = datetime.now().strftime("%H:%M") # Gets the local time

                # If the date already passed
                if current_date > the_date:
                    print("Please add a date that as not passed yet!")
                    return

                # If the date to post is today
                elif the_date == current_date:
                    # If the time is the same
                    if str(the_time) == str(current_time):
                        # Post
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".g6RW6"))).click()
                        time.sleep(10) # Pauses the program before closing the window
                        return
                    
                # Pauses the program for 10 seconds before checking the time again
                time.sleep(10)


file = open("posts_to_schedule.json", "r") # Opens the json file to get the post information
data = json.load(file)

# Gets all the posts information
posts = data["posts"]

# For each post in the posts list, gets the data in an object, and runs a function to upload it
for post in posts:
    the_post = {
        "caption": post["caption"],
        "commenting": post["allow_commenting"],
        "post_date": post["date"],
        "post_time": post["time"],
        "images": post["images"]
    }

    upload_post(the_post)
