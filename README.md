[![CodeQL](https://github.com/Shield-Cyber/ShieldCyber-REST-API/actions/workflows/codeql.yml/badge.svg)](https://github.com/Shield-Cyber/ShieldCyber-REST-API/actions/workflows/codeql.yml)

# Shield Scanner

Shield Cyber's network-based scanner that connects to the Shield platform is maintained and updated in this repository.  This scanner should be used for internal network vulnerability scans or discovery scans for different network locations where it will be deployed.  Before proceeding to install the scanner, please make sure you have the following required values to link the scanner properly:
  - **Subscription ID** - Subscription ID where the scanner needs to link back to.
  - **Location Name** - Location name where the scanner is deployed. Users should create this value and make sure it is unique for each subscription.
  - **API Key** - API Key located within the [**My Account**](https://platform.shieldcyber.io/account) page, under the **Subscriptions** tab.  Use the `Copy` button within the Subscriptions table to access the API Key.

To install the scanner, please follow the platform-specific instructions below.  You may also refer to the Shield Platform Documentation site, which can be found here: [Shield Platform Documentation](https://docs.shieldcyber.io).

## Installation Instructions

### Linux-Based OS (Preferred)
To install on a Linux based OS, there is a single script that can be downloaded and executed to install and start the Shield service.  Once the Shield service is installed, the scanner can then be installed, where the password needs to be set.

#### Download the Install.sh Script

`sudo wget https://raw.githubusercontent.com/Shield-Cyber/ShieldCyber-REST-API/main/install.sh`

#### Install & Deploy the Shield Service

`sudo ./install.sh -s 'SUBSCRIPTION-ID' -l 'LOCATION' -k 'API-KEY'`

#### Install & Configure the Shield Scanner

`sudo shield -I -P 'CREATE-SCANNER-PASSWORD'`

### Windows or MacOS

There are limitations installing the Shield scanner on Windows systems.  Specifically, to run the scanner, the Windows host needs to have Docker Desktop installed which can only run on Windows workstations.  Additionally, the installation process is not as automated as the Linux versions of the deployment.

#### Dependencies

To install the Shield scanner successfully on a Mac or Windows 10/11 OS, WSL (Windows only) and Docker Desktop need to be installed and available.  Once Docker Desktop is installed, make sure the Docker engine is started before attempting to install the Shield Scanner.

- [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

#### Install & Configure the Shield Scanner

1. Download and unzip this repository: [Shield Scanner](https://github.com/Shield-Cyber/ShieldCyber-REST-API/archive/refs/heads/main.zip)
2. Unzip the folder contents
3. Navigate to the *ShieldCyber-REST-API-main* folder
4. Open the *example.env* file within a text editor & change the `yourpasswordhere` value and save
5. Re-name the example.env file as .env
6. Open a command prompt as administrator, and navigate to the *ShieldCyber-REST-API-main* folder
7. Install and start the Shield scanner with the following command: `docker compose up -d`

**Note**: You will need to install the Shield Cyber Agent.Shield service following the instructions within the [Shield Documentation](https://docs.shieldcyber.io/docs/deployment/network-scans.html) and use the Shield Service MSI to complete the Agent.Shield service installation.

## Link the Shield Scanner within the Platform
To use the scanner, it will need to be linked within the Shield platform.  To complete this step, navigate to the **Settings** -> **Scan Config** -> **Shield** page, click **New Configuration**, and then enter the following values, then save the created configuration:
  - **Location** - Select the location that was created for the scanner that is being linked.  The Shield service needs to be installed and running for the Location value to populate.
  - **Access Key** - Enter the username for the scanner.  **Admin** is the default username for all Shield scanner installations.
  - **Secret Key**: Enter the password for the scanner that had previously been created.
  - **API URL**: Enter the URL for the API of the scanner.  By default the API runs on port 8000, so if the scanner is running on the same device where the service is running, then the API value would be the following `https://localhost:8000/`

### Notes
- Username is _admin_
- Startup of services may take a few minutes as the databases need to update before the scanner can create and start scans.
- Windows and MacOS Environments need to have a user login to the system _BEFORE_ the docker engine will start, this installation is not reccomended for an unattanded or server setup.
