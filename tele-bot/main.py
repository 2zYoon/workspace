
import telegram
import json
import threading
import datetime
import os
import platform

from pprint import pprint
from telegram.ext import Updater, CommandHandler
from constant import *


class TeleBot:
    def __init__(self):
        with open(PATH_DATA + "admin") as f:
            self._id = int(f.read().strip())
            print("[INFO] Successfully loaded admin ID (%d)" % self._id)

        with open(PATH_DATA + 'token') as f:
            tok = f.read().strip()
            print("[INFO] Successfully loaded token (%s)" % tok) 

        self.core = telegram.Bot(token=tok)
        self.updater = Updater(tok)
        self.updater.stop()

    def __del__(self):
        print("[INFO] TeleBot instance is deleted.")
        self.stop()

    def get_adminid(self):
        return self._id

    def send_msg(self, chatid, msg):
        self.core.sendMessage(chat_id=chatid, text=msg)

    def add_handler(self, cmd, func):
        self.updater.dispatcher.add_handler(CommandHandler(cmd, func))

    def start(self):
        self.send_msg(self._id, 'Hi, admin, I woke up. (DON\'T FORGET TO BE READY)')
        self.updater.start_polling()
        self.updater.idle()

    def stop(self):
        self.updater.start_polling()
        self.updater.dispatcher.stop()
        self.updater.job_queue.stop()
        self.updater.stop()



# DATA #
# runtime data
users = dict()
bot = TeleBot()


# misc
get_ready = False
mutex = threading.Lock()
pid = -1

# INITIALIZATION #
# some init
def init_first():
    global pid
    if not os.path.isdir(PATH_DATA[:-1]):
        print("[ERROR] Admin data not found...")
        print("REQUIRED:\n\tadmin\n\ttoken\n\tusers (empty JSON)")
        exit(1)

    # get pid
    print("[INFO] telebot is running with pid {}".format(os.getpid()))
    pid = os.getpid()

# load users JSON file
def init_load_users():
    global users

    with open(PATH_DATA + 'users') as f:
        users = json.load(f)
        print("[INFO] Successfully loaded user data")


# FUNCTIONS #
# save_to_file: save current dict(users) to JSON file
# called asynchronously, and before exist
def save_to_file():
    print("[INFO] Saving user data...")
    #pprint(users)

    with open(PATH_DATA + "users", 'w') as f:
        json.dump(users, f)
        print("[INFO] User data was succesfully saved")

# get_yymmdd: get integer YYMMDD
def get_yymmdd():
    return int(datetime.datetime.now().strftime("%y%m%d"))

# get_next_flag: return next flag time (is_nextday, HHMM)
# note: exclude sun 23:30 and mon 00:30
def get_next_flag():

    nowtime = int(datetime.datetime.now().strftime("%H%M")) # get current HHMM
    mtwtfss = datetime.datetime.today().weekday() # check weekday
    
    if (nowtime >= 2030 and mtwtfss == 6) or (nowtime < 30 and mtwtfss == 0): 
        return True, 130 
    elif nowtime >= 2330:
        return True, 30
    else:
        if nowtime % 100 < 30:
            return False, (nowtime // 100) * 100 + 30
        else:
            return False, (nowtime // 100) * 100 + 130

# is_now_flag: return True if now is flag time
#   now: hhmm
def is_now_flag(now):
    mtwtfss = datetime.datetime.today().weekday() # check weekday
    if now % 100 == 30:
        if now // 100 == 23 and mtwtfss == 6:
            return False
        elif now // 100 == 0 and mtwtfss == 0:
            return False
        else:
            return True

    return False



# first_callee: check existence of user and add to dict(users) if not exist.
# called by every handler
def first_callee(update, context):
    global users

    if users.get(str(update.effective_chat.id)) == None:
        tmp = dict()
        tmp['dailycheck'] = dict()
        tmp['weeklycheck'] = dict()
        tmp['flag'] = -1
        tmp['lastused'] = get_yymmdd()
        tmp['daysum'] = 0

        users[str(update.effective_chat.id)] = tmp

        print("[INFO] New user added (%d)" % update.effective_chat.id)

    users[str(update.effective_chat.id)]['lastused'] = get_yymmdd()

    # handle later patch [patch, default value]
    later_patches = [["daysum", 0],]
    for i in later_patches:
        if users[str(update.effective_chat.id)].get(i[0], None) == None:
            users[str(update.effective_chat.id)][i[0]] = i[1]


# admin_check: check current chat ID
# returns 0 if admin, otherwise 1
def admin_check(update, context, msg="Hi, admin."):
    global bot

    if update.effective_chat.id != bot.get_adminid():
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="This command is only allowed to admin.")
        return 1
    else:
        if msg != None:
            context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=msg)
        return 0

