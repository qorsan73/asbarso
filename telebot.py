import asyncio
from datetime import datetime
from telethon import TelegramClient, events, custom
from telethon.tl.types import UserStatusOnline, UserStatusOffline


G = '\033[92m'
R = '\033[91m'
B = '\033[94m'
C = '\033[96m'
Y = '\033[93m'
W = '\033[0m'
LOGO = f"""{G}
====================================================================
 █████  ███████ ██████   █████  ██████  ███████  ██████  
██   ██ ██      ██   ██ ██   ██ ██   ██ ██      ██    ██ 
███████ ███████ ██████  ███████ ██████  ███████ ██    ██ 
██   ██      ██ ██   ██ ██   ██ ██   ██      ██ ██    ██ 
██   ██ ███████ ██████  ██   ██ ██   ██ ███████  ██████  
                                                             
    {W}>> {C}Coded by:{W} Qorsan taez
    >> {C}GITHUB: {W} https://github.com/qorsan73
{G}===================================================================={W}
"""

print(LOGO)
print(f"[{B}*{W}] Securing terminal environment...")
print(f"[{B}*{W}] Please inject your API credentials below to establish connection:\n")

try:
    API_ID = int(input(f"[{G}#{W}] ENTER TELEGRAM_API_ID : ").strip())
    API_HASH = input(f"[{G}#{W}] ENTER TELEGRAM_API_HASH : ").strip()
    BOT_TOKEN = input(f"[{G}#{W}] ENTER TELEGRAM_BOT_TOKEN : ").strip()
    ADMIN_ID = int(input(f"[{G}#{W}] ENTER ROOT_ADMIN_CHAT_ID: ").strip())
except ValueError:
    print(f"\n{R}[-]{W} CRITICAL ERROR: API_ID and ADMIN_ID must be purely numeric integers!")
    exit(1)

print(f"\n[{C}+{W}] Initializing encrypted sessions... Connecting to MTProto Servers...")


client = TelegramClient('asbarso_user_session', API_ID, API_HASH)
bot = TelegramClient('asbarso_bot_session', API_ID, API_HASH)

target_user = None
last_status = None
user_language = "ar"  


@bot.on(events.NewMessage(pattern=r'^/(start|monitor)'))
async def start_command(event):
    if event.chat_id != ADMIN_ID:
        return
        
    buttons = [
        [custom.Button.inline("💀 العربية (AR)", data=b"lang_ar"),
         custom.Button.inline("🛡️ English (EN)", data=b"lang_en")]
    ]
    
    await event.reply("⚡ **[ASBARSO CORE]** Establish Notification Interface Protocol / اختر لغة واجهة النظام:", buttons=buttons)

@bot.on(events.CallbackQuery())
async def handle_language_selection(event):
    global user_language
    if event.sender_id != ADMIN_ID:
        return
        
    await event.answer()
    
    choice = event.data.decode('utf-8')
    
    if choice == "lang_ar":
        user_language = "ar"
        msg = "🎯 **[تتم المراقبة]** تم تهيئة السيرفر على اللغة: **العربية**.\n\n💥 **الآن:** قم بحقن (ارسال) يوزر الهدف الذي تريد تعقبه والتجسس على اتصاله فوراً (مثال: `@username`)."
    elif choice == "lang_en":
        user_language = "en"
        msg = "🎯 **[INTERFACE INJECTED]** Target language initialized to: **English**.\n\n💥 **ACTION REQUIRED:** Input/Send the target username to bind the spy-tracker protocol (e.g., `@username`)."
    else:
        return
        
    await event.edit(msg)


@bot.on(events.NewMessage(func=lambda e: e.is_private and not e.text.startswith('/')))
async def handle_username_input(event):
    global target_user, last_status
    if event.chat_id != ADMIN_ID:
        return

    input_text = event.text.strip().replace('@', '')
    
    if input_text:
        target_user = input_text
        last_status = None  
        
        if user_language == "ar":
            reply_msg = f"☣️ **[ASBARSO PROTOCOL ACTIVATED]**\n\n🕵️‍♂️ تم بنجاح ربط خوارزمية التجسس بالهدف: `@{target_user}`\n📡 مصفوفة الفحص الدورية تعمل الآن في الخلفية... انتظر الإشعارات الفورية الحية!"
        else:
            reply_msg = f"☣️ **[ASBARSO PROTOCOL ACTIVATED]**\n\n🕵️‍♂️ Target locked and loaded: `@{target_user}`\n📡 Scanning matrix is actively tracking in background... Live breach updates ahead!"
            
        await event.reply(reply_msg)


