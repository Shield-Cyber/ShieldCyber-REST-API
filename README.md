[![CodeQL](https://github.com/Shield-Cyber/OpenVAS-REST-API/actions/workflows/codeql.yml/badge.svg)](https://github.com/Shield-Cyber/OpenVAS-REST-API/actions/workflows/codeql.yml)

# Installation Instructions

[Linux Script (Recommended Method)](#install-via-script)

[Linux Manual](#linux)

[Windows/MacOS Manual](#windows-or-macos)

## Linux

#### Dependecies
- [Docker Engine](https://docs.docker.com/engine/install/#server)

Ubuntu / Apt Package Manager Installation Script

Download
```
git clone https://github.com/Shield-Cyber/ShieldCyber-REST-API.git
```

Install dependencies and start the Shield Scanner

```
cd ShieldCyber-REST-API/ && ./install.sh
```

#### Install
- Clone this Repo
- CD into Cloned Directory
- Change Default Password, Modify the '_example.env_' File and rename to '_.env_' This password is recommended to be at minimum 12 characters in length and complex.
  - **IMPORTANT NOTE**: Upon first startup the REST API will save the password set and it will not be able to be changed without deleting the _redis-db_ docker container and its associated volume.
  - If you do not modifiy this file the password defaults to _admin_
- Run Command `docker compose up -d`

#### Install Via Script
- Make Dir for Install
- CD into Dir
- Download File
- `wget https://raw.githubusercontent.com/Shield-Cyber/ShieldCyber-REST-API/main/install.sh`
- Run install.sh
- Follow Prompts

#### Services
- API: https://x.x.x.x:8000
- Greenbone UI: http://x.x.x.x:9392

#### Notes
- Username is _admin_
- Startup of services may take a few minutes as the databases need to update before the scanner can create and start scans.

## Windows or MacOS

#### Dependecies
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

#### Install
- Clone this Repo
- CD into Cloned Directory
- Change Default Password, Modify the '_example.env_' File and rename to '_.env_' This password is recommended to be at minimum 12 characters in length and complex.
  - **IMPORTANT NOTE**: Upon first startup the REST API will save that password set and it will not be able to be changed without deleting the _redis-db_ docker container and its associated volume.
  - If you do not modifiy this file the password defaults to _admin_
- Run Command `docker compose up -d`

#### Services
- API: https://x.x.x.x:8000
- Greenbone UI: http://x.x.x.x:9392

#### Notes
- Username is _admin_
- Startup of services may take a few minutes as the databases need to update before the scanner can create and start scans.
- Windows and MacOS Environments need to have a user login to the system _BEFORE_ the docker engine will start, this installation is not reccomended for an unattanded or server setup.

# Future Additions

API Endpoints that **CAN** be added, only a small subset have been added at this point in time.

https://greenbone.github.io/python-gvm/api/api.html
