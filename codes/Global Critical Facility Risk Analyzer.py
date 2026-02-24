import sys
import json

def predict_risk(facilities):
    risk_scores = []
    for facility in facilities:
        hist = facility.get("historical_risk", [0.2])
        ftype = facility.get("type", "").lower()
        
        if len(hist) >= 3:
            trend = 0.2 * hist[0] + 0.2 * hist[1] + 0.6 * hist[2]
        elif len(hist) == 2:
            trend = 0.4 * hist[0] + 0.6 * hist[1]
        else:
            trend = hist[0]
        
        if ftype == "power":
            score = trend * 1.1176
        elif ftype == "water":
            score = trend * 1.3846
        else:
            score = trend
        
        risk_scores.append(round(max(0.0, min(1.0, score)), 2))
    
    return risk_scores

input_data = sys.stdin.read().strip()
facilities = json.loads(input_data)
result = predict_risk(facilities)
print(result)
