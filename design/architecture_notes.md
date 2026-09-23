# Architecture Notes

Layered design: UI -> application services -> relational data store.
Enterprise systems (SAP, L2L, DP3) remain systems of record; this system stores references and workflow coordination data.
Security controls include authentication, RBAC, validation, HTTPS, audit logging, and backups.
