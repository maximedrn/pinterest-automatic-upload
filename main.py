"""
@author: Maxime.

Github: https://github.com/maximedrn
Version: 1.0
"""

# Colorama module: pip install colorama
from colorama import init, Fore, Style

# Selenium module imports: pip install selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException as TE
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.common.by import By

# Python default import.
from datetime import datetime as dt
from glob import glob
import sys
import os


"""Colorama module constants."""
init(convert=True)  # Init colorama module.
red = Fore.RED  # Red color.
green = Fore.GREEN  # Green color.
yellow = Fore.YELLOW  # Yellow color.
reset = Style.RESET_ALL  # Reset color attribute.


class Data:
    """Read and extract data from CSV and JSON file."""

    def __init__(self, file: str, filetype: str) -> None:
        """Open data file and read it."""
        self.filetype = filetype
        if filetype == '.json':
            from json import loads
            self.file = loads(open(file, encoding='utf-8').read())['pin']
            self.lenght = len(self.file)  # Lenght of file.
        elif filetype == '.csv':
            self.file = open(file, encoding='utf-8').read().splitlines()[1:]
            self.lenght = len(self.file)  # Lenght of file.
        else:
            raise Exception(f'{red}File format is not supported.')

    def create_data(self, data: list) -> None:
        """Store Pin data that can be get by Pinterest class."""
        self.pinboard = data[0]  # Required.
        self.file_path = data[1]  # Required.
        self.title = data[2]  # Required.
        self.description = data[3]  # Optional.
        self.alt_text = data[4]  # Optional.
        self.link = data[5]  # Optional.
        self.date = data[6]  # Optional. Default: publish now.

    def check_data(self) -> bool:
        """Check if data format is correct and return a boolean."""
        # Check if required values are missing.
        for data in [self.pinboard, self.file_path, self.title]:
            if data == '':
                return False, 'Missing required value.'
        # Check if description and alt text is too long.
        if len(self.description) > 500 or len(self.alt_text) > 500:
            return False, 'Description or alt text is too long ' + \
                '(maximum 500 characters long).'
        # Check if title is too long.
        if len(self.title) > 100:
            return False, 'Title is too long (maximum 100 characters long).'
        # Check if file to upload is missing.
        if not os.path.isfile(self.file_path):
            return False, 'File doesn\'t exist.'
        # Check date format.
        if self.date != '':
            try:
                now = dt.strptime(dt.strftime(
                    dt.now(), '%d/%m/%Y %H:%M'), '%d/%m/%Y %H:%M')
                # Check if difference is less than 6 months.
                if (dt.strptime(self.date, '%d/%m/%Y %H:%M')
                        - now).total_seconds() / 60 > 20160:
                    return False, 'Difference must be less than 14 days.'
                # Check if starting date has passed.
                if now > dt.strptime(self.date, '%d/%m/%Y %H:%M'):
                    return False, 'Starting date has passed.'
            except ValueError:
                return False, 'Date format is invalid.'
            # If date is not "XX:00" or "XX:30".
            if self.date[-2:] != '30' and self.date[-2:] != '00':
                return False, 'Time must be every 30 minutes.'
        return True, None

    def format_data(self, number: int) -> None:
        """Format data in list."""
        self.number = number
        if self.filetype == '.json':
            self.json_file()
        elif self.filetype == '.csv':
            self.csv_file()
        else:
            raise Exception(f'{red}File format is not supported.')

    def json_file(self) -> None:
        """Create a list with JSON data."""
        pin_data = self.file[self.number]
        # Get key's value from the Pin data.
        self.create_data([pin_data[data].strip() for data in pin_data])

    def csv_file(self) -> None:
        """Create a list with CSV data."""
        pin_data = self.file[self.number].split(';;')
        self.create_data([data.strip() for data in pin_data])


