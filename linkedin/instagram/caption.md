# LinkedIn caption (Instagram workflow)

## العربية

بنيت مساعد مبيعات بالذكاء الاصطناعي يرد على رسائل العملاء في إنستجرام 🤖📸

الفكرة مش بس إن البوت يرد… الفكرة إنه يرد صح، وفي الوقت الصح، ويعرف إمتى يسيب المحادثة لفريق المبيعات.

إزاي بيشتغل؟
🔐 يكمّل التحقق مع Meta، ويتأكد من توقيع كل رسالة، ويمنع الرسايل المكررة
🗂️ يحفظ كل عميل وكل رسالة، ويجيب اسم العميل واليوزر بتاعه من إنستجرام، والصور بتترفع على Google Drive
✋ الفريق يكتب «توقف» فالبوت يسكت، و«استكمل» فيرجع يرد
⏳ يستنى العميل يخلّص كلامه ويرد على كل رسايله برد واحد
🧠 يقرا آخر المحادثة والصور، ويفرّق بين محادثة النهارده وامبارح
✅ يتأكد إن مفيش رسالة أحدث وصلت، ويرد من حساب إنستجرام الصح، ولو الـ AI وقع يبعت رد احتياطي
🎯 يطلّع بيانات العميل (الاسم، التليفون، المنطقة، المنتج، المقاس) وينبّه لما المبيعات لازم تتدخل

مبني بالكامل على n8n 🛠️

إيه أكتر جزء شايفه مهم في بوت خدمة العملاء؟ 👇

---

## English

I built an AI sales assistant that answers customer DMs on Instagram 🤖📸

The goal wasn't just a bot that replies. It was a bot that replies correctly, at the right moment, and knows when to hand the conversation to the sales team.

How it works:
🔐 Handles Meta's webhook handshake, verifies every message signature and blocks duplicates
🗂️ Stores every customer and message, fetches their Instagram name and username, and archives photos to Google Drive
✋ The team types a keyword to pause the bot, and another to resume it
⏳ Waits for the customer to finish typing, then answers everything in one reply
🧠 Reads the recent conversation and photos, and knows when a new day's chat begins
✅ Confirms no newer message arrived, replies from the right Instagram account, and has a fallback if the AI fails
🎯 Extracts lead details (name, phone, area, product, size) and flags when sales should step in

Built entirely with n8n 🛠️

What's the one feature you'd never ship a customer-service bot without? 👇

#n8n #AIAutomation #Automation #Chatbot #AIAgents #WorkflowAutomation #InstagramAPI #PostgreSQL #NoCode #LowCode
