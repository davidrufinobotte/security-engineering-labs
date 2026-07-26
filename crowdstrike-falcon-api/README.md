# CrowdStrike Falcon API — Detection Lab

A hands-on lab to test API access to CrowdStrike Falcon EDR, using a safe simulated attack instead of a real one. Built as a follow-up to the Entra ID + Sentinel lab, using the EDR tool.

## Status: Complete ✅

Sensor installed, API connected, real detection generated and read back through a script.

## What I did
- Installed the Falcon sensor on a test laptop (15-day trial, no cost)
- Created an API client with minimal scope (alerts read, hosts read/write only)
- Wrote a Python script (FalconPy) to read alerts from the API
- Generated a real detection using Atomic Red Team (safe MITRE ATT&CK simulation)
- Confirmed the script correctly reads the detection

## Problems I solved
- **Old API was dead**: my first script used the classic Detects API. CrowdStrike retired it. Fixed by switching to the current Alerts API.
- **Wrong permission scope**: after switching APIs, got a 403 error. The old scope name didn't match the new API. Fixed by updating the API client scope.
- **EICAR test file did not work**: this is normal. EICAR tests old signature-based antivirus. Falcon is behavior-based (NGAV/EDR), so a static test file on disk doesn't trigger it.
- **Switched to Atomic Red Team instead**: this simulates real attacker behavior (MITRE technique T1053.005 — scheduled task persistence), which Falcon is built to detect. Result: 10 alerts, across Execution, Machine Learning, and Malware categories.

## Cost
Free — 15-day trial, no credit card.

## Next steps
- Add screenshots to the repo
- Optional future project: automated containment (isolate host on high severity) — not part of this lab
