# WORK IN PROGRESS

1. Create a `.token` in the same folder as the bot, and set its contents to your Discord bot token (with no new line
   at the end of the file).
1. Run `docker build -t <bot-name> .` and wait for the build to complete.
1. Run `docker run -d <bot-name>` and observe that the bot starts in a detached state.
