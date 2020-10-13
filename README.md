Reference Steps for new project:
sudo apt-get install curl python-software-properties
curl -sL https://deb.nodesource.com/setup_12.x | sudo bash -
sudo apt-get install -y nodejs
node -v
npm -v

npm init -y
npm install --save discord.js dotenv

make file called ".env" that contains one line
DISCORD_TOKEN=[INSERT YOUR TOKEN HERE]

make file called "bot.js"

node version expected: 12.18.3
npm version expected: 6.14.6

# cbusbot
run command in linux terminal:
node bot.js

// makes git store credentials
git config --global credential.helper store

// clone command
git clone https://github.com/warebec/cbusbot.git

// commit local changes
git add .
git commit -m "added birthday function for hot dog" -a
git push

// on bot server, pull changes, restart bot
pm2 stop bot.js
git pull
pm2 start bot.js

// to see logs
pm2 logs
