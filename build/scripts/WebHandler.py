from requests import post, get, ConnectionError
from base64 import b64decode, b64encode
from webbrowser import open as browse
from os import mkdir, path
from io import BytesIO
from PIL import Image
from env import CLIENT_ID, CLIENT_SECRET, VERSION

#* DEBUG
from logging import INFO, basicConfig, info


open('./utils/log.txt', 'w').write('')
basicConfig(filename='./utils/log.txt', level=INFO)


def log(msg: str):
    print(f'Twitch Activity: {msg}')
    info(f'Twitch Activity: {msg}')


log(f'! Loading Twitch Activity plugin | v{VERSION}')

#* DEBUG

CHANNELS: dict = {}
isOnline = True


#!#
def checkOnline():
    global isOnline

    try:
        get('https://www.twitch.tv/')
        log('? Check online | True')
        isOnline = True
        return True
    except ConnectionError:
        log('? Check online | False')
        isOnline = False
        return False


def openChannelStream(channel: str):
    browse(f'https://www.twitch.tv/{channel}')


def getChannelsInfo(channels: list[str], set: bool = False) -> list:
    global CHANNELS

    if set:
        log(f'! Setting data | {channels}')

        #? Check available icons
        if not path.exists('./Icons'): mkdir("./Icons")
        noIconUsers: list = []

        for channel in channels:
            if not path.exists(f"./Icons/{channel.lower()}.png"): noIconUsers.append(channel)

        if len(noIconUsers) != 0:
            noIconUsersDataApi = API.getUsers(noIconUsers)
            noIconUsersData = [] if noIconUsersDataApi == None else noIconUsersDataApi['data']

            for noIconUser in noIconUsers:
                userData = getChannelUserData(noIconUsersData, noIconUser)
                saveIcon(userData['defIcon'], noIconUser)

            log(f"! New Icon for | {noIconUsers}")

        streamsDataApi = API.getStreams(channels)
        streamsData = [] if streamsDataApi == None else streamsDataApi['data']

        for channel in channels:
            userData = {'display_name': channel, 'defIcon': getIcon(channel)}
            streamData = getChannelStreamData(streamsData, channel)

            CHANNELS[channel.lower()] = {
                'display_name': userData['display_name'],   #? get Users
                'defIcon': userData['defIcon'],             #? get Users
                'cState': streamData['cState'],             #? get Streams
                'cViewers': streamData['cViewers'],         #? get Streams
            } # yapf: disable

    else:
        log(f'* Updated data | {channels}')

        streamsDataApi = API.getStreams(channels)
        streamsData = [] if streamsDataApi == None else streamsDataApi['data']

        for channel in channels:
            streamData = getChannelStreamData(streamsData, channel)

            CHANNELS[channel.lower()]['cState'] = streamData['cState']
            CHANNELS[channel.lower()]['cViewers'] = streamData['cViewers']

    output: list = []
    for channel in CHANNELS:
        output.append(CHANNELS[channel])

    return output


#*#


class Twitch:
    CLIENT_ID: str = ''
    CLIENT_SECRET: str = ''
    TOKEN: str = ''

    def __init__(self, client_id: str, client_secret: str):
        log('! Twitch initialization')
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.newToken()

    def newToken(self):
        global isOnline

        if not isOnline: return None

        try:
            self.TOKEN = post(f'https://id.twitch.tv/oauth2/token?client_id={self.CLIENT_ID}&client_secret={self.CLIENT_SECRET}&grant_type=client_credentials').json()['access_token']
        except ConnectionError:
            isOnline = False

    def getStreams(self, users: list):  #! Check if token is gone   #* Channels & Viewers
        #? user_login -> Returns streams broadcast by one or more specified user login names. You can specify up to 100 names.
        #* Get Images #https://dev.twitch.tv/docs/api/reference#get-streams

        global isOnline

        if not isOnline: return None

        query: str = ''
        for user in users:
            query += f'&user_login={user}'

        try:
            res = get(f'https://api.twitch.tv/helix/streams?{query[1:]}', headers={'Authorization': f'Bearer {self.TOKEN}', 'Client-Id': self.CLIENT_ID}).json()
            return None if res.get('data') == None else res
        except ConnectionError:
            isOnline = False

    def getUsers(self, users: list):  #! Check if token is gone
        #? login -> User login name. Multiple login names can be specified. Limit: 100.
        #* Get Images #https://dev.twitch.tv/docs/api/reference#get-users

        global isOnline

        if not isOnline: return None

        query: str = ''
        for user in users:
            query += f'&login={user}'

        try:
            res = get(f'https://api.twitch.tv/helix/users?{query[1:]}', headers={'Authorization': f'Bearer {self.TOKEN}', 'Client-Id': self.CLIENT_ID}).json()
            return None if res.get('data') == None else res
        except ConnectionError:
            isOnline = False


#*#

API = Twitch(CLIENT_ID, CLIENT_SECRET)


def getChannelUserData(usersData: list, channel: str) -> dict:
    output: dict = {
        'display_name': channel,
        'defIcon': None,
    }

    for userData in usersData:
        if userData['login'] == channel.lower():
            output['display_name'] = userData['display_name']
            output['defIcon'] = getDefImage(userData['profile_image_url'])
            return output

    return output


def getChannelStreamData(streamsData: list, channel: str) -> dict:
    output: dict = {
        'cState': 'Offline',
        'cViewers': '',
    }

    for streamData in streamsData:
        if streamData['user_login'] == channel.lower():
            output['cState'] = 'Offline' if streamData['type'] == '' else 'Online'
            output['cViewers'] = str(streamData['viewer_count'])
            return output

    return output


def getDefImage(imgURL: str) -> str | None:
    global isOnline

    if not isOnline: return None

    try:
        imgBytes = get(imgURL).content
    except ConnectionError:
        isOnline = False
        return None

    #!#
    imgDef = Image.open(BytesIO(imgBytes))
    #!#

    #? Convert to B64
    buffered = BytesIO()
    imgDef.save(buffered, format="PNG")
    imgB64 = b64encode(buffered.getvalue()).decode('ascii')

    return imgB64


def getGrayImage(b64Image: str) -> str | None:
    if b64Image == None: return None

    #? Convert to byte
    imgBytes = b64decode(b64Image)

    #!#
    #? Convert to Image object
    imgDef = Image.open(BytesIO(imgBytes))

    #? Convert to Gray
    imgGray = imgDef.convert('LA')
    #!#

    #? Convert to B64
    buffered = BytesIO()
    imgGray.save(buffered, format="PNG")
    imgGrayB64 = b64encode(buffered.getvalue()).decode('ascii')

    return imgGrayB64

def saveIcon(b64Image: str, channel: str) -> None:
    if not path.exists('./Icons'): mkdir("./Icons")
    if b64Image == None: return

    with open(f"./Icons/{channel.lower()}.png", "wb") as icon:
        #? Convert to byte
        imgBytes = b64decode(b64Image)

        #? Convert to Image object
        imgDef = Image.open(BytesIO(imgBytes))

        #? Convert to PNG
        buffered = BytesIO()
        imgDef.save(buffered, format="PNG")

        icon.write(buffered.getvalue())


def getIcon(channel: str) -> str | None:
    if not path.exists(f"./Icons/{channel.lower()}.png"): return None

    #? Convert to Image object
    imgDef = Image.open(f"./Icons/{channel.lower()}.png")

    #? Convert to B64
    buffered = BytesIO()
    imgDef.save(buffered, format="PNG")
    imgB64 = b64encode(buffered.getvalue()).decode('ascii')

    return imgB64