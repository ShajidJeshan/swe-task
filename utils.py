from datetime import datetime


def parse_data(data):
    readings = []
    lines = data.split("\n")
    for line in lines:
        line = line.strip()
        if line:
            parts = line.split()
            if len(parts) == 3:
                str_time = int(parts[0])
                timestamp = datetime.fromtimestamp(str_time)
                print("type==", type(timestamp))
                name = parts[1]
                value = float(parts[2])
                readings.append({"timestamp": timestamp, "name": name, "value": value})
    return readings
