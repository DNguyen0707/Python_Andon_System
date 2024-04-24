from webui import webui # GUI
import time
import socket # To get local IP

andonDictonary = {              # dictionary data type to hold data for each andon
    "IP": "xxx.xxx.xxx.xxx",
    "Name": "Andon XX",
    "Status": "Green",
    "Down Time": "12:34:56 PM"
}

listOfAndons = [] # Array of andon dictionaries
listOfAndons.append(andonDictonary) 

def get_local_ip():
    # The IP address of the local machine is found by creating a socket connection.
    # The socket connects to an external address, but does not send any data.
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        # Failed, return 'localhost'
        local_ip = 'localhost'
    finally:
        s.close()
    return local_ip

def all_events(e : webui.event):
	if e.event_type == webui.eventType.CONNECTED:
		print('Connected.')
	if e.event_type == webui.eventType.DISCONNECTED:
		print('Disconnected.')

def exit(e : webui.event):
	webui.exit()


def my_python_function(e : webui.event):
    print("Data from JavaScript: " + e.window.get_str(e, 0)) # Message from JS
    return "Message from Python"


def main():

    html = f"""
        <html>
        <head>
        <title>Qualitel Andon Monitor</title>

        <!-- formatting for table -->
        <style> 
        table {{
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
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

        <body>

        <h1>Qualitel Andon Monitor</h1>
        <p>The following table holds the current status of Qualitel Andon lights.</p>

        <table> 
        <tr> <!-- Header for table -->
            <th>Location</th>
            <th>Status</th>
            <th>Time Status Changed</th>
        </tr>
        """
    
    for i in listOfAndons:
        html + f"""
            <tr>
            <td>{listOfAndons[0]["Name"]}</td>
            <td style="background-color:{listOfAndons[0]["Status"]}">{listOfAndons[0]["Status"]}</td>
            <td>{listOfAndons[0]["Down Time"]}</td>
            </tr>
            """
        
    html + f"""
        </table>
        </body>
        </html>
        """

    print(html)
    # New window
    MyWindow = webui.window()

    # Make the window URL accessible from public networks
    MyWindow.set_public(True)

    # Wait forever (Otherwise WebUI will timeout after 30s)
   # webui.set_timeout(0)
	
    # Bind
    MyWindow.bind('', all_events)
    MyWindow.bind('Exit', exit)
    MyWindow.bind("my_python_function",my_python_function)
    # Start the window without any browser
    # MyWindow.show(html, webui.browser.NoBrowser)
    
    while True:
        color = "blue"
        MyWindow.show(html)
        time.sleep(1)

      #  color = "red"
      #  MyWindow.show('<html><script src="webui.js"></script> Hello World from Python! the Andon is: %s </html>' % (color))
      #  time.sleep(1)

    # Get URL of the window
    url = MyWindow.get_url()
	
    # Get local IP
    local_ip = get_local_ip()
	
    # Replace `localhost` with IP
    link = url.replace('localhost', local_ip)
	
    # Print
    print(f'The UI link is: {link}')


    # Wait until all windows are closed
    webui.wait()
    print('Thank you.')

if __name__ == "__main__":
	main()
