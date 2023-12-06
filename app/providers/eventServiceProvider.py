from pythoniq.framework.illuminate.foundation.support.providers.eventServiceProvider import \
    EventServiceProvider as ServiceProvider


class EventServiceProvider(ServiceProvider):
    # The event to listener mappings for the application.
    _listen = {
        'app.events.testEvent.TestEvent': [
            'app.listeners.testEvent.test.Test',
        ],
        'app.libraries.gsm.events.hardware.opening.Opening': [],
        'app.libraries.gsm.events.hardware.opened.Opened': [],
        'app.libraries.gsm.events.hardware.closing.Closing': [],
        'app.libraries.gsm.events.hardware.closed.Closed': [],
        'app.libraries.gsm.events.hardware.powerOpening.PowerOpening': [],
        'app.libraries.gsm.events.hardware.powerOpened.PowerOpened': [],
        'app.libraries.gsm.events.hardware.powerClosing.PowerClosing': [],
        'app.libraries.gsm.events.hardware.powerClosed.PowerClosed': [],
        'app.libraries.gsm.events.hardware.simCardInserted.SimCardInserted': [
            'app.listeners.gsm.hardware.simCardInserted.restart.Restart',
        ],
        'app.libraries.gsm.events.hardware.simCardRemoved.SimCardRemoved': [
            'app.listeners.gsm.hardware.deActivated.gsmLedOff.GsmLedOff'
        ],
        'app.libraries.gsm.events.hardware.activating.Activating': [],
        'app.libraries.gsm.events.hardware.activated.Activated': [
            'app.listeners.gsm.hardware.activated.setBaudRate.SetBaudRate',
            'app.listeners.gsm.hardware.activated.gsmLedOn.GsmLedOn'
        ],
        'app.libraries.gsm.events.hardware.deActivating.DeActivating': [],
        'app.libraries.gsm.events.hardware.deActivated.DeActivated': [
            'app.listeners.gsm.hardware.deActivated.gsmLedOff.GsmLedOff'
        ],
        'app.libraries.gsm.events.sim.ready.Ready': [
            'app.listeners.gsm.sim.ready.autoCsqStart.AutoCsqStart',
        ],
        'app.libraries.gsm.events.network.attached.Attached': [
            'app.listeners.gsm.network.attached.queryGsmNetwork.QueryGsmNetwork',
        ],
        'app.libraries.gsm.events.network.gsmNetworkRegistered.GsmNetworkRegistered': [
            'app.listeners.gsm.network.gsmNetworkRegistered.queryGprsNetwork.QueryGprsNetwork'
        ],
        'app.libraries.gsm.events.network.networkNotRegistered.NetworkNotRegistered': [
            'app.listeners.gsm.network.networkNotRegistered.queryLteNetwork.QueryLteNetwork'
        ],
        'app.libraries.gsm.events.network.networkRegistered.NetworkRegistered': [
            'app.listeners.gsm.network.networkRegistered.setPdpContext.SetPdpContext',
            'app.listeners.gsm.network.networkRegistered.activatePdpContext.ActivatePdpContext',
            'app.listeners.gsm.network.networkRegistered.getPdpAddress.GetPdpAddress',
        ],
        'app.libraries.gsm.events.network.pdpAddressSet.PdpAddressSet': [
            'app.listeners.gsm.network.pdpAddressSet.setApplicationMode.SetApplicationMode',
            'app.listeners.gsm.network.pdpAddressSet.socketServiceStart.SocketServiceStart',
        ],
        'app.libraries.gsm.events.network.networkOpen.NetworkOpen': [
            'app.listeners.gsm.network.networkOpen.networkLedOn.NetworkLedOn',
            'app.listeners.gsm.network.networkOpen.serverStart.ServerStart',
        ],
        'app.libraries.gsm.events.statusControl.signalQualityChanged.SignalQualityChanged': [
            'app.listeners.gsm.statusControl.signalQualityChanged.ledUpdate.LedUpdate',
        ],

        'app.events.hardware.protectionCover.opened.Opened': [
            'app.listeners.hardware.protection.opened.alarm.Alarm',
        ]
    }

    _listen2 = {
        'app.events.gsm.sim.ready.Ready': [
            'app.listeners.gsm.sim.ready.autoCsqStart.AutoCsqStart',
            'app.listeners.gsm.sim.ready.gsmLedOn.GsmLedOn',
        ],
        'app.events.gsm.sim.removed.Removed': [
            'app.listeners.gsm.sim.removed.gsmLedOff.GsmLedOff',
            'app.listeners.gsm.sim.removed.gprsQualityLedAllOff.GprsQualityLedAllOff',
            'app.listeners.gsm.sim.removed.signalQualityLedAllOff.SignalQualityLedAllOff',
        ],
        'app.events.gsm.sms.receive.Receive': [
            'app.listeners.gsm.sms.receive.readAndDeleteSms.ReadAndDeleteSms',
        ],
        'app.events.gsm.sms.read.Read': [
            'app.listeners.gsm.sms.read.processing.Processing'
        ],
        'app.events.gsm.sms.send.Send': [
            'app.listeners.gsm.sms.send.sendMessage.SendMessage',
        ],

    }

    # Register any events for your application.
    def boot(self) -> None:
        pass

    # Determine if events and listeners should be automatically discovered.
    def shouldDiscoverEvents(self) -> bool:
        return False
