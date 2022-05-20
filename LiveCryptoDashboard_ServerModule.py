# Anvil Server Live Crypto Dashboard
# # This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.

#Importing Libraries
import requests
import pytz
import datetime
from datetime import datetime, timedelta
import anvil.tables as tables
from anvil.tables import app_tables
import anvil.server
import time
from time import sleep
import anvil.mpl_util
import plotly.graph_objects as go
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

## Defining Master Function
@anvil.server.callable
def GetHourlyData(flag, tdelta):
    ## Setting global variables
    #  Current Time
    tz = pytz.timezone('UTC')
    Current_Time = datetime.now().isoformat()
    Last_Active = (datetime.utcnow() - timedelta(minutes=tdelta)).isoformat()
    #Last_Active = parser.parse(Current_Time).isoformat()
    
    #  Opening JSON Config File
    configs = app_tables.active_miners
    
    ## Defining Tables
    HNT_Helium_Data = app_tables.hnt_helium
    ETH_Ethermine_Data = app_tables.eth_ethermine
    ERG_Nanopool_Data = app_tables.erg_nanopool
    PLANETS_AlgoExplorer_Data = app_tables.planets_algoexplorer
    XCH_SpacePool_Data = app_tables.xch_spacepool
    XMR_MoneroOcean_Data = app_tables.xmr_moneroocean
    ETH_Nanopool_GRP_Data = app_tables.eth_nanopool_grp
    XMR_MoneroOcean_GRP_Data = app_tables.xmr_moneroocean_grp
    GPU_Health_Data = app_tables.gpu_health
    Prices = app_tables.prices

    ## Getting Price Data
    [ERG_USD, ETH_USD, HNT_USD, PLANETS_USD, XCH_USD, XMR_USD, API_Error] = GetPrices()
    Prices.add_row(Time=datetime.fromisoformat(Current_Time), ERG=round(ERG_USD,2), ETH=round(ETH_USD,2), HNT=round(HNT_USD,2), PLANETS=round(PLANETS_USD,3), XCH=round(XCH_USD,2), XMR=round(XMR_USD,2), API_Error=API_Error)
    
    ## Getting Data for All Active Miners
    for row in configs.search():
        # Testing if miner is active
        if row['Active'] == "Yes":
            if row['Coin']+"-"+row['MiningPool/API'] == "HNT-Helium":
                [Price, Status, Rewards, Earnings, API_Error] = GetHeliumData(row['Wallet'],row['Name'], HNT_USD, Last_Active, tz)
                HNT_Helium_Data.add_row(Time=datetime.fromisoformat(Current_Time), Price=round(Price, 2), Status=Status, Rewards=round(Rewards, 6), Earnings=round(Earnings, 2), API_Error=API_Error)

                # Sending Offline Miner Email
                SendEmail(row, Status, HNT_Helium_Data)

            if row['Coin']+"-"+row['MiningPool/API'] == "ETH-Ethermine":
                [Price, Status, Rewards, Earnings, API_Error] = GetEthermineData(row['Wallet'], ETH_USD, Last_Active, tz)
                ETH_Ethermine_Data.add_row(Time=datetime.fromisoformat(Current_Time), Price=round(Price, 2), Status=Status, Rewards=round(Rewards, 6), Earnings=round(Earnings, 2), API_Error=API_Error)

                # Creating flag to turn off nbminer
                if Status == 0:
                    GPUflag = 0
                else:
                    GPUflag = 1

                # Sending Offline Miner Email
                SendEmail(row, Status, ETH_Ethermine_Data)
            
            if row['Coin']+"-"+row['MiningPool/API'] == "ERG-Nanopool":
                [Price, Status, Rewards, Earnings, API_Error] = GetERGNanopoolData(row['Wallet'], ERG_USD, Last_Active, tz)
                ERG_Nanopool_Data.add_row(Time=datetime.fromisoformat(Current_Time), Price=round(Price, 2), Status=Status, Rewards=round(Rewards, 6), Earnings=round(Earnings, 2), API_Error=API_Error)

                # Creating flag to turn off nbminer
                if Status == 0:
                    GPUflag = 0
                else:
                    GPUflag = 1

                # Sending Offline Miner Email
                SendEmail(row, Status, ERG_Nanopool_Data)

            if row['Coin']+"-"+row['MiningPool/API'] == "PLANETS-AlgoExplorer":
                [Price, Status, Rewards, Earnings, API_Error] = GetAlgoExplorerData(row['Wallet'], PLANETS_USD, tz)

                if API_Error == "Yes":
                    PLANETS_AlgoExplorer_Data.add_row(Time=datetime.fromisoformat(Current_Time), Price=round(Price, 2), Status=Status, Rewards=Rewards, Earnings=Earnings, API_Error=API_Error)
                else:
                    if len(Rewards) != 0:
                        PLANETS_AlgoExplorer_Data.add_row(Time=datetime.fromisoformat(Current_Time), Price=round(Price, 2), Status=Status, Rewards=round(Rewards[0], 6), Earnings=round(Earnings[0], 2), API_Error=API_Error)
                    else:
                        last_row = PLANETS_AlgoExplorer_Data.search(tables.order_by('Time',False))[0]
                        PLANETS_AlgoExplorer_Data.add_row(Time=datetime.fromisoformat(Current_Time), Price=last_row['Price'], Status=Status, Rewards=last_row['Rewards'], Earnings=last_row['Earnings'], API_Error=API_Error)
                
                # Sending Offline Miner Email
                SendEmail(row, Status, PLANETS_AlgoExplorer_Data)

            if row['Coin']+"-"+row['MiningPool/API'] == "XCH-SpacePool":
                [Price, Status, Rewards, Earnings, API_Error] = GetSpacePoolData(row['Wallet'], row['Name'], XCH_USD, Last_Active, tz)
                XCH_SpacePool_Data.add_row(Time=datetime.fromisoformat(Current_Time), Price=round(Price, 2), Status=Status, Rewards=round(Rewards, 6), Earnings=round(Earnings, 2), API_Error=API_Error)

                # Sending Offline Miner Email
                SendEmail(row, Status, XCH_SpacePool_Data)

            if row['Coin']+"-"+row['MiningPool/API'] == "XMR-MoneroOcean":
                [Price, Status, Rewards, Earnings, API_Error] = GetMoneroOceanData(row['Wallet'], XMR_USD, Last_Active, tz)
                XMR_MoneroOcean_Data.add_row(Time=datetime.fromisoformat(Current_Time), Price=round(Price, 2), Status=Status, Rewards=round(Rewards, 6), Earnings=round(Earnings, 2), API_Error=API_Error)

                # Sending Offline Miner Email
                SendEmail(row, Status, XMR_MoneroOcean_Data)

            if row['Coin']+"-"+row['MiningPool/API'] == "ETH-Nanopool (GRP)":
                [Price, Status, Rewards, Earnings, API_Error] = GetETHNanopoolGRPData(row['Wallet'], ETH_USD, Last_Active, tz)
                ETH_Nanopool_GRP_Data.add_row(Time=datetime.fromisoformat(Current_Time), Price=round(Price, 2), Status=Status, Rewards=round(Rewards, 6), Earnings=round(Earnings, 2), API_Error=API_Error)

                # Sending Offline Miner Email
                SendEmail(row, Status, ETH_Nanopool_GRP_Data)

            if row['Coin']+"-"+row['MiningPool/API'] == "XMR-MoneroOcean (GRP)":
                [Price, Status, Rewards, Earnings, API_Error] = GetMoneroOceanData(row['Wallet'], XMR_USD, Last_Active, tz)
                XMR_MoneroOcean_GRP_Data.add_row(Time=datetime.fromisoformat(Current_Time), Price=round(Price, 2), Status=Status, Rewards=round(Rewards, 6), Earnings=round(Earnings, 2), API_Error=API_Error)
                
                # Sending Offline Miner Email
                SendEmail(row, Status, XMR_MoneroOcean_GRP_Data)
                    
            if row['Coin']+"-"+row['MiningPool/API'] == "GPUSTATS-NBMiner":
                if GPUflag == 1:
                    GetGPUStats(row['Wallet'],row['Name'], GPU_Health_Data, Current_Time)
    if flag == 1:
        app_tables.countdown.search()[0]['Last_Update'] = datetime.now()
        print("{} EST  |  Updated at: {} EST. Unscheduled update requested by dashboard user.\r".format(datetime.strftime(datetime.now(), "%m-%d-%y %I:%M %p"), datetime.strftime(datetime.now(), "%m-%d-%y %I:%M %p")))

