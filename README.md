# TESTING

1. Create a `.token` in the same folder as the bot, and set its contents to your Discord bot token (with no new line
   at the end of the file).
1. Run `docker build -t redmac-bot .`, and wait for the build to complete.
1. Run `docker run -d redmac-bot`, and observe that the bot starts in a detached state.
