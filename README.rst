================================================
PowerAdm - IBM Power/PowerVM Administration tool
================================================

:PowerAdm:      IBM Power/PowerVM Administration tool
:Copyright:     Copyright (c) 2014-2016  Kairo Araujo <kairo@kairo.eti.br>
:License:       BSD
:Development:   https://github.com/kairoaraujo/PowerAdm

PowerAdm is a free (BSD License) tool to administrate IBM Power Logical
Partition (LPAR) creation, operational system deploy and basics PowerVM (VIOS)
troubleshooting.
PowerAdm there is integration with VMware vCenter Ochestrator (vCO), that can
be used as a request portal (Cloud) or integrated with another process
management tool by HTTP REST.

PowerAdm uses a single configuration file and works directly with Hardware
Management Console (HMC). Easy to setup and to uses.

.. image:: http://poweradm.org/img/poweradm-0.13.png

Links
-----

- Website: http://poweradm.org

Features
--------

- Centralized config file
- Supports HMC 7 and 8, including vHMC
- Create Logical Partition (LPAR) profile
- Supports multiple systems/frames
- Supports dual VIOSes
- Virtual SCSI (vSCSI) with automatic mapping between LPAR and VIOSes
- NPIV (vFC/vHBA) with automatic vfcmap between LPAR/VIOSes
- Shared Storage Pool (SSP)
- Add disks from SSP
- Supports multiples Virtual Switches
- Virtual Ethernet Adapter (vNIC)
- Deploy AIX from the NIM Server
- Works with VMware vCenter Orchestrator (vCO)
   - Example Workflow for LPAR creation included!
   - Example Workflow for LPAR Operation System deploy included!
- Possibility to use vCO Portal or integrate with a customized tool or portal
  using HTTP REST to create requests.
- Troubleshooting help
   - Environment (SEA and NPIV)
   - Specific LPAR using ID or searching LPAR (Informations, configurations,
     NPIV, SEA, SCSI etc)
- Optional: Standardized IDs =)

Latest release
--------------

https://github.com/kairoaraujo/PowerAdm/releases

Installation
------------

See INSTALL file or go to http://poweradm.org


How is it developed?
--------------------

It's developed using Python and uses some Shell Scripting.
I'm a sysadmin not a developer so sorry if it is not looking great. Your help
is important and kindly accept to improve the tool.

If you don't have an HMC and a Power to run tests, don't worry. I've an some
code with simulation on createlparconf.py, newid.py. Directory simulation is
available upon request.

License
-------

This software is BSD License. Please more details in LICENSE file.

IMPORTANT:
IBM, PowerVM (a.k.a. VIOS), smitty are registered trademarks of IBM Corporation
in the United States, other countries, or both.

VMware, vCenter, vCenter Orchestrator are registered trademarks of VMware Inc
in the United States, other countries, or both.