# HANDLER # 
# help: show help message
def handler_help(update, context):
    first_callee(update, context)
    msg = ""

    if len(context.args) == 0:
        msg = MSG_HELP
    else:
        if context.args[0] == "daily":
            if len(context.args) > 1:
                if context.args[1] == "show":
                    msg = MSG_DAILYCHECK_SHOW_USE
                elif context.args[1] == "add":
                    msg = MSG_DAILYCHECK_ADD_USE
                elif context.args[1] == "remove":
                    msg = MSG_DAILYCHECK_REMOVE_USE
                else:
                    msg = MSG_DAILYCHECK_USE
            else:
                msg = MSG_DAILYCHECK_USE

        elif context.args[0] == "weekly":
            if len(context.args) > 1:
                if context.args[1] == "show":
                    msg = MSG_WEEKLYCHECK_SHOW_USE
                elif context.args[1] == "add":
                    msg = MSG_WEEKLYCHECK_ADD_USE
                elif context.args[1] == "remove":
                    msg = MSG_WEEKLYCHECK_REMOVE_USE
                else:
                    msg = MSG_WEEKLYCHECK_USE
            else:
                msg = MSG_WEEKLYCHECK_USE

        elif context.args[0] == "flag":
            msg = MSG_FLAG_USE

        elif context.args[0] == "goodbye":
            msg = MSG_GOODBYE_USE

        elif context.args[0] == "daysum":
            msg = MSG_DAYSUM_USE

    if msg == "":
        msg = MSG_HELP

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg)


# daysum: daily counter
def handler_daysum(update, context):
    global users

    first_callee(update, context)
    msg = "OOOPS..."

    # if length is 0, show help
    if len(context.args) >= 1:
        cmd = context.args[0]

        if cmd == 'show':
            msg = "?????? ???????????? %d ?????????." % users[str(update.effective_chat.id)]['daysum']
        
        elif cmd == 'clear':
            users[str(update.effective_chat.id)]['daysum'] = 0
            msg = "???????????? ????????????????????????." 
        
        elif cmd.isdigit():
            users[str(update.effective_chat.id)]['daysum'] += int(cmd)
            msg = "%d??? ???????????????. ?????? ???????????? %d ?????????." % (int(cmd), users[str(update.effective_chat.id)]['daysum'])

        else:
            msg = MSG_DAYSUM_USE

    else:
        msg = MSG_DAYSUM_USE


    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=msg)

