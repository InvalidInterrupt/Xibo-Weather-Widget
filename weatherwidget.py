#!/usr/bin/python2.7
# coding=utf-8

#   Copyright 2013 School of Computer Science and Engineering, California State University San Bernardino
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# Change the path above to match the location of Python 2.7 on your system

# Written by Garry Lawrence
# Student Assistant
# School of Computer Science and Engineering,
# California State University San Bernardino

# Weather icons are from CyanogenMod's LockClock,
# and can be downloaded from here:
# https://github.com/CyanogenMod/android_packages_apps_LockClock/tree/cm-10.2/res/drawable-xhdpi

# The number in the image names correlate the Yahoo Weather API's
# condition codes.
#
# The documentation for the Yahoo Weather API can be found at:
# http://developer.yahoo.com/weather/
#
# You can also find how to change the location from there.
#
# I found the current WOEID using the method used here:
# https://github.com/CyanogenMod/android_packages_apps_LockClock/blob/cm-10.2/src/com/cyanogenmod/lockclock/weather/YahooWeatherProvider.java

# Please note that the CSS in this page was developed for the browser embedded in the .NET Xibo client.
# As such, when adjusting styles, use Microsoft Internet Explorer with Compatibility View turned on.

try:
    import urllib2
    import datetime

    # Download weather info for San Bernardino for Yahoo Weather's API
    # To change the location, replace the WOEID in this URL. See the API reference linked above.
    # Try again in the event of a gateway timeout on the server
    # TODO: Add handling of more errors as necessary
    while True:
        try:
            yhowthr = urllib2.urlopen("http://weather.yahooapis.com/forecastrss?w=12796475&u=f")
            break
        except urllib2.HTTPError as detail:
            # In the past, I have occasionally received gateway timeouts.
            # In that event, wait a few moments, then retry.
            if (detail.code == 504):
                time.sleep(2)
                continue
            else:
                # I don't know what other errors we may feasibly run into.
                # If something else unexpected happens here, throw it back up the stack.
                raise

    all_lines = yhowthr.readlines()
    # Find the line # of the current weather conditions 
    currentline = ""
    for line in all_lines:
        if (line.find("<yweather:condition") == 0):
            currentline = line
            break
        
    # Note the location of the weather code within that line
    loc = currentline.find("code=\"")

    # Create an array with the forecast lines.
    forecastlines = []
    for line in all_lines:
        if (line.find("<yweather:forecast") == 0):
            forecastlines.append(line)
            
    # Yahoo now returns more than two forecasts. Only take those for today and tomorrow.
    index_of_today = -1
    index_of_tomorrow = -1
    days = {x: ("Mon","Tue","Wed","Thu","Fri","Sat","Sun")[x] for x in range(7)}
    for i, line in enumerate(forecastlines):
        if (line.find("day=\"" + days[datetime.date.today().weekday()] + "\"") != -1):
            index_of_today = i
        elif (line.find("day=\"" + days[(datetime.date.today().weekday() + 1) % 7] + "\"") != -1):
            index_of_tomorrow = i
        if (index_of_tomorrow != -1 and index_of_today != -1):
            break

except:
    import traceback
    import sys
    traceback.print_exception(*sys.exc_info())
    print '''Content-Type: text/html; charset=utf-8

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  </head>
  <body style="background-image:url('weather2.png'); background-repeat:no-repeat; color:white; width:277px;">
  </body>
</html>'''
  
else:
    # Output headers
    print "Content-Type: text/html; charset=utf-8\n"

    # Output HTML document
    print '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  </head>
  <body style="background-image:url('weather2.png'); background-repeat:no-repeat; color:white; width:277px;">'''
    # Start current conditions
    print '''    <p style="text-align:center; font-size:xx-large; margin-bottom:0px; margin-top:10px;">Currently:</p>
    <table style="margin-bottom:100px;">
      <tr>
        <td align=center style="width:138px">
          <div style="position:relative; height:100px;">
            <img src="weather_''' + currentline[loc + 6:loc +11].partition("\"")[0] + '''.png" alt="" style="position:absolute; left:-12px;">
          </div>
        </td>
        <td align=center style="width:139px;">
          <div style="position:relative; height:100px">
            <p style="text-align:center; position:absolute; font-size:xx-large; width:140px; left:-30px; top:30px;">'''
    loc = currentline.find("temp=\"")
    print currentline[loc +6: loc + 11].partition("\"")[0] + ''' °F
            </p>
          </div>
        </td>
      </tr>
    </table>'''
    # Start forecasted conditions
    loc = forecastlines[index_of_today].find("code=\"")
    print '''    <p style="vertical-align:middle; text-align:center; font-size:x-large;">Forecasted:</p>
    <table style="margin-bottom: 30px;">
      <tr>
        <td align=center style="width:138px">
          <div style="position:relative; height:100px;">
            <img src="weather_''' + forecastlines[index_of_today][loc + 6:loc +11].partition("\"")[0] + '''.png" alt="" style="position:absolute; left:-12px;">
          </div>
        </td>
        <td style="width:139px;">
          <div style="position:relative; height:100px;">'''
    loc = [forecastlines[index_of_today].find("high=\""), forecastlines[index_of_today].find("low=\"")]
    print "            <p style=\"text-align:center; font-size:x-large; position:absolute; width:140px; left:-30px; top:34px;\">"
    print forecastlines[index_of_today][loc[0] +6: loc[0] + 11].partition("\"")[0] \
          + " °F&nbsp;&nbsp;&nbsp;&nbsp;" + forecastlines[index_of_today][loc[1] +5: loc[1] + 10].partition("\"")[0] + \
          ''' °F
            </p>
          </div>
        </td>
      </tr>
    </table>
    <p style="text-align:center; font-size:x-large;">Tomorrow:</p>
    <table>
      <tr>'''
    loc = forecastlines[index_of_tomorrow].find("code=\"")
    print '''        <td align=center style="width:138px">
          <div style="position:relative; height:100px;">
            <img src="weather_''' + forecastlines[index_of_tomorrow][loc + 6:loc +11].partition("\"")[0] + '''.png" alt="" style="position:absolute; left:-12px;">
          </div>
        </td>
        <td style="width:139px;">
          <div style="position:relative; height:100px;">'''
    loc = [forecastlines[index_of_tomorrow].find("high=\""), forecastlines[index_of_tomorrow].find("low=\"")]
    print "            <p style=\"text-align:center; position:absolute; width:140px; left:-30px; top:34px; font-size:x-large;\">"
    print forecastlines[index_of_tomorrow][loc[0] +6: loc[0] + 11].partition("\"")[0] \
          + " °F&nbsp;&nbsp;&nbsp;&nbsp;" + forecastlines[index_of_tomorrow][loc[1] +5: loc[1] + 10].partition("\"")[0] + \
          ''' °F
            </p>
          </div>
        </td>
      </tr>
    </table>
  </body>
</html>'''
