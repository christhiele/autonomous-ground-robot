import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import os
import time
import processkey

# following code used Random Nerd Tutorials as a base framework (https://github.com/RuiSantosdotme/Random-Nerd-Tutorials/blob/master/Projects/rpi_camera_surveillance_system.py).

processresult = True

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()
    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301) #redirect
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = os.getcwd()+'/'+'index.html'
            content = open(content)
            content = content.read()
            content = content.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

    def do_POST(self):
        """Handle a post request by returning the square of the number."""
        length = int(self.headers.get('content-length'))
        data_string = self.rfile.read(length)
        try:
            result = data_string.decode()
        except:
            result = 'error'
        # print(result)
        global processresult
        processresult = processkey.processkey(result)
        if processresult is False:
            print(time.asctime(), "Server Stopped")
            hostedserver.shutdown()
            # note - do not need to invoke camera.stop-recording b/c finally statement below.


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def startserver():
    # see https://picamera.readthedocs.io/en/release-1.13/fov.html#camera-modes to set camera mode
    global output
    global hostedserver
    with picamera.PiCamera(resolution='1296x972', sensor_mode=4) as camera: #default rez = 640x480 best= 1296x972 (4)
        # print(camera.MAX_RESOLUTION) #useful to identify whether v1 or v2 of camera.
        output = StreamingOutput()
        camera.start_recording(output, format='mjpeg') #default = mjpeg
        try:
            address = ('', 8081)
            hostedserver = StreamingServer(address, StreamingHandler)
            print(time.asctime(), "Server Started")
            hostedserver.serve_forever()
        except KeyboardInterrupt:
            processkey.endprocesses()
            hostedserver.server_close()
            print(time.asctime(), "Server Stopped")
        except:
            processkey.endprocesses()
            hostedserver.server_close()
            print(time.asctime(), "Server Stopped")
        finally:
            camera.stop_recording()

if __name__ == '__main__':
    startserver()