# daily: daily reminder
# dailycheck item format: 'name': [hhmm, 'description', called]
#   hhmm: hour/minute to remind
#   description: description of reminder
#   called: lastly called day (YYMMDD)
def handler_daily(update, context):
    global users

    first_callee(update, context)
    msg = "OOOPS..."

    # if length is 0, show help
    if len(context.args) >= 1:
        cmd = context.args[0]

        # show reminders
        if cmd == 'show':
            items = users[str(update.effective_chat.id)]['dailycheck'].items()

            if len(items) == 0:
                msg = "?????? ????????? ?????? ??????????????? ????????????."
            else:
                msg = "????????? ?????? ???????????? ?????? (??? {}???):\n".format(len(items))
                for name, dat in items:
                    msg += "[{}] ?????? {}??? {}???\n".format(name, dat[0] // 100, dat[0] % 100)

        # add reminder
        elif cmd == 'add':
            # argument check
            ok = True
            hhmm = -1

            if len(context.args) < 3: # argc check
                msg = MSG_DAILYCHECK_ADD_USE
                ok = False
            else:
                if not context.args[2].isdigit(): # is hhmm digit?
                    msg = "<HHMM>??? ????????? ?????????????????????. ?????? ????????? 24???????????? ??????????????????."
                    ok = False
                else:
                    hhmm = int(context.args[2])
                    if hhmm >= 2400 or hhmm % 100 >= 60: # is hhmm time format?
                        msg = "<HHMM>??? ????????? ?????????????????????. ?????? ????????? 24???????????? ??????????????????."
                        ok = False
        
            if ok:
                if len(context.args) >= 4:
                    desc = ' '.join(context.args[3:])
                else:
                    desc = ""

                # duplication check
                if users[str(update.effective_chat.id)]['dailycheck'].get(context.args[1], None) != None:
                    msg = "?????? ?????? ????????? ?????? ??????????????? ????????????.\n\"/daily show\"??? ???????????????,\n\"/daily remove {}\"??? ?????? ??? ?????? ??????????????????.".format(context.args[1])

                elif context.args[1] in NAME_PROHIBITED:
                    msg = "??? ??????({})??? ????????? ??? ????????????. ?????? ???????????? ?????? ??????????????????.".format(context.args[1])

                else:
                    users[str(update.effective_chat.id)]['dailycheck'][context.args[1]] = [hhmm, desc, 0]
                    msg = "?????? ??????????????? ??????????????? ?????????????????????."

        # remove reminder
        elif cmd == 'remove':
            # argument check
            ok = True

            if len(context.args) < 2:
                msg = MSG_DAILYCHECK_REMOVE_USE
                ok = False
            
            if ok:
                if context.args[1] == "all":
                    users[str(update.effective_chat.id)]['dailycheck'] = dict()
                    msg = "?????? ??????????????? ?????? ??????????????????."

                else:
                    # existence check
                    if users[str(update.effective_chat.id)]['dailycheck'].get(context.args[1], None) == None:
                        msg = "???????????? ?????? ?????? ?????????????????????."
                    else:
                        del users[str(update.effective_chat.id)]['dailycheck'][context.args[1]]
                        msg = "?????? ????????????({})??? ??????????????????.".format(context.args[1])

        # invalid argument
        else:
            msg = MSG_DAILYCHECK_USE
    else:
        msg = MSG_DAILYCHECK_USE
    
    # show current dailycheck list
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=msg)

