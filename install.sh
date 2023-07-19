echo Installing OpenVAS and its Dependencies
echo This version of OpenVAS has an additional piece of software to allow for the Shield Agent to connect to it via an API.

read -p "Do you want to continue? (Y/N): " answer

if [[ $answer == [Yy] ]]; then
    echo "Continuing..."
elif [[ $answer == [Nn] ]]; then
    echo "Exiting..."
    exit 0
else
    echo "Invalid input. Please answer with Y or N."
fi

echo Installing Docker...

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
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

echo Docker Installed!

echo Downloading OpenVAS Compose File...

wget https://raw.githubusercontent.com/Shield-Cyber/OpenVAS-REST-API/main/compose.yml

echo OpenVAS Compose File Downloaded!

read -sp "Enter OpenVAS / API Admin Password: " password

touch .env

echo "PASSWORD=$password" >> .env

docker compose up -d
