# Agador
Agador is a tool that collects operational data from the network and stores it in a database. It's intended to be a replacement for rancid
and other perl tools that currently handle this for us.

Note that the name isn't an acronym for anything, I just needed to not call this code "new rancid" anymore so I named it after Agador Sparticus - my favorite character
from one of my favorite movies.

## Overview
Agador brings together several different tools:
* **Netbox** is used as an inventory source for devices.
* **Cyberark** is used as the source for credentials (but plain text creds work too).
* **[umnet-napalm](https://github.com/umich-its-networking/umnet-napalm)** is custom code based on [NAPALM](https://github.com/napalm-automation/napalm) that runs various commands on network devices and returns normalized data across all vendors.
* **[umnet-db](https://github.com/umich-its-networking/umnet-db)** is the custom database where this normalized data is stored.
* **git** is how we store versioned data in files - stuff that we don't want to put in umnet-db. Currently this is just [config backups](https://github.com/umich-its-networking/umnet-config-backups), but could be expanded to include other things if applicable.
* **[Nornir](https://github.com/nornir-automation/nornir)** manages this whole process. This is a public library that provides Ansible-like functionality - it runs a series of tasks across a set of devices and do stuff with the results.

## Inventory Filters
One thing that Agador is concerned with is how to identify different subsets of devices within your inventory. This allows you to restrict gathering certain types of data to only certain types of devices - you don't really want to do 'show mpls' on a firewall, for example. To that end, you must provide Agador with a file that defines [Nornir inventory filter functions](https://nornir.readthedocs.io/en/latest/tutorial/inventory.html#Filter-functions). These functions can then be referenced in the *Command Map* and *Credential Map* (more details below). Here are some notable examples - see `inventory_filters.py` in the `examples` directory of this repo for more.
```
### identifies a specific host by name
def fw_cpp(host):
    return host.name == "fw-cpp"

### Identifies any host that starts with 'ngfw'
def ngfw(host):
    return host.name.startswith("ngfw")

### Identifies netbox roles that map to devices that route
def routers_filter(host):
    """
    Netbox roles that indicate a router
    """
    return host.data["role"]["slug"] in [
        "core",
        "bin",
        "data-center",
        "distribution",
        "security",
        "ngfw",
        "legacy-bin",
        "legacy-core",
        "legacy-data-center",
        "legacy-distribution",
    ]
```

## Command Map
The heart of Agador is the command map file. See `command_map.yml` in the example folder of this repo. The first section of the file is where you specify which device role(s) in Netbox are relevant to Agador.
If this section is commented out, all devices will be considered - but they must be of status *Active* and have a *Primary IP* address, otherwise they will be ignored no matter what.
```
netbox_roles:
  - av
  - access-layer-switch
  - bin
```

The *commands* section is where you specificy what data to gather, how often, from what subset of devices, and how to store that data.
```
commands:

  config:
    frequency: 0 0 * * *
    getter: get_config
    save_to_file:
      mapper: SaveConfig
      destination: ${FILES_DIR}/umnet-config-backups

  lldp_neighbors:
    frequency: 0 0 * * *
    getter: get_lldp_neighbors
    inventory_filter: non_security_filter
    save_to_db: UpdateNeighbor
```

Let's talk about the components of each command:
| Parameter  | Required | Description |
| ------------- | ------------- | ------------- |
| frequency  | Yes | How often to run this command in crontab format |
| getter  | Yes | The [umnet-napalm getter](https://github.com/umich-its-networking/umnet-napalm/blob/main/umnet_napalm/abstract_base.py) to run for this command |
| inventory_filter | No | A [Nornir inventory filter function](https://nornir.readthedocs.io/en/latest/tutorial/inventory.html#Filter-functions) in the `inventory_filters.py` file that defines which types of devices this command should run against |
| save_to_file | No* | If the resulting data should be saved to a file, specify how this should be done with the following required sub-arguments:<br>    _mapper_ - name of mapper class in `agador.mappers.save_to_file` to use<br>    _destination_ - destination directory for the data<br> |
| save_to_db | No* | If the resulting data should be saved to umnetdb, the name of the mapper class in `agador.mappers.save_to_db` to use to save the data. Note that before a new mapper can be created, a corresponding model must be built in [umnet-db](https://github.com/umich-its-networking/umnet-db) |

*Note: You must specify at least one of `save_to_file` or `save_to_db` so Agador knows what to do with the data it pulls. You can specify both if applicable.

## Credential map
The credential map file tells Agador how to retrieve credentials for logging into the devices. Currently two methods of credential retrieval are supported - Cyberark and plaintext. Here's an example:
```
defaults:
  mapper: cyberark_umnet
  username: automaton
  password: automaton_user_automaton
  enable: Infrastructure_from_2020-05-01_to_current_enable

custom:

  - inventory_filter: fw_cpp
    mapper: cyberark_nso
    username: srancid
    password: fw-cpp_srancid
    enable: fw-cpp_enable

  - inventory_filter: fw_uhs
    mapper: plaintext
    username: srancid
    password: Abc123!
```

Let's talk about the components of each section:
| Parameter  | Required | Description |
| ------------- | ------------- | ------------- |
| mapper | Yes | How to look up the password and enable. Three methods are currently supported: cyberark_nso, cyberark_umnet, and plaintext. |
| username | Yes | Credential username |
| password | Yes | Credential password. For cyberark, provide the string to query the Cyberark API for that will return the password. For plaintext, just provide the password in plain text. |
| enable | default only | Credential enable. You must provide this in the `defaults` section, it's optional in the `custom` section. |
| inventory_filter | custom only | Required when providing a custom credential. This is a reference to a filter function in your `inventory_filters.py` file that tells agador which hosts the custom parameter applies to |

Note that when deciding which custom credentials apply to which hosts, the first custom match will be applied. So if your matches overlap, it's best to put the most specific ones at the top and more broad ones below.
If no match is found for a host in the `custom` section, the `default` credentials will apply.

The credential map is located at `/etc/agador/credential_map.yml` on wintermute.

## Running Agador
#### agador-run
`agador-run` runs everything once, ignoring the `frequency` value for each command in the command map. You can restrict the run to a specific device, a specific Netbox device role, or a
subset of commands. For example, the following command will pull lldp neighbors off of dl-arbl-1 and store them in the umnet-db.
```
agador-run --cmds lldp_neighbors --device dl-arbl-1
```
This command will pull the arp and route tables off of all the non-legacy DLs and store them in the umnet-db. The `role` must match a Netbox device role.
```
agador-run --cmds arp_table,route  --role distribution
```
Note that this command does consult the **command_map** to tell it what commands are relevant for what devices. If you try to
run a command on a device or a role that does not match the `inventory_filter` function (ie like running `arp_table` for an AL), you won't get any results.

Use `--help` to see all options, you'll see a lot of logging options as well.

#### agador-run-with-schedule
`agador-run-with-schedule` is designed to run forever as a background process. It pulls data from the network at regular intervals based on the **command_map** file.

## Configuration
Agador requires you to provide it with a path to a configuration file, either on the cli when you invoke it, or as the environment variable `AGADOR_CFG`.
On wintermute this config file is located at `/etc/agador/agador.conf`. `/etc/profile.d/agador.sh` sets `AGADOR_CFG` to this file for all users when they log in.
Look at the example config file in the `examples` folder of this repo for details on what parameters are required.




