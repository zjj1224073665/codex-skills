---
name: ppt-workflow
description: 当要完成学术ppt的时候使用
---

先提示user，要先把ppt的目录想好，分哪几个部分，然后先一次只完成一个部分。接下来和user对话捋清它想完成的那一部分的思路，然后给出这一部分各个slides的文字部分。再然后，为每个slides分配一个sub agent, 按照4:3的比例直接生成这一页slides的图片，使用image gen。完成以后，提示用户检查并用网页版的ChatGPT去再精修更改这些图片