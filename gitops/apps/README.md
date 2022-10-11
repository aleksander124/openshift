#### Migrating Service Connections to another cluster

Assuming we want to migrate from ss to new-ss.

1. Make sure `adoServiceConnectionCreator.clusterPrefix` is the same on ss and
   new-ss so that Service Connection names are the same between ss and new-ss.
2. Define Service Connections in ss and set
   `adoServiceConnectionCreator.enabled` to `true`. cronjobs create Service
   Connections.
3. Switch deployments in ADO to use newly created Service Connections.
4. Set `adoServiceConnectionCreator.enabled` to `false` in ss. This will
   prevent helm from generating cronjobs in ss. Run prun in argo. Cronjobs are
   deleted.
5. Define Service Connections in the new-ss namespaces. Set
   `adoServiceConnectionCreator.selfHeal` to `"true"` (this will instruct the
   script to update Service Connections) and
   `adoServiceConnectionCreator.enabled` to `true`. Synchronize argo. Cronjobs
   on the new-ss overwrite Service Connections with the same name to use the
   new cluster - `adoServiceConnectionCreator.clusterPrefix` helm variable name
   ensures the name of SC is the same.
6. Set `adoServiceConnectionCreator.selfHeal` to `"false"` to disable updating
   Service Connections.