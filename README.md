# Automated Mining Performance Dashboard
The Automated Mining Performance Dashboard tool can be used to store and display real-time performance and status information for multiple popular cryptocurrency miners, mining pools, and mining software. The dashboard is accessible from any device (even non-local to the mining operation) via a personal URL.

The program is written in Python and requires an Anvil account in order to utilize the dashboarding features.

# Features:
*	Automated real-time mining performance tracking
*	Web-based dashboarding
*	Real-time mining status alerts
*	Ability to track multiple coins, pools, and mining software
*	Automatic cryptocurrency price trending

# Accessible Data:
This program can currently access data from the following sources:
| Mining Pool / API | Coin |
| ----------------- | ---- |
| Ethermine	| Ethereum (ETH)|
| Nanopool	| Ethereum (ETH)|
|	Nanopool	| Ergo (ERG)|
| MoneroOcean	| Monero (XMR)|
| SpacePool	| Chia (XCH)|
| Helium Explorer	| Helium (HNT)|
| AlgoExplorer	| PlanetWatch (PLANETS)|

Although multiple options for GPU mining software are available, this program is currently only able to access the status information for NBMiner. Future updates plan to enable access to other major GPU mining software (such as T-Rex, Nanominer, etc.).

# Installation
This section describes the system requirements as well as the steps required to configure and use this tool.

## Requirements:
* Windows 10* with Python 3 installed on a host computer
* An Anvil account
* Stable internet connection on the host computer

* In order to access the NBMiner statistics, the computer running this program must be the same computer that is running the POW miners.

## Setup:
The program is packaged in two parts:
1. A “server” module that runs in a windows environment. This module connects to the desired API’s, captures and pushes the data to the “dashboarding” module, and sends status alerts.
2. A “dashboarding” module that runs within as an Anvil dashboard.

## Server Module Setup & Configuration:
1. Download the ServerModule.zip file from the github repository
   a. Using Git Bash:
      1. Navigate to the folder in which you want to store the server module
      2. Right-click and select "Git Bash here"
      3. Run the following command: '''git clone  https://github.com/sameleff/Automated-Mining-Performance-Dashboard.git'''
2. Ensure Python 3 is installed on the host computer

