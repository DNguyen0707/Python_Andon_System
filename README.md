# Python_Andon_System
**Authors:** Kris Cote, Dai Nguyen

Andon system for Qualitel using python and UDP Client-Server for machinery status. 
 
## Connection
Copy `mainAndon.py` into a Raspberry Pi and run it. Make sure that the Pi is connected to the local network and changed the IP address accordingly in the script.

Run `AsyncServerMain.py` on a host computer to check the status of all the Pi's.

Be sure to run `pip install -r requirements.txt` to install all necessary packages

# Note: python3.11 is required for webui (pip install open-webui), turn your directory into a python virtual enviroment with "py -3.11 -m venv ./" before installing. 
