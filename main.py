import asyncio
import websockets
import json

CHANNEL_NAME = "اسم_قناتك"  # ← غيّرها لاسم قناتك في Kick بدون @

async def listen():
    ws_url = f"wss://chat.kick.com/socket.io/?channel={CHANNEL_NAME}&EIO=3&transport=websocket"

    async with websockets.connect(ws_url) as websocket:
        await websocket.send("40")  # Handshake

        print(f"📡 البوت يعمل الآن على قناة: {CHANNEL_NAME}")

        while True:
            try:
                message = await websocket.recv()
                if "42" in message:
                    payload = json.loads(message[2:])
                    if payload[0] == "chat_message":
                        data = payload[1]
                        username = data["sender"]["username"]
                        msg = data["content"]
                        print(f"{username}: {msg}")

                        # ✅ الرد على !قوانين
                        if msg.strip() == "!قوانين":
                            response = (
                                "📜 قوانين البث الرسمية:\n"
                                "1️⃣ الاحترام واجب بين الجميع – يُمنع السب أو الإساءة.\n"
                                "2️⃣ يمنع الترويج لحسابات أو قنوات أخرى ❌\n"
                                "3️⃣ لا تُكرر الرسائل (Spam) أو تزعج المتابعين.\n"
                                "4️⃣ النقاش يكون حول محتوى البث فقط 🎮🎥\n"
                                "5️⃣ يُمنع الكلام في السياسة أو المواضيع الحساسة 🛑\n"
                                "6️⃣ الالتزام بتعليمات المود أو صاحب البث.\n"
                                "🚨 المخالفة = كتم أو حظر دائم.\n"
                                "💚 استمتع بالبث وخلّك إيجابي!"
                            )
                            print(f"🟢 رد البوت: {response}")
                            # ⚠️ لا يمكن إرسال الرسالة فعليًا في Kick بدون Authorization Token

            except Exception as e:
                print(f"⚠️ خطأ: {e}")

asyncio.run(listen())
