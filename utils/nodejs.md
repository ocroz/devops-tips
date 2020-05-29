# node js

```bash
sudo yum install epel-release -y
curl --silent --location https://rpm.nodesource.com/setup_12.x | sudo bash -
sudo yum install nodejs git -y
```

```bash
git clone https://github.com/floyd-may/hwaas.git
cd hwaas
npm install && npm run-script build
node .
```
