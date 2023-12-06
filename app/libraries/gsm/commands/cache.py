def config():
    return {
        "sim": {
            "cpin": "app.libraries.gsm.simcom.commands.sim.cpin.CPIN"
        },
        "sms": {
            "cmgl": "app.libraries.gsm.simcom.commands.sms.cmgl.CMGL",
            "cmgs": "app.libraries.gsm.simcom.commands.sms.cmgs.CMGS",
            "cmgd": "app.libraries.gsm.simcom.commands.sms.cmgd.CMGD"
        },
        "statusControl": {
            "csq": "app.libraries.gsm.simcom.commands.statusControl.csq.CSQ"
        }
    }

