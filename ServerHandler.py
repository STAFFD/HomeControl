from controller import youtubeController
from randomVideos import getRandomVideo
from urllib.parse import parse_qs
from soundManager import Sounder
import http.server


class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        message = "Success"

        if self.path.endswith("play_pause"):
            youtubeController.play_pause()
        elif self.path.endswith("skip_ad"):
            youtubeController.skip_ad()
        elif self.path.endswith("playRandom"):
            Sounder().receive1()
            youtubeController.openURL(getRandomVideo(), keep=True)
            Sounder().receive2()
        elif self.path.endswith("getVideo"):
            message = youtubeController.url

        # Construct a server response.
        self.send_response(200)
        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send message back to client
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length).decode("utf-8") # <--- Gets the data itself
        data = parse_qs(post_data)

        if self.path.endswith("setVolume"):
            youtubeController.setVolume(data["set"][0])
        else:
            Sounder().receive1()
            youtubeController.openURL(data["url"][0])

        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
