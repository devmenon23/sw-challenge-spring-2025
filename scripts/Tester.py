from DataInterface import DataInterface

def main():
  dataDir = "data"
  dataInterface = DataInterface(dataDir)

  dataInterface.interface()

if __name__ == '__main__':
  main()