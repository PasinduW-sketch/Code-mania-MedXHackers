from typing import List
import statistics
import sys

def anomaly_score(data: List[List[int]]) -> int:
    N = len(data)
    T = len(data[0])
    total_anomalies = 0

    # 1. Duplicate readings - ONCE per streak > 2
    for sensor in data:
        count = 1
        for i in range(1, T):
            if sensor[i] == sensor[i-1]:
                count += 1
            else:
                if count > 2:  # Count ONCE when streak ends
                    total_anomalies += 1
                count = 1
        if count > 2:  # Handle streak at end
            total_anomalies += 1

    # 2. Outlier deviations - FIXED median logic
    for sensor in data:
        diffs = [abs(sensor[i] - sensor[i-1]) for i in range(1, T)]
        if not diffs:
            continue
        median_diff = statistics.median(diffs)
        if median_diff == 0:
            continue  # No outliers if all values identical
        for i in range(1, T):
            if abs(sensor[i] - sensor[i-1]) > 2 * median_diff:
                total_anomalies += 1

    # 3. Cross-sensor conflicts
    for t in range(T):
        readings_at_t = [data[s][t] for s in range(N)]
        for s in range(N):
            others = readings_at_t[:s] + readings_at_t[s+1:]
            if not others:
                continue
            min_val, max_val = min(others), max(others)
            range_val = max_val - min_val
            if range_val == 0:
                if readings_at_t[s] != min_val:
                    total_anomalies += 1
            else:
                lower = min_val - 0.5 * range_val
                upper = max_val + 0.5 * range_val
                if readings_at_t[s] < lower or readings_at_t[s] > upper:
                    total_anomalies += 1

    # 4. Silent failures - ONCE per streak >= 3
    for sensor in data:
        count = 0
        for val in sensor:
            if val == 0:
                count += 1
                if count == 3:  # ONCE when reaching exactly 3
                    total_anomalies += 1
            else:
                count = 0

    return total_anomalies

# HackerRank input parsing
input_data = sys.stdin.read().split()
index = 0
N = int(input_data[index])
T = int(input_data[index + 1])
index += 2

data = []
for i in range(N):
    row = [int(input_data[index + j]) for j in range(T)]
    data.append(row)
    index += T

print(anomaly_score(data))
