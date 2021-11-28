# zoombuddy
app to determine and track ip connection suitability for teleconferencing

## Description
Designed to be run continuously to monitor the quality of your Internet coonnection. Tracks current and average latency, jitter, and speed up and down. Indicator lights show suitability for teleconferencing. Latency must be less than 75 ms (milliseconds), jitter less than 8 ms, download speed more than 5Mbps (megabits per second), and upload more than 3Mbps to be considered fully Zommready (green). If these criteria are not met but latency is less 100ms, jitter less than 15ms, download faster than 2Mbps, and upload more than 1Mbps, the Zoomresy status is "iffy" (green). Anything else including inability to connect is status red - not usable for teleconferencing. You will usually find yourself freezing on Zoom and other teleconferencing platforms if your Zoombuddy status is red.

## Installation

To download the Windows executable, click [here](https://github.com/tevslin/zoombuddy/raw/main/zoombuddy.exe). There are currently no Linux and Mac versions. The Python source is availablr from a Github repository at 

