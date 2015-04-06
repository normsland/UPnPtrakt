# UPnPtrakt

Monitors an UPnP device, logs changes into a database and scrobbles new episodes to [trakt.tv](http://trakt.tv) using trakt API v2.0.

UPnP devices are mounted into the file system (by means of [`djmount`](http://djmount.sourceforge.net/), the content of the »Last Viewed« folder is checked against entries of a database. If new episodes are detected, they are added to the database and scrobbled to trakt.tv.

Made for OS X and Linux.
## TL;DR
Install needed stuff (see **Prerequisites**), run `./getKey.py` put your trakt.tv credentials in, watch something new and run

```shell
./upnptrakt.py
```

## Features
UPnPtrakt tracks your last viewed shows as indicated by your UPnP/DLNA devices. It parses the show, retrieves proper (meta) data from trakt.tv and fills up a database. New shows are scrobbled to trakt.tv.

`upnptrakt.py` has quite a few features accessable while calling, just check `./upnptrakt.py --help`.
## Prerequisites
There's some stuff which has to be on your system in order for UPnPtrakt to work.
### Program: djmount
As I was unable to find a Python package for monitoring UPnP devices, UPnPtrakt relies on [djmount](http://djmount.sourceforge.net/) to interface between the current host and all UPnP/DLNA devices in your network.

`djmount` is both available in Homebrew and Ubuntu/Debian's packages repository. To install, either run (OS X)

```shell
brew install djmount
```
or (Ubuntu/Debian)

```shell
sudo apt-get install djmount
```
If your Linux flavor is not Ubuntu or Debian, there's probably a package for djmount around for your distro as well. If you're running Windows, I don't know (neither about `djmount` nor about this stuff here running at all.)

### Python Packages
This Python program uses quite a few packages including moogar0880's great [PyTrakt] (https://github.com/moogar0880/PyTrakt/) which is included in this repo. All of them can be installed via [pip](http://www.pip-installer.org/):

```shell
pip install guessit psutil simplejson requests requests-oauthlib 
```

## Setup
Use `createLocalDb.py` to create the necessary SQLite3 database. Use `--dropDB` to drop the database before recreating it.

Use `getKey.py` to create your trakt api OAuth token needed to scrobble to trakt. Simply run `./getKey.py` then follow the on screen instructions. Eg. fill in your trakt.tv username, copy and post paste authorization url in to a web browser. Copy the OAuth Authorization Code from trakt.tv then paste in to command window. `getKey.py` will then create `trakt-config.json` in the upnptrakt directory with your UPnPtrakt api_key. 

Manually test mounting UPnP devices by calling
```shell
mkdir test
djmount test
ls -l test
umount test; rm -rf test
```
If you get an error you might need to load the FUSE kernel module first: `modprobe fuse`)
## Usage
Calling `upnptrakt.py -h` should be pretty much self-explanatory. The default values are tuned for my personal case, you might need to customize them in the call to the script. Especially the `--path-to-last-viewed` is probably different for your UPnP/DLNA server (or not, if you're running Serviio on a host named Andisk2…).

Let's get through the parameters, sorted by importance (and then through the flags):

* **--path-to-last-viewed _PATH_**: The path to the *last viewed* folder of your UPnP/DLNA server. You probably need to find this out by running a manual `djmount` (see **Setup**). Don't care too much about trailing / ending slashes. This should be taken care of automatically.  
*Default*: `Serviio (SERVERNAME)/Video/Last Viewed`. 
* **--trakt-config-json _FILE_**: Filename of the json config used to login to trakt.tv. See **Setup**.  
*Default*: `trakt-config.json`
* **--series-mismatched-json _FILE_**: Sometimes the trakt.tv search is unable to find the current show. Put this in to mismatched then. Please see the `seriesMismatched.json` for an example.  
*Default*: `seriesMismatched.json`
* **--database-file _FILE_**: SQLite3 database filename to store all episode information in.  
*Default*: `episodes.db`
* **--mount-path _PATH_**: Location, where `djmount` will mount the UPnP network surroundings in.  
*Default*: `.upnpDevices` (yes, it's hidden)

Flags provided (all off by default):

* **--dont-store**: Don't store information about new shows into the database. Becomes a *dry run* when used in combination with --dont-post.
* **--dont-post**: Don't post new episodes to trakt.tv. Only use the database. You might want to use this to initially fill up the database. Becomes a *dry run* when used together with --dont-store.
* **--restart-djmount**: In case of troubles with `djmount`, this flag gets rid of all `djmount` process, unmounts the mount path (as provided by `--mount-path`) and deletes the folder. *Attention:* ALL `djmount` processes are killed! If you have some other folders in your system mounted with the tool, you might get some funny behavior there.

After setting up all needed tools, creating and the initial populating of your database, you probably want to create a cronjob calling `upnptrakt.py` every so often.

## Limits & Todos
* At the moment the load to trakt.tv is quite high, as every episode's proper data is retrieved from there. Resulting in a slow script. This is going to be changed soon. Hopefully.
* No error handling whatsoever is included. No logging either.
* No documentation in the files.
* If you use Serviio and like this script please add a comment/vote +1 on the [Serviio issue - trakt.tv support] (https://bitbucket.org/xnejp03/serviio/issue/594/trakttv-support) and [Serviio forums - trakt.tv] (http://forum.serviio.org/viewtopic.php?f=3&t=7996) to get trakt.tv functionality included in Serviio. I don't really think I will be improving on this beyond getting it all to work with trakt API 2.0. 

Thanks to [AndiH] (https://github.com/AndiH) for the [original script] (https://github.com/AndiH/UPnPtrakt) of which this is based and moogar0880 for [pytrakt] (https://github.com/moogar0880/PyTrakt/)