def GetPrices():
    # Get CoinGecko Coin ID's Here
    # https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit#gid=0
    
    Count = 0

    # Getting ERG Price
    try:
        ID = "ergo"
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids="+ID+"&vs_currencies=USD")
        data = r.json()
        ERG_USD = data[ID]['usd']
        Count = Count + 1
    except:
        print("\n{}  |  ERROR: Ergo price Coingecko error.".format(datetime.strftime(datetime.now(), "%m-%d-%y %I:%M %p")))
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print("\n")
        ERG_USD = 0

    # Getting ETH Price
    try:
        ID = "ethereum"
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids="+ID+"&vs_currencies=USD")
        data = r.json()
        ETH_USD = data[ID]['usd']
        Count = Count + 1
    except:
        print("\n{}  |  ERROR: Ethereum price Coingecko error.".format(datetime.strftime(datetime.now(), "%m-%d-%y %I:%M %p")))
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print("\n")
        ETH_USD = 0
    
    # Getting HNT Price
    try:
        ID = "helium"
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids="+ID+"&vs_currencies=USD")
        data = r.json()
        HNT_USD = data[ID]['usd']
        Count = Count + 1
    except:
        print("\n{}  |  ERROR: Helium price Coingecko error.".format(datetime.strftime(datetime.now(), "%m-%d-%y %I:%M %p")))
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print("\n")
        HNT_USD = 0
    
    # Getting PLANETS Price
    try:
        ID = "planetwatch"
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids="+ID+"&vs_currencies=USD")
        data = r.json()
        PLANETS_USD = data[ID]['usd']
        Count = Count + 1
    except:
        print("\n{}  |  ERROR: Planetwatch price Coingecko error.".format(datetime.strftime(datetime.now(), "%m-%d-%y %I:%M %p")))
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print("\n")
        PLANETS_USD = 0
    
    # Getting XCH Price
    try:
        ID = "chia"
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids="+ID+"&vs_currencies=USD")
        data = r.json()
        XCH_USD = data[ID]['usd']
        Count = Count + 1
    except:
        print("\n{}  |  ERROR: Chia price Coingecko error.".format(datetime.strftime(datetime.now(), "%m-%d-%y %I:%M %p")))
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print("\n")
        XCH_USD = 0
    
    # Getting XMR Price
    try:
        ID = "monero"
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids="+ID+"&vs_currencies=USD")
        data = r.json()
        XMR_USD = data[ID]['usd']
        Count = Count + 1
    except:
        print("\n{}  |  ERROR: Monero price Coingecko error.".format(datetime.strftime(datetime.now(), "%m-%d-%y %I:%M %p")))
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print("\n")
        XMR_USD = 0
    
    if Count == 6:
        API_Error = "No"
    else:
        API_Error = "Yes"
    
    return(ERG_USD, ETH_USD, HNT_USD, PLANETS_USD, XCH_USD, XMR_USD, API_Error)

