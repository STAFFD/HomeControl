from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from randomVideos import getRandomVideo
from selenium import webdriver
from os.path import join
import logging


logging.basicConfig(filename="YTControlLog.log", level=logging.DEBUG)
logging.debug("Running Youtube control script!!")
try:
    import pyautogui as pag
    from decorator import reset_mouse
except Exception as reason:
    logging.debug("Fail to load GUI controller. Check if you are using GUI desktop!")
    print(reason)
    exit()


class YouTubeController:

    def __init__(self):
        self.url = ""
        self.makeWindow()

    def __del__(self):
        self.destroyWindow()

    def windowFullScreen(self):
        pag.press('f11')

    def makeWindow(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        try:
            self.driver = webdriver.Chrome("./chromedriver", options=chrome_options)
        except SessionNotCreatedException:
            print("Failed to find suitable ChromeDriver.")
            print("Please Download a suitable one into the root folder via the following address:")
            print("https://chromedriver.chromium.org/downloads")
            exit()
        self.driver.maximize_window()
        self.LARGE_PLAY_BUTTON = "ytp-large-play-button"
        self.FULL_SCREEN_BUTTON = "ytp-fullscreen-button"
        self.SKIP_AD_BUTTON = "ytp-ad-skip-button"
        self.SKIP_BANNER_BUTTON = "ytp-ad-overlay-close-button"
        self.PLAY_BUTTON = "ytp-play-button"
        self.SKIP_TRAIL_BUTTON = "yt-simple-endpoint"
        self.windowFullScreen()
        self.openURL(getRandomVideo(), keep=True)

    def destroyWindow(self):
        try:
            self.driver.close()
        except AttributeError:
            print("Exited.")

    @reset_mouse
    def clickButton(self, buttonName, wait=False):
        try:
            if wait:
                button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, buttonName))
                )
            else:
                button = self.driver.find_element_by_class_name(buttonName)
            button.click()
            print(buttonName + "clicked successfully!")
        except NoSuchElementException:
            print("Can not find the "+ buttonName +"skip"" button!")
        except ElementNotInteractableException:
            print("Can not click the " + buttonName + " button!")

    @reset_mouse
    def skip_trial(self):
        try:
            skip_button = self.driver.find_element_by_xpath("//ytd-button-renderer[@id='dismiss-button']")
            print("kip trial successfully!")
            skip_button.click()
        except NoSuchElementException:
            print("Can not find the skip button!")
        except ElementNotInteractableException:
            print("Can not click the skip button!")

    @reset_mouse
    def play_pause(self):
        try:
            self.clickButton(self.PLAY_BUTTON)
        except ElementClickInterceptedException:
            self.skip_trial()

    @reset_mouse
    def skip_ad(self):
        self.clickButton(self.SKIP_AD_BUTTON)
        self.clickButton(self.SKIP_BANNER_BUTTON)

    def setVolume(self, commmand):
        assert commmand == "up" or commmand == "down"
        pag.press(commmand)

    def openURL(self, url, keep=False):
        self.url = url if keep else join("https://www.youtube.com/embed", url.split("/")[-1])
        try:
            self.driver.get(url)
        except (WebDriverException, NoSuchWindowException):
            print("Window is probaly closed. Creating a new one...")
            self.makeWindow()
            self.driver.get(url)
        self.clickButton(self.LARGE_PLAY_BUTTON, wait=True)


youtubeController = YouTubeController()
