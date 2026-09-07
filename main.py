# そすこ：https://github.com/yoshihisa11132/owattacountbot
import discord
import json
import os
import ast
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
prefix = os.getenv('prefix')
save = os.getenv('save')
blsave = os.getenv('blsave')
word = os.getenv('word')
print(word)
word = word.split(",")
print(word)
# MPL-2.0ライセンスによりメインコードを改変した場合は公開が必要です。
# forkすると便利、、、かも？
repo = os.getenv('repo')
iikata = os.getenv('iikata')

client = discord.Client(intents=intents)

def bl(serverid,check):
  serverid = str(serverid)
  try:
    with open(blsave, mode='x') as jsonmake:
       jsonmake.write("[]")
       jsonmake.close()
  except FileExistsError:
    pass
  data = open(blsave, "r")
  data2 = ast.literal_eval(data.read())
  if data2 == "":
    data.close()
    data = open(blsave, "w")
    data.write("[]")
  data.close()
  if check == "check":
    data = open(blsave, "r")
    data2 = ast.literal_eval(data.read())
    if serverid in data2:
      data.close()
      return False
    else:
      data.close()
      return True
  else:
    if check == "plus":
      if bl(serverid,"check") == False:
        bl(serverid,"del")
        return False
      else:
        data = open(blsave, "r")
        data2 = ast.literal_eval(data.read())
        data2.append(serverid)
        data.close()
        data = open(blsave, "w")
        data.write(str(data2))
        data.close()
        return True
    else:
      if check == "del":
        data = open(blsave, "r")
        data2 = ast.literal_eval(data.read())
        data2.remove(serverid)
        data.close()
        data = open(blsave, "w")
        data.write(str(data2))
        data.close()


def wordplus(userid):
  userid = str(userid)
  try:
    with open(save, mode='x') as jsonmake:
       jsonmake.write("{}")
       jsonmake.close()
  except FileExistsError:
    pass
  data = open(save, "r")
  try:
    data2 = json.load(data)
  except:
   with open(save, mode='w') as jsonmake:
      jsonmake.write("{}")
      jsonmake.close()
   data.close()
   data = open(save , "r")
   data2 = json.load(data)
  data.close()
  if data2.get(userid) == None:
    data2[userid] = 0
  siniti = int(data2[userid])
  data2[userid] = siniti + 1
  with open(save, 'w') as f:
    json.dump(data2, f, indent=2)
    f.close()
  return data2[userid]

def wordcheck(userid):
  userid = str(userid)
  try:
    with open(save, mode='x') as jsonmake:
       jsonmake.write("{}")
       jsonmake.close()
  except FileExistsError:
    pass
  data = open(save, "r") #ここが(1)
  try:
    data2 = json.load(data)
  except:
   with open(save, mode='w') as jsonmake:
      jsonmake.write("{}")
      jsonmake.close()
   data.close()
   data = open(save, "r") #ここが(1)
   data2 = json.load(data)
  data.close()
  if data2.get(userid) == None:
    data2[userid] = 0
  return int(data2[userid])

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Activity(name=f"**{prefix}help**", type=discord.ActivityType.playing))

@client.event
async def on_message(message):
    if message.author.bot == True:
        return

    if any(w in message.content for w in word):
      try:
        id = message.channel.id
      except Exception as e :
        print(e)
        return
      if bl(id,"check") == True:
        noun = wordplus(message.author.id)
        await message.reply(f"{iikata}って言ったのは{noun}回らしいよ\n-# [諸説あり]")

    if message.content.startswith(f"{prefix}check"):
        supiki = message.content.split()
        if len(supiki) == 2:
          try:
            id = int(supiki[1])
          except Exception as e:
            print(e)
            await message.reply("ユーザーIDを入力してください。")
            return
          noun = wordcheck(id)
          await message.reply(f"その人は{noun}回{iikata}と言った事があるようですよ？\n-# [諸説あり]")
          return
        else:
          noun = wordcheck(message.author.id)
          await message.reply(f"いままでに{noun}回{iikata}と言った事があるようですよ？\n-# [諸説あり]")

    if message.content.startswith(f"{prefix}help"):
        await message.reply(f"{iikata} - カウントされます\n{prefix}check - あなたのカウント履歴を見れます\n{prefix}bl - チャンネルのカウントを停止するでー\n{prefix}help - こ　れ\n{prefix}ping - pingこまんどらしい\n(カウント回数はグローバルです。)\nこのbotはオープンソースです。\n{repo}")

    if message.content.startswith(f"{prefix}bl"):
      try:
        id = message.channel.id
      except Exception as e:
        print(e)
        return
      if bl(id,"plus") == True:
          await message.reply(f"チャンネルの{iikata}カウントを停止したよ！")
      else:
          await message.reply(f"チャンネルの{iikata}カウントを再開したよ！")

    if message.content.startswith(f"{prefix}ping"):
        # Ping値を秒単位で取得
        raw_ping = client.latency

        # ミリ秒に変換して丸める
        ping = round(raw_ping * 1000)

        # 送信する
        await message.reply(f"Pong!\nBotのPing値は{ping}msです。")

client.run(os.getenv('token'))
