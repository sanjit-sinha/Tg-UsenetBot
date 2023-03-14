<div align="center">
<img src="https://te.legra.ph/file/eabcc7c6b84fa33ca6f22.png" align="center" style="width: 50%" />
</div>

<h1 align="center"> Telegram UsenetBot </h1>
<p align="center">
<img src="https://img.shields.io/github/stars/sanjit-sinha/Tg-UsenetBot">
<img src="https://img.shields.io/github/forks/sanjit-sinha/Tg-UsenetBot">
<img src="https://img.shields.io/github/repo-size/sanjit-sinha/Tg-UsenetBot">
<img src="https://img.shields.io/badge/License-MIT-green.svg">
<img src="https://www.repostatus.org/badges/latest/active.svg">
</p>
<br>

Telegram UsenetBot is a bot that provides an easy and convenient way to track the progress of your Usenet downloads using Sabnzbd API and can also search in Indexers using Nzbhydra APIs. With Telegram UsenetBot, you can receive your downloads' progress and post processing updates  directly on your Telegram chat. 

<br>

| ![](https://te.legra.ph/file/5b001d5e030e35b2fb637.png) | ![](https://te.legra.ph/file/383068b3409d164167591.png)|
|--------------------------------------------------------|--------------------------------------------------------|

_____

> **Note** Bot is in BETA currently. Better and detailed readme will be added later.
> Join [Testing Group](https://t.me/+auLVb3tIJp8yOTU1) to test and help into identify more Bugs.
> ( Group is not open for everyone, please only join if you have prior knowledge of using Usenet.)

_____

<div align="center">
<img src="https://graph.org/file/e00d2950b79aa9ea994ac.png" width="40"> <b><a href="https://www.reddit.com/r/usenet">r/usenet<a> • <a href="https://www.reddit.com/r/sabnzbd">r/sabnzbd</a> • <a href="https://www.reddit.com/r/nzbhydra/">r/nzbhydra</a></b>
</div>
<br>
 
**More about Usenet : [IITK Article](http://www.iitk.ac.in/LDP/HOWTO/Usenet-News-HOWTO/x27.html) • [Basic Guide](https://graph.org/EVERYTHING-YOU-NEED-TO-KNOW-ABOUT-USENET-09-04) • [Usenet Reddit wiki](https://www.reddit.com/r/usenet/wiki/index/)**

***Note: This bot doesn't download any NZB files or content. It simply interacts with various APIs such as Sabnzbd and NZBHydra to display progress and allow user to control them via Telegram.***

____

<div align="center">
<h2><b> Bot Commands and Usage</b></h2>
</div>

- `/status` - To see progress status with live update.
- `/stats` - Get  detail stats of Bot server.
- `/pause` - Pause the given Taskid task.
- `/resume` - Resume the given Taskid task.
- `/cancel` - Delete the given Taskid task.
- `/nzbmirror` - Reply to a .nzb file to add it in sabnzbd.
- `/nzbgrab` or `/nzbadd` - Add multiple IDs which we get from search.
- `/resumeall` `/pauseall` `/cancelall` (sudo commands)

searching stuff -

- `/nzbfind`- Search your query.
- `/movie` - Movie name / IMDB ID / IMDB link.
- `/series` - Series Name / IMDB ID / IMDB link.
- `/indexers` - List all your indexers. (sudo command)

 ( Few more commands `/start` `/help` `/ping` `/update` `/logs` )
 
____
 
<div align="center">
<h2><b>Screenshots</b></h2>
</div>

![](https://te.legra.ph/file/9316fc0e3e6d8da8a066c.jpg) | ![](https://te.legra.ph/file/40ffe2791139e7bcbea03.jpg) | ![](https://te.legra.ph/file/b2f025ce4a5967dd29168.jpg) |
|----------------------------------------------------------|----------------------------------------------------------|----------------------------------------------------------|
![](https://te.legra.ph/file/7bffbfd8db669065b6252.jpg) | ![](https://te.legra.ph/file/503f8220837b56b133f52.jpg) | ![](https://te.legra.ph/file/4cf86a41b96c8d04e0708.jpg) |

_____
 
<div align="center">
<h2><b>Deployment</b></h2>
</div>

 
<b><img src="https://graph.org/file/b077fae73ac7b1e487069.png" width="30"> SABNzbd post-processing script that automatically uploads completed download files to Google Drive and sends Telegram notifications once the file has been successfully uploaded with the drive link : https://github.com/sanjit-sinha/Tg-UsenetBot/blob/main/TelegramBot/usenetbot/postproc.py (edit according to your need)

**[Sabnzbd installation](https://sabnzbd.org/wiki/installation/install-ubuntu-repo) ( Install it as a service to use rclone ) • [NZBHydra Installation](https://hotio.dev/containers/nzbhydra2/)**

Sabnzbd Settings - 
 
`settings -> switches -> post-processing -> Untick Post-Process Only Verified Jobs `
<br>
`settings -> switches -> post-processing -> Tick Deobfuscate final filenames`
<br>
`settings -> sorting ->  Enable sortings [ Movie: %title (%y)/%fn.%ext   series: %sn/Season %s/%fn.%ext ]`
<br> 
 
Docker Installation of Usenet Bot

```
git clone https://github.com/sanjit-sinha/Tg-UsenetBot
cd Tg-UsenetBot
```

Now edit and fill all the config vars by typing `nano config.env` and save it by pressing <kbd>ctrl</kbd>+<kbd>o</kbd> and to exit press <kbd>ctrl</kbd>+<kbd>x</kbd>.

Running Bot in docker container 
```
sudo docker build . -t usenetbot 
sudo docker run usenetbot 
```
</b>
<br>

-----
 
<h2 align="center"><b>Credits and Contibution</b></h2>
<img src="https://telegra.ph/file/b26313d73e4d05de84a85.png" align="right" width="150">

<br>

Based on : https://github.com/sanjit-sinha/TelegramBot-Boilerplate

<a href="https://t.me/abhieshekk"><strong>Abhishek</strong></a> and <a href="https://t.me/Mohitjoshi155"><strong>Mohitjoshi</strong></a> for helping out with usenet stuff.
 
Any kind of feedback, bug reports, or contributions is greatly appreciated! :)
 
------


<h2 align="center"><b>Copyright and License</b></h2>
</div>
<br>
  
* copyright (C) 2023 by [Sanjit sinha](https://github.com/sanjit-sinha)
* Licensed under the terms of the [The MIT License](https://github.com/sanjit-sinha/Tg-UsenetBot/blob/main/LICENSE)

-------
