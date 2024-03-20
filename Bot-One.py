from pyrogram import Client, filters
import logging
import string
import random
import sqlite3
import time
import config 

def db_setup():
    conn = sqlite3.connect(database="uploader.db")
    cur = conn.cursor()
    cmd = "CREATE TABLE IF NOT EXISTS File(Chat_id INTEGER,File_id STRING,Msg_id INTEGER)"
    cur.execute(cmd)
    conn.commit()
    cur.close()
    conn.close()

def db_addFile(Chat_id, File_id, Msg_id):
    conn = sqlite3.connect(database="uploader.db")
    cur = conn.cursor()
    cmd = "INSERT INTO FILE (CHAT_ID,File_id,Msg_id) VALUES (?,?,?)"
    args = (Chat_id, File_id, Msg_id)
    cur.execute(cmd, args)
    conn.commit()
    cur.close()
    conn.close()

def get_file(file_id):
    conn = sqlite3.connect(database="uploader.db")
    cur = conn.cursor()
    cmd = "SELECT CHAT_ID,Msg_id,File_id FROM FILE WHERE File_id=(?)"
    args = (file_id,)
    cur.execute(cmd, args)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result
    
def is_member(chat_id):
    try:
        member_status = str(app.get_chat_member(chanel1_id, chat_id).status)
        if member_status in ["ChatMemberStatus.OWNER", "ChatMemberStatus.ADMINISTRATOR", "ChatMemberStatus.MEMBER"]:
            return True
        else:
            return False
    except:
        return False

    
api_id = config.api_id
api_hash = config.api_hash
Token = config.Token
chanel1_id= config.chanel1_id

app = Client(
    config.Bot_name,
    api_id=api_id,
    api_hash=api_hash,
    bot_token=Token
)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
LOGGER = logging.getLogger("name")

@app.on_message(filters.private)
def hello(_, message):
    Msg_id = message.id
    chat_id = int(message.chat.id)
    msg = message.text or message.photo or message.video
    if message.text:
        if msg.startswith("/start"):
            
            if (len(msg.split(" "))) == 2:
                if is_member(chat_id):

                    app.send_message(
                        chat_id,
                        text="در حال ارسال فایل.....",
                        reply_to_message_id=Msg_id
                    )
                    file_id = msg.split(" ")[1]
                    result = get_file(file_id)[0]
                    user_chatid, user_msgid, user_fileid = result
                    file = app.get_messages(user_chatid,user_msgid)
                    
                    file.copy(chat_id)
                    app.send_message(
                        chat_id,
                        text="<B>فایل بعد از 60 ثانیه پاک میشود \nدر پیام های ذخیره شده,ذخیره کنید</B>",
                        reply_to_message_id=Msg_id
                    )
                    app.delete_messages(
                        chat_id,
                        message_ids=Msg_id+1
                    )
                    time.sleep(60)
                    app.delete_messages(
                        chat_id,
                        message_ids=Msg_id+2
                    )
                    app.delete_messages(
                        chat_id,
                        message_ids=Msg_id+3
                    )
                    app.send_message(
                        chat_id,
                        text=f"برای دریافت دوباره روی لینک فایل کلیک کن",
                        reply_to_message_id=Msg_id
                    )
                    # if file.photo :
                    #     app.send_photo(
                    #         chat_id,
                    #         photo=file.photo.file_id,
                    #         caption=""
                    #     )
                    # elif file.video:
                    #     app.send_video(
                    #         chat_id,
                    #         video=file.video.file_id,
                    #         caption=""
                    #     )
                    # else :
                    #     app.send_document(
                    #         chat_id,
                    #         document=file.document.file_id,
                    #         caption=""
                    #     )
                    # file.forward(chat_id)
                    app.delete_messages(
                        chat_id,
                        message_ids=Msg_id+1
                    )
                else:
                    app.send_message(
                        chat_id,
                        f'در کانال ربات عضو نیستی جهت عضویت روی <a href="{config.chanel1_Join_link}">لینک</a> کلیک کنید\n{config.chanel1_Join_link}',
                        reply_to_message_id=Msg_id
                    )
            else:
                app.send_message(
                    chat_id,
                    text=f"سلام به ربات آپلودر {config.Bot_name} خوش آمدید \n یک فایل بفرست تا لینک دریافت دوبارشو بهت بدم ",
                    reply_to_message_id=Msg_id
            )
        elif msg == "/upload":
            app.send_message(
                chat_id,
                "فایلتو بفرست تا لینکشو بهت بدم",
                reply_to_message_id=Msg_id
            )
    else:
        def T_file_size():
            if message.photo:
                file_size = str(int(message.photo.file_size / 1024))
            elif message.video:
                file_size = str(int(message.video.file_size / 1024))
            else:
                file_size = str(int(message.document.file_size / 1024))
            return file_size

        def T_file_id():
            file_id = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
            return file_id

        file_size = T_file_size()
        file_id = T_file_id()
        db_addFile(chat_id, file_id, Msg_id)

        app.send_message(
            chat_id,
            text=(f"حجم فایل شما {file_size} کیلوبایت است.\nآیدی فایل شما <code>{file_id}</code> است.\n<a href='{config.chanel1_Join_link}'>لینک</a> فایل: <code>https://t.me/One_my_Telegram_Bot?start={file_id}</code>"),
            reply_to_message_id=Msg_id
        )

db_setup()
app.run()
