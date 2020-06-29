# ReconTarget

[![Build Status](https://travis-ci.com/relarizky/ReconTarget.svg?branch=master)](https://relarizky/ReconTarget)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/relarizky/ReconTarget)
![GitHub repo size](https://img.shields.io/github/repo-size/relarizky/ReconTarget)
![GitHub last commit](https://img.shields.io/github/last-commit/relarizky/ReconTarget)
![GitHub stars](https://img.shields.io/github/stars/relarizky/ReconTarget)
![tested os](https://img.shields.io/badge/Tested%20on-ubuntu%2019.10-critical)

> Web Based Reconnaisance Tool Built With __Flask__

***ReconTarget*** is web based reconnaisance tool that can help you to do `reconnaisance` and `manage your target` in your local machine. 
This tool is integrated with database so you dont need to store your target list in a file. 
This tool is also can be used by multiple user with different privilege (inspired by [Nessus](https://docs.tenable.com/nessus/Content/GettingStarted.htm)).

<img src='https://raw.githubusercontent.com/relarizky/ReconTarget/master/screenshot/1.png' width=30% height=25%> <img src='https://raw.githubusercontent.com/relarizky/ReconTarget/master/screenshot/2.png' width=30% height=25%> <img src='https://raw.githubusercontent.com/relarizky/ReconTarget/master/screenshot/3.png' width=30% height=25%>

<img src='https://raw.githubusercontent.com/relarizky/ReconTarget/master/screenshot/4.png' width=30% height=25%> <img src='https://raw.githubusercontent.com/relarizky/ReconTarget/master/screenshot/5.png' width=30% height=25%> <img src='https://raw.githubusercontent.com/relarizky/ReconTarget/master/screenshot/6.png' width=30% height=25%>

## Instalation

first of all, you need to create one database before installing this tool, you can do that by typing

```
sudo mysql -u <your mysql user> -p -e 'CREATE DATABASE <name for db you'd like to create>

ex : sudo mysql -u root -p -e 'CREATE DATABASE recon_target'
```

Then, you can install this web app by typing these following

```
$ git clone https://github.com/relarizky/ReconTarget.git
$ cd ReconTarget
$ pip3 install -r requirements.txt
$ chmod +x install.py
$ ./install.py
```

## Usage

after installation, you can now access this web app in http://127.0.0.1:5000 by typing this command

```
$ python3 run.py
```

and then, you can log in to web app with these 2 default users

1. sayang:sayang123
2. hekmen:hekmen123

you can change or add new user for security reason

## Feature

- Multiple user with different role

- Manage user (add, edit, update, delete)

- Auto Update

- Reverse IP (bing, hackertarget, yougetsignal)

- DNS Lookup

- Whois (whois.com, hackertarget)

- Link Scrapper (manual, hackertarget)

- Wordpress User Finder
