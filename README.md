# Make-A-Toon: The Now-Defunct Twitter Bot

> Bot that tweets a new, randomly generated Toontown Rewritten toon every 30 minutes!

Make-A-Toon was a twitter bot I hosted I hosted from 2021 to 2023 over on 
[the twitter account @MakeAToon](https://x.com/makeatoon/). It was one of my first "actual" Panda3D projects. I made the 
decision to shut it down in 2023 following the acquisition of Twitter by Elon Musk and the following API changes.

This repository contains the mostly-unchanged source code for that bot. I've cleaned up a few visual aspects of the code
here and there, but beyond that it is relatively untouched.

The largest change I have made is removing the tweepy implementation entirely. The function to make tweets is still
present, but will just take a screenshot and save it to toon.png, as well as print what would be the tweet content.

### As such, please note that the code within this repository is VERY old, very messy and lacking consistent comments.

## Notes

- This bot was made before gender was removed, and does not reflect the current state of Toontown Rewritten's
Make-A-Toon. In general, changes made after 2021/2022 may not be reflected.
- Almost all colours are colour-picked and the scale of Crocodile and Deer is estimated.
- In order to run the bot, you need phase_3.mf decompiled to a folder named phase_3 in the same directory as main.py.
- The New Stripes Shirt / New Denim Shorts are missing. I made the decision to remove these from the code because the
way they were implemented involved getting the texture elsewhere and renaming it, and I wanted this version of the code
to be relatively plug-and-play.

## Special Thanks

- @Vhou-Atroph, who was responsible for most of the name-selection code.
- Toontown Rewritten and its team.