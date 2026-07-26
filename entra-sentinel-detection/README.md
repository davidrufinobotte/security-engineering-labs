# Automated Sign-In Risk Detection & Response — Entra ID + Sentinel

A hands-on lab building an end-to-end detection and automated response pipeline, using Microsoft Entra ID, Microsoft Sentinel, and Logic Apps. Built to apply my Microsoft 365 / Intune / endpoint background to security engineering and SIEM operations.

## Architecture

```
Entra ID (Sign-in Logs)
   → Log Analytics Workspace
   → Sentinel Analytics Rule
   → Incident Created
   → Automation Rule
   → Logic App Playbook → Email Alert
```

## What it does
- Ingests Entra ID sign-in logs into Sentinel
- Runs a scheduled detection rule every 5 minutes
- Auto-creates an incident when triggered
- Triggers a Logic App playbook that sends an email alert with incident details (title, severity, link)

## Key decisions
- **Reused an existing Conditional Access policy** instead of creating a duplicate, after auditing the tenant's current controls
- **Email alert, not auto-containment** — safer choice for a single-admin test tenant, while still proving the full pipeline works
- **Logic App on Consumption plan**, not Standard, to avoid fixed hosting costs
- **Manually triaged and closed all test incidents** as *Benign Positive*, with notes — standard SOC practice, not blanket dismissal

## Problems solved along the way
- Cross-tenant Azure subscription setup failed repeatedly (expired transfer) — fixed by explicitly specifying accepting account and destination tenant
- Entra ID data connector was missing — required installing it from the Sentinel Content Hub first
- Avoided a soon-to-be-retired feature (legacy Identity Protection risk policy) in favor of the supported Conditional Access path
- Playbook wasn't selectable in the automation rule — fixed via Sentinel permissions on the Logic App
- Alerts appeared "missing" from Incidents — turned out to be a UI filter issue, not a broken rule

## Environment & cost
Microsoft 365 Developer tenant + Azure Pay-As-You-Go. Total cost: under US$5, using Sentinel's free ingestion trial and Logic Apps' pay-per-execution pricing.

## Possible next steps
- Filter detection specifically on sign-in risk level (medium/high)
- Replace email alert with automated containment in a governed environment
- Extend the same pattern to a CrowdStrike Falcon EDR data source
