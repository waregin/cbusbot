require('dotenv').config();
const {
  Client,
  Intents
} = require('discord.js');
const intents = new Intents([
  Intents.NON_PRIVILEGED, // include all non-privileged intents, would be better to specify which ones you actually need
  "GUILD_MEMBERS", // lets you request guild members (i.e. fixes the issue)
]);
const client = new Client({
  ws: {
    intents
  }
});
const cron = require("node-cron");
const fs = require('fs');
const lineReader = require('line-reader');
const schedule = require('node-schedule');
const fetch = require('node-fetch');
const cbusGuildID = '555243907534028830';
const spotifyUri = require('spotify-uri');

var inspirationalImages = fs.readdirSync('./inspirePics');
var twerks = fs.readdirSync('./twerking');
var generalChannelID = '766529200113975327';
let songList = [];


async function searchForGif(searchTerm, chan) {
  var url = 'https://g.tenor.com/v1/search?q=' + searchTerm + '&key=' + process.env.TENORKEY + '&limit=25';
  var response = await fetch(url);
  var json = await response.json();
  var chosen = Math.floor(Math.random() * json.results.length);
  var chosenGif = json.results[chosen].url;
  chan.send(chosenGif);
}

async function checkAddAfterDarkRole(member) {
  var lvl10RoleID = '715997180476784721';
  var agedRoleID = '842861994449436673';
  var afterDarkRoleID = '850121444032643092';
  var afterDarkRole = client.guilds.cache.get(cbusGuildID).roles.cache.get(afterDarkRoleID);

  var roleCache = member.roles.cache;

  if (roleCache.has(lvl10RoleID) && roleCache.has(agedRoleID) && !roleCache.has(afterDarkRoleID)) {
    member.roles.add(afterDarkRole);
  }
}

function getSotdSubmissions() {
  let submissions = [];
  let last7Submitters = [];
  let count = 0;
  lineReader.eachLine('songs.txt', line => {
    let submission = {};
    const info = line.split(' ');
    submission.date = info[0];
    submission.songUrl = info[1];
    submission.member = info[2];
    submissions.push(submission);

    if (count < 7) {
      last7Submitters.push(info[2]);
    }
    count++;
  })
  return [submissions, last7Submitters];
}

function submitterIsValid(last7Submitters, memberId) {
  let valid = true;
  last7Submitters.forEach(submitterId => {
    if (memberId == submitterId) {
      valid = false;
    }
  })
  return valid;
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

client.on('message', msg => {

  //adds song to SOTD
  if (msg.content.toLowerCase().startsWith('!sotd ')) {
    try {
      const sotdSplit = msg.content.split(' ');
      if (sotdSplit.length == 2) {
        const songUrl = sotdSplit[1];
        const songData = spotifyUri.parse(songUrl);
        const [submissions, last7Submitters] = getSotdSubmissions();
        if (songData.type == 'track') {
          if (submitterIsValid(last7Submitters, member.id)) {
            const now = new Date();
            fs.appendFile('songs.txt', `\n${now} ${songUrl} ${msg.member.id}`, function (err) {
              if (err) {
                console.log('failed to add song');
              } else {
                console.log('song added');
              }
            })
          } else {
            msg.reply('You\'ve already got a song lined up within the next week.');
          }
        }
      }
    } catch (err) {
      msg.reply('Error queueing song');
    }
  }

  // replies to "ping" with "pong"
  if (msg.content.toLowerCase() === 'ping') {
    msg.reply('pong');
  }
  // replies to mentions
  if (!msg.mentions.everyone && msg.mentions.has(client.user)) {
    if (new RegExp("\\binspire\\b").test(msg.content.toLowerCase())) {
      // ... containing "inspire" with image from inspire folder
      var chosen = inspirationalImages[Math.floor(Math.random() * inspirationalImages.length)];
      msg.channel.send('', {
        files: ['inspirePics/' + chosen]
      });
    } else if (msg.member != null && msg.member.id === '325030773054767133') {
      // ... from me with "Your wish is my command"
      msg.reply('Your wish is my command');
    } else if (msg.member != null && msg.member.id === '325030773054767133') {
      // ... from me with "Your wish is my command"
      msg.reply('Yes, your majesty');
    } else {
      // ... with "Greetings fleshbags!" as default
      msg.reply('Greetings fleshbags!');
    }
  }
  // replies to messages containing "vore" with "YOU RUINED IT!" and puts the vore image in general
  if (new RegExp("\\bvore\\b").test(msg.content.toLowerCase())) {
    msg.reply('YOU RUINED IT!');
    client.channels.fetch(generalChannelID).then(channel => channel.send('<@' + msg.member + '> reset the count', {
      files: ["vore.png"]
    }));
  }
  // replies to "she bite" with "SHE NO BITE!!"
  if (new RegExp("\\bshe bite\\b").test(msg.content.toLowerCase()) ||
    new RegExp("\\bcosette bite\\b").test(msg.content.toLowerCase()) ||
    new RegExp("\\bcossete bite\\b").test(msg.content.toLowerCase())) {
    msg.reply('SHE NO BITE!!');
  }
  // replies to mentions of food channel with "Every channel is food channel"
  if (!msg.mentions.everyone && msg.mentions.has('573026220833243137')) {
    var picking = new Date().getTime();
    if (picking % 2 == 1) {
      msg.channel.send('', {
        files: ["food.png"]
      });
    } else {
      msg.channel.send('Every channel is food channel');
    }
  }
  // replies to messages containing "compiling" with xkcd comic
  if (new RegExp("\\bcompiling\\b").test(msg.content.toLowerCase())) {
    msg.channel.send('', {
      files: ["compiling.png"]
    });
  }
  // replies to messages from elle (or me) containing "dance" with twerking gif
  // admin role id: 718201180815097896 birthday role id: 693811236218994788
  if (new RegExp("\\bdance\\b").test(msg.content.toLowerCase()) && msg.member != null && (msg.member.id === '533716168062664742' ||
      msg.member.id === '325030773054767133' || msg.member.roles.cache.get('718201180815097896') != null ||
      msg.member.roles.cache.get('693811236218994788') != null)) {
    searchForGif("twerking", msg.channel);
  }
  // replies to messages from kiwi (or me) containing "I would die for " with euphie's meme
  if (msg.member != null && (msg.member.id === '155457021150232576' || msg.member.id === '325030773054767133') &&
    new RegExp("\\bi would die for\\b").test(msg.content.toLowerCase())) {
    msg.channel.send('', {
      files: ["kiwi.png"]
    });
  }
});

// every hour, check for members who have both the lvl10 and 18+ roles and ensure they have the after dark role
cron.schedule("0 * * * *", function () {
  client.guilds.cache.get(cbusGuildID).members.fetch().then(members => members.each(member => checkAddAfterDarkRole(member)));
});

// post siren gif every Wednesday at noon
cron.schedule("0 12 * * WED", function () {
  var searchWords = ["woooo", "siren", "awoo"];
  var chosen = Math.floor(Math.random() * searchWords.length);
  client.channels.fetch(generalChannelID).then(channel => searchForGif(searchWords[chosen], channel));
});

// change server name to "Columbugs" on May 1st
cron.schedule("0 0 1 5 *", function () {
  client.guilds.cache.get(cbusGuildID).setName('Columbugs');
});

// feature removed by request
// every morning at 8, put image from inspirePics folder into support channel
//cron.schedule("0 8 * * *", function() {
//  var chosen = inspirationalImages[Math.floor(Math.random() * inspirationalImages.length)];
//  client.channels.fetch('630807691291525131').then(channel => channel.send('', {files: ['inspirePics/' + chosen]}));
//});