from selenium import webdriver
import datetime
import time as sleepy
import pandas as pd

driver = webdriver.Chrome(executable_path='C:/Users/micha/Documents/Python/chromedriver')
time = datetime.datetime.today().time()

initialInvestment = 1000

purchased = 0
sold = purchased
profit = 0
COH = initialInvestment + profit
portfolio = 0
averagePrice = 10000
closingTime = datetime.datetime.today().replace(hour=17,minute=0,second=0,microsecond=0).time()
buying = True
x = 0
curTicker = "FUCK"
driver.get("https://finance.yahoo.com/")
while time < closingTime:
    x += 1
    time = datetime.datetime.today().time()
    driver.refresh()
    sleepy.sleep(10)
    ticker = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div[3]/div[2]/div/div/div/div/div/div[3]/div/div/section/div/section[6]/table/tbody/tr[1]/td[1]/a").get_attribute("innerText")
    data = driver.find_element_by_xpath('//*[@id="data-util-col"]/section[6]/table/tbody/tr[1]/td[2]/span').get_attribute("innerText")
    
    print('\n\nTime: ' + str(time))
    print(ticker)
    
    datadf = pd.DataFrame(columns = ["Time","Price"])
    if ticker != curTicker:
        curTicker = ticker
        datadf=pd.DataFrame(columns = ["Time","Price"])
    datadf = datadf.append(pd.Series([time, data], index=datadf.columns), ignore_index=True)
    averagePrice = datadf["Price"].mean()
    currentPrice = float(data)
    print('Current Price: ' + str(currentPrice))
    print('Average Price: ' + str(averagePrice))
    if buying == True:  
            if x == 1:
                purchased = currentPrice
                shares = COH / purchased
                COH -= purchased * shares
                print('Purchased at: ' + str(purchased))
                buying = False 
            elif currentPrice < averagePrice:
                purchased = currentPrice
                shares = COH / purchased
                COH -= purchased * shares
                print('Purchased at: ' + str(purchased))
                buying = False
    else:
            if currentPrice > purchased:
                sold = currentPrice
                COH += sold * shares
                print('Sold at: ' + str(sold))
                print('Profit of: ' + str((sold - purchased)*shares))
                purchased = 0
                shares = 0
                buying = True
            elif currentPrice < (purchased * .9):
                print('Fear Sell')
                sold = currentPrice
                COH += sold * shares
                print('Sold at: ' + str(sold))
                print('Profit of: ' + str((sold - purchased)*shares))
                purchased = 0
                shares = 0
                buying = True
    portfolio = currentPrice * shares
    profit = (COH + portfolio) - initialInvestment
    print('Profit: ' + str(profit))
    print('Cash on Hand: ' + str(COH))
    print('Portfolio: ' + str(portfolio))
    print('Own @ ' + str(purchased))
    sleepy.sleep(60)
driver.quit()

