# !/usr/bin/env python3
# Asyncronous UDP Server for Qualitel Andon system, using asyncio for threads, 
#   * Main thread: spins off the following threads: 
#       * UDP_Thread: polls for measeges comming from the individual Andon lights.
#       * HTML_Thread: posts andon light status to webpage.
#       * Database_Thread: logs state changes of all Andons 


######   Import packages   ######   
from datetime import datetime   # to get today date
from webui import webui         # for HTML
import socket                   # for UDP
import time                     # time.sleep(seconds)
import asyncio                  # for threads
from UDP_Thread import *        # import all definitions for the UDP_Thread
from HTML_Thread import *       # import all definitions for the HTML_Thread
from Database_Thread import *   # import all definitions for the Database_Thread

def run_UDP_Thread(queue):
    asyncio.run(UDP_Thread(queue))

def run_Database_Thread(queue):
    asyncio.run(Database_Thread(queue))

######   Main function spins off the threads   ######           
async def main():
    print("starting main")
    queue = asyncio.Queue(maxsize=100)

    udp_task = asyncio.to_thread(run_UDP_Thread, queue)
    database_task = asyncio.to_thread(run_Database_Thread, queue)
    html_task = asyncio.to_thread(HTML_Thread)

    asyncio.gather(
        html_task,
        udp_task,
        database_task)

asyncio.run(main(), debug=True)