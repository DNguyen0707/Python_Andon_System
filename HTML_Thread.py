
from datetime import datetime   # to get today date
from webui import webui         # for HTML
import socket                   # for UDP
import time                     # time.sleep(seconds)
import asyncio                  # for threads and queues
from UDP_Thread import *        # get definition of "list of Andons"

def all_events(e : webui.event):
	if e.event_type == webui.eventType.CONNECTED:
		print('Connected.')
	if e.event_type == webui.eventType.DISCONNECTED:
		print('Disconnected.')

def exit(e : webui.event):
	webui.exit()

######   HTML Thread publishes the current state of the andons   ######     
async def HTML_Thread(queue: asyncio.Queue):
    print("starting HTML Thread")
    # New window
    MyWindow = webui.window()

    # Make the window URL accessible from public networks
    MyWindow.set_public(True)
    MyWindow.set_kiosk(False) # full screen mode
    MyWindow.set_port(6001)

    # Wait forever (Otherwise WebUI will timeout after 30s)
    webui.set_timeout(1)
	
    # Bind
    MyWindow.bind('', all_events)
    MyWindow.bind('Exit', exit)
    # Start the window without any browser
    #MyWindow.show(html, webui.browser.NoBrowser)
    

    url = MyWindow.get_url()            # Get URL of the window
	
    # Get local IP
    local_ip ="10.100.100.102"# getIP()                  #"10.100.100.102" 
	
    # Replace `localhost` with IP
    link = url.replace('localhost', local_ip)
    print(link)
    while True:
        html = f"""
            <html>
            <head>
            <title>Qualitel Andon Monitor</title>

            <meta http-equiv="refresh" content="10">

            <!-- formatting for table -->
            <style> 
            table {{
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width="750";
            }}

            td, th {{
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
            }}

            tr:nth-child(even) {{
            background-color: #dddddd;
            }}
            </style>
            </head>

            <body style="background-color:DodgerBlue;">

            <h1>Qualitel Andon Monitor</h1>
            <p>The following table holds the current status of Qualitel Andon lights.</p>

            <table> 
            <tr> <!-- Header for table -->
                <th>Location</th>
                <th>Status</th>
                <th>Time Status Changed</th>
            </tr>
            """

        for i in range(0, len(listOfAndons)):
            html = html + f"""
                <tr>
                <td>{listOfAndons[i]["Name"]}</td>
                <td style="background-color:{listOfAndons[i]["Status"]}">{listOfAndons[i]["Status"]}</td>
                <td>{listOfAndons[i]["Date Time"]}</td>
                </tr>
                """
            print(i)
            
        html = html + """
            </table>
            </body>
            </html>
            """
        
        MyWindow.set_port(6001)
        MyWindow.show(html, webui.browser.NoBrowser)

        time.sleep(1)