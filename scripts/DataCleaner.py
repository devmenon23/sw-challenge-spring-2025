from multiprocessing import Pool, cpu_count

class DataCleaner:
  def __init__(self):
    pass

  def clean_data(self, dataSet):
    numWorkers = cpu_count()
    chunkSize = len(dataSet) // numWorkers

    chunks = [dataSet[i:i + chunkSize] for i in range (0, len(dataSet), chunkSize)]

    # Pool all cleaning workers in chunks
    with Pool(numWorkers) as pool:
      results = pool.map(self.cleaning_worker, chunks)

    # Combine results from chunk workers
    cleanedDataSet = []
    totalLinesRemoved = 0
    for cleanedChunk, linesRemoved in results:
      cleanedDataSet.extend(cleanedChunk)
      totalLinesRemoved += linesRemoved

    print(str(totalLinesRemoved) + " lines removed while cleaning")
    return cleanedDataSet

  def cleaning_worker(self, chunk):
    cleanedChunk = []
    seen = set()
    linesRemoved = 0

    # Get all prices for IQR 
    prices = [float(record[1]) for record in chunk if record[1] != "" and float(record[1]) > 0]
    if prices:
      prices.sort()
      
      # Calculate quartiles
      Q1 = prices[len(prices) // 4]
      Q3 = prices[(3 * len(prices)) // 4]
      IQR = Q3 - Q1
      
      # Calculate lower and upper bounds for outliers
      lower_bound = Q1 - 1.5 * IQR
      upper_bound = Q3 + 1.5 * IQR
      
      # Get median of valid prices to replace outlier
      valid_prices = [price for price in prices if lower_bound <= price <= upper_bound]
      median_price = self.calculate_median(valid_prices)

    for i in range(len(chunk)):
      record = chunk[i]

      # Check blank price error
      if (record[1] == ""):
        linesRemoved += 1
        continue
      
      # Check outlier price data
      if float(record[1]) < lower_bound or float(record[1]) > upper_bound:
          if median_price is not None:
              record[1] = str(median_price)  # Replace with median of valid prices
          else: 
              linesRemoved += 1
              continue

      # Check duplicate data
      recordTuple = tuple(record) # To add to seen set as tuple is hashable
      if (recordTuple in seen):
        linesRemoved += 1
        continue
      
      # Check negative price error
      elif (float(record[1]) < 0):
        record = [record[0], str(abs(float(record[1]))), record[2]]
      
      cleanedChunk.append(record)
      seen.add(recordTuple)
    
    return cleanedChunk, linesRemoved
  
  def calculate_median(self, prices):
      n = len(prices)
      if n == 0:
          return None
      
      prices.sort()
      if n % 2 == 1:
          return prices[n // 2]
      else:
          return (prices[n // 2 - 1] + prices[n // 2]) / 2
      
