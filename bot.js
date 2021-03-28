require('dotenv').config();
const Discord = require('discord.js');
const client = new Discord.Client();
const cron = require("node-cron");
const fs = require('fs');
const lineReader = require('line-reader');
const schedule = require('node-schedule');
const fetch = require('node-fetch');

var inspirationalImages = fs.readdirSync('./inspirePics');
var twerks = fs.readdirSync('./twerking');

//client.on('debug', console.log);

client.login(process.env.DISCORD_TOKEN);

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);

  // assigns birthday role and sends birthday greeting in general based on dates in file
  var birthdayRole = client.guilds.cache.get('555243907534028830').roles.cache.get('604442101425504261');
  lineReader.eachLine('birthdates.txt', function(line) {
    var info = line.split(' ');
    var birthdayMember = client.guilds.cache.get('555243907534028830').members.cache.get(info[0])
    var job = schedule.scheduleJob({month: info[1], date: info[2], hour: 0, minute: 0}, function(){
      birthdayMember.roles.add(birthdayRole);
      client.channels.fetch('681914541029982268').then(channel => channel.send('<@' + birthdayMember + '> HAPPY BIRTHDAY!', {files: ["birthday.jpeg"]}));
    });
    //console.log(job.nextInvocation());
    // removes role next day
    var revertJob = schedule.scheduleJob({month: info[1], date: parseInt(info[2]) + 1, hour: 0, minute: 0}, function(){
      birthdayMember.roles.remove(birthdayRole);
    });
    //console.log(revertJob.nextInvocation());
  });
});

client.on('message', msg => {
  // replies to "ping" with "pong"
  if (msg.content.toLowerCase() === 'ping') {
    msg.reply('pong');
  }
  // replies to mentions
  if (!msg.mentions.everyone && msg.mentions.has(client.user)) {
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
    client.channels.fetch('766529200113975327').then(channel => channel.send('<@' + msg.member + '> reset the count', {files: ["vore.png"]}));
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
    msg.channel.send(gifSearch("twerking"));
//    var chosen = twerks[Math.floor(Math.random() * twerks.length)];
//    msg.channel.send('', {files: ['twerking/' + chosen]});
  }
});

// post siren gif every Wednesday at noon
cron.schedule("0 0 12 * * WED *", function() {
    client.channels.fetch('766529200113975327').then(channel => channel.send(gifSearch("woo")));
});

// change server name to "Columbugs" on May 1st
cron.schedule("0 0 1 5 *", function() {
    client.guilds.fetch('555243907534028830').then(guild => guild.setName('Columbugs'));
});

// feature removed by request
// every morning at 8, put image from inspirePics folder into support channel
//cron.schedule("0 8 * * *", function() {
//  var chosen = inspirationalImages[Math.floor(Math.random() * inspirationalImages.length)];
//  client.channels.fetch('630807691291525131').then(channel => channel.send('', {files: ['inspirePics/' + chosen]}));
//});

async function gifSearch(searchTerm) {
    var url = 'https://g.tenor.com/v1/search?q=' + searchTerm + '&key=' + process.env.TENORKEY + '&limit=8';
    var response = await fetch(url);
    var json = await response.json();
//    var json = "https://g.tenor.com/v1/search?q=${searchTerm}&key=${process.env.TENORKEY}&limit=8";
    var chosen = Math.floor(Math.random() * json.results.length);
    console.log(json.results[chosen]);
    console.log(json.results[chosen].url);
    return json.results[chosen].url;
}
