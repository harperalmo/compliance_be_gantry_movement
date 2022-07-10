'''
This is a network server example. The file NetConnectBoot.py should
be copied to boot.py on the chip and this file should be main.py
'''

from debug import Debug
import extract_cmd

db   = Debug()
din  = db.inf
dout = db.outf
dmsg = db.msg
dreset = db.reset
dsleep = db.sleep
dwake = db.wake
dpause = db.set_disp_pause
ddp = db._set_deep_print

#creates a web page. Handy to have a function for each page in the website.
def web_page_main():
    html = """<html><head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            </head>
            <body><h1>Hello, World!</h1>
              <form action="http://192.168.101.2/my-form-page" method="post">
              <ul>
                <li>
                  <label for="cmd">Command:</label>
                  <input name="cmd" id="cmd" value="nop">
                  </li>
                <li>
                  <label for="dir">Direction:</label>
                  <input name="dir" id="dir" value="forward">
                  </li>
                <li>
                  <label for="dist">Distance:</label>
                  <input name="dist" id="dist" value="0.0">
                  </li>
                <li>
                  <label for="ledstate">DLED State:</label>
                  <input name="ledstate" id="ledstate" value="off">
                </li>

                <li class="button">
                  <button type="submit">Send</button>
                  </li>
                </ul>
              </form>
            </body>
        </html>"""
    return html
#create, bind, and accept connections
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#empty string refers to localhost (could be the ip addr.)
#80 is the port. tuple parm.
server_sock.bind(('',80)) 
server_sock.listen(5) #max number of queued connecton

while True:
    client_sock, addr = server_sock.accept()
    print('Connection from: <%s>' % str(addr))
    dmsg(str(addr))
    client_request = client_sock.recv(1024)
    print('   Content = <<%s>>' % str(client_request))
    #s.find() returns -1 if nothing found
    if str(client_request).find('POST', 0,10) != -1:
       extract_cmd.run_cmd(str(client_request))
    
    server_response = web_page_main()
    client_sock.send('HTTP/1.1 200 OK\n')
    client_sock.send('Content-Type: text/html\n')
    client_sock.send('Connection: close\n\n')
    client_sock.sendall(server_response)
    client_sock.close()
    