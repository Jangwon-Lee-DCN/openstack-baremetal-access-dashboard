# OpenStack Bare Metal Access Dashboard

Horizon panels for the DCN project-scoped bare metal request workflow. The
plugin proxies the authenticated user's token to the internal Bare Metal Access
API; browsers never receive an internal service URL and never access Ironic or
NetBox directly.
