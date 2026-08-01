# CrowdStrike Falcon API — Detection Lab

A hands-on lab to test API access to CrowdStrike Falcon EDR, using a safe simulated attack instead of a real one. Built as a follow-up to the Entra ID + Sentinel lab, using an EDR platform commonly deployed in enterprise environments.

## Status: Complete ✅

Sensor installed, API connected, real detection generated and read back through a script.

## What I did
- Installed the Falcon sensor on a test laptop (15-day trial, no cost)
- Created an API client with minimal scope (alerts read, hosts read/write only)
- Wrote a Python script (FalconPy) to read alerts from the API
- Generated a real detection using Atomic Red Team (safe MITRE ATT&CK simulation)
- Confirmed the script correctly reads the detection
- Extended the script to triage alerts via API — update status and add an audit comment
- Extended the script again to automatically contain a host when it has a High severity alert
- Investigated the contained host, then lifted containment

## Problems I solved
- **Old API was dead**: my first script used the classic Detects API. CrowdStrike retired it. Fixed by switching to the current Alerts API.
- **Wrong permission scope**: after switching APIs, got a 403 error. The old scope name didn't match the new API. Fixed by updating the API client scope.
- **EICAR test file did not work**: this is normal. EICAR tests old signature-based antivirus. Falcon is behavior-based (NGAV/EDR), so a static test file on disk doesn't trigger it.
- **Switched to Atomic Red Team instead**: this simulates real attacker behavior (MITRE technique T1053.005 — scheduled task persistence), which Falcon is built to detect. Result: 10 alerts, across Execution, Machine Learning, and Malware categories.
- **Wrong parameter name when updating alerts**: got a 400 error using `ids`. The API expects `composite_ids`. Fixed by checking the field name in the docs.
- **Wrong status value when closing alerts**: got a second 400 error. Fixed by reading the exact accepted values from the API's own error message (`closed`, `new`, `in_progress`, `reopened`).

## Containment step
- Extended the script to find hosts with a High severity alert and isolate them from the network, using the Falcon API (`Hosts.perform_action`, action `contain`).
- Built in a safety default: the script runs in dry-run mode by default (shows what it would do) and only takes action with an explicit `--execute` flag.
- Ran it from a separate laptop, not the target machine, so containing the test host wouldn't cut my own network access.
- After containment, investigated the host before lifting it:
  - Reviewed the process tree for the alert in the Falcon console
  - Used Real Time Response (RTR) to confirm the Atomic Red Team scheduled task was already removed by its own cleanup step
  - Ran an additional scan as a final check
  - Documented findings, then lifted containment via the console

This follows the standard incident response order: Identify → Contain → Eradicate → Recover — not just isolate and immediately undo it.

## Testing across multiple MITRE ATT&CK tactics
To go beyond a single technique, ran two more Atomic Red Team tests, covering different tactics than the original one:

- **T1082 (System Information Discovery — Discovery tactic)**: ran cleanly, but generated no alert. This is expected — `systeminfo` is a native, extremely common Windows command. On its own, without other suspicious behavior around it, it isn't distinct enough to trigger a detection.
- **T1112 (Modify Registry — Defense Evasion tactic)**: the test itself was blocked by Falcon's prevention layer (`cmd.exe` was denied access to start) — but the attempt still generated a **High severity Defense Evasion alert**. This shows prevention and detection working together: Falcon didn't just stop the action, it also correctly flagged the attempt as suspicious.

Also hit a real environment issue along the way: Falcon's file-based prevention was deleting the Atomic Red Team test folder before tests could even run. Fixed by creating a scoped file exclusion (`C:\AtomicRedTeam\**`) limited to the test host group only, and confirmed it was applied by checking host group membership, not just waiting.

## Cost
Free — 15-day trial, no credit card.

## Next steps
- Add screenshots to the repo