## Defining GPU Health Function
def GetGPUStats(apihost, port, GPU_Health_Data, Current_Time):
    try:
        r = requests.get("http://"+apihost+":"+port+"/api/v1/status")
        data = r.json()

        for i in range(len(data['miner']['devices'])):
            ID = data['miner']['devices'][i]['id']
            Hashrate = data['miner']['devices'][i]['hashrate_raw'] / 1000000
            Power = data['miner']['devices'][i]['power']
            Temp = data['miner']['devices'][i]['temperature']
            API_Error = "No"
            GPU_Health_Data.add_row(Time=datetime.fromisoformat(Current_Time), ID=ID, Hashrate_MH = round(Hashrate, 2), Power_W = round(Power, 1), Temp_C = round(Temp, 1), Efficiency = round(Hashrate*1000/Power,0), API_Error=API_Error)
    except:
        print("\n{}  |  NBMiner API error.".format(datetime.strftime(datetime.now(), "%m-%d-%y %I:%M %p")))
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print("\n")
        ID = 0
        Hashrate = 0
        Power = 0
        Temp = 0
        API_Error = "Yes"
        GPU_Health_Data.add_row(Time=datetime.fromisoformat(Current_Time), ID=ID, Hashrate_MH = round(Hashrate, 2), Power_W = round(Power, 1), Temp_C = round(Temp, 1), API_Error=API_Error)

