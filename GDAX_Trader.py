import gdax, time, datetime , json, csv
from websocket import create_connection

'''
[Low, High, Time placed, phase, buy/sell, stoploss, time when traded, trade price, placeholder]
'''
amt = 15
betA = []
betfrequency=2
Limit=0.01
margin=0.002
takerFee=0.003
lifespan=betfrequency*amt
for i in range(0,amt):
    betA.append([])
print("Lifespan: {} minutes".format(lifespan))

class myWebsocketClient(gdax.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.gdax.com/"
        self.products = ["ETH-EUR"]
        self.message_count = 0
        self.bet=True
        self.betnumber=0
        self.channels = [
            {
            "name": "ticker",
            "product_ids": [
            "ETH-EUR"
            ]
            }
        ]

        print(self.channels)

        #print("Lets count the messages!")
    def _connect(self):
        sub_params = {
            "type": "subscribe",
            "product_ids": [
                "ETH-USD",
            ],
            "channels": [
                "level2",
                "heartbeat",
                {
                    "name": "ticker",
                    "product_ids": [
                        "ETH-EUR",
                    ]
                }
            ]
        }
        self.ws = create_connection(self.url)
        self.ws.send(json.dumps(sub_params))
    def on_message(self, msg):
        self.message_count += 1
        if 'price' in msg and 'type' in msg and msg['product_id'] == 'ETH-EUR':
            print ("Price: {:.2f}".format(float(msg["price"])))
            lastprice=float(msg["price"])
            if self.bet:
                self.bet=False
                if betA[self.betnumber]:
                    if betA[self.betnumber][10]:
                        betA[self.betnumber][10]=False
                        betA[self.betnumber][9]=lastprice
                        secondBet(betA[self.betnumber],lastprice)
                betA[self.betnumber] = placeBet(lastprice, str(datetime.datetime.utcnow())[:-7])
                if self.betnumber==(amt-1):
                    self.betnumber=0
                else:
                    self.betnumber+=1

            for bet in betA:
                if bet:
                    checkBet(bet, lastprice)
    def on_close(self):
        print("-- Goodbye! --")
def placeBet(price, time):
    lowbet = price*(1-margin)
    highbet = price*(1+margin)
    print("Buy: {:.2f}".format(float(lowbet)), "Sell: {:.2f}".format(float(highbet)))
    return [time,lowbet, highbet, False,"","",0.0,price,"",0.0,True]
'''[Time placed, Low, High, Phase, time when hit, Buy or sell, Stoploss,  Price, Close time, Close Price,active
    0              1    2      3        4           5           6           7       8           9           10'''

def checkBet(bet, price):
    if bet[3]:
        secondBet(bet,price)
    else:
        if bet[1]<price<bet[2]:
            return
        elif price >= bet[2]:
            bet[5]="sell"
        else:
            bet[5]="buy"
        bet[3]=True
        bet[4]=str(datetime.datetime.utcnow())[:-7]
        betHit(bet)

def betHit(bet):
    if bet[5]=="sell":
        stoploss=bet[2]*(1+Limit)
    else:
        stoploss=bet[1]*(1-Limit)
    bet[6]=stoploss
    print(bet)

def secondBet(bet,price):
    if bet[5]=="sell":
        if float(price)>float(bet[6]) and bet[10]:
            print("Stoploss hit")
            bet[9]=bet[6]*(1+takerFee)
            bet[10]=False
        if float(price)<float(bet[7]) and bet[10]:
            bet[9]=bet[7]
            bet[10]=False
            print("Winner winner chicken dinner")
        if not bet[10]:
            bet[8]=str(datetime.datetime.utcnow())[:-7]
            print(bet)
    else:
        if float(price)<float(bet[6]) and bet[10]:
            print("Stoploss hit")
            bet[9]=bet[6]*(1-takerFee)
            bet[10]=False
        if float(price)>float(bet[7]) and bet[10]:
            bet[9]=bet[7]
            bet[10]=False
            print("Winner winner chicken dinner")
        if not bet[10]:
            bet[8]=str(datetime.datetime.utcnow())[:-7]
            print(bet)
            writeToCSV(bet)

def writeToCSV(bet):
    with open("betcsv.csv",'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(bet)
    '''
    write to csv "Timestamp when placed", "Timestamp of first thing", Timestamp of finish",
    "Price at placing", "Sell or buy price", "Ended by profit or loss"
    '''

wsClient = myWebsocketClient()
wsClient.start()
'''
file="betfile.csv"

print(wsClient.url, wsClient.products)
with open(file,'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
'''
while True:
    if datetime.datetime.now().minute % betfrequency == 0:
        wsClient.bet=True
    #do algorithm
    time.sleep(60)

#wsClient.close()
