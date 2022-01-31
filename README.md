# Instagram-Post-Scheduler (Readme file still in progress)

A bot that can be used to schedule Instagram posts without the need of Hootsuite or Facebook Business Suite!

Note: This was a fun project for experimental and learning purposes. 
</br> Please do not use this for malicious behaviour, because YOU will be responsible! 

# Installation
1. Download the code from this repository

2. install the following module
```python
pip install selenium
```

3. Find the version of your Chrome browser in "Settings" --> "About Chrome". 

</br>Then [install a Webdriver for Chrome that supports your browser's version](https://sites.google.com/a/chromium.org/chromedriver/downloads)

4. Once your web driver has been installed, put it somewhere on your computer and copy and paste it's path (The path should start with C:\\, E:\\, etc.) onto line 31.

</br> Example:
```python
PATH = "C:\Program Files (x86)\chromedriver.exe"  # Step 4 of the installations instructions 
```

### If you are stuck on step 3 or 4, watch this short [tutorial!](https://www.youtube.com/watch?v=Xjv1sY630Uc&feature=youtu.be&t=260)
5. Create a .env file
6. In the .env file, create a variable called "instagram_username" and "instagram_password"

```env
instagram_username = ""
instagram_password = ""
```
7. Inside the quotations, insert your Instagram username (Do not include the @) and password

# How to use
1. Create a folder called "scheduledposts" and add all your post images into the folder
2. Open up "posts_to_schedule.json"
3. Modify the json data for your post, and then run "main.py"
- If you are scheduling mutiple posts, please ensure that they are ordered from earliest to latest!

Example:
```json
{
    "posts": [
        {
            "caption": "Posted this with Python!",
            "allow_commenting": true,
            "date": "2021-11-17",
            "time": "15:00",
            "images": [
             {
                    "file": "image1.jpg",
                    "tags": []
                },
                {
                    "file": "image2.jpg",
                    "tags": ["donald.k.lee"]
                },
                {
                    "file": "image3.jpg",
                    "tags": []
                }
            ]
        },
        {
            "caption": "Post number 2!",
            "allow_commenting": false,
            "date": "2021-11-18",
            "time": "13:00",
            "images": [
             {
                    "file": "image4.jpg",
                    "tags": []
             }
            ]
        }
    ]
}
```

# Terms of Service 
Please do **NOT** use this for spam, bullying, etc. 

</br> By using this script, YOU will take FULL responsibility for anything that happens to ANYONE you use this on and anything you do with this script!. 

</br> Additionally, using this script may involve a risk of you being banned and even other risks including but not limited to: being hacked, etc. Use this script at your own risk!

</br> These terms may be changed without notice.
