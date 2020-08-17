require('dotenv').config();
const Discord = require('discord.js');
const client = new Discord.Client();
const cron = require("node-cron");

var fs = require('fs');
var inspirationalImages = fs.readdirSync('./inspirePics');
var twerks = fs.readdirSync('./twerking');

client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
});

client.on('message', msg => {
  // replies to "ping" with "pong"
  if (msg.content.toLowerCase() === 'ping') {
    msg.reply('pong');
  }
  // replies to mentions
  if (msg.mentions.has(client.user)) {
    if (new RegExp("\\binspire\\b").test(msg.content.toLowerCase())) {
      // ... containing "inspire" with image from inspire folder
      var chosen = inspirationalImages[Math.floor(Math.random() * inspirationalImages.length)];
      msg.channel.send('', {files: ['inspirePics/' + chosen]});
    } else if (msg.member != null && msg.member.id === '325030773054767133') {
      // ... from me with "Your wish is my command"
      msg.reply('Your wish is my command');
    } else {
      // ... with "Greetings fleshbags!" as default
      msg.reply('Greetings fleshbags!');
    }
  }
  // replies to messages containing "vore" with "YOU RUINED IT!" and puts the vore image in shitposting
  if (new RegExp("\\bvore\\b").test(msg.content.toLowerCase())) {
    msg.reply('YOU RUINED IT!');
    client.channels.fetch('555243907534028834').then(channel => channel.send('<@' + msg.member + '> reset the count', {files: ["vore.png"]}));
  }
  // replies to "she bite" with "SHE NO BITE!!"
  if (msg.content.toLowerCase() === 'she bite' || msg.content.toLowerCase() === 'cosette bite' || msg.content.toLowerCase() === 'cossete bite') {
    msg.reply('SHE NO BITE!!');
  }
  // replies to mentions of food channel with "Every channel is food channel"
  if (msg.mentions.has('573026220833243137')) {
    var picking = new Date().getTime();
    if (picking % 2 == 1) {
      msg.channel.send('', {files: ["food.png"]});
    } else {
      msg.channel.send('Every channel is food channel');
    }
  }
  // replies to messages containing "compiling" with xkcd comic
  if (new RegExp("\\bcompiling\\b").test(msg.content.toLowerCase())) {
    msg.channel.send('', {files: ["compiling.png"]});
  }
  // replies to messages from elle (or me) containing "dance" with twerking gif
  if (msg.member != null && (msg.member.id === '533716168062664742' || msg.member.id === '325030773054767133') && new RegExp("\\bdance\\b").test(msg.content.toLowerCase())) {
    var chosen = twerks[Math.floor(Math.random() * twerks.length)];
    msg.channel.send('', {files: ['twerking/' + chosen]});
  }
});

// feature removed by request
// every morning at 8, put image from inspirePics folder into support channel
//cron.schedule("0 8 * * *", function() {
//  var chosen = inspirationalImages[Math.floor(Math.random() * inspirationalImages.length)];
//  client.channels.fetch('630807691291525131').then(channel => channel.send('', {files: ['inspirePics/' + chosen]}));
//});

client.login(process.env.DISCORD_TOKEN);
