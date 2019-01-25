#  coding: utf-8 
import socketserver
import os.path

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, James Vo
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        # need string 
        data = self.data.decode("utf-8").splitlines()[0].split(" ")
        location = ""
        if data[0] != "GET":
            status = "405 Method Not Allowed\n\n"

        else:
            protocol = "HTTP/1.1 "
            path = data[1]

            if path[-1] == "/":
                path += "index.html"
            path = "www" + path
                
            # check for file
            try:
                verify_fileordir = os.path.abspath(data[1])
                cwd = os.getcwd()
                entire_path = cwd + "/www/" 
                check = entire_path + verify_fileordir

                pathway = open(path, "r")
                with pathway as info:
                    content = info.read()
                    # check if the path is a dir
                    if not os.path.isdir(check):
                        # check if the path is a file
                        if not os.path.isfile(check):  
                            # print("not valid")                          
                            status = "404 Page Not Found\n\n"
                            content = ""
                            content_type = "" 
                        else:
                            # print("it's valid")
                            status = "200 OK\r\n"
                    else:
                        status = "200 OK\r\n"

                # need the content type
                extension = os.path.splitext(path)[1]
                extension = extension[1:]
                content_type = "Content-type: text/" + extension + "\n\n"

            except:
                # file is not available, 404
                status = "404 Page Not Found\n\n"
                content = ""
                content_type = "" 

                # check for / 
                if data[1][-1] != "/":
                    status = "301 Moved Permanently\n"
                    location = "Location: " + data[1] + "/" +'\n\n'
                    content = ""
                    content_type = ""

            response = protocol + status + location + content_type + content + "\n"
            # print(response) 
            self.request.sendall(bytearray(response, "utf-8"))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
