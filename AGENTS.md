# Bare Metal Access Horizon plugin contract

Read `/home/ubuntu/AGENTS.md` first. This repository owns only the Horizon UI,
forms, same-origin proxy views, URLs, visibility rules, and browser workflows
for project-scoped bare metal requests. The access API and Ironic/NetBox
reconciliation belong to `netbox-ironic-controller`; deployment and live
topology belong to the authoritative platform repositories.

Never expose BMC data or credentials. Full Ironic administration and approval
UI require the exact DCN project UUID and `baremetal_admin`; requester UI
requires a project-scoped token and an explicit bare metal requester/operator
role. Run the complete test suite before completion.