## Defining Helium Miner Function
def GetHeliumData(HNTAcct, HNTName, HNT_USD, Last_Active, tz):
    ## LoRaWAN Miner Data
    #  Assumptions:
    #  1. HNT value given by API is 1/100000000 of HNT
    #  2. "Accounts" API call will automatically set the min_time and max_time parameters equal to now unless they are specified (see Time Delay)
    #  3. Helium rewards are calculated based on ACTUAL payments within the rolling search time frame (1 day)

    #Use the following three lines in order to track the number of active hotspots on the helium network
    #r = requests.get("https://api.helium.io/v1/stats")
    #data = r.json()
    #Hotspots = data['data']['counts']['hotspots']

    #  Time_Delay Format: "- value %20 interval"
    #  e.g. -1%20day will tell the code to include data from 1 day prior to now up to now
    #  e.g. -2%20week will tell the code to include data from 2 weeks prior to now up to now (notice that <week> is not plural) 
    Time_Delay = "-1%20day"

    try:
        r = requests.get("https://api.helium.io/v1/accounts/"+HNTAcct+"/rewards/sum?min_time="+Time_Delay)
        data = r.json()
        HNT_Rewards = data['data']['total']

        r = requests.get("https://api.helium.io/v1/hotspots/name/"+HNTName)
        data = r.json()
        HNT_Status = data['data'][0]['status']['online']
        if HNT_Status == 'online':
            HNT_Status = 1
        else:
            HNT_Status = 0

        HNT_Earned = HNT_USD * HNT_Rewards
        API_Error = "No"

    except:
        print("\n{}  |  ERROR: HNT-Helium API error.".format(datetime.strftime(datetime.now(), "%m-%d-%y %I:%M %p")))
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print("\n")
        HNT_Status = 0
        HNT_Rewards = 0
        HNT_Earned = 0
        API_Error = "Yes"

    return(HNT_USD, HNT_Status, HNT_Rewards, HNT_Earned, API_Error)

## Defining GPU (Ethermine) Miner Function
def GetEthermineData(ETHAcct, ETH_USD, Last_Active, tz):
    ## COMPLETE
    ## GPU Miner Data
    #  Assumptions:
    #  1. Miner pool destination is Ethermine
    #  2. Coin data is estimated by the API and given on a per minute basis
    #  3. Ethereum rewards are calculated based on the current hashrate and difficulty, and converted into an daily amount of ETH

    try:
        r = requests.get("https://api.ethermine.org/miner/"+ETHAcct+"/dashboard")
        data = r.json()
        ETH_Status = data['data']['statistics'][0]['activeWorkers']

        r = requests.get("https://api.ethermine.org/miner/"+ETHAcct+"/currentStats")
        data = r.json()
        ETH_Rewards = data['data']['coinsPerMin']*60*24
        ETH_Earned = ETH_USD * ETH_Rewards
        API_Error = "No"
    except:
        print("\n{}  |  ERROR: ETH-Ethermine API error.".format(datetime.strftime(datetime.now(), "%m-%d-%y %I:%M %p")))
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print("\n")
        ETH_Status = 0
        ETH_Rewards = 0
        ETH_Earned = 0
        API_Error = "Yes"

    return(ETH_USD, ETH_Status, ETH_Rewards, ETH_Earned, API_Error)

