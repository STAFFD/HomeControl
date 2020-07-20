import http.server
import socketserver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, WebDriverException, ElementNotInteractableException, ElementClickInterceptedException
from urllib.parse import parse_qs
import _thread
from time import sleep
import logging
logging.basicConfig(filename="/home/sheldon/HomeControl/YTControlLog.log", level=logging.DEBUG)
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
        self.makeWindow()

    def __del__(self):
        self.destroyWindow()

    def windowFullScreen(self):
        pag.press('f11')

    def makeWindow(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])

        self.driver = webdriver.Chrome("/home/sheldon/HomeControl/chromedriver", options=chrome_options)
        self.driver.maximize_window()
        self.LARGE_PLAY_BUTTON = "ytp-large-play-button"
        self.FULL_SCREEN_BUTTON = "ytp-fullscreen-button"
        self.SKIP_AD_BUTTON = "ytp-ad-skip-button"
        self.SKIP_BANNER_BUTTON = "ytp-ad-overlay-close-button"
        self.PLAY_BUTTON = "ytp-play-button"
        self.SKIP_TRAIL_BUTTON = "yt-simple-endpoint"
        self.windowFullScreen()

    def destroyWindow(self):
        self.driver.close()

    def clickButton(self, buttonName):
        try:
            # button = WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.CLASS_NAME, buttonName))
            # )
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

    def fullScreen(self):
        button = WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, self.FULL_SCREEN_BUTTON))
        )
        try:
            while button.get_attribute("title") == "Full screen (f)":
                pag.press('f')
                # button.click()
                print("f\n")
        except NoSuchElementException:
            print("Can not find the "+ self.FULL_SCREEN_BUTTON +"skip"" button!")


    def openURL(self, url):
        try:
            self.driver.get(url)
        except (WebDriverException, NoSuchWindowException):
            print("Window is probaly closed. Creating a new one...")
            self.makeWindow()
            self.driver.get(url)

        # self.clickButton(self.FULL_SCREEN_BUTTON)
        # self.fullScreen()
        # self.clickButton(self.LARGE_PLAY_BUTTON)
        _thread.start_new_thread(self.enter_play, ("Thread-1", 2))

    @reset_mouse
    def enter_play(self, threadName, delay):
        self.fullScreen()
        self.clickButton(self.LARGE_PLAY_BUTTON)


yc = YouTubeController()


class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        if self.path.endswith("play_pause"):
            yc.play_pause()
        if self.path.endswith("skip_ad"):
            yc.skip_ad()
        # Construct a server response.
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        message = "Success"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length).decode("utf-8") # <--- Gets the data itself
        data = parse_qs(post_data)
        yc.openURL(data["url"][0])
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


print('Server listening on port 8000...')
try:
    httpd = socketserver.TCPServer(('192.168.2.240', 8000), Handler)
except OSError:
    exit()
try:
    httpd.serve_forever()
except KeyboardInterrupt as identifier:
    pass
httpd.server_close()