# weekly: weekly reminder
# weeklycheck item format: 'name': [hhmm, weekday, 'description', called]
def handler_weekly(update, context):
    global users

    first_callee(update, context)
    msg = "ooops..."


    if len(context.args) >= 1:
        cmd = context.args[0]

        if cmd == 'show':
            items = users[str(update.effective_chat.id)]['weeklycheck'].items()

            if len(items) == 0:
                msg = "?????? ????????? ?????? ??????????????? ????????????."
            else:
                msg = "????????? ?????? ???????????? ?????? (??? {}???):\n".format(len(items))
                for name, dat in items:
                    weekday = dat[1]
                    weekday_str_show = []
                    if weekday % 2 == 1:
                        weekday_str_show.append("???")
                    if (weekday >> 1) % 2 == 1:
                        weekday_str_show.append("???")
                    if (weekday >> 2) % 2 == 1:
                        weekday_str_show.append("???")
                    if (weekday >> 3) % 2 == 1:
                        weekday_str_show.append("???")
                    if (weekday >> 4) % 2 == 1:
                        weekday_str_show.append("???")
                    if (weekday >> 5) % 2 == 1:
                        weekday_str_show.append("???")
                    if (weekday >> 6) % 2 == 1:
                        weekday_str_show.append("???")


                    msg += "[{}] ?????? {}?????? {}??? {}???\n".format(name, ','.join(weekday_str_show), dat[0] // 100, dat[0] % 100)

        elif cmd == 'add':
            # arg check
            ok = True
            hhmm = -1
            weekday_int = 0
            
            if len(context.args) < 4:
                msg = MSG_WEEKLYCHECK_ADD_USE
                ok = False
            else:
                if not context.args[2].isdigit():
                    msg = "<HHMM>??? ????????? ?????????????????????. ?????? ????????? 24???????????? ??????????????????."
                    ok = False
                else:
                    hhmm = int(context.args[2])
                    if hhmm >= 2400 or hhmm % 100 >= 60:
                        msg = "<HHMM>??? ????????? ?????????????????????. ?????? ????????? 24???????????? ??????????????????."
                        ok = False
            if ok:
                # get weekday
                weekday_str = context.args[3]
                
                if "???" in weekday_str:
                    weekday_int += 1
                if "???" in weekday_str:
                    weekday_int += 2
                if "???" in weekday_str:
                    weekday_int += 4
                if "???" in weekday_str:
                    weekday_int += 8
                if "???" in weekday_str:
                    weekday_int += 16
                if "???" in weekday_str:
                    weekday_int += 32
                if "???" in weekday_str:
                    weekday_int += 64
                
                if weekday_int == 0:
                    msg = "<??????>??? ????????? ?????????????????????. \"?????????????????????\" ??? ?????? ????????? ??????????????????."
                    ok = False

                if ok:
                    if len(context.args) >= 5:
                        desc = ' '.join(context.args[4:])
                    else:
                        desc = ''

                    if users[str(update.effective_chat.id)]['weeklycheck'].get(context.args[1], None) != None:
                        msg = "?????? ?????? ????????? ?????? ??????????????? ????????????.\n\"/weekly show\"??? ???????????????,\n\"/weekly remove {}\"??? ?????? ??? ?????? ??????????????????.".format(context.args[1])

                    elif context.args[1] in NAME_PROHIBITED:
                        msg = "??? ??????({})??? ????????? ??? ????????????. ?????? ???????????? ?????? ??????????????????.".format(context.args[1])

                    else:
                        users[str(update.effective_chat.id)]['weeklycheck'][context.args[1]] = [hhmm, weekday_int, desc, 0]
                        msg = "?????? ??????????????? ??????????????? ?????????????????????."

        elif cmd == 'remove':
                if context.args[1] == "all":
                    users[str(update.effective_chat.id)]['weeklycheck'] = dict()
                    msg = "?????? ??????????????? ?????? ??????????????????."

                else:
                    # existence check
                    if users[str(update.effective_chat.id)]['weeklycheck'].get(context.args[1], None) == None:
                        msg = "???????????? ?????? ?????? ?????????????????????."
                    else:
                        del users[str(update.effective_chat.id)]['weeklycheck'][context.args[1]]
                        msg = "?????? ????????????({})??? ??????????????????.".format(context.args[1])


        else:
            msg = MSG_WEEKLYCHECK_USE
    else:
        msg = MSG_WEEKLYCHECK_USE
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg)

def handler_goodbye(update, context):
    global users
    first_callee(update, context)

    del users[str(update.effective_chat.id)]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="?????? ????????? ?????? ??????????????????. ??????????????? ????????? ?????? ???????????? ????????? ??? ????????????!")




# flag: (maple) flag reminder
# instant notification. For simplification, remove data after reminder
def handler_flag(update, context):
    global users

    first_callee(update, context)
    f = get_next_flag()
    users[str(update.effective_chat.id)]['flag'] = 1
    msg = "????????? ????????? ????????? ??????????????? ?????????????????????. ?????? ???????????? {} {}??? {}??? ?????????.".format(("??????" if f[0] else "??????"), f[1] // 100, f[1] % 100)
    
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=msg)

# publish: publish global message
# ONLY FOR ADMIN
def handler_publish(update, context):
    global users

    if admin_check(update, context):
        return  

    msg = "[??????]\n"
    msg += ' '.join(context.args)

    for chatid, _ in users.items():
        bot.send_msg(int(chatid), msg)

# deluser: delete user
# ONLY FOR ADMIN
def handler_deluser(update, context):
    global users

    if admin_check(update, context):
        return  

    msg = ""

    if len(context.args) >= 1:
        if users.get(context.args[0], None) != None:
            if context.args[0] != str(bot.get_adminid()):    
                del users[context.args[0]]
                msg = "??????????????? ?????? ID??? ????????? ??????????????????."
            else:
                msg = "???????????? ????????? ??? ????????????."
        else:
            msg = "?????? ID??? ????????? ???????????? ????????????."
    else:
        msg = "????????? ????????? ID??? ??????????????????."

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=msg)

