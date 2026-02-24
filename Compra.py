from datetime import datetime
import alpaca_trade_api as tradeapi
import time
from alpaca_trade_api.rest import TimeFrame
import pandas as pd
import numpy as np   
import pytz
import matplotlib
import matplotlib.pyplot as plt
import os
from pathlib import Path
import keyboard

API_KEY = "xxxxxxxxxxxxxxx"
API_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"


# Import the TimeFrame class to use in 'get_bars'
from alpaca_trade_api.rest import TimeFrame

stockUniverse = ["AAPL","NVDA",'TSLA',"MSFT","NFLX",'QCOM']


class Compra:
  def __init__(self):
    self.alpaca = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v2')
    
    # Get our account information.
    account = self.alpaca.get_account()

    precioactual = 0
    
    #Imprimimos el saldo inicial
    cashBalance = 0
    cashBalance = self.alpaca.get_account().cash
    valorporfolio = self.alpaca.get_account().portfolio_value
    print("El saldode nuestra cuenta es" + cashBalance)
    print("El saldode nuestro porfolio es" + valorporfolio) 
    balance = cashBalance

    # Imprimimos el cambio de balance de uestar cuenta
    balance_change = float(account.equity) - float(account.last_equity)
    print(f'Hoy el cambio de balance de nuestra cartera es: ${balance_change}')

    short_window = 20 #short window for SMA (in minutes)
    long_window = 50 #long window to SMA (in minutes)

    # Set a constant for UTC timezone
    UTC = pytz.timezone('UTC')

    #stockUniverse
    self.analizastock()

    # Format the allStocks variable for use in the class.
    self.allStocks = []
    for stock in stockUniverse:
      self.allStocks.insert(len(stockUniverse),[stock, 0]) 
    
    for i in range(len(stockUniverse)):
      print("el array es ", self.allStocks[i])
      i+=1  

    #creaCreaos un archivo con la ejecucion usando "x"
    fechaactual = str(datetime.now())
    mifichero = open("C:/alpaca-trade-api-python-master/Salida_Operaciones/resultado.txt", "a")
    #mifichero = open(r"C:\alpaca-trade-api-python-master\Salida_Operaciones\resultado_" + fechaactual + ".txt", "x")

    self.blacklist = set()
    self.timeToClose = None

  def run(self):
    # First, cancel any existing orders so they don't impact our buying power.
    orders = self.alpaca.list_orders(status="open")
    for order in orders:
      print("Tenemos la orden" + order.id)
      self.alpaca.cancel_order(order.id)

    #Vamos a ver que porfolio tenemos
    self.pintaporfolio()

    #Vamos a vender todo lo que tenemos
    self.vendetodo()

    # Wait for market to open.
    """print("Waiting for market to open...")
    tAMO = threading.Thread(target=self.awaitMarketOpen)
    tAMO.start()
    tAMO.join()
    print("Market opened.")"""
    
    # Rebalance the portfolio every minute, making necessary trades.
    while True:
      if keyboard.is_pressed("q"): #returns True if "q" is pressed
        #Vamos a vender todo lo que tenemos
        print("Has presionado la tecla q en el primer while")
        self.vendetodo()
        break #break the while loop is "q" is pressed
      else:
        print("No Key pressed.") 
        break
        # Figure out when the market will close so we can prepare to sell beforehand.
        """clock = self.alpaca.get_clock()
        closingTime = clock.next_close.replace(tzinfo=datetime.timezone.utc).timestamp()
        currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
        self.timeToClose = closingTime - currTime

        if(self.timeToClose < (60 * 15)):
        
          # Close all positions when 15 minutes til market close.
          print("Market closing soon.  Closing positions.")

          positions = self.alpaca.list_positions()

          # Run script again after market close for next trading day.
          print("Sleeping until market close (15 minutes).")
          time.sleep(60 * 15)
        
          #esto es real
          #Vamos a ver que porfolio tenemos
          self.pintaporfolio()

          #Vamos a vender todo lo que tenemos
          self.vendetodo()

        else:"""
        #self.pintaporfolio()
        
          #Vamos a carpturar lo datos de los ultimos minutos de muestro objetivo AAPL
          #aapl_position = self.alpaca.get_open_position('AAPL')
          #Descarga datos para ver analsis de tendencias en 'AAPL')
          # Define el símbolo de AAPL y el rango de fechas que deseas (por ejemplo, los últimos 30 días)
      
          #APPLE_DATA = sself.alpaca.get_bars('AAPL', 'minute', limit=100).df# Preview Dataprint(APPLE_DATA.df.head())
          #APPLE_DATA = self.alpaca.get_bars('AAPL', TimeFrame.Minute, limit=100).df# Preview Dsataprint(APPLE_DATA.df.head())
          #Recorrremos stockUniverse

      
        for x in stockUniverse:
          nomacc = x
          print ("La accion que estamos tratando es " + nomacc)
          APPLE_DATA = self.alpaca.get_bars(nomacc, TimeFrame.Minute, limit=100)
          """APPLE_DATA = self.alpaca.get_bars(nomacc, TimeFrame.Minute,start="2024-07-04", 
                          end="2024-08-04",
                          adjustment='raw',
                          limit=100
                            )
          print ("x ",x)"""
          #print(APPLE_DATA.df.head())
          #print(APPLE_DATA.df.tail())
          #print ("mi 20  " + str(mi20))
          #if mi20 != 1:
          #  mi20 = 1            
          self.analisis( APPLE_DATA,nomacc)
        
        #repite el proceso cada 60 seg
        time.sleep(60)

  #Analizamosel stock para rellenar stockuniverse
  def analizastock(sellf):
    #Primero abrimos el fichero de resultado para cargar las
    # ultimas acciones que tuvimos
    

  #Pintamos nuestra cartera = porfolio
  def pintaporfolio(self):
    # First get all the positions into a dataframe indexed by symbol
    import pandas as pd

    # Get our account information.
    account = self.alpaca.get_account()
    
    # Check if our account is restricted from trading.
    if account.trading_blocked:
      print('Account is currently restricted from trading.')

    # Check our current balance vs. our balance at the last market close
    balance_change = float(account.equity) - float(account.last_equity)
    print(f'Today\'s portfolio balance change: ${balance_change}')

    account = self.alpaca.get_account()
    
    my_positions = self.alpaca.list_positions()

    # Get our account information.
    account = self.alpaca.get_account()
    # Get a list of all of our positions.
    portfolio = self.alpaca.list_positions()

    # Print the quantity of shares for each position.
    for position in portfolio:
      print("{} En pintaporfolio Tenemos la cantidad de  {}".format(position.qty, position.symbol))
      

  def vendetodo(self):
    
    positions = self.alpaca.list_positions()
    mifichero=open("C:/alpaca-trade-api-python-master/Salida_Operaciones/resultado.txt", "a")
    
    #Por cada elemento position de porfolio (positions)
    #Damos la orden de vender
    for position in positions:
      print("{} En vendetodo tenemos la cantidad en la accion {}".format(position.qty, position.symbol + "y de cara" + position.side))
      resultado = self.alpaca.submit_order(symbol=position.symbol, side="sell", qty = position.qty, type='market', time_in_force='gtc')
      fechaactual = str(datetime.now())
      mifichero.write("Vendemos en vendetodo accion de " + position.symbol + " en cantidad " + str(position.qty) + " en fecha" + fechaactual + "\n")
    
    #Cerramos el fichero
    mifichero.close()

    #Grabamos el porfolio
    self.escribeporfolio()

    #Imprimimos el saldo inicial
    saldofinal = self.alpaca.get_account().cash
    print("El saldo de nuestra cuenta es" + saldofinal)

  #Finalizamos la jornada
  def finalizar(self):
    # Antes de acabar la jornada, cancel any existing orders so they don't impact our buying power.
    orders = self.alpaca.list_orders(status="open")
    for order in orders:
      print("Vendemos orden " + order.id)
      self.alpaca.cancel_order(order.id)

    #Vendemos todo nuestro porfolio
    self.vendetodo()
    
    #pintamos el porfolio despuesde la venta
    self.pintaporfolio()
    
    #Mandamos el contenido del porfolio junto al smi a otro fichero
    self.escribeporfolio()    

    #Una vez se ha vedido todo lo del dia vemos como queda nuestra cuenta
    #Imprimimos el saldo final
    saldofinal = self.alpaca.get_account().cash
    print("El saldode nuestra cuenta es" + saldofinal)
    balance = saldofinal

    # Imprimimos el cambio de balance de nuestra cuenta
    account = self.alpaca.get_account()
    balance_change = float(account.equity) - float(account.last_equity)
    print(f'Hoy el cambio de balance de nuestra cartera es: ${balance_change}')
    

  # Wait for market to open.
  def awaitMarketOpen(self):
    isOpen = self.alpaca.get_clock().is_open
    while(not isOpen):
      clock = self.alpaca.get_clock()
      openingTime = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()
      currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
      timeToOpen = int((openingTime - currTime) / 60)
      print(str(timeToOpen) + " minutes til market open.")
      time.sleep(60)
      isOpen = self.alpaca.get_clock().is_open

  
  #Funcion que hace la compra o venta
  #ver luego como queda el porfolio o cartera
  def EjecutaOperacion(self,ELSMA20,ELSMA50,simbolo,compraoventa,precioaejecutar):
    import math as mt
    from alpaca_trade_api.rest import TimeFrame 
    from datetime import datetime, timedelta, timezone,date
 
    #Pintamos las posiciones abiertas
    positions = self.alpaca.list_positions()

    #Imprimimos nuestro saldo
    cashBalance = self.alpaca.get_account().cash
    print("El saldo de nuestra cuenta es" + cashBalance)

    #Ahora debemos saber cuanto invertir en nuesta operacion
    #Riesgo máximo permitido = 2% de nuestro capital total por operación
    #Luego compramos el 2% del cashBalance
    cantidadagastar = (float(cashBalance) * 2) / 100

    #Ahora para calcular la candidad de acciones a comprar se divide
    # cantidadagastar / precio de la accion en el mercado
    current_date = datetime.now(tz=timezone.utc)
    fechaactual = current_date.strftime("%Y-%m-%d")
    #symbol_bars = self.alpaca.get_bars(simbolo, "minute", 1).df
    ####ESTO EN REAL DESCOMENTAR PORQUE ES LO BUENO***
    """symbol_bars = self.alpaca.get_bars(simbolo, 
                    tradeapi.rest.TimeFrame.Minute, 
                    fechaactual,                     
                    adjustment='raw',
                    limit=1).df.iloc[0]
    
    precioaejecutar = symbol_bars.close"""

    accionesacomprar = int(float(cantidadagastar / precioaejecutar))

       
    if compraoventa == "buy":
      resultado = self.alpaca.submit_order(symbol=simbolo, side="buy", qty = accionesacomprar, type='market', time_in_force='gtc')
      #Mandamos el resultado al fichero
      fechaactual = str(datetime.now())
      mifichero=open("C:/alpaca-trade-api-python-master/Salida_Operaciones/resultado.txt", "a")
      mifichero.write("Compramos accion de " + simbolo + " en cantidad " + str(accionesacomprar) + " en fecha" + fechaactual + "\n")
      mifichero.close()
    else:
      print("Se trata de una venta")
      #Si se trata de una venta porque el SMI ha cambiado deveriamos verder todo el porfolio
      #De ese simbolo
      #Get a list of all of our positions.
      positions = self.alpaca.list_positions()

      for position in positions:
        if position.symbol == simbolo:  
            print("{} En ejecutaoperacion Tenemos la cantidad en la accion {}".format(position.qty, position.symbol + "y de side " + position.side))
            #Ahora vendemos
            resultado = self.alpaca.submit_order(symbol=simbolo, side="sell", qty = position.qty, type='market', time_in_force='gtc')
            fechaactual = str(datetime.now())
            mifichero=open("C:/alpaca-trade-api-python-master/Salida_Operaciones/resultado.txt", "a")
            mifichero.write("Vendemos accion de " + simbolo + " en cantidad " + str(position.qty) + " en fecha" + fechaactual + "\n")
            mifichero.close()
    return resultado 

  def escribeporfolio(self):
    
    mifichero=open("C:/alpaca-trade-api-python-master/Salida_Operaciones/porfolio.txt", "w")
        
    for l in (range(len(stockUniverse))):
      if (self.allStocks[l][1]!=0):
        #Mandamos los dos valores de la posicion en el fichero
        mifichero.write(self.allStocks[l][0] + " " + self.allStocks[l][1] + "\n")
        l+=1
    mifichero.close()

  def analisis(self,APPLE_DATA,simbolo):
      from datetime import datetime
      import numpy as np
      import talib
      import pandas as pd

      barTimeframe =  "1Min" #"1H", 5Min, 15Min, 1H, 1D
      assetsToTrade = len(stockUniverse)

      # Tracks position in list of symbols to download
      iteratorPos = 0 
      assetListLen = assetsToTrade

      print ("Tratamos la accion en el proc de analisis " + simbolo)

      timeList = []
      openList = []
      highList = []
      lowList = []
      closeList = []
      volumeList = []
    
      # Reads, formats and stores the new bars
      for bar in APPLE_DATA:
        midato = (bar.t)
        midato = str(midato)
        timeList.append(midato)#(datetime.strptime(bar.t,'%Y-%m-%dT%H:%M:%SZ'))
        openList.append(bar.o)
        highList.append(bar.h)
        lowList.append(bar.l)
        closeList.append(bar.c)
        volumeList.append(bar.v)
        iteratorPos += 1

      precioactual = bar.c    

      # Processes all data into numpy arrays for use by talib
      timeList = np.array(timeList)
      openList = np.array(openList,dtype=np.float64)
      highList = np.array(highList,dtype=np.float64)
      lowList = np.array(lowList,dtype=np.float64)
      closeList = np.array(closeList,dtype=np.float64)
      volumeList = np.array(volumeList,dtype=np.float64)
      

      # Calculated trading indicators
      SMA20 = talib.SMA(closeList,20)[-1]
      SMA50 = talib.SMA(closeList,50)[-1]
     
      # First get all the positions into a dataframe indexed by symbol

      #positions = self.alpaca.list_positions()
      print("Pintamos porfolio dentro de analisis antes del if")
      self.pintaporfolio()
      
      j=0
      for i in (range(len(stockUniverse))):
        if (self.allStocks[i][0] == simbolo) and (int(self.allStocks[i][1])!=0):
          print ("self.allStocks[i][0] ",self.allStocks[i][1])
          mi20 = self.allStocks[i][1]
          j = i
          break
        else:
          mi20 = 0
        i+=1
      print("el sma20 es antes del if: ", mi20)
      # Calculates the trading signals
      if (SMA20 < mi20) and (mi20!=0):
        #En este caso habria que vender
        #mi20 = SMA20
        # Opens new position if one does not exist
        self.alpaca.get_position(simbolo)
        #Hay que comparar el SMI con el SMI anterior (si operamos en varios dias)
        #para ver si compramos o vendemos
        #De momento como es un solo dia vendemos todo
        #vemos nuestra posicion abierta en el simbolo
        posicion_abierta_en_simbolo = self.alpaca.get_position(simbolo)  
        print("{} Ahora tenemos accciones y vamos a vendenlas {}".format(posicion_abierta_en_simbolo.qty, posicion_abierta_en_simbolo.symbol))
        #resultado = self.alpaca.submit_order(symbol=simbolo, side="sell", qty = posicion_abierta_en_simbolo.qty, type='market', time_in_force='gtc')
        self.EjecutaOperacion(SMA20,SMA50,simbolo,"sell",precioactual) 
        #Vemos como esta el porfolio despues de la venta
        for i in range(len(stockUniverse)):
          print("el array tras venta es ", self.allStocks[i])
          i+=1
        #Metemos de nuevo un cero en la posicion          
          k=0
          for stock in stockUniverse:
            if self.allStocks[k][0]==simbolo:
              self.allStocks[k][1]=0
            k+=1
      else:
        # Ordenamos abrir una posicion
        if (SMA20 > SMA50) and (mi20==0):
          self.EjecutaOperacion(SMA20,SMA50,simbolo,"buy",precioactual) 
          print("Ahora hay que ver las posiciones abiertas en la cartera") 
          k=0
          for stock in stockUniverse:
            if self.allStocks[k][0]==simbolo:
              self.allStocks[k][1]=SMA20
            k+=1
          self.pintaporfolio()
          for i in range(len(stockUniverse)):
            print("el array tras compra es ", self.allStocks[i])
            i+=1    
        else:
          print ("No hay cambio de tendencia del sma")          

while True:
  if keyboard.is_pressed("q"): #returns True if "q" is pressed
    #Vamos a vender todo lo que tenemos
    print("Has presionado la tecla q")
    Compra.vendetodo
    break #break the while loop is "q" is pressed
  else:
    # Ejecuta el programa
    ls = Compra()
    ls.run()
    ls.finalizar()
