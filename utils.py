def format_reply(reply):
    """
    A helping function that formats all the printers responses to get all the important and required information.
    :param reply: The unformated printer response.
    :return: A Json object containing all the information.
    """

    status = {}
    for entry in reply:
        if "Machine Name: " in entry:
            status["printer_name"] = entry.replace("Machine Name: ", "")
        if "MachineStatus: " in entry:
            status["printer_status"] = entry.replace("MachineStatus: ", "") \
                .replace("BUILDING_FROM_SD", "printing") \
                .replace("READY", "inactive")
        if "MoveMode: " in entry:
            m = entry.replace("MoveMode: ", "")
            if m == "PAUSED":
                status["printer_status"] = "paused"
        if "T0:" in entry:
            t = entry.replace("T0:", "").split(" B:")
            t0_temp = t[0].replace(" /", "/").split("/")
            bed_temp = t[1].split("/")
            temp = {
                "t0": {
                    "actual": t0_temp[0],
                    "set": t0_temp[1]
                },
                "bed": {
                    "actual": bed_temp[0],
                    "set": bed_temp[1]
                }
            }
            status["temperature"] = temp
        if "SD printing byte " in entry:
            p = entry.replace("SD printing byte ", "").split("/")
            status["printer_progress"] = p[0] if p[1] == "100" else str(float(p[0]) / 10)
    return status


def offline_message():
    """
    Returns a Json Object with the standard response if the printer is offline.
    :return: Json Object with standard answer.
    """
    return {
        "printer_name": "Bresser REX II",
        "printer_status": "inactive",
        "printer_progress": "0",
        "temperature": {
            "t0": {
                "actual": "-",
                "set": "-"
            },
            "bed": {
                "actual": "-",
                "set": "-"
            }
        }
    }
