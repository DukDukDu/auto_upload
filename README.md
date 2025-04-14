# Description
This repo is used to upload SM or DM(maybe) info to database automatically
All you need is selenium and a Webdriver, and the way to get selenium is 
```
pip install selenium
```
and the way you get a Webdriver is downloading from website, for Edge is:
*https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH#downloads*
You can also use Chrome or Firefox. However Safari is limited, because it cannot be set to 
headless mode.

Before you run, please copy info from your google spread sheet to your own txt file. Attention:
**first line of your txt file should be set as header like csv**.

Usage:
```
python upload.py --txt txtfile.txt --csv csvfile.csv --user Username --pw password
```

