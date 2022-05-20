# Automated Mining Performance Dashboard
The Automated Mining Performance Dashboard tool can be used to store and display real-time performance and status information for multiple popular cryptocurrency miners, mining pools, and mining software. The dashboard is accessible from any device (even non-local to the mining operation) via a personal URL.

The program is written in Python and requires an Anvil account in order to utilize the dashboarding features.

# Features
*	Automated real-time mining performance tracking
*	Web-based dashboarding
*	Real-time mining status alerts
*	Ability to track multiple coins, pools, and mining software
*	Automatic cryptocurrency price trending

# Accessible Data
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

## Requirements
* Windows 10* with Python 3 installed on a host computer
* An Anvil account
* Stable internet connection on the host computer

* In order to access the NBMiner statistics, the computer running this program must be the same computer that is running the POW miners.

## Setup
The program is packaged in two parts:
1. A “server” module that runs in a windows environment. This module connects to the desired API’s, captures and pushes the data to the “dashboarding” module, and sends status alerts.
2. A “dashboarding” module that runs within as an Anvil dashboard.

## Dashboard Module Setup
1. Download the DashboardModule.zip file from the github repository
   - Using Git Bash:
     - In Windows Explorer, navigate to the folder in which you want to store your project files
     - Right-click and select "Git Bash here"
     - Run the following command: `git clone https://github.com/sameleff/Automated-Mining-Performance-Dashboard.git`
       NOTE: This command will download all files associated with this project, not just those associated with the dashboard module
   - Using GitHub:
     - Navigate to the [releases](https://github.com/sameleff/Automated-Mining-Performance-Dashboard/releases) page
     - Download the DashboardModule.zip file
     - Extract the contents into the folder in which you want to store your project files
2. Create an Anvil account
   - Navigate to the [Anvil](https://anvil.works/login) webpage
   - Create a new account or login to your existing one
   - Navigate to the "My Apps" page (it is located in the top toolbar)
   - Under the large "Create App" button, click the "Import from file link"
   - Navigate to the folder where you saved the project files and import the anvil.yaml file stored at \Live_Crypto_Dashboard\anvil.yaml

## Dashboard Module Configuration
1. Navigate to the ***Data Tables*** service
2. Select the **Active_Miners** table
3. Next to each miner that you want to monitor:
   - Enter a "Yes" in the *Active* column
   - Enter your public wallet receive address in the *Wallet* column
   - Enter a "Yes" in the *Send Alerts*
   - See the Non-Standard Miner Configuration section for all non-POW miners
4. Select the **Email_Notify** table
5. Enter your email address in the fields for both *Send Address* and *Receive Address*
6. Enter your email account password in the *Password* field
NOTE: Most modern email providers allow you to configure app passwords to enable programatic access to your email account. App passwords are recommended in order to protect your main account password.
   Here are several links for instructions to create app passwords for the three major email providers:
   - [Google (Gmail)](https://support.google.com/accounts/answer/185833?hl=en)
   - [Microsoft (Outlook)](https://support.microsoft.com/en-us/account-billing/manage-app-passwords-for-two-step-verification-d6dc8c6d-4bf7-4851-ad95-6d07799387e9)
   - [Yahoo](https://my.help.yahoo.com/kb/account/generate-third-party-passwords-sln15241.html)
7. Enter your SMTP Server and Port number. These vary by provider. Here are the values for the same 3 popular email providers:

| Provider| Server | SSL Port | TLS Port |
| ------- | ------ | -------- | -------- |
| Google/Gmail | smtp.gmail.com | 465 | 587 |
| Microsoft/Outlook | smtp-mail.outlook.com | 465 | 587|
| Yahoo | smtp.mail.yahoo.com | 465 | 587 |

The TLS port is recommended.

8. Open the project settings page (click the gear icon in the left pane) and select "Uplink..."
9. Click the "Server Code" toggle button, and write down the uplink key
10. Open the project setting page (click the gear icon in the left pane) and select "Share app..."
11. Write down or copy the URL for the private URL link

### Non-Standard Miner Configuration
#### Helium Miners
Enter the name of your hotspot in the *Name* column

#### PlanetWatch Miners
Your wallet address must match the address used to connect your device to the Algorand blockchain. This address needs to register transactions when PlanetWatch sends mining rewards.

#### Chia Miners
##### SpacePool
1. Open your pool login link in a webpage
   - You can find your login link by following [these](https://github.com/Chia-Network/chia-blockchain/wiki/Pooling-User-Guide) instructions from Chia
2. In the Account Settings popup:
   - In the Account Alias field, name your account.
   - Click "Request API Key" under the Developer API Key section and complete the process. This program queries data every 30 minutes, but SpacePool only asks so they can estimate the API request load on their servers.
3. Enter your developer key in the *Wallet* field
4. Enter your Account Alias in the *Name* field

#### NBMiner
In the GPUSTATS, NBMiner row:
1. Enter the IP address for your web monitor in the *Wallet* field
2. Enter the port number for your web monitor in the *Name* field

If you don't know already, you can find the URL & port of your web monitor by:
1. Navigating to the folder where you installed NBMiner
2. Double-clicking the "open_web_monitor.url" file
3. This will open a webpage of format: `http://<your IP>:<your port>`

## Server Module Setup & Configuration
1. Ensure Python 3 is installed on the host computer
2. Download the ServerModule.zip file from the github repository
   - Using Git Bash:
     - In Windows Explorer, navigate to the folder in which you want to store and run the server module
     - Right-click and select "Git Bash here"
     - Run the following command: `git clone https://github.com/sameleff/Automated-Mining-Performance-Dashboard.git`
        NOTE: This command will download all files associated with this project, not just those associated with the server module
   - Using GitHub:
     - Navigate to the [releases](https://github.com/sameleff/Automated-Mining-Performance-Dashboard/releases) page
     - Download the ServerModule.zip file
     - Extract the contents into the folder in which you want to store and run the server module
3. Open a Windows Terminal window and run the following command within your Python environment to ensure the required packages are properly installed: `pip install -r requirements.txt`
4. Open the ***Crypto-Dashboard-Server.py*** code in your editor of choice
5. Scroll to the bottom until you see the line that begins with `anvil.server.connect`
6. Paste the uplink key that you copied from the Anvil project in double quotes in the location shown
   e.g. the line should look like this: `anvil.server.connect("<your uplink key>")`
7. Configure the dashboard update frequency by changing the value of the variable `tdelta`. Values are in units of minutes. The recommended (and defaul) interval is 30 minutes. Some API sources do not support high frequency queries, and longer intervals will result in longer delays between status updates. 

# Running the Program
1. Run the ServerModule.py program in Windows Terminal
2. It should print the following text to the Terminal window:
   Connecting to wss://anvil.works/uplink
   Anvil websocket open
   Connected to "Default environment" as SERVER
3. Once the server program is operational, you can access the dashboard from any device that can access the web using the private URL link from the Anvil project

# Server Usage
The Terminal window running the server must remain open in order to maintain the link between the server and the dashboard.
In order to quit the server program press `ctrl + c` within the Terminal window and then type `Y` and `Enter`

# Dashboard Usage
The dashboard automatically generates 4 pages that summarize different aspects of the performance history. The user can select the page using the menu pane on the left side of the screen. The last option within this menu is titled **UPDATE DATA**. Selecting this option will send a command to the server code to perform an unscheduled data update. The current dashboard page will automatically refresh once the update is completed. Future scheduled updates will still proceed as normal.

The dashboard automatically refreshes the current webpage every 1 minute in order to ensure that it does not go to sleep. 

## Today Page
This page displays current data (using only data from the last update). It summarizes daily earnings for each miner as well as the current status of the miners as well as their respective API's. Whenever a miner or API goes offline, it will be highlighted in red font and bolded.

![Today Page](https://github.com/sameleff/Automated-Mining-Performance-Dashboard/blob/main/ReadmeFiles/Today-Page.PNG)

## Mining History Page
This page displays a time-series chart that trends the mining reward (in units of each coin) as well as the miner status. The user can select which miner to trend via the dropdown menu in the upper right hand corner of the screen.

![Mining History Page](https://github.com/sameleff/Automated-Mining-Performance-Dashboard/blob/main/ReadmeFiles/Mining-History-Page.PNG)

## Price History Page
This page displays a time-series chart that trends the price history of each coin that the server code is tracking. The user can choose to display all coins or any subset of them by deselecting them from the chart legend or by using the dropdown menu in the upper right hand corner of the screen.

![Price History Page](https://github.com/sameleff/Automated-Mining-Performance-Dashboard/blob/main/ReadmeFiles/Price-History-Page.PNG)

## GPU Health Page
This page displays a time-series chart that trends several critical performance criteria for GPU miners. The user can select which GPU to display (for those with multi-GPU rigs) as well as two data fields using the dropdown menus in the upper right hand corner of the screen. The available data that can be displayed is:
* Hashrate in MH/s
* Power in W
* Temperature in C
* Efficiency in H/s per W

![GPU Health Page](https://github.com/sameleff/Automated-Mining-Performance-Dashboard/blob/main/ReadmeFiles/GPU-Health-Page.PNG)
