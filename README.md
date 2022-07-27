# 3D printer connector
A connection script for the 3d printer REX II from Bresser. This is only one part of a two component application. This is the python scrit that connects to the 3d printer to gather all the neccessary information and send it to an api. You can find the webapplication with the api and a website to control the printer in this repository: [Will be added in the near future (hopefully)]

Here you will only find an explanation of the part of the script and what it expects the api to answer.

## Description
The 3d printer REX II from Bresser is a pretty expensive printer and comes with a network interface. The printer communicates directly with its own slicer software REXPrint so it's not compatible with OctoPrint. So I created this little project / script to monitor the printing progress and the temperatures and also provide a possibility to pause the print remotely.

## How it works
The script runs permanently on a device in the same network as the printer itself. It's connecting to the printer every 30 seconds via a TCP connection and checks if the printer is busy or not. If not the scripts disconnects again so it doesn't interfere with the connection from REXPrint (this is important since the printer can only handle one connection at a time).

If the printer is printing, the connection is being kept alive to check the printing status every second. The script collects the following data:
- nozzle temperature
- print bed temperature
- progress percentage
- printer name

All these information are being stored within a JSON object to send it to a specified API URL. To protect the api from receiving unallowed data the script also sends an api authentication token which you can specify in the settings file.

## API
For this script to work perfectly you will need an api or something like that, that saves the current status information of the printer. It should also provide a controlling interface so you can stop the print when you want to. For more information about the whole concept read the documentation of the webapplication repository.

## Future plans
There are some functions I want to add in the near future:
- Sending start and stopp messages to a specified webhook url / api, like Discord or Telegram to get a notification once the print finished.
- Better stability
- Maybe for future updates: More possibilities to control the printer like setting temperatures.