## Defining HDD (Chia) Miner Function
def GetSpacePoolData(XCHKey, XCHAcct, XCH_USD, Last_Active, tz):
    ## COMPLETE
    ## HDD Miner Data
    #  Assumptions:
    #  1. XCH rewards are estimated from the farm size vs. the netspace size and the block emission rate

    #  Daily_Blocks = the number of blocks that should release every day
    #  Block_Reward = the value (in XCH) released each block
    Daily_Blocks = 4608
    Block_Reward = 2

    try:
        headers = {"Developer-Key": XCHKey}
        r = requests.get("https://developer.pool.space/api/v1/farms/"+XCHAcct, headers=headers)
        data = r.json()
        Farm_Size = data['estimatedPlotSizeTiB']
        time.sleep(1)

        r = requests.get("https://developer.pool.space/api/v1/pool", headers=headers)
        data = r.json()
        Space_Size = data['totalNetSpaceTiB']
        Win_Chance = 1 - ( (1 - Farm_Size / Space_Size) ** Daily_Blocks)
        XCH_Rewards = Win_Chance * Block_Reward
        XCH_Earned = XCH_Rewards * XCH_USD
        time.sleep(1)

        r = requests.get("https://developer.pool.space/api/v1/farms/"+XCHAcct+"/partials",headers=headers)
        data = r.json()
        Last_Submission = data['results'][0]['submissionDateTimeUtc']

        if Last_Submission > Last_Active:
            # Status is online
            XCH_Status = 1
        else:
            # Status is offline
            XCH_Status = 0
        API_Error = "No"
    except:
        print("\n{}  |  ERROR: XCH-SpacePool API error.".format(datetime.strftime(datetime.now(), "%m-%d-%y %I:%M %p")))
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print("\n")
        XCH_Status = 0
        XCH_Rewards = 0
        XCH_Earned = 0
        API_Error = "Yes"

    return(XCH_USD, XCH_Status, XCH_Rewards, XCH_Earned, API_Error)

## Defining Atmotube (PlanetWatch) Miner Function
def GetAlgoExplorerData(PLANETSAcct, PLANETS_USD, tz):
    ## COMPLETE
    ## Environmental Miner Data
    #  Assumptions:
    #  1. PLANETS rewards are estimated from ACTUAL once daily payouts

    #  Asset_ID = because the Algorand blockchain can hold multiple assets, asset ID's must be specified in order to search for the right token
    #  27165954 is the Asset_ID for the PLANETS token
    Asset_ID = str(27165954)
    Last_Active = (datetime.utcnow() - timedelta(minutes=60)).isoformat()
    PLANETS_Status = 0

    try:
        r = requests.get("https://algoindexer.algoexplorerapi.io/v2/accounts/"+PLANETSAcct+"/transactions?asset-id="+Asset_ID)
        data = r.json()
        Num_Trans = len(data['transactions'])
        Trans_Time = []
        PLANETS_Rewards = []
        PLANETS_Earned =  []

        for i in range(Num_Trans):
            Last_Submission = datetime.fromtimestamp(data['transactions'][i]['round-time'], tz).isoformat()
            if Last_Submission > Last_Active:
                PLANETS_Status = 1
                New_Reward = data['transactions'][i]['asset-transfer-transaction']['amount'] / 1000000
                if New_Reward > 0:
                    Trans_Time.append(Last_Submission)
                    PLANETS_Rewards.append(New_Reward)
                    PLANETS_Earned.append(round(New_Reward * PLANETS_USD,2))
        
        if PLANETS_Status != 1:
            PLANETS_Status = 0
        
        API_Error = "No"
    except:
        print("\n{}  |  ERROR: PLANETS-Algoexplorer API error.".format(datetime.strftime(datetime.now(), "%m-%d-%y %I:%M %p")))
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print("\n")
        PLANETS_Status = 0
        PLANETS_Rewards = 0
        PLANETS_Earned = 0
        API_Error = "Yes"

    return(PLANETS_USD, PLANETS_Status, PLANETS_Rewards, PLANETS_Earned, API_Error)

