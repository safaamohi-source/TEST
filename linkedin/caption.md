# LinkedIn caption

## العربية

بنيت مساعد مبيعات بالذكاء الاصطناعي يرد على رسائل العملاء في ماسنجر وإنستجرام 🤖💬

الفكرة مش بس إن البوت يرد… الفكرة إنه يرد صح، وفي الوقت الصح، ويعرف إمتى يسيب المحادثة لفريق المبيعات.

إزاي بيشتغل؟
🔐 يتحقق من توقيع كل رسالة جاية من Meta ويتجاهل الرسايل المكررة
🗂️ يحفظ كل عميل وكل رسالة في PostgreSQL، والصور بتترفع على Google Drive
✋ الفريق يكتب «توقف» فالبوت يسكت، و«استكمل» فيرجع يرد
⏳ يستنى العميل يخلّص كلامه ويرد على كل رسايله برد واحد
🧠 يقرا آخر المحادثة والصور، ويفرّق بين محادثة النهارده وامبارح
✅ يتأكد إن مفيش رسالة أحدث وصلت قبل ما يبعت الرد، ولو الـ AI وقع يبعت رد احتياطي
🎯 يطلّع بيانات العميل (الاسم، التليفون، المنطقة، المنتج، المقاس) وينبّه لما المبيعات لازم تتدخل

مبني بالكامل على n8n 🛠️

إيه أكتر جزء شايفه مهم في بوت خدمة العملاء؟ 👇

---

## English

I built an AI sales assistant that answers customer DMs on Messenger & Instagram 🤖💬

The goal wasn't just a bot that replies. It was a bot that replies correctly, at the right moment, and knows when to hand the conversation to the sales team.

How it works:
🔐 Verifies every Meta webhook signature and drops duplicate messages
🗂️ Stores every customer and message in PostgreSQL; images are archived to Google Drive
✋ The team types a keyword to pause the bot, and another to resume it
⏳ Waits for the customer to finish typing, then answers everything in one reply
🧠 Reads the recent conversation and photos, and knows when a new day's chat begins
✅ Confirms no newer message arrived before sending, with a fallback reply if the AI fails
🎯 Extracts lead details (name, phone, area, product, size) and flags when sales should step in

Built entirely with n8n 🛠️

What's the one feature you'd never ship a customer-service bot without? 👇

#n8n #AIAutomation #Automation #Chatbot #AIAgents #WorkflowAutomation #MetaAPI #PostgreSQL #NoCode #LowCode
