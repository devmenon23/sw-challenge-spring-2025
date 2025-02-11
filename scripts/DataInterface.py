from DataLoader import DataLoader
from DataCleaner import DataCleaner
import datetime
import csv
import time

class DataInterface:
  def __init__(self, directory):
    self.directory = directory

  def interface(self):
    while True:
      try:
        self.interval = input("What would you like the interval of your OHLCV bars to be (_d_h_m_s): ")
        rawStart = input("What would you like the start of your time frame to be (YYYY-MM-DD XX:XX:XX.XXX): ")
        rawEnd = input("What would you like the end of your time frame to be (YYYY-MM-DD XX:XX:XX.XXX): ")

        startTime = time.time()
        loader = DataLoader()
        cleaner = DataCleaner()

        format = "%Y-%m-%d %H:%M:%S.%f"
        self.start = datetime.datetime.strptime(rawStart, format)
        self.end = datetime.datetime.strptime(rawEnd, format)

        print("Loading Data...")
        self.dataSet = loader.read_csv_files(self.directory)
        print("Cleaning Data...")
        self.dataSet = cleaner.clean_data(self.dataSet)

        self.process_data()
        endTime = time.time()

        print(f"Execution time: {endTime - startTime:.2f}")
        break
      except Exception as e:
        print("Please enter a valid format of interval or timeframe")

  # Turn string interval to timedelta
  def parse_interval(self, interval: str):
    intervalDict = {"d": 0, "h": 0, "m": 0, "s": 0}
    tempTime = ""

    for char in interval:
      if (char.isdigit()):
        tempTime += char
      elif (char in intervalDict):
        intervalDict[char] = int(tempTime)
        tempTime = ""
    
    return datetime.timedelta(days=intervalDict["d"], 
                                hours=intervalDict["h"], 
                                minutes=intervalDict["m"], 
                                seconds=intervalDict["s"])
  
  # Filter data to only have trades in timeframe
  def filter_data(self):
    format = "%Y-%m-%d %H:%M:%S.%f"
    
    # Use a generator to avoid loading all the data at once
    for trade in self.dataSet:
        timestamp = datetime.datetime.strptime(trade[0], format)
        if self.start <= timestamp <= self.end:
            yield trade
    
  # Create list with OHLCV data from filtered data in regular intervals
  def aggregate_ohlcv(self, filteredData, interval): 
    ohlcvBars = []
    format = "%Y-%m-%d %H:%M:%S.%f"
    currentTime = self.start
    barData = []

    for trade in filteredData:
        timestamp = datetime.datetime.strptime(trade[0], format)
        if timestamp < currentTime + interval:
            barData.append(trade)
        else:
            if barData:
                # Add bar data when the interval ends
                ohlcvBars.append(self.create_ohlcv_bar(barData, currentTime))
            currentTime += interval
            barData = [trade]
    
    if barData:
        ohlcvBars.append(self.create_ohlcv_bar(barData, currentTime))

    return ohlcvBars
  
  def create_ohlcv_bar(self, barData, currentTime):
    open_price = barData[0][1]
    high_price = max(float(trade[1]) for trade in barData)
    low_price = min(float(trade[1]) for trade in barData)
    close_price = barData[-1][1]
    volume = sum(int(trade[2]) for trade in barData)
    
    # Put in dictionary to use key valuu pairs later in writing to CSV
    return {"timestamp": currentTime, 
            "open": open_price, 
            "high": str(high_price), 
            "low": str(low_price), 
            "close": close_price, 
            "volume": str(volume)}
  
  # Save OHLCV data into csv flat file
  def saveToCSV(self, ohlcvBars, fileName="ohclv_bars.csv"):
    with open(fileName, "w", newline="") as f:
      writer = csv.writer(f)
      writer.writerow(["Timestamp", "open price", "high price", "low price", "close price", "volume"])
      for bar in ohlcvBars:
        # Write data using key value pairs
        writer.writerow([bar["timestamp"], bar["open"], bar["high"], bar["low"], bar["close"], bar["volume"]])

  # Process data throughout a timeframe in regular intervasl to generate aa file with OHLCV data
  def process_data(self):
    print("Processing Data...")
    intervalTimeDelta = self.parse_interval(self.interval)
    filteredData = self.filter_data()
    ohlcvBars = self.aggregate_ohlcv(filteredData, intervalTimeDelta)
    self.saveToCSV(ohlcvBars)
    
    