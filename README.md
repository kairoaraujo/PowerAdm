# Power Adm - Power Administration to cloud

## Why this software

Who manages environment with IBM Power through the Hardware Management Console (HMC) or Integrated Virtualization Manager (IVM) know that we have an easy management creating LPAR, but we need to manage the IDs of devices, such as virtual network, virtual fiber channel, virtual scsi etc.

Although an easy runs it is necessary to manage information such as maximum and minimum memory and CPUs.

These IDs are well organized, assist in the identification of devices, particularly in times of troubleshooting.
These IDs also help in managing the Live Partition Mobility, that is, if well organized will remain independent of the box.

The objective of this application in the first instance, is to adopt a standard IDs based on LPAR ID and facilitate the creation for the team avoiding filling more complex information, facilitating the use of analysts with a knowledge in Power not as advanced.

For this, the following rule was established:

All LPAR has a maximum number of virtual devices 40 and the following structure:
Virtual Network IDs will be between 10 and 19
Virtual SCSI IDs will be between 20 and 29 (default 21 primary VIO, 22 secondary VIO)
Virtual Fibre Channel IDs will be between 30 and 39 (default 33 primary VIO, 34 secondary VIO)

In "VIOS" settings have the following default:
Maximum number of virtual devices in VIO Primary is 3500 and Secondary VIO 4500 allowing a total of 500 LPARs on the set of VIOS

Virtual SCSI IDs:  the VIO Primary 1 + 'LPAR ID' and on VIO Secondary 2 + 'LPAR ID'
Fiber Channel IDs: the VIO Primary 3 + 'LPAR ID' and on VIO Secondary 4 + 'LPAR ID'

Example:

VIOS1 - ID: 1 Maximum number of virtual IDs: 3500
VIOS2 - ID: 2 Maximum number of virtual IDs: 4500

LPAR AIX1
ID: 11
Virtual devices:
- 11: Network adapter date
- 12: Network adapter backup
- 21: Virtual SCSI (Server: 111 VIOS1)
- 22: Virtual SCSI (Server: 211 VIOS2)
- 33: Fiber Channel (Server: 311 VIOS1)
- 34: Fiber Channel (Server: 411 VIOS2)

LPAR AIX1
ID: 12
Virtual devices:
- 11: Network adapter date
- 12: Network adapter backup
- 21: Virtual SCSI (Server: 112 VIOS1)
- 22: Virtual SCSI (Server: 212 VIOS2)
- 33: Fiber Channel (Server: 312 VIOS1)
- 34: Fiber Channel (Server: 412 VIOS2)


VIOS1
ID: 1
Virtual devices:
- 111 Virtual SCSI (Client ID: 11 / Virtual Client: 21)
- 112 Virtual SCSI (Client ID: 12 / Virtual Client: 21)
- 311 Fiber Channel (Client ID: 11 / Virtual Client: 33)
- 312 Fiber Channel (Client ID: 12 / Virtual Client: 33)

VIOS2
ID: 2
Virtual devices:
- 211 Virtual SCSI (Client: 11 / Virtual Client: 22)
- 212 Virtual SCSI (Client: 12 / Virtual Client: 22)
- 411 Fiber Channel (Client: 11 / Virtual Client: 34)
- 412 Fiber Channel (Client: 12 / Virtual Client: 34)


With this example we can see how easy it is to identify within the VIO's virtual devices, searching for the partition ID.

## How is it development?

It's developing using Python and uses some Shell Scripting.
I'm not a developer. I'm a System Administrator. Please sorry if not look great but your help is important to improve.

If you don't have an HMC and a Power to run tests, don't worry. I've an some codes with simulation on createlparconf.py, newid.py. D
irectory simulation is available upon request.


