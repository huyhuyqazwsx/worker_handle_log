from collections import defaultdict
import math

acc = defaultdict(lambda: defaultdict(lambda: {
    "count": 0,
    "sum": 0.0,
    "min": math.inf,
    "max": -math.inf,
}))

def add_metric(device_id, metric, value):
    bucket = acc[device_id][metric]
    bucket["count"] += 1
    bucket["sum"] += value
    bucket["min"] = min(bucket["min"], value)
    bucket["max"] = max(bucket["max"], value)

def reset_metric(bucket):
    bucket["count"] = 0
    bucket["sum"] = 0.0
    bucket["min"] = math.inf
    bucket["max"] = -math.inf
