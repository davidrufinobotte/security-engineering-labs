# Security Engineering Labs

Hands-on labs built to apply my Microsoft 365 / Intune / endpoint background to security engineering — identity security, SIEM, and EDR. Built while preparing for a transition from Senior Desktop Engineer to Security Engineer.

## Labs

### 1. [Entra ID + Sentinel — Automated Sign-In Risk Detection & Response](./entra-sentinel-detection/README.md)
End-to-end pipeline: risky sign-in → Sentinel detection → incident → automated email alert. Covers SIEM engineering, KQL, Conditional Access, and incident triage.

### 2. [CrowdStrike Falcon API — Detection Lab](./crowdstrike-falcon-api/README.md)
API access to Falcon EDR, real detection generated via a safe MITRE ATT&CK simulation (Atomic Red Team), read back through a Python script using FalconPy.

## Why these labs
Both labs follow the same idea: build something real, break it, fix it, and document what happened — not just follow a tutorial. Each README includes the real problems I hit along the way (expired API, wrong permission scopes, deprecated features, wrong test method) and how I solved them.

## About
David Botte — Senior Desktop Engineer at NZX Limited, working toward Security Engineer.
[linkedin.com/in/david-rufino-botte](https://linkedin.com/in/david-rufino-botte)
