import time

start_min = time.localtime().tm_min

while start_min < 20:
    if time.localtime().tm_sec % 5 == 0:
        print("Health Check")