class Pinterest:
    """Main class of the Pinterest uploader."""

    def __init__(self, email: str, password: str) -> None:
        """Set path of used file and start webdriver."""
        self.email = email  # Pinterest email.
        self.password = password  # Pinterest password.
        self.webdriver_path = 'assets/chromedriver.exe'
        self.driver = self.webdriver()  # Start new webdriver.
        self.login_url = 'https://www.pinterest.com/login/'
        self.upload_url = 'https://www.pinterest.com/pin-builder/'

    def webdriver(self):
        """Start webdriver and return state of it."""
        options = webdriver.ChromeOptions()  # Configure options for Chrome.
        options.add_argument('--lang=en')  # Set webdriver language to English.
        # options.add_argument('headless')  # Headless ChromeDriver.
        options.add_argument('log-level=3')  # No logs is printed.
        options.add_argument('--mute-audio')  # Audio is muted.
        driver = webdriver.Chrome(self.webdriver_path, options=options)
        driver.maximize_window()  # Maximize window to reach all elements.
        return driver

    def element_clickable(self, element: str) -> None:
        """Click on element if it's clickable using Selenium."""
        WDW(self.driver, 5).until(EC.element_to_be_clickable(
            (By.XPATH, element))).click()

    def element_visible(self, element: str):
        """Check if element is visible using Selenium."""
        return WDW(self.driver, 30).until(EC.visibility_of_element_located(
            (By.XPATH, element)))

    def element_send_keys(self, element: str, keys: str) -> None:
        """Send keys to element if it's visible using Selenium."""
        try:
            WDW(self.driver, 5).until(EC.visibility_of_element_located(
                (By.XPATH, element))).send_keys(keys)
        except TE:
            # Some elements are not visible but are still present.
            WDW(self.driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, element))).send_keys(keys)

    def window_handles(self, window_number: int) -> None:
        """Check for window handles and wait until a specific tab is opened."""
        WDW(self.driver, 30).until(lambda _: len(
            self.driver.window_handles) == window_number + 1)
        # Switch to asked tab.
        self.driver.switch_to.window(self.driver.window_handles[window_number])

    def login(self) -> None:
        """Sign in to Pinterest."""
        try:
            print('Login to Pinterest.', end=' ')
            self.driver.get(self.login_url)  # Go to the login URL.
            # Input email and password.
            self.element_send_keys('//*[@id="email"]', self.email)
            self.element_send_keys('//*[@id="password"]', self.password)
            # Click on "Sign in" button.
            self.element_clickable(
                '//div[@data-test-id="registerFormSubmitButton"]/button')
            # Wait until URL changes.
            WDW(self.driver, 30).until(
                lambda _: self.driver.current_url != self.login_url)
            print(f'{green}Logged.{reset}\n')
        except TE:
            sys.exit(f'{red}Failed.{reset}\n')

    def upload_pins(self, pin: int) -> None:
        """Upload pins one by one on Pinterest."""
        try:
            print(f'Uploading pins n°{pin + 1}/{data.lenght}.', end=' ')
            self.driver.get(self.upload_url)  # Go to upload pins URL.
            # Click on button to change pinboard.
            self.element_clickable(
                '//button[@data-test-id="board-dropdown-select-button"]')
            # Input pinboard name.
            self.element_send_keys(
                '//*[@id="pickerSearchField"]', data.pinboard)
            # Select pinboard.
            try:
                self.element_clickable(
                    '//div[@data-test-id="boardWithoutSection"]/div')
            except TE:
                raise TE('Pinboard name is invalid.')
            # Upload image / video.
            self.element_send_keys(
                '//input[contains(@id, "media-upload-input")]', data.file_path)
            # Input a title.
            self.element_send_keys(
                '//textarea[contains(@id, "pin-draft-title")]', data.title)
            # Input a description.
            self.element_send_keys(
                '//*[contains(@id, "pin-draft-description")]/div/div/div[2]'
                '/div/div/div/div/span/br', data.description)
            # Click on "Add alt text" button.
            self.element_clickable(
                '//div[@data-test-id="pin-draft-alt-text-button"]/button')
            # Input an alt text.
            self.element_send_keys('//textarea[contains(@id, "pin-draft'
                                   '-alttext")]', data.alt_text)
            # Input a link.
            self.element_send_keys(
                '//textarea[contains(@id, "pin-draft-link")]', data.link)
            if len(data.date) > 0:
                date, time = data.date.split(' ')
                # Select "Publish later" radio button.
                self.element_clickable('//label[contains(@for, "pin-draft-'
                                       'schedule-publish-later")]')
                # Input date.
                self.element_clickable('//input[contains(@id, "pin-draft-'
                                       'schedule-date-field")]/../../../..')
                # Get month name.
                month_name = dt.strptime(date, "%d/%m/%Y").strftime("%B")
                # Remove useless "0" in day number.
                day = data.date[:2][1] if \
                    data.date[:2][0] == '0' else data.date[:2]
                self.element_clickable('//div[contains(@aria-label, '
                                       f'"{month_name} {day}")]')
                # Input time.
                self.element_clickable('//input[contains(@id, "pin-draft-'
                                       'schedule-time-field")]/../../../..')
                self.element_clickable(f'//div[@title="{time}"]/../..')
            # Click on upload button.
            self.element_clickable(
                '//button[@data-test-id="board-dropdown-save-button"]')
            # If a dialog div appears, pin is uploaded.
            self.element_visible('//div[@role="dialog"]')
            print(f'{green}Uploaded.{reset}')
        except TE as error:
            print(f'{red}Failed. {error}{reset}')


