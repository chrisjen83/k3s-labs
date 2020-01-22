# Microk8s Virtual Machine

The files in this folder consist of a self extracting 7zip virtual machine. The virtual machine is targeting the Vmware Workstation 10.x hardware which is compatible with ESXi5.5+, Fusion 6.x+ and Workstation 10.x+. The default configuration consumes only 2 GiB of RAM. You may want to increase this if your pods require more memory to run.

Download all the files and run the K8S.exe on a Windows computer. For Mac and Linux users, you can download the p7zip and 7za packages respectively. On these platforms you can directly decompress the .001 file.

After decompressing, add the virtual machine to your hypervisor of choice.

The default user name and password are provided as an annotation on the VM image itself.

On first boot, you will be prompted to create a config for the default Microk8s installation. It is recommended that you answer yes (or 1) to that prompt.

Please note that this image is NOT secure. It should only be run locally on a secured machine and never in a cloud provider or open to the Internet.
_____________________________________________________________________________________________________________________________________________________________________________________________

[Return to Main Page](https://github.com/chrisjen83/k3s-labs)