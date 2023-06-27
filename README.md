# Installation Instructions

## Linux

#### Dependecies
- [Docker Engine](https://docs.docker.com/engine/install/#server)

Ubuntu / Apt Package Manager Commands - For other systems click the link above.
```
sudo apt-get remove docker docker-engine docker.io containerd runc

sudo apt-get update
sudo apt-get install ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo done
```

#### Install
- Clone this Repo
- CD into Cloned Directory
- Change Default Password, Modify the '_example.env_' File and rename to '_.env_' This password is recommended to be at minimum 12 characters in length and complex.
  - **IMPORTANT NOTE**: Upon first startup the REST API will save the password set and it will not be able to be changed without deleting the _redis-db_ docker container and its associated volume.
  - If you do not modifiy this file the password defaults to _admin_
- Run Command `docker compose up -d`

#### Services
- API: https://x.x.x.x:8000
- Greenbone UI: http://x.x.x.x:9392

#### Notes
- Username is admin
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
- Username is admin
- Startup of services may take a few minutes as the databases need to update before the scanner can create and start scans.
- Windows and MacOS Environments need to have a user login to the system _BEFORE_ the docker engine will start, this installation is not reccomended for an unattanded or server setup.

# Future Additions

API Endpoints that **CAN** be added, only a small subset have been added at this point in time.

https://greenbone.github.io/python-gvm/api/api.html
