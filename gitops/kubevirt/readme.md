<h2>Virtual Machines as Code with OpenShift GitOps and OpenShift Virtualization</h2>
<h4>Prerequisites</h4>
OpenShift GitOps from the Operator Catalog and ensure a supported storage class is available for automated PVC provisioning.

<h4>Use Case: Installing OpenShift Virtualization</h4>
OpenShift Virtualization is simple to install through the Operator Hub, but there are benefits to installing it via OpenShift GitOps. Placing the OpenShift Virtualization configuration under revision control could prove valuable. In addition, using an ArgoCD application to install OpenShift Virtualization allows us to define role bindings so ArgoCD can manage the custom resources provided by OpenShift Virtualization.

The following YAML directs ArgoCD to create an OpenShift Virtualization deployment on the cluster based on the kustomization.yaml manifest in the same directory. Important features to note are:

1. The destination namespace is set to default. This has no effect on where the operator installs because all the YAML manifests include .metadata.namespace
2. repoURL should be replaced with your own fork of the repo if you ran setup/install.sh
3. The application here is set to automatically synchronize. This means once the YAML is applied to the cluster, ArgoCD will start reconciling it immediately. We will discuss later why sometimes it is better to adopt a manual synchronization process.

```