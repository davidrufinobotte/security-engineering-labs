"""
CrowdStrike Falcon - Alert Reader
----------------------------------
Authenticates via OAuth2 (using FalconPy) and lists recent alerts
from the Falcon platform, using the current Alerts API.

Note: this replaces the older Detects API, which CrowdStrike
decommissioned. See:
https://supportportal.crowdstrike.com/s/article/Tech-Alert-Planned-Decommission-Announcement-of-the-DetectionSummaryEvent-and-detects-API

Setup:
    pip install crowdstrike-falconpy

Environment variables required:
    FALCON_CLIENT_ID
    FALCON_CLIENT_SECRET
"""

import os
import sys
from falconpy import Alerts


def get_credentials():
    client_id = os.environ.get("FALCON_CLIENT_ID")
    client_secret = os.environ.get("FALCON_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("Error: FALCON_CLIENT_ID and FALCON_CLIENT_SECRET must be set as environment variables.")
        sys.exit(1)

    return client_id, client_secret


def list_recent_alerts(limit=10):
    client_id, client_secret = get_credentials()

    falcon = Alerts(client_id=client_id, client_secret=client_secret)

    # get_alerts_combined returns full alert records in one call —
    # no need for a separate query + details step like the old Detects API.
    response = falcon.get_alerts_combined(
        limit=limit,
        sort="created_timestamp|desc",
    )

    if response["status_code"] != 200:
        print("Failed to retrieve alerts:", response["body"].get("errors"))
        sys.exit(1)

    alerts = response["body"]["resources"]

    if not alerts:
        print("No alerts found yet. This is expected on a fresh trial with no test activity.")
        return

    print(f"\nFound {len(alerts)} alert(s):\n")
    print(f"{'Hostname':<20} {'Severity':<10} {'Status':<15} {'Created':<25} {'Tactic':<20}")
    print("-" * 95)

    for a in alerts:
        hostname = a.get("device", {}).get("hostname", "unknown")
        severity = a.get("severity_name", "unknown")
        status = a.get("status", "unknown")
        created = a.get("created_timestamp", "unknown")
        tactic = a.get("tactic", "unknown")

        print(f"{hostname:<20} {severity:<10} {status:<15} {created:<25} {tactic:<20}")


if __name__ == "__main__":
    list_recent_alerts(limit=10)

