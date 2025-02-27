Documentation

Data Loading:
- In order to load the data I decided to use Python's multiprocessing library instead of the multithreading library as the Global Interpreter Lock prevents python from running multiple threads in parallel. However, multiprocessing is able to pool each file into parallel processes and combine at the end similar to multithreading.
- I record each line of the csv file while skipping the field headers into a list that I can later use during the data cleaning stage.
- I used the multithreading library initially, but did not see an improvement between single threaded and multi threaded implementations as Python's Global Interpreter Lock (GIL) was preventing the program from running multiple threads. Therefore, I had to learn about multi processing in order to implement this most efficiently, which was definitely a challenge when it came to optimization of the loader.

Data Cleaning:
- The data cleaner checks for blank prices, negative prices, duplicate trades, and most importantly outlier data. Negative prices were easily made positive while blank and duplicate fields were removed from the data as manipualting them is not likely to give accurate replacements. I employed the Interquartile Range method to identify outliers and decide whether to replace them or remove them from the data. I replace some of the outlier data with a simple median of all prices in the data.
- I assumed that the outliers were mostly typos as most of them were close to the number 40, a common typo to the median close to 400. Therefore, I replace the outlier with a number close to the median.

Data Interface (How to use interface):
- The user is able to type any interval (_d_h_m_s) for the OHLCV bars using the data in a specific timeframe with a start and an end (YYYY-MM-DD XX:XX:XX.XXX). The Data Interface will then filter the data set with the given timeframe to produce a csv flat file depicting the OHLCV data on the given regular intervals.
- The following CSV flat files found in the sw-challenge-spring-2025 folder correspond to the following parameters
    - ohclv_bars_example1.csv = Interval: 12m46s, start: 2024-09-16 10:23:34.464, end: 2024-09-16 15:34:34.543
    - ohclv_bars_example2.csv = Interval: 1h, start: 2024-09-16 09:30:00.076, end: 2024-09-16 15:34:34.543
    - ohclv_bars_example2.csv = Interval: 4m, start: 2024-09-16 09:30:00.076, end: 2024-09-16 15:34:34.543
- We do assume that the csv timestamps from the original data contains similar formatting to the user input format which is caught in a try-except statement if not corresponding.

