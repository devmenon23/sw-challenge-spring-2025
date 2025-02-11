import os
import csv
from multiprocessing import Pool, cpu_count

class DataLoader:
  def __init__(self):
    pass

  # Find the csv files in directory
  def find_csv_files(self, directory):
    try:
      # Get every file from the directory folder
      csvFiles = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".csv")]
    except Exception as e:
      print(f"Error accessing {directory}: {e}")
    
    return csvFiles
  
  # Read the csv files found in data folder
  def read_csv_files(self, directory):
    csvFiles = self.find_csv_files(directory)
    numWorkers = cpu_count()

    # Pool csv files into multiple processes
    with Pool(numWorkers) as pool:
      results = pool.map(self.reading_worker, csvFiles)

    # Merge all data from workers into one dataSet
    dataSet = []
    for sublist in results:
      for row in sublist:
        dataSet.append(row)
    
    return dataSet

  def reading_worker(self, file):
    recordData = []

    try:
      # Read and append each row in the csv file
      with open(file, mode="r", newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
          recordData.append(row)
    except Exception as e:
      print(f"Error reading {file}: {e}")
    
    return recordData
