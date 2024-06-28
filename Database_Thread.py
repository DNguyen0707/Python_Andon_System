from datetime import datetime   # to get today date
from webui import webui         # for HTML
import socket                   # for UDP
import time                     # time.sleep(seconds)
import asyncio                  # for threads
from UDP_Thread import *        # get definition of "list of Andons"
import pyodbc

dbDictonary = {              # dictionary data type to hold data for each andon
    "IP": "xxx.xxx.xxx.xxx",
    "Name": "Andon XX",
    "Status": "Color",
    "Down Time": "01.01.01"
}

async def Database_Thread(queue: asyncio.Queue):
    print("starting Database Thread") 
    connectionString = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ=\\\\QEA.LOCAL\\QMS\\03. Engineering\\80. Test Engineering\\Uncontrolled\\Andon\\Andon Monitor 2024.accdb'
    conn = pyodbc.connect(connectionString)
    while True: 
        time.sleep(0.1)
        if queue.empty() == False:
            
            print("database task got message:")
            dbDictonary = await queue.get()
            AndonName = dbDictonary["Name"]
            Status = dbDictonary["Status"]
            DateTime = dbDictonary["Date Time"]
            
            
            cursor = conn.cursor()
            SQLCommand = f"INSERT INTO AndonTable (Andon_ID, Status, Date_Time)  \nVALUES (\'{AndonName}\', \'{Status}\', \'{DateTime}\');"
            print(SQLCommand)
            cursor.execute(SQLCommand)
            
            cursor.commit()

            cursor = conn.cursor()
            cursor.execute('select * from AndonTable')
        