## Defining GPU (ETH-NanoPool) Miner Function
def GetETHNanopoolGRPData(ETHAcct, ETH_USD, Last_Active, tz):
    ## COMPLETE
    ## GPU-grp Miner Data
    #  Assumptions:
    #  1. 

    try:
        r = requests.get("https://api.nanopool.org/v1/eth/user/"+ETHAcct)
        data = r.json()
        Daily_Avg_Hash = data['data']['avgHashrate']['h3']
        LastShare = data['data']['workers'][0]['lastshare']
        LastShare = datetime.fromtimestamp(LastShare, tz).isoformat()

        #  Checking if miner is active
        if LastShare > Last_Active:
            # Status is Online
            ETH_Status = 1
        else:
            # Status is Offline
            ETH_Status = 0

        r = requests.get("https://api.nanopool.org/v1/eth/approximated_earnings/"+str(Daily_Avg_Hash))
        data = r.json()
        ETH_Rewards = data['data']['day']['coins']/3
        ETH_Earned = data['data']['day']['dollars']/3
        API_Error = "No"
    except:
        print("\n{}  |  ERROR: ETH-Nanopool API error.".format(datetime.strftime(datetime.now(), "%m-%d-%y %I:%M %p")))
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print("\n")
        ETH_Status = 0
        ETH_Rewards = 0
        ETH_Earned = 0
        API_Error = "Yes"

    return(ETH_USD, ETH_Status, ETH_Rewards, ETH_Earned, API_Error)

## Defining GPU (ERG-NanoPool) Miner Function
def GetERGNanopoolData(ERGAcct, ERG_USD, Last_Active, tz):
    ## COMPLETE
    ## GPU-grp Miner Data
    #  Assumptions:
    #  1.

    try:
        r = requests.get("https://api.nanopool.org/v1/ergo/user/"+ERGAcct)
        data = r.json()
        Daily_Avg_Hash = data['data']['avgHashrate']['h3']
        LastShare = data['data']['workers'][0]['lastshare']
        LastShare = datetime.fromtimestamp(LastShare, tz).isoformat()

        #  Checking if miner is active
        if LastShare > Last_Active:
            # Status is Online
            ERG_Status = 1
        else:
            # Status is Offline
            ERG_Status = 0

        r = requests.get("https://api.nanopool.org/v1/ergo/approximated_earnings/"+str(Daily_Avg_Hash))
        data = r.json()
        ERG_Rewards = data['data']['day']['coins']
        ERG_Earned = data['data']['day']['dollars']
        API_Error = "No"
    except:
        print("\n{}  |  ERROR: ERG-Nanopool API error.".format(datetime.strftime(datetime.now(), "%m-%d-%y %I:%M %p")))
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print("\n")
        ERG_Status = 0
        ERG_Rewards = 0
        ERG_Earned = 0
        API_Error = "Yes"

    return(ERG_USD, ERG_Status, ERG_Rewards, ERG_Earned, API_Error)

## Defining Monero Miner Function
def GetMoneroOceanData(XMRAcct, XMR_USD, Last_Active, tz):
    ## COMPLETE
    ## CPU-grp Miner Data
    #  Assumptions:
    #  1. 

    #  Coin_Flag - this is the ID for the rx/0 algorithm (XMR native algo)
    Coin_Flag = str(18081)

    try:
        r = requests.get("https://api.moneroocean.stream/pool/stats")
        data = r.json()
        Profit_Rate = data['pool_statistics']['coinProfit'][Coin_Flag]

        r = requests.get("https://api.moneroocean.stream/miner/"+XMRAcct+"/stats")
        data = r.json()
        Last_Hash = data['lastHash']
        Hashrate = data['hash2']
        XMR_Rewards = Hashrate * Profit_Rate
        XMR_Earned = XMR_Rewards * XMR_USD
        Last_Hash = datetime.fromtimestamp(Last_Hash, tz).isoformat()

        #  Checking if miner is active
        if Last_Hash > Last_Active:
            # Status is Online
            XMR_Status = 1
        else:
            # Status is Offline
            XMR_Status = 0
        API_Error = "No"
    except:
        print("\n{}  |  ERROR: PLANETS-Algoexplorer API error.".format(datetime.strftime(datetime.now(), "%m-%d-%y %I:%M %p")))
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print("\n")
        XMR_Status = 0
        XMR_Rewards = 0
        XMR_Earned = 0
        API_Error = "Yes"

    return(XMR_USD, XMR_Status, XMR_Rewards, XMR_Earned, API_Error)

