import http.server
import socketserver
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, WebDriverException, ElementNotInteractableException, ElementClickInterceptedException
from urllib.parse import parse_qs
import _thread
from time import sleep
import pyautogui as pag
import logging

logging.basicConfig(filename="YTControlLog.log", level=logging.DEBUG)
logging.debug("Running Youtube control script!!")
screenSize = pag.size()


def reset_mouse(method):
    def reset(*args, **kw):
        method(*args, **kw)
        pag.moveTo(0, screenSize[1])
    return reset


class YouTubeController:

    def __init__(self):

        # self.makeWindow()

    def __del__(self):
        self.destroyWindow()

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

    def destroyWindow(self):
        self.driver.close()

    def clickButton(self, buttonName):
        try:
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

    def openURL(self, url):
        try:
            self.driver.get(url)
        except (WebDriverException, NoSuchWindowException):
            print("Window is probaly closed. Creating a new one...")
            self.makeWindow()
            self.driver.get(url)
        _thread.start_new_thread(self.enter_play, ("Thread-1", 2))

    @reset_mouse
    def enter_play(self, threadName, delay):
        sleep(delay)
        self.clickButton(self.FULL_SCREEN_BUTTON)
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
