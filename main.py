import logging
import requests
import time
from argparse import ArgumentParser
from connector import Connector
from settings import Settings
from utils import format_reply, offline_message

"""
A list of all the commands that are needed to gather the  required information for the website
M25 - Pause print
M27 - Print status
M105 - Temperature (hotend and print bed)
M115 - Maschine Name, Firmware, MacAdress
M119 - Maschine status
"""


def is_printing(c):
    """
    Determines if the printer is currently printing or not.
    :param c: A connection object.
    :return: True if device is printing, else false.
    """

    if not c.socket:
        return False

    reply = c.send_command("M119")

    if not reply or reply == []:
        logging.info("Printer seems to be offline.")
        return False

    for entry in reply:
        if "BUILDING_FROM_SD" in entry:
            logging.info("Printer is printing right now.")
            return True

    logging.info("Printer is idling right now.")
    return False


def update_status(status, settings):
    """
    A method to update the status information by sending it to the API specified in the printer_settings.json file
    :param status: The status information as a json object
    :param settings: The settings object
    :return: A request object containing all the information of that request
    """

    status["printer_id"] = settings.get("id")
    status["printer_name"] = settings.get("name")
    headers = {'key': settings.get("api_key")}
    return requests.post(settings.get("api_addr"), json=status, headers=headers)


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

    parser = ArgumentParser()
    parser.add_argument("-i", "--id", dest="id", help="set printer id, standard value is 1", default=1)
    args = parser.parse_args()

    # initialize a settings object by loading the printer_settings.json file. Edit the file if needed.
    settings = Settings("printer_settings.json", args.id)
    # initialize a connection objection with the specified ip and port of the printer
    connector = Connector(settings.get("ip"), settings.get("port"), settings.get("name"))

    _is_printing = False

    while True:
        while not _is_printing:
            # while the printer is in idle mode check every 30 seconds for a new print job
            connector.connect()
            _is_printing = is_printing(connector)
            if not _is_printing:
                connector.disconnect()
                time.sleep(settings.get("loop_time"))

        while _is_printing:
            # while the printer is busy check its status information every second and update the database via the api
            status = format_reply(connector.send_commands(["M27", "M105", "M115", "M119"]))
            logging.debug(status)
            if update_status(status, settings).status_code == 418:
                # if the api respondes with the status code 418, pause the printer
                connector.send_command("M25")

            # if the printer is done with the print and also its temperature is below 100°C go back to idle mode
            if (status["printer_status"] == "inactive" or status["printer_status"] == "paused")\
                    and float(status["temperature"]["t0"]["actual"]) < 100:
                _is_printing = False
                update_status(offline_message(), settings)
            time.sleep(1)

        connector.disconnect()
        time.sleep(settings.get("loop_time"))


if __name__ == "__main__":
    main()
