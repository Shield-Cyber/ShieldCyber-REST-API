# Default Creds
- admin/admin

To change default environment variables look at 'example.env' file and rename to '.env' after options have been set.

API Endpoints that **CAN** be added, only a small subset have been added at this point in time.
https://greenbone.github.io/python-gvm/api/api.html

### [Linux Install](Linux)
### [Windows Install](Windows-or-MacOS)

# Installation Instruction

## Linux

#### Dependecies
- [Docker Engine](https://docs.docker.com/engine/install/)

#### Install
- Clone this Repo
- CD into Cloned Directory
- Run Command `docker compose up -d`

#### Notes
- Startup may take a few minutes as the databases need to update before the machine can create and start scans.

## Windows or MacOS

#### Dependecies
- [Docker Engine](https://docs.docker.com/engine/install/)

#### Install
- Clone this Repo
- CD into Cloned Directory
- Run Command `docker compose up -d`

#### Notes
- Startup may take a few minutes as the databases need to update before the machine can create and start scans.
- Windows and MacOS Environments need to have a user login to the system _BEFORE_ the docker engine will start, this installation is not reccomended for an unattanded or server setup.
