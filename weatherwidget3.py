#!/usr/bin/python3.3
# coding=utf-8

# Some ofthe css here is not up to date with the 2.7 version of the script
import urllib.request
import datetime

yhowthr = urllib.request.urlopen("http://weather.yahooapis.com/forecastrss?w=12796475&u=f")
alllines = yhowthr.readlines()
currentline = ""
for line in alllines:
    line = str( line, encoding='utf8' )
    if (line.find("<yweather:condition") == 0):
        currentline = line
        break
loc = currentline.find("code=\"")
forecastlines = []
for line in alllines:
    line = str( line, encoding='utf8' )
    if (line.find("<yweather:forecast") == 0):
        forecastlines.append(line)
index_of_today = -1
days = {x: ("Mon","Tue","Wed","Thu","Fri","Sat","Sun")[x] for x in range(7)}
for i in (0,1):
    if (forecastlines[i].find("day=\"" + days[datetime.datetime.today().weekday()] + "\"") != -1):
        index_of_today = i
        break
print("Content-Type: text/html; charset=utf-8\n")
print("<html>\n<head>\n  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\n</head>")
print("<body style=\"background-image:url('weather2.png'); background-repeat:no-repeat; color:white; width:277px;\">")
print("  <p style=\"text-align:center; font-size:xx-large; margin-bottom:0px; margin-top:10px;\">Currently:</p>")
print("  <table style=\"margin-bottom:100px;\">\n    <tr>\n     <td align=center style=\"width:138px\">\n       <div style=\"position:relative; height:100px;\">\n        <img src=\"weather_" + currentline[loc + 6:loc +10].partition("\"")[0] \
+ ".png\" alt=\"\" style=\"position:absolute; left:-12px;\">\n     </div>\n      </td>\n      <td style=\"width:139px;\">\n      <div style=\"position:relative; height:100px;\">")
loc = currentline.find("temp=\"")
print("        <p style=\"text-align:center; position:absolute; font-size:xx-large; width:140; left:-30px; top:-2px;\">\n" + currentline[loc +6: loc + 11].partition("\"")[0] \
      + " °F\n        </p>\n      </div>\n      </td>\n    </tr>\n  </table>")
print("  <p style=\"text-align:center; font-size:x-large;\">Forecasted:</p>\n  <table style=\"margin-bottom: 30px;\">\n    <tr>")
loc = forecastlines[index_of_today].find("code=\"")
print("      <td align=center style=\"width:138px\">\n       <div style=\"position:relative; height:100px;\">\n        <img src=\"weather_" + forecastlines[index_of_today][loc + 6:loc +10].partition("\"")[0] \
      + ".png\" alt=\"\" style=\"position:absolute; left:-12px;\">\n     </div>\n      </td>\n      <td style=\"width:139px;\">\n      <div style=\"position:relative; height:100px;\">")
loc = []
loc.append(forecastlines[index_of_today].find("high=\""))
loc.append(forecastlines[index_of_today].find("low=\""))
print("        <p style=\"text-align:center; font-size:x-large; position:absolute; width:140; left:-30px; top:3px;\">\n" + forecastlines[index_of_today][loc[0] +6: loc[0] + 11].partition("\"")[0] \
      + " °F&nbsp;&nbsp;&nbsp;&nbsp;" + forecastlines[index_of_today][loc[1] +5: loc[1] + 10].partition("\"")[0] + \
      " °F\n        </p>\n      </div>\n      </td>\n    </tr>\n  </table>")
print("  <p style=\"text-align:center; font-size:x-large;\">Tomorrow:</p>\n  <table>\n    <tr>")
loc = forecastlines[not index_of_today].find("code=\"")
print("      <td align=center style=\"width:138px\">\n       <div style=\"position:relative; height:100px;\">\n        <img src=\"weather_" + forecastlines[not index_of_today][loc + 6:loc +10].partition("\"")[0] \
      + ".png\" alt=\"\" style=\"position:absolute; left:-12px;\">\n      </td>\n     </div>      <td style=\"width:139px;\">\n      <div style=\"position:relative; height:100px;\">")
loc = []
loc.append(forecastlines[not index_of_today].find("high=\""))
loc.append(forecastlines[not index_of_today].find("low=\""))
print("        <p style=\"text-align:center; position:absolute; width:140; left:-30px; top:3px; font-size:x-large;\">\n" \
      + forecastlines[not index_of_today][loc[0] +6: loc[0] + 11].partition("\"")[0] \
      + " °F&nbsp;&nbsp;&nbsp;&nbsp;" + forecastlines[not index_of_today][loc[1] +5: loc[1] + 10].partition("\"")[0] + " °F\n        </p>\n      </div>\n      </td>\n    </tr>\n  </table>")
print("</body>\n</html>")
