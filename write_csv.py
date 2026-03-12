import csv
import os
# File name for the CSV
filename = "marine_traffic.csv"
 

# Write ships data to CSV
def write_csv(mmsi, lat,lon, speed, destination, time_stamp):
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        try:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["SHIP_ID", "LATITUDE", "LONGITUDE", "SPEED", "DESTINATION", "TIME"])  # Add a header row
            
            writer.writerow([mmsi, lat, lon, speed, destination, time_stamp])  # Write ship data to a new row
        
        except Exception as e:
            log_file = "error_log.txt"
            with open(log_file, "a") as log:
                log.write(f"Error writing to CSV: {e}\n")
    