def cls() -> None:
    """Clear console function."""
    # Clear console for Windows using 'cls' and Linux & Mac using 'clear'.
    os.system('cls' if os.name == 'nt' else 'clear')


def read_file(file_: str, question: str) -> str:
    """Read file or ask for data to write in text file."""
    if not os.path.isfile(f'assets/{file_}.txt'):
        open(f'assets/{file_}.txt', 'a')
    with open(f'assets/{file_}.txt', 'r+', encoding='utf-8') as file:
        text = file.read()
        if text == '':
            text = input(question)
            if input(f'Do you want to save your {file_} in'
                     ' text file? (y/n) ').lower() == 'y':
                file.write(text)
                print(f'{green}Saved.{reset}')
            else:
                print(f'{yellow}Not saved.{reset}')
        return text


def data_file() -> str:
    """Read data folder and extract JSON and CSV files."""
    while True:
        folder = [glob(f'data/{extension}')
                  for extension in ['*.json', '*.csv']]
        print(f'{yellow}\nChoose your file:{reset}')
        file_number = 0
        files = []
        print('0 - Browse file on PC.')
        for extension in folder:
            for file in extension:
                file_number += 1
                files.append(file)
                print(f'{file_number} - {file}')
        answer = input('File number: ')
        cls()  # Clear console.
        if answer.isdigit():
            if int(answer) == 0:
                # Browse file on PC.
                from tkinter import Tk  # pip install tk
                from tkinter.filedialog import askopenfilename
                Tk().withdraw()  # Hide Tkinter tab.
                return askopenfilename(filetypes=[('', '.json .csv')])
            elif int(answer) <= len(files):
                return files[int(answer) - 1]
            else:
                print(f'{red}File doesn\'t exist.{reset}')
        else:
            print(f'{red}Answer must be an integer.{reset}')


if __name__ == '__main__':

    cls()  # Clear console.

    print(f'{green}Made by Maxime.'
          f'\n@Github: https://github.com/maximedrn{reset}')

    email = read_file('email', '\nWhat is your Pinterest email? ')
    password = read_file('password', '\nWhat is your Pinterest password? ')

    file = data_file()  # Ask for file.
    # Init Data class.
    data = Data(file, os.path.splitext(file)[1])
    # Init Pinterest class.
    pinterest = Pinterest(email, password)
    pinterest.login()

    for pin in range(data.lenght):
        data.format_data(pin)  # Get data's pin.
        check = data.check_data()
        if not check[0]:
            print(f'{red}Data of pin n°{pin + 1}/{data.lenght} is incorrect.'
                  f'\nError: {check[1]}{reset}')
        else:
            pinterest.upload_pins(pin)  # Upload it.