## Defining Email Function
def SendEmail(row, Status, Data_Table):
    # Setting Variables for Email Notifications
    Email_Data = app_tables.email_notify
    send_address = Email_Data.search()[0]['Send Address']
    receive_address = Email_Data.search()[0]['Receive Address']
    pswd = Email_Data.search()[0]['Password']
    mail_server = Email_Data.search()[0]['SMTP Server']
    mail_port = Email_Data.search()[0]['SMTP Port']

    # Sending Offline Mail Alert
    if row['Send Alerts'] == "Yes":
        if Status == 0 and Data_Table.search()[len(Data_Table.search())-2]['Status'] != 0:
            smtp_server=smtplib.SMTP(mail_server,mail_port)
            smtp_server.ehlo()
            smtp_server.starttls()
            smtp_server.ehlo()
            smtp_server.login(send_address, pswd)

            msg = MIMEMultipart()
            msg['From'] = send_address
            msg['To'] = receive_address
            msg['Subject'] = row['Coin']+"-"+row['MiningPool/API']+" Miner Offline"
            msg['X-Priority'] = '2'
            msgtext = "Miner detected offline at: " + datetime.strftime(datetime.now(), "%m-%d-%y %I:%M %p") + " EST"
            msg.attach(MIMEText(msgtext,'plain'))

            smtp_server.sendmail(send_address, receive_address, msg.as_string())
            smtp_server.quit()
        
        # Sending Back Online Mail Alert
        elif Status == 1 and Data_Table.search()[len(Data_Table.search())-2]['Status'] != 1:
            smtp_server=smtplib.SMTP(mail_server,mail_port)
            smtp_server.ehlo()
            smtp_server.starttls()
            smtp_server.ehlo()
            smtp_server.login(send_address, pswd)

            msg = MIMEMultipart()
            msg['From'] = send_address
            msg['To'] = receive_address
            msg['Subject'] = row['Coin']+"-"+row['MiningPool/API']+" Miner Back Online"
            msg['X-Priority'] = '2'
            msgtext = "Miner detected back online at: " + datetime.strftime(datetime.now(), "%m-%d-%y %I:%M %p") + " EST"
            msg.attach(MIMEText(msgtext,'plain'))

            smtp_server.sendmail(send_address, receive_address, msg.as_string())
            smtp_server.quit()

anvil.server.connect("<your uplink key>")

## Defining Routine to Extract New Data Every Hour
TimeTillUpdate = 0
flag = 0
tdelta = 30

try:
    while True:
        if TimeTillUpdate <= 1:
            GetHourlyData(flag, tdelta)
            LastUpdate = datetime.now()
            NextUpdate = LastUpdate + timedelta(minutes=tdelta)
            TimeTillUpdate = round((NextUpdate - LastUpdate).total_seconds()/60,0)
            app_tables.countdown.delete_all_rows()
            app_tables.countdown.add_row(Last_Update = LastUpdate, Next_Update = NextUpdate, Minutes_Until_Update = TimeTillUpdate)
            print("{} EST  |  Updated at: {} EST. Next Update in {:.1f} minutes at {} EST.\r".format(datetime.strftime(datetime.now(), "%m-%d-%y %I:%M %p"),datetime.strftime(LastUpdate, "%m-%d-%y %I:%M %p"), TimeTillUpdate, datetime.strftime(NextUpdate, "%m-%d-%y %I:%M %p")))
        else:
            time.sleep(58)
            TimeTillUpdate = round((NextUpdate - datetime.now()).total_seconds()/60,0)
            app_tables.countdown.delete_all_rows()
            app_tables.countdown.add_row(Last_Update = LastUpdate, Next_Update = NextUpdate, Minutes_Until_Update = TimeTillUpdate)
            print("{} EST  |  Next Update in {:.1f} minutes at {} EST.\r".format(datetime.strftime(datetime.now(), "%m-%d-%y %I:%M %p"), TimeTillUpdate, datetime.strftime(NextUpdate, "%m-%d-%y %I:%M %p")))
except KeyboardInterrupt:
    print("\nProgram quit by user!\n")