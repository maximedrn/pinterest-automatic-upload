# Automatically upload as many Pins as you want to Pinterest.

* **(_Version 1.0 - November 04, 2021_).**
* Note: The upload limit on Pinterest is about 150 pins in a row.  
  **You can do multiple upload sessions in a day but risk having your account suspended.**

# Table of contents:

* **[Changelog](https://github.com/maximedrn/pinterest-automatic-uploader#changelog).**
* **[What does this bot do?](https://github.com/maximedrn/pinterest-automatic-uploader#what-does-this-bot-do)**
* **[To do list](https://github.com/maximedrn/pinterest-automatic-uploader#to-do-list).**
* **[Instructions](https://github.com/maximedrn/pinterest-automatic-uploader#instructions)**.
  * [Basic installation of Python for beginners](https://github.com/maximedrn/pinterest-automatic-uploader#basic-installation-of-python-for-beginners).
  * [Configuration of bot](https://github.com/maximedrn/pinterest-automatic-uploader#configuration-of-bot).
* **[Known issues](https://github.com/maximedrn/pinterest-automatic-uploader#known-issues).**
* **[Data files structure](https://github.com/maximedrn/pinterest-automatic-uploader#data-files-structure).**
  * [CSV file](https://github.com/maximedrn/pinterest-automatic-uploader#csv-file).
  * [JSON file](https://github.com/maximedrn/pinterest-automatic-uploader#json-file).
* **[Set bot fully in the background](https://github.com/maximedrn/pinterest-automatic-uploader#set-bot-fully-in-the-background).**

## Changelog:

* **Version 1.0:** 
  * Inital commit.

## What does this bot do?

This script allows you to upload as many Pins as you want to Pinterest, all automatically and quickly (about 4 Pins per minute).

## To do list:

* ✔ <strike>Pinterest automatic login.</strike>
* ❌ Pinterest two-factor authentication support.
* ✔ <strike>Automatic Pins uploader.</strike>
* ✔ <strike>Data file browsing feature.</strike>
* ✔ <strike>CSV structure reader and interpreter.</strike>
* ✔ <strike>JSON structure reader and interpreter.</strike>

## Instructions:

* ### Basic installation of Python for beginners:

  * Download this repository or clone it:
```
git clone https://github.com/maximedrn/pinterest-automatic-uploader.git
```
  * It requires [Python](https://www.python.org/) 3.7 or a newest version.
  * Install [pip](https://pip.pypa.io/en/stable/installation/) to be able to have needed Python modules.
  * Open a command prompt in repository folder and type:
```
pip install -r requirements.txt
```

* ### Configuration of bot:

  * Download and install [Google Chrome](https://www.google.com/intl/en_en/chrome/).
  * Download the [ChromeDriver executable](https://chromedriver.chromium.org/downloads) that is compatible with the actual version of your Google Chrome browser and your OS (Operating System). Refer to: _[What version of Google Chrome do I have?](https://www.whatismybrowser.com/detect/what-version-of-chrome-do-i-have)_
  * Extract the executable from the ZIP file and copy/paste it in the `assets/` folder of the repository. You may need to change the path of the file:
```python
class Pinterest:
    """Main class of the Pinterest uploader."""

    def __init__(self, email: str, password: str) -> None:
        """Set path of used file and start webdriver."""
        self.email = email  # Pinterest email.
        self.password = password  # Pinterest password.
        self.webdriver_path = 'assets/chromedriver.exe'             # <-- Edit this line and change the ".exe".
        self.driver = self.webdriver()  # Start new webdriver.
        self.login_url = 'https://www.pinterest.com/login/'
        self.upload_url = 'https://www.pinterest.com/pin-builder/'
```
  * **Optional:** password and recovery phrase are asked when you run the bot.
    * Create an open the `assets/email.txt` file and write your Pinterest email.
    * Create an open the `assets/password.txt` file and write your Pinterest password.
  * Create your Pins data file containing all details of each Pin. It can be a JSON or CSV file. Save it in the data folder.  
    **[What structure should the files have?](https://github.com/maximedrn/pinterest-automatic-uploader#data-files-structure)**
    
## Known issues:

* If you are using a Linux distribution or MacOS, you may need to change some parts of the code:  
  * Colorama module sometimes does not work.
  * ChromeDriver extension may need to be changed from `.exe` to something else.
* **If you use a JSON file for your Pins data, the file path should not contain a unique "\\". It can be a "/" or a "\\\\":**
```json
"file_path": "C:/Users/Admin/Desktop/Pinterest/image.png",
// or:
"file_path": "C:\\Users\\Admin\\Desktop\\Pinterest\\image.png",
// but not:
"file_path": "C:\Users\Admin\Desktop\Pinterest\image.png", // You can see that "\" is highlighted in red.
```
* The waiting time (`WebDriverWait().until()`) for the element to be clickable or visible is sometimes too short if your PC is slow and this raises an exception, so you can increase the waiting time:
```python
def element_clickable(self, element: str) -> None:
    """Click on element if it's clickable using Selenium."""
    WDW(self.driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, element))).click()

def element_visible(self, element: str):
    """Check if element is visible using Selenium."""
    return WDW(self.driver, 50).until(EC.visibility_of_element_located(
        (By.XPATH, element)))

def element_send_keys(self, element: str, keys: str) -> None:
    """Send keys to element if it's visible using Selenium."""
    try:
        WDW(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, element))).send_keys(keys)
    except TE:
        # Some elements are not visible but are still present.
        WDW(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, element))).send_keys(keys)
```

* ### Data files structure:

  * #### **CSV file:**

    * <strong>required value *</strong>
    * _default value_
          
   <br>
   <table>
      <tbody>
         <tr>
            <td>Settings</td>
            <td>Types</td>
            <td>Examples</td>
         </tr>
         <tr>
            <td><strong>Pinboard *</strong></td>
            <td>String</td>
            <td>My Pinboard;;</td>
         </tr>
         <tr>
            <td><strong>File Path *</strong></td>
            <td>String</td>
            <td>C:/Users/Admin/Desktop/Pinterest/image.png;;</td>
         </tr>
         <tr>
            <td><strong>Title *</strong></td>
            <td>String
               <br>(maximum 100 characters).</td>
            <td>My Pin;;</td>
         </tr>
         <tr>
            <td>Description</td>
            <td>String
               <br>(maximum 500 characters).</td>
            <td>This is my pin;;</td>
         </tr>
         <tr>
            <td>Alt text</td>
            <td>String
               <br>(maximum 500 characters).</td>
            <td>A beautiful dog;;</td>
         </tr>
         <tr>
            <td>Link</td>
            <td>String</td>
            <td>https://google.com/;;</td>
         </tr>
         <tr>
            <td>Date
               <br>Maximum 14 days later.
               <br>Format: DD/MM/YYYY hh:mm.</td>
            <td>String</td>
            <td>25/12/2021 12:00;;</td>
         </tr>
      </tbody>
   </table>

   You should have something like [this](https://github.com/maximedrn/pinterest-automatic-uploader/blob/master/data/csv_structure.csv):
```
pinboard;; file_path;; title;; description;; alt_text;; link;; date
My Pinboard;; C:/Users/Admin/Desktop/Pinterest/image.png;; My Pin;; This is my pin;; A beautiful dog;; https://google.com/;; 25/12/2021 12:00
My Pinboard;; C:/Users/Admin/Desktop/Pinterest/image.png;; My Pin;; This is my pin;; A beautiful dog;; https://google.com/;; 
My Pinboard;; C:/Users/Admin/Desktop/Pinterest/image.png;; My Pin;; This is my pin;; ;; ;; 
```
        
  * #### **JSON file**:
    
    * <strong>required value *</strong>
    * _default value_

   <br>
   <table>
      <tbody>
         <tr>
            <td>Settings</td>
            <td>Types</td>
            <td>Examples</td>
         </tr>
         <tr>
            <td><strong>Pinboard *</strong></td>
            <td>String</td>
            <td>"pinboard": "My Pinboard",</td>
         </tr>
         <tr>
            <td><strong>File Path *</strong></td>
            <td>String</td>
            <td>"file_path": "C:/Users/Admin/Desktop/Pinterest/image.png",</td>
         </tr>
         <tr>
            <td><strong>Title *</strong></td>
            <td>String
               <br>(maximum 100 characters).</td>
            <td>"title": "My Pin",</td>
         </tr>
         <tr>
            <td>Description</td>
            <td>String
               <br>(maximum 500 characters).</td>
            <td>"description": "This is my pin",</td>
         </tr>
         <tr>
            <td>Alt text</td>
            <td>String
               <br>(maximum 500 characters).</td>
            <td>"alt_text": "A beautiful dog",</td>
         </tr>
         <tr>
            <td>Link</td>
            <td>String</td>
            <td>"link": "https://google.com/",</td>
         </tr>
         <tr>
            <td>Date
               <br>Maximum 14 days later.
               <br>Format: DD/MM/YYYY hh:mm.</td>
            <td>String</td>
            <td>"date": "25/12/2021 12:00"</td>
         </tr>
      </tbody>
   </table>
         
   And it gives you something like [this](https://github.com/maximedrn/pinterest-automatic-uploader/blob/master/data/json_structure.json):
   ```json
   {
    "pin": [
      {
        "pinboard": "My Pinboard",
        "file_path": "C:/Users/Admin/Desktop/Pinterest/image.png",
        "title": "My Pin",
        "description": "This is my pin",
        "alt_text": "A beautiful dog",
        "link": "https://google.com/",
        "date": "25/12/2021 12:00"
      },
      {
        "pinboard": "My Pinboard",
        "file_path": "C:/Users/Admin/Desktop/Pinterest/image.png",
        "title": "My Pin",
        "description": "This is my pin",
        "alt_text": "A beautiful dog",
        "link": "https://google.com/",
        "date": ""
      },
      {
        "pinboard": "My Pinboard",
        "file_path": "C:/Users/Admin/Desktop/Pinterest/image.png",
        "title": "My Pin",
        "description": "This is my pin",
        "alt_text": "",
        "link": "",
        "date": ""
      }
    ]
  }
   ```

## Set bot fully in the background:
```python
def webdriver(self):
   """Start webdriver and return state of it."""
   options = webdriver.ChromeOptions()  # Configure options for Chrome.
   options.add_argument('--lang=en')  # Set webdriver language to English.
   # options.add_argument('headless')  # Headless ChromeDriver.             # <-- Edit this line and remove the first "# ".
   options.add_argument('log-level=3')  # No logs is printed.
   options.add_argument('--mute-audio')  # Audio is muted.
   driver = webdriver.Chrome(self.webdriver_path, options=options)
   driver.maximize_window()  # Maximize window to reach all elements.
   return driver
```
