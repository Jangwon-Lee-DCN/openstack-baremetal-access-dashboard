# OpenStack Bare Metal Access Dashboard

Horizon panels for the DCN project-scoped bare metal request workflow. The
plugin proxies the authenticated user's token to the internal Bare Metal Access
API; browsers never receive an internal service URL and never access Ironic or
NetBox directly.

The project panel uses an instance-style inventory: pending and completed
requests plus active leases are shown in one table, request and launch forms
open as modals, and request details include sanitized hardware identity and
operation history. Node actions are rendered only for an active lease in the
current project. A DCN-domain `member` may request capacity; a project `admin`
or explicit `baremetal_operator` may launch, power, and return its leased node.
Neither domain membership nor a role in another project grants project access.
