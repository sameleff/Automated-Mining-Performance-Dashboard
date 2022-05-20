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
     1. In Windows Explorer, navigate to the folder in which you want to store your project files
     2. Right-click and select "Git Bash here"
     3. Run the following command: `git clone https://github.com/sameleff/Automated-Mining-Performance-Dashboard.git`
        NOTE: This command will download all files associated with this project, not just those associated with the dashboard module
   - Using GitHub:
     1. Navigate to the [releases](https://github.com/sameleff/Automated-Mining-Performance-Dashboard/releases) page:
     2. Download the DashboardModule.zip file
     3. Extract the contents into the folder in which you want to store your project files
2. Create an Anvil account
   - Navigate to the [Anvil](https://anvil.works/login) webpage
   - Create a new account or login to your existing one
   - Navigate to the "My Apps" page (it is located in the top toolbar)
   - Under the large "Create App" button, click the "Import from file link"
   - Import the Live-Crypto-Dashboard (??) file

## Dashboard Module Configuration
1. Navigate to the ***Data Tables*** service
2. Select the **Active_Miners** table
3. Next to each miner that you want to monitor:
   a. Enter a "Yes" in the *Active* column
   b. Enter your public wallet receive address in the *Wallet* column
   c. Enter a "Yes" in the *Send Alerts*
   d. See the Non-Standard Miner Configuration section for all non-POW miners
4. Select the **Email_Notify** table
5. Enter your email address in the fields for both *Send Address* and *Receive Address*
6. Enter your email account password in the *Password* field
   NOTE: Most modern email providers allow you to configure app passwords to enable programatic access to your email account. App passwords are recommended in order to protect your main account password.
   Here are several links for instructions to create app passwords for the three major email providers:
   a. [Google (Gmail)](https://support.google.com/accounts/answer/185833?hl=en)
   b. [Microsoft (Outlook)](https://support.microsoft.com/en-us/account-billing/manage-app-passwords-for-two-step-verification-d6dc8c6d-4bf7-4851-ad95-6d07799387e9)
   c. [Yahoo](https://my.help.yahoo.com/kb/account/generate-third-party-passwords-sln15241.html)
7. Enter your SMTP Server and Port number. These vary by provider. Here are the values for the same 3 popular email providers:

| Provider| Server | SSL Port | TLS Port |
| ------- | ------ | -------- | -------- |
| Google/Gmail | smtp.gmail.com | 465 | 587 |
| Microsoft/Outlook | smtp-mail.outlook.com | 465 | 587|
| Yahoo | smtp.mail.yahoo.com | 465 | 587 |
The TLS port is recommended.

### Non-Standard Miner Configuration
#### Helium Miners
Enter the name of your hotspot in the *Name* column

#### PlanetWatch Miners
Your wallet address must match the address used to connect your device to the Algorand blockchain. This address needs to register transactions when PlanetWatch sends mining rewards.

#### Chia Miners
##### Spacepool
1. Open your pool login link in a webpage
   a. You can find your login link by following [these](https://github.com/Chia-Network/chia-blockchain/wiki/Pooling-User-Guide) instructions from Chia
2. In the Account Settings popup:
   a. In the Account Alias field, name your account.
   b. Click "Request API Key" under the Developer API Key section and complete the process. This program queries data every 30 minutes, but SpacePool only asks so they can estimate the API request load on their servers.
3. Enter your developer key in the *Wallet* field
4. Enter your Account Alias in the *Name* field

#### NBMiner
In the GPUSTATS, NBMiner row:
1. Enter the IP address for your web monitor in the *Wallet* field
2. Enter the port number for your web monitor in the *Name* field

If you don't know already, you can find the URL & port of your web monitor by:
1. Navigating to the folder where you installed NBMiner
2. Double-clicking the "open_web_monitor.url" file
3. This will open a webpage of format: http://<your IP>:<your port>

## Server Module Setup & Configuration
1. Ensure Python 3 is installed on the host computer
2. Download the ServerModule.zip file from the github repository
   - Using Git Bash:
     1. In Windows Explorer, navigate to the folder in which you want to store and run the server module
     2. Right-click and select "Git Bash here"
     3. Run the following command: `git clone https://github.com/sameleff/Automated-Mining-Performance-Dashboard.git`
        NOTE: This command will download all files associated with this project, not just those associated with the server module
   - Using GitHub:
     1. Navigate to the [releases](https://github.com/sameleff/Automated-Mining-Performance-Dashboard/releases) page:
     2. Download the ServerModule.zip file
     3. Extract the contents into the folder in which you want to store and run the server module
3. Open a Windows Terminal window and run the following command within your Python environment to ensure the required packages are properly installed: `pip install -r requirements.txt`
4. 

