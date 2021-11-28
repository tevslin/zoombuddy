# zoombuddy
Beta release of free app to determine and track the quaklity of your internet connection on a contiuous basis, especially the connection's suitability for teleconferencing. 

##Uses
1. determine whether it is your connection or someone elses which is causing freezes and disconnects
2. measure whether your Internet Service Provider (ISP) is delivering the level of service you were promised including peak periods
3. find which rooms in your house have the best WiFi connections
4. determine whether a hotel connection or other temporary connection is good enough for teleconferencing

## Description
Designed to be run continuously to monitor the quality of your Internet coonnection. Tracks current and average latency, jitter, and speed up and down. Indicator lights show suitability for teleconferencing. Latency must be less than 75 ms (milliseconds), jitter less than 8 ms, download speed more than 5Mbps (megabits per second), and upload more than 3Mbps to be considered fully Zommready (green). If these criteria are not met but latency is less 100ms, jitter less than 15ms, download faster than 2Mbps, and upload more than 1Mbps, the Zoomresy status is "iffy" (green). Anything else including inability to connect is status red - not usable for teleconferencing. You will usually find yourself freezing on Zoom and other teleconferencing platforms if your Zoombuddy status is red.

## Installation

###Windows

To download the Windows executable, click [here](https://github.com/tevslin/zoombuddy/raw/main/zoombuddy.exe). You may have to contend with virus blockers or Windows itself warning that the software is from an unknown publisher (me). The software has only been tested on Windows 10.

###Mac and Linux

There are currently no Linux or Mac versions. 

###Python source

The Python source is availablr from this Github repository. 

