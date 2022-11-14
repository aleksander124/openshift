# Openshift installation

Everything is base on official openshift installation documentation: [openshift](https://docs.openshift.com/container-platform/4.7/installing/installing_bare_metal/installing-bare-metal.html)

## Requirements

### VMs

1. One bootstrap machine
2. Three control plane, or master, machines
3. Workers
4. The bootstrap and control planes must be use Red Hat Enterprise Linux CoreOS, Compute machines canchoose between RHCOS or RHEL

### Network

All the Red Hat Enterprise Linux CoreOS (RHCOS) machines require network in initramfs during boot to fetch Ignition config files from the Machine Config Server. During the initial boot, the machines require either a DHCP server or that static IP addresses be set in order to establish a network connection to download their Ignition config files. Additionally, each OpenShift Container Platform node in the cluster must have access to a Network Time Protocol (NTP) server. If a DHCP server provides NTP servers information, the chrony time service on the Red Hat Enterprise Linux CoreOS (RHCOS) machines read the information and can sync the clock with the NTP servers.

### Createing the user-provisioned infrastructure

1. Configure DHCP or set static IP addresses on each node.
2. Provision the required load balancers.
3. Configure the ports for your machines.
4. Configure DNS.
5. Ensure network connectivity.

### Installing the OpenShift CLI by downloading the binary

1. Navigate to the [OpenShift Container Platform downloads page](https://access.redhat.com/downloads/content/290) on the Red Hat Customer Portal.
2. Select the appropriate version in the Version drop-down menu.
3. tar xvzf <...>
4. Place binary in $PATH

## Installation configuration parameters

When you create the install-config.yaml installation configuration file, you provide values for the required parameters through the command line. If you customize your cluster, you can modify the install-config.yaml file to provide more details about the platform.

All parameters you can find here: [parameters](https://docs.openshift.com/container-platform/4.7/installing/installing_bare_metal/installing-bare-metal.html)

### Sample install-config.yml for bare metal

```yaml
apiVersion: v1
baseDomain: example.com 
compute: 
- hyperthreading: Enabled 
  name: worker
  replicas: 0 
controlPlane: 
  hyperthreading: Enabled 
  name: master
  replicas: 3 
metadata:
  name: test 
networking:
  clusterNetwork:
  - cidr: 10.128.0.0/14 
    hostPrefix: 23 
  networkType: OpenShiftSDN
  serviceNetwork: 
  - 172.30.0.0/16
platform:
  none: {} 
fips: false 
pullSecret: '{"auths": ...}' 
sshKey: 'ssh-ed25519 AAAA...' 
```

## Creating the Kubernetes manifest and Ignition config files

Because you must modify some cluster definition files and manually start the cluster machines, you must generate the Kubernetes manifest and Ignition config files that the cluster needs to make its machines.

The installation configuration file transforms into the Kubernetes manifests. The manifests wrap into the Ignition configuration files, which are later used to create the cluster.

### Prerequisites

1. You obtained the OpenShift Container Platform installation program.
2. You created the `install-config.yaml` installation configuration file.

### Procedure

1. Change to the directory that contains the installation program and generate the Kubernetes manifests for the cluster:

```shell
./openshift-install create manifests --dir <installation_directory>
```
