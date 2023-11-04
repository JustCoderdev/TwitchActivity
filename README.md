# TwitchActivity

A plugin for [Touch Portal](https://www.touch-portal.com/) to get information about live Twitch channels

This documentation is partially generated with [Python TouchPortal SDK](https://github.com/KillerBOSS2019/TouchPortal-API).

## Quick Setup

<details><summary>1.  Download and import the plugin from the <a href="https://github.com/JustCoderdev/TwitchActivity/releases/latest">release</a> section (if it get's stuck during installation check <a href="#common-error-handling">handling errors</a>)
</summary> <img src="https://github.com/JustCoderdev/TwitchActivity/blob/main/resources/images/QuickSetup1.png" height="300" />
</details>

2. Go to the plugin settings and change `Channel names` to the names of the channels that you follow and, if you need, adjust the refresh time (as minutes)
   > [!NOTE]
   > - `Channel names` **must** be formatted like: `NAMEA,NAMEB,NAMEC` (ex. MonikaCinnyRoll,xSgtPepperx) with `,` between the names and can contain up to 100 channels (if more are inserted, they will be ignored)
   > - The Twitch API ignores capitalisation but you can use it to "prettify" the names

3. Import a simple button from [`resources\touchportal\buttons\`](https://github.com/JustCoderdev/TwitchActivity/tree/main/resources/touchportal/buttons)

4. Go to the _On Pressed_ button and change `Open stream` action field to any channel name (doesn't need to be one from `Channel names`, anyone is fine)

<details> <summary>5. Go to <i>On Event</i> tab and change the value in <code>Update Button text...</code> from <code>${...state.xSgtPepperx.viewers}</code> to <code>${...state.YOURCHANNELNAME.viewers}</code> and <code>Change the icon...</code> from <code>xSgtPepperx icon</code> to <code>YOURCHANNELNAME icon</code>
</summary> <br> <img src="https://github.com/JustCoderdev/TwitchActivity/blob/main/resources/images/QuickSetup4.png" height="200" /> </details>

5. Done! Now you can customize this button as you wish like:
      - Adding a shade of red when the connection is lost
      - Showing 🔴 next to the viewers number
      - Adding a default image to avoid a blank icon (on desktop app)
      - Showing the channel name
      - etc...

_view the [FAQ](#faq) for more info_

## Extra

<details> <summary>Setting custom icons</summary>
<img src="https://github.com/JustCoderdev/TwitchActivity/blob/main/resources/images/custom_icons.png" height="250" /></details>

> Integrate your own set of icons with the plugin (they can even be grayed out automatically!)

1. After installation wait until the plugin loads all the default icons inside the `icons\` folder in the plugin directory (see below)
2. Remove the default icons and move your own in the folder
   > [!NOTE]
   > - The icons **must** be PNGs and preferably squared
   > - The icon name **must** be written as `YOURCHANNELNAME.png` with `YOURCHANNELNAME` in lowercase (ex. monikacinnyroll.png)
3. Done! If it doesn't show instantly don't worry, just restart the desktop and mobile app and it should set correctly or just wait until TP update itself

- Reading the Logs

  > You want to see if the plugin has updated the state of your favorite channel? The log file has a symbol before each action to help visualize what happens

  - `!`: initialization process
  - `?`: general information log
  - `*`: states update

- Find the plugin directory
  - The plugin directory should be here: `%APPDATA%\TouchPortal\plugins\TwitchActivity\`

- The plugin id is `com.github.justcoderdev.twitchactivity`

## Plugin features

### Actions

| Action Name | Description                                              | Format           | Data                                       | On Hold |
| ----------- | -------------------------------------------------------- | ---------------- | ------------------------------------------ | :-----: |
| Refresh     | This action will refresh the channels states             |                  |                                            |   No    |
| Open stream | This action will open selected channel stream in browser | Open \[1] stream | 1. Type: text &nbsp; Default: **ImKibitz** |   No    |

### States

| Id                        | Description        | DefaultValue      | parentGroup     |
| ------------------------- | ------------------ | ----------------- | --------------- |
| .state.refresh_state      | Refresh state      | idle              | Twitch Activity |
| .state.time_until_refresh | Time until refresh | 600               | Twitch Activity |
| .state.blank_icon         | Blank icon         | _b64 blank Image_ | Twitch Activity |

### Streamer Specific States

| Id                               | Description               | DefaultValue | parentGroup       |
| -------------------------------- | ------------------------- | ------------ | ----------------- |
| .state.`YOURCHANNELNAME`.state   | `YOURCHANNELNAME` state   | Offline      | `YOURCHANNELNAME` |
| .state.`YOURCHANNELNAME`.icon    | `YOURCHANNELNAME` icon    | ''           | `YOURCHANNELNAME` |
| .state.`YOURCHANNELNAME`.viewers | `YOURCHANNELNAME` viewers | 0            | `YOURCHANNELNAME` |

### Events

| Id                      | Name             | Evaluated State Id   | Format  | Type   | Choice(s)                                                            |
| ----------------------- | ---------------- | -------------------- | ------- | ------ | -------------------------------------------------------------------- |
| .event.on_refresh_state | On refresh state | .state.refresh_state | On $val | choice | <ul> <li>refresh</li> <li> idle </li> <li>connection error</li></ul> |

## FAQ

### - What does `Open stream` do?

Open Stream, will open a new twitch.tv webpage to open the channel live

<details><summary><h3 style="display:inline">What does the <code>Dynamic image</code> setting do?</h3></summary><img src="https://github.com/JustCoderdev/TwitchActivity/blob/main/resources/images/online_offline.png" height="200" /></details>

- If set to `false` (`0`)
The icon the plugin will provide (contained in `YOURCHANNELNAME icon` value) is going to be the default channel icon (or the provided icon in the `icons\` folder)

- If set to `true` (`1`)
The icon will react to the state of the channel. The icon will remain the default when the channel is live, however, when the channel is offline the icon will be grayed out

<details><summary><h3 style="display:inline">What happen <code>On refresh state</code>?</h3></summary>
<img src="https://github.com/JustCoderdev/TwitchActivity/blob/main/resources/images/refresh_states.png" height="200" />
</details>

- On `refresh` the plugin fetches new data from Twitch and updates all states
- On `idle` the plugin is just sitting there, chilling, until the countdown reaches 0 to update it's states
- On `connection error` the plugin detected a connection error and, when the problem goes away, the plugin will continue to work as intended

### - In which format is the `viewers count` shown?

The viewers count, if the channel is offline, it's a simple empty string (`''`) otherwise it's the actual number of viewers (ex. `'248'`)

## Common Error handling

In case the countdown doesn't tick anymore, the plugin probably crashed, try reloading TP or just stop and restart the plugin. If the problem persists [contact me](##Notes)

In case your PC stays on for weeks (hope not), the plugin may stop fetching data and give a connection error even if it has connection to internet. Reload the plugin or restart TP to update the Twitch access token

If, during installation, the plugin get stuck and the slider don't move try to install the plugin manually:

1. Rename `TwitchActivity.tpp` to `TwitchActivity.zip` and unzip it
2. Move the unzipped folder in `%Appdata%\touchportal\plugins\` and restart TP

## Notes

In case there are bugs or you need support contact me on [Touch Portal discord](https://discord.gg/mXWvEUczEK)

I want to thank all of the person that helped me on **Touch Portal discord**
