#!/usr/bin/env python3
from src.ai_resume_analyzer.monitoring.drift_detector import compare_distribution
import json, sys

def main():
    # fields to check
    fields = ["duration", "num_matches", "num_emails"]
    report = {}
    for f in fields:
        r = compare_distribution(f)
        report[f] = r
    print(json.dumps(report, indent=2, ensure_ascii=False))
    # return non-zero if any distance exceed threshold
    threshold = 1.0
    for f,v in report.items():
        if v.get("ok") and v.get("distance", 0) > threshold:
            print(f"DRIFT ALERT: {f} distance={v['distance']}")
            sys.exit(2)
    print("No drift detected (threshold {})".format(threshold))

if __name__ == "__main__":
    main()