# showuser: show current users info (to terminal)
# ONLY FOR ADMIN
def handler_showuser(update, context):
    first_callee(update, context)

    if admin_check(update, context):
        return

    pprint(users)

# save: save to JSON file
# ONLY FOR ADMIN
def handler_shutdown(update, context):
    first_callee(update, context)

    if admin_check(update, context, "shutdown... goodbye."):
        return
    
    save_to_file()

    if platform.system() == "Windows":
        print("[INFO] Current system is Windows, trying taskkill...")
        os.system('taskkill /pid {} /f'.format(pid))
    elif platform.system() == "Linux":
        print("[INFO] Current system is Linux, trying kill...")
        os.system('kill {}'.format(pid))
    else:
        print("[INFO] I don't know about this system, trying kill...")
        os.system('kill {}'.format(pid))

# ready: notify the bot is ready
# ONLY FOR ADMIN
def handler_ready(update, context):
    global get_ready

    first_callee(update, context)

    if admin_check(update, context, "Now, the bot is ready!"):
        return  

    if get_ready:
        print("[INFO] multithreading workers are already ready")
        return
    else:
        get_ready = True
        mutex.release()
    
        print("[INFO] multithreading works are now ready")



# MULTITHREAD WORKS #

# work_sparse: does something every 15 min
def work_sparse():
    save_to_file()

    th = threading.Timer(60*15, work_sparse)
    th.start()

# work_notification: check things to notify
# it is used for minute-level notification (but polls more frequently)
def work_notification():
    global users 

    now = int(datetime.datetime.now().strftime("%H%M"))

    # foreach user
    for chatid, dat in users.items():
        # midnight
        if now == 0:
            users[chatid]['daysum'] = 0

        # foreach dailycheck item
        for name, info in dat['dailycheck'].items():
            if info[0] == now and info[2] < get_yymmdd():
                # send reminder
                msgtosend = "[?????? ????????????] {}\n{}".format(name, info[1])
                bot.send_msg(int(chatid), msgtosend)

                # set called_today
                users[chatid]['dailycheck'][name][2] = get_yymmdd()

        # foreach weeklycheck item
        for name, info in dat['weeklycheck'].items():
            if info[0] == now and \
                info[3] < get_yymmdd() and \
                (info[1] >> datetime.datetime.today().weekday()) % 2 == 1:

                # send reminder
                msgtosend = "[?????? ????????????] {}\n{}".format(name, info[2])
                bot.send_msg(int(chatid), msgtosend)

                # set called_today
                users[chatid]['weeklycheck'][name][3] = get_yymmdd()


        # flag alarm
        if dat['flag'] == 1 and is_now_flag(now):
            users[chatid]['flag'] = 0
            bot.send_msg(int(chatid), "[????????? ????????? ??????] ??? ?????? ?????????!")

    th = threading.Timer(10, work_notification)
    th.start()

# multithread_caller: spawns multithreaded workers
# only called once
def multithread_caller():
    global mutex

    mutex.acquire()
    mutex.release()

    th1 = threading.Thread(target=work_notification)
    th2 = threading.Thread(target=work_sparse)
    
    th1.start()
    th2.start()



def main():
    global mutex
    global bot

    # initial setup
    init_first()
    init_load_users()

    # main thread acquires mutex lock (that is released after /ready)
    mutex.acquire()
    
    # general command
    bot.add_handler('help', handler_help)
    bot.add_handler("daysum", handler_daysum)
    bot.add_handler("daily", handler_daily)
    bot.add_handler("flag", handler_flag)
    bot.add_handler("weekly", handler_weekly)
    bot.add_handler("goodbye", handler_goodbye)
    
    # command only for admin (test, maintenance, management)
    bot.add_handler("ready", handler_ready)
    bot.add_handler("showuser", handler_showuser)
    bot.add_handler('shutdown', handler_shutdown)
    bot.add_handler('publish', handler_publish)
    bot.add_handler('deluser', handler_deluser)
    
    # spawn threads for asynchronous work
    th = threading.Thread(target=multithread_caller)
    th.start()

    # polls and handles command
    bot.start()

if __name__ == "__main__":
    main()