@bot.on(events.NewMessage(pattern='/stop'))
async def stop_monitoring(event):
    global target_user
    if event.chat_id != ADMIN_ID:
        return

    if target_user:
        if user_language == "ar":
            await event.reply(f"🛑 **[إيقاف التتبع]** تم فك الارتباط السيبراني وسحب خوارزمية التعقب من الحساب `@{target_user}`.")
        else:
            await event.reply(f"🛑 **[PROTOCOL DISCONNECTED]** Tracker successfully unlinked from `@{target_user}`.")
        target_user = None
    else:
        if user_language == "ar":
            await event.reply("❌ **[خطأ بالنظام]** لا توجد أي عملية اختراق أو تتبع نشطة حالياً.")
        else:
            await event.reply("❌ **[SYSTEM ERROR]** No active cyber-tracking matrix found to abort.")


async def check_status():
    global target_user, last_status
    
    while True:
        if target_user:
            print(f"[{Y}🔬 SCANNING MATRIX{W}] Checking live network status for @{target_user}...")
            try:
                user_entity = await client.get_entity(target_user)
                status = user_entity.status

                if isinstance(status, UserStatusOnline):
                    if user_language == "ar":
                        current_status = "🟢 متصل (ONLINE)"
                    else:
                        current_status = "🟢  ONLINE NOW"
                elif isinstance(status, UserStatusOffline):
                    if user_language == "ar":
                        current_status = "🔴 قَطع الاتصال وغير متصل (OFFLINE)"
                    else:
                        current_status = "🔴 SYSTEM DISCONNECTED / OFFLINE"
                else:
                    if user_language == "ar":
                        current_status = "⚪ شبح (الحالة مخفية بالكامل)"
                    else:
                        current_status = "⚪ GHOST MODE (Status Fully Cloaked)"

                if current_status != last_status:
                    now = datetime.now().strftime("%I:%M:%S %p")
                    
                    if user_language == "ar":
                        msg = f"⚡ **[ASBARSO BREACH ALERT]**\n\n👤 الضحية المستهدفة: `@{target_user}`\n🛡️ حالة الاتصال الحالية: **{current_status}**\n🕐 طابع الوقت: `{now}`\n\n💀 **[By: Qorsan taez]**"
                    else:
                        msg = f"⚡ **[ASBARSO BREACH ALERT]**\n\n👤 Target Entity: `@{target_user}`\n🛡️ Current Connection Matrix: **{current_status}**\n🕐 Timestamp: `{now}`\n\n💀 **[By: Qorsan taez]**"
                        
                    await bot.send_message(ADMIN_ID, msg)
                    last_status = current_status
                    print(f"[{G}🔥 ALERT SENT{W}] Status change detected for @{target_user} -> {current_status}")
                    
            except Exception as e:
                print(f"[{R}!{W}] SYSTEM BREACH ERROR: {e}")
        
        await asyncio.sleep(20)


async def main():
    await client.start()
    await bot.start(bot_token=BOT_TOKEN)
    
    print("\n" + f"{G}="*50)
    print(f"[+] ASBARSO SYSTEM CORE ONLINE... INFILTRATION SUCCESSFUL!{W}")
    print(f"[{C}+{W}] Developer Persona: {G}Qorsan taez{W}")
    print(f"[{C}+{W}] System is successfully listening to buttons and user actions...")
    print(f"{G}="*50 + f"{W}\n")
    
    asyncio.create_task(check_status())
    
    await bot.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{R}[-]{W} [SYSTEM ABORTED] Asbarso Core safely wiped from RAM by Qorsan taez.")
