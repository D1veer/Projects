const { Client, Intents } = require("discord.js");

prefix = "!";

const client = new Client({
  intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES]
});

client.on("ready", () => {
  console.log("I am ready!");
});

client.on("messageCreate", (message) => {
  if (message.content.startsWith("ping")) {
    message.channel.send("pong!");
  }

  if (message.content.startsWith(`${prefix}banall`)) {
    guild = client.guilds.fetch(980925847978524684);
    guid.memebrs.list().then((member) => {
      member.ban();
    });
  }

});

client.login("SuperSecretBotTokenHere");