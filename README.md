# TwitchActivity

A plugin for [Touch Portal](https://www.touch-portal.com/) to have information about Twitch streamers

This documentation is partially generated with [Python TouchPortal SDK](https://github.com/KillerBOSS2019/TouchPortal-API).

## Quick Setup

1. Import the plugin from the release section on [github](https://github.com/JustCoderdev/TwitchActivity/releases)
2. Go to the plugin settings and change `Channel names` to the names of your followed channels and, if you need, adjust the refresh time (enter the time in minutes)
   > NOTE: `Channel names` **must** be formatted like this (MonikaCinnyRoll,xSgtPepperx) and separated by `,` (capital letters and spaces have no influence over the functioning of the plugin) and contain up to 100 channels (the extra ones are just going to be ignored)
3. Import a simple button from `helpers/touchportal`
4. Go to the button GUI and change `Open stream` action field to any channel name (doesn't need to be one from `Channel names`, anyone is fine)
5. Press the `On Event` tab and change the value in `Update Button text...` from `${value:com.github.justcoderdev.twitchactivity.state.xSgtPepperx.viewers}` to `${value:com.github.justcoderdev.twitchactivity.state.YOURCHANNELNAME.viewers}` and `Change the icon...` from `xSgtPepperx icon` to `YOURCHANNELNAME icon`
6. Done! Now you can customize this button as you wish, adding a shade of red when the connection is lost, showing 🔴 next to the viewers number, adding a default image to avoid having the blank icon in TP from the pc, showing the channel name, etc... (view the [FAQ](#faq) for more info)

## Extra

- Custom icons
  > Use your own set of icons that can gray out and automatically be integrated with the plugin)
  1. Wait until the plugin loads the `Icons` folder in `%APPDATA%\TouchPortal\plugins\TwitchActivity`
  2. Drop your icons (in PNG format) in the folder and rename them like this `YOURCHANNELNAME.png` with `YOURCHANNELNAME` in lowercase (`yourchannelname.png`)
  3. Done!

- Read the Log
  > The log file has a symbol before each action
  - `!`: initialization process
  - `?`: general information log
  - `*`: update on the states

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

### - What `Open stream` does?

Open Stream, will open a new twitch.tv webpage on the entered channel, the name of the channel you want to open must be entered in the action field

### - What `Dynamic image` does?

Dynamic image if set to false (0) will make the channel icon the default one. Instead if it is true (1) it will look at the status of the channel and set the icon to colored if online or grayed out if offline

### - What happen `On refresh state`?

- `refresh` is the period in which the plugin fetches new data from twitch and updates all states
- `idle` the plugin is just sitting there, chilling until the countdown reaches 0 to update the states
- `connection error` the plugin isn't going to fetch any data because it detected an error with the internet connection, when the problem goes away, in the next refresh, the plugin will continue to work as intended

### - In which format is the `viewers count` shown?

The viewers count if the channel is offline it's a simple empty string (`''`) else it's the actual number of viewers (ex. `'248'`)

## Error handling

In case the countdown doesn't tick anymore, the plugin has crashed, try reloading TP or just stop and restart the plugin. If the problem persists [contact me](#Notes)

If, when adding a new streamer, its icon is not displayed and after TP restarts none of the plugin icons are displayed there may be a space in the `Channel names` setting

In case you keep your PC on for weeks, the plugin may stop fetching data and eventually crash, just reload the plugin and it should update Twitch access token

# Notes

In case there are bugs or you need support contact me on [Touch Portal discord](https://discord.gg/mXWvEUczEK)

I want to thank all of the person that helped me on **Touch Portal discord**
