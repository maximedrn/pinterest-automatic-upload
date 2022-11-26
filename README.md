# Automatically upload as many Pins as you want to Pinterest.

**Version 1.1 - December 27, 2021**
Note: The upload limit on Pinterest is about 150 pins in a row. **You can do multiple upload sessions in a day but risk having your account suspended.**
_**This script is not maintained anymore in free version.**_


## Pinterest Pinbuilder

https://user-images.githubusercontent.com/91475935/204109238-1476af4c-c173-4ae1-902e-5d76bac99a73.mp4

With this tool, you can automatically upload your Pins to Pinterest. This tool has an elegant graphical interface and is very easy to use.

All you have to do is create a file with all the necessary information for each of your Pins. You can choose your Pinboard, add a title, a description, an alt text, a link to an external website and schedule your Pins (only if you have a business account). Finally, all you have to do is select this file and start the process. The tool will do everything for you automatically.


## Table of contents:

* **[Changelog](https://github.com/maximedrn/pinterest-automatic-upload#changelog).**
* **[What does this bot do?](https://github.com/maximedrn/pinterest-automatic-upload#what-does-this-bot-do)**
* **[Instructions](https://github.com/maximedrn/pinterest-automatic-upload#instructions)**.
  * [Basic installation of Python for beginners](https://github.com/maximedrn/pinterest-automatic-upload#basic-installation-of-python-for-beginners).
  * [Configuration of the bot](https://github.com/maximedrn/pinterest-automatic-upload#configuration-of-the-bot).
* **[Known issues](https://github.com/maximedrn/pinterest-automatic-upload#known-issues).**
* **[Data files structure](https://github.com/maximedrn/pinterest-automatic-upload#data-files-structure).**


## Changelog:

* **Version 1.1:**
  * Pinboard issue fixed.
  * Description issue fixed.
  * Minor bugs fixed. 

* **Version 1.0:** 
  * Inital commit.


## What does this bot do?

This script allows you to upload as many Pins (150 in a row) as you want to Pinterest, all automatically and quickly (about 4 Pins per minute).  
The upload limit on Pinterest is about 150 pins in a row. **You can do multiple upload sessions in a day but risk having your account suspended.**


## Instructions:

### Basic installation of Python for beginners:
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


### Configuration of bot:

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
            self.webdriver_path = os.path.abspath('assets/chromedriver.exe')  # Edit this line with your path.
            self.driver = self.webdriver()  # Start new webdriver.
            self.login_url = 'https://www.pinterest.com/login/'
            self.upload_url = 'https://www.pinterest.com/pin-builder/'
    ```
  * **Optional:** the email and the password are asked when you run the bot, but you can:
    * create and open the `assets/email.txt` file, and then write your Pinterest email;
    * create and open the `assets/password.txt` file, and then write your Pinterest password.
  * Create your Pins data file containing all details of each Pin. It can be a JSON or CSV file. Save it in the data folder.  
    **[What structure should the files have?](https://github.com/maximedrn/pinterest-automatic-upload#data-files-structure)**


## Known issues:

* If you are using a Linux distribution or MacOS, you may need to change some parts of the code:  
  * ChromeDriver extension may need to be changed from `.exe` to something else.
* **If you use a JSON file for your Pins data, the file path should not contain a unique "\\". It can be a "/" or a "\\\\":**

```json
  "file_path": "C:/Users/Admin/Desktop/Pinterest/image.png",
  // or:
  "file_path": "C:\\Users\\Admin\\Desktop\\Pinterest\\image.png",
  // but not:
  "file_path": "C:\Users\Admin\Desktop\Pinterest\image.png", // You can see that "\" is highlighted in red.
  ```

* ### Data files structure:

   * <strong>required value *</strong>
          
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
         </tr>
         <tr>
            <td><strong>File Path *</strong></td>
            <td>String</td>
         </tr>
         <tr>
            <td><strong>Title *</strong></td>
            <td>String (maximum 100 characters).</td>
         </tr>
         <tr>
            <td>Description</td>
            <td>String (maximum 500 characters).</td>
         </tr>
         <tr>
            <td>Alt text</td>
            <td>String (maximum 500 characters).</td>
         </tr>
         <tr>
            <td>Link</td>
            <td>String</td>
         </tr>
         <tr>
            <td>Date</td>
            <td>String (Maximum 14 days later)
              <br>(Format: DD/MM/YYYY HH:MM).</td>
            <td>"01/01/2022 12:00" or "01/01/2022 15:30"</td>
         </tr>
      </tbody>
   </table>

You should have something like this:  [JSON](https://github.com/maximedrn/pinterest-automatic-upload/blob/master/data/json_structure.json), [CSV](https://github.com/maximedrn/pinterest-automatic-upload/blob/master/data/csv_structure.csv).
