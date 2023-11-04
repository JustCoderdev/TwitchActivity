@REM Script by JustCoderdev, github here -> https://github.com/JustCoderdev/

@echo off

set pluginPath="D:\01_Personal\.GitHub\TwitchActivity"
set pluginsFolder="C:\Users\perin\AppData\Roaming\TouchPortal\plugins"
set tpPath="D:\02_Apps\TouchPortal\Touch Portal\TouchPortal.exe"

taskkill /IM TouchPortal.exe /T /F

cd ./build/scripts&C:\Users\perin\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts\pyinstaller --onefile index.py --clean --workpath %pluginPath%\build\temp --distpath %pluginPath%\TwitchActivity

rmdir %pluginsFolder%\TwitchActivity /s /q

mkdir %pluginsFolder%\TwitchActivity

xcopy %pluginPath%\TwitchActivity %pluginsFolder%\TwitchActivity /E /Y

start "" %tpPath%

@REM timeout 5 >nul

@REM start notepad++ "%pluginsFolder%\TwitchActivity\utils\log.txt""