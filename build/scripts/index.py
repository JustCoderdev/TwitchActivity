from TouchPortalAPI import Client, TYPES
from WebHandler import getChannelsInfo, openChannelStream, checkOnline, getGrayImage
from threading import Thread
from time import sleep

## TODO: Check if Token has died in -> 2 Month

ID = 'com.github.justcoderdev.twitchactivity'

REFRESH: dict = {'time': '0', 'state': 'idle'}
CHANNELS: list[str] = []
DYNAMIC: bool = False

isRunning: bool = True
isOnline: bool = True

#!#
TP = Client(ID)

#*#
def updateStates(set: bool = False):
    global ID, CHANNELS, DYNAMIC, isOnline

    isOnline = checkOnline()

    if isOnline:
        TP.stateUpdate(f'{ID}.state.refresh_state', 'refresh')

        infos:list = getChannelsInfo(CHANNELS, set)
        for info in infos:
            icon:str = info['defIcon'] if info['cState'] == 'Online' else getGrayImage(info['defIcon']) if DYNAMIC else info['defIcon']

            TP.stateUpdateMany([
                {'id': f'{ID}.state.{info["display_name"]}.state', 'value': info['cState']},      # Update state state
                {'id': f'{ID}.state.{info["display_name"]}.icon', 'value': icon},                 # Update icon state
                {'id': f'{ID}.state.{info["display_name"]}.viewers', 'value': info['cViewers']},  # Update viewers state
            ]) # yapf: disable

        TP.stateUpdate(f'{ID}.state.refresh_state', 'idle')
    else:
        TP.stateUpdate(f'{ID}.state.refresh_state', 'connection error')


def updateSettings(data):
    global ID, REFRESH, CHANNELS, DYNAMIC

    # Remove old states
    for channel in CHANNELS:
        TP.removeStateMany([
            f'{ID}.state.{channel}.state',    # Remove state state
            f'{ID}.state.{channel}.icon',     # Remove icon state
            f'{ID}.state.{channel}.viewers',  # Remove viewers state
        ]) # yapf: disable

    # Update settings
    REFRESH['time'] = int(data[1]['Refresh Time (m)'])
    CHANNELS = data[0]['Channel names'].replace(' ', '').split(',')[:100]
    DYNAMIC = True if data[2]['Dynamic image (bool)'] == '1' else False

    # Create new states
    for channel in CHANNELS:
        TP.createStateMany([
            {'id': f'{ID}.state.{channel}.state', 'desc': f'{channel} state', 'value': 'Offline', 'parentGroup': channel},  # Create state state
            {'id': f'{ID}.state.{channel}.icon', 'desc': f'{channel} icon', 'value': '', 'parentGroup': channel},           # Create icon state
            {'id': f'{ID}.state.{channel}.viewers', 'desc': f'{channel} viewers', 'value': '0', 'parentGroup': channel}     # Create viewers state
        ]) # yapf: disable

    updateStates(True)


def loop():
    global ID, REFRESH, isRunning

    while isRunning:
        TP.stateUpdate(f'{ID}.state.time_until_refresh', str(0))

        updateStates()

        for i in range(REFRESH['time'] * 60):
            TP.stateUpdate(f'{ID}.state.time_until_refresh', str((REFRESH['time'] * 60) - i))
            sleep(1)


#!#
uThread = Thread(target=loop)


@TP.on(TYPES.onConnect)
def onStart(data):
    global CHANNELS, REFRESH, uThread

    CHANNELS = data['settings'][0]['Channel names'].split(',')
    REFRESH['time'] = data['settings'][1]['Refresh Time (m)']

    updateSettings(data['settings'])

    uThread.start()


@TP.on(TYPES.onAction)
def onActions(data):
    global ID

    if data['actionId'] == f'{ID}.act.refresh':
        updateStates()

    if data['actionId'] == f'{ID}.act.open_stream':
        openChannelStream(data['data'][0]['value'])


@TP.on(TYPES.onSettingUpdate)
def onSettingUpdate(data):
    updateSettings(data['values'])


@TP.on(TYPES.onShutdown)
def onShutdown(data):
    global uThread, isRunning

    isRunning = False
    if uThread.is_alive(): uThread.join()

    TP.disconnect()


#!#
TP.connect()
