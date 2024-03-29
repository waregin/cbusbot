import dotenv from "dotenv";
import { Client, GatewayIntentBits } from "discord.js";
import cron from "node-cron";
import fs from "fs";
import lineReader from "line-reader";
import schedule from "node-schedule";
import fetch from "node-fetch";

dotenv.config();
const client = new Client({intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent, GatewayIntentBits.GuildMembers]});
const cbusGuildID = '555243907534028830';

var inspirationalImages = fs.readdirSync('./inspirePics');
var twerks = fs.readdirSync('./twerking');
var generalChannelID = '766529200113975327';

async function searchForGif(searchTerm, chan) {
    var url = 'https://g.tenor.com/v1/search?q=' + searchTerm + '&key=' + process.env.TENORKEY + '&limit=25';
    var response = await fetch(url);
    var json = await response.json();
    var chosen = Math.floor(Math.random() * json.results.length);
    var chosenGif = json.results[chosen].url;
    chan.send(chosenGif);
}

//client.on('debug', console.log);
client.login(process.env.DISCORD_TOKEN);

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);

    // commenting out birthday role feature for now, to be improved
    // assigns birthday role and sends birthday greeting in general based on dates in file
//  var birthdayRole = client.guilds.cache.get(cbusGuildID).roles.cache.get('604442101425504261');
//  lineReader.eachLine('birthdates.txt', function(line) {
//    var info = line.split(' ');
//    var birthdayMember = client.guilds.cache.get(cbusGuildID).members.cache.get(info[0])
//    var job = schedule.scheduleJob({month: info[1], date: info[2], hour: 0, minute: 0}, function(){
//      birthdayMember.roles.add(birthdayRole);
//      client.channels.fetch('681914541029982268').then(channel => channel.send('<@' + birthdayMember + '> HAPPY BIRTHDAY!', {files: ["birthday.jpeg"]}));
//    });
//    //console.log(job.nextInvocation());
//    // removes role next day
//    var revertJob = schedule.scheduleJob({month: info[1], date: parseInt(info[2]) + 1, hour: 0, minute: 0}, function(){
//      birthdayMember.roles.remove(birthdayRole);
//    });
//    //console.log(revertJob.nextInvocation());
//  });
});

client.on('messageCreate', msg => {
  // replies to "ping" with "pong"
  if (msg.content.toLowerCase() === 'ping') {
    msg.reply('pong');
  }
  // replies to mentions
  if (!msg.mentions.everyone && msg.mentions.has(client.user)) {
    if (new RegExp("\\binspire\\b").test(msg.content.toLowerCase())) {
      // ... containing "inspire" with image from inspire folder
      var chosen = inspirationalImages[Math.floor(Math.random() * inspirationalImages.length)];
      msg.channel.send({files: ['inspirePics/' + chosen]});
    } else if (msg.member != null && msg.member.id === '325030773054767133') {
      // ... from me with "Your wish is my command"
      msg.reply('Your wish is my command');
    } else {
      // ... with "Greetings fleshbags!" as default
      msg.reply('Greetings fleshbags!');
    }
  }
  // replies to messages containing "vore" with "YOU RUINED IT!" and puts the vore image in general
  if (new RegExp("\\bvore\\b").test(msg.content.toLowerCase())) {
    msg.reply('YOU RUINED IT!');
    client.channels.fetch(generalChannelID).then(channel => channel.send({ content: '<@' + msg.member + '> reset the count', files: ["vore.png"]}));
  }
  // replies to "she bite" with "SHE NO BITE!!"
  if (new RegExp("\\bshe bite\\b").test(msg.content.toLowerCase())
       || new RegExp("\\bcosette bite\\b").test(msg.content.toLowerCase())
       || new RegExp("\\bcossete bite\\b").test(msg.content.toLowerCase())) {
    msg.reply('SHE NO BITE!!');
  }
  // replies to mentions of food channel with "Every channel is food channel"
  if (!msg.mentions.everyone && msg.mentions.has('573026220833243137')) {
    var picking = new Date().getTime();
    if (picking % 2 == 1) {
      msg.channel.send({files: ["food.png"]});
    } else {
      msg.channel.send('Every channel is food channel');
    }
  }
  // replies to messages containing "compiling" with xkcd comic
  if (new RegExp("\\bcompiling\\b").test(msg.content.toLowerCase())) {
    msg.channel.send({files: ["compiling.png"]});
  }
  // replies to messages from elle (or me) containing "dance" with twerking gif
  // admin role id: 718201180815097896 birthday role id: 693811236218994788
  if (new RegExp("\\bdance\\b").test(msg.content.toLowerCase()) && msg.member != null && (msg.member.id === '533716168062664742'
        || msg.member.id === '325030773054767133' || msg.member.roles.cache.get('718201180815097896') != null
        || msg.member.roles.cache.get('693811236218994788') != null)) {
    searchForGif("twerking", msg.channel);
  }
  // replies to messages from kiwi (or me) containing "I would die for " with euphie's meme
  if (msg.member != null && (msg.member.id === '155457021150232576' || msg.member.id === '325030773054767133')
      && new RegExp("\\bi would die for\\b").test(msg.content.toLowerCase())) {
    msg.channel.send({files: ["kiwi.png"]});
  }

  // changes roles for mentioned member based on welcome command by Server Staff (role id: 718201268283375617)
  // removes Unverified (id: 1215014250645291068) and adds Columbusites (id: 587495795897532437)
  if (msg.content.startsWith("!welcome") && msg.member != null && msg.member.roles.cache.get('718201268283375617') != null
      && msg.mentions != null && msg.mentions.members != null && msg.mentions.members.length > 0) {
    msg.mentions.members.foreach((member) => {
      if (member.roles.cache.get('1215014250645291068') != null) {
        member.roles.remove('1215014250645291068');
      }
      if (member.roles.cache.get('587495795897532437') == null) {
        member.roles.add('587495795897532437');
      }
    });
  }
});

// post siren gif every Wednesday at noon
cron.schedule("0 12 * * WED", function() {
    var searchWords = ["woooo", "siren", "awoo"];
    var chosen = Math.floor(Math.random() * searchWords.length);
    client.channels.fetch(generalChannelID).then(channel => searchForGif(searchWords[chosen], channel));
});

// change server name to "Columbugs" on May 1st
cron.schedule("0 0 1 5 *", function() {
    client.guilds.cache.get(cbusGuildID).setName('Columbugs');
});

// feature removed by request
// every morning at 8, put image from inspirePics folder into support channel
//cron.schedule("0 8 * * *", function() {
//  var chosen = inspirationalImages[Math.floor(Math.random() * inspirationalImages.length)];
//  client.channels.fetch('630807691291525131').then(channel => channel.send({files: ['inspirePics/' + chosen]}));
//});
