var butterflyMessage = 'The following members are level 15 but do not have access to the butterfly sanctuary:\n';

async function checkSocialRole(member) {
    var lvl15RoleID = '850385192769290241';
    var socialCaterpillarRoleID = '607696693760360450';
    var socialButterflyRoleID = '590030281352937489';

    var roleCache = member.roles.cache;
    if (roleCache.has(lvl15RoleID) && !(roleCache.has(socialCaterpillarRoleID)
        || roleCache.has(socialButterflyRoleID))) {
        butterflyMessage = butterflyMessage + member.displayName + '\n';
    }
}

// post non-butterfly peeps every Monday at 10PM
cron.schedule("0 22 * * MON", function() {
    var adminChannelID = '718201857646002237';
    client.guilds.cache.get(cbusGuildID).members.fetch().then(members => members.each(member => checkSocialRole(member)));
    client.channels.fetch(adminChannelID).then(channel => channel.send(butterflyMessage));
    butterflyMessage = 'The following members are level 15 but do not have access to the butterfly sanctuary:\n';
});

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

// every hour, check for members who have both the lvl10 and 18+ roles and ensure they have the after dark role
cron.schedule("0 * * * *", function() {
    client.guilds.cache.get(cbusGuildID).members.fetch().then(members => members.each(member => checkAddAfterDarkRole(member)));
});
