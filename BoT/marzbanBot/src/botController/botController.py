import traceback

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton ,ReplyKeyboardRemove , InlineKeyboardMarkup, InlineKeyboardButton

from src.controller.authCtrl import Authorization
from src.controller.userCtrl import User
from src.controller.managerCtrl import Manager
from src.controller.adminCtrl import Admin

from datetime import datetime
import json

def startController(message,bot,api_prefix):
    try:
        chat_id = message.chat.id
        auth = Authorization(api_prefix)
        result = auth.checkUser(chat_id)

        if (result.status_code == 401):
            new_user(message,bot)
        elif result.status_code == 500:
            handleError(message,bot,"")
        else:
            userData = result.json()
            userData = userData["body"]["data"]


            if userData['admit'] == 0:
                handleNoneAdmit(message,bot)
            else:
                if userData['spam'] == 1:
                    handleBanned(message,bot)
                else:
                    if userData["rule"] == "user":
                        userLogedin(message,bot,userData)
                    elif userData["rule"] == "manager":
                        managerLogedin(message, bot, userData)
                    elif userData["rule"] == "admin":
                        adminLogedin(message, bot, userData)
                    else:
                        bot.reply_to(message, """\
                                    متاسفانه اکانت شما تشخیص داده نشد
                                    """)
    except Exception as e:
        handleError(message,bot,e)

def new_user(message,bot):
    try:
        contactTxt = "اشتراک گذاری شماره"
        cancelTxt = "لغو احراز هویت"
        keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True,row_width=1)
        contact = KeyboardButton(text=contactTxt, request_contact=True)
        cancel = KeyboardButton(text=cancelTxt)
        keyboard.add(contact, cancel)
        replyMsg = """دوست عزیز ظاهرا هنوز عضوی از ما نشدی !!!\
                     برای استفاده از این ربات باید حتما به ما بپیوندی. لطفا شماره موبایل خودت رو اجازه بده داشته باشیم."""
        bot.send_message(message.chat.id, replyMsg, reply_markup=keyboard)

    except Exception as e:
        handleError(message, bot, e)

def sharedContact(message,bot,api_prefix):
    try:
        user = message.from_user
        contact = message.contact
        auth = Authorization(api_prefix)
        result = auth.newUser(
            user.id
            ,user.first_name+" "+user.last_name
            ,user.username
            ,contact.phone_number
            ,None
        )
        if(result.status_code ==200):
            authorizationSuccess(message,bot)
            startController(message,bot,api_prefix)
        else:
            handleError(message,bot)
    except Exception as e:
        handleError(message, bot, e)
def authorizationSuccess(message,bot):
    try:
        replyMsg = """اکانت شما با موفقت ساخته شد🙏
    """
        bot.reply_to(message, replyMsg)
    except Exception as e:
        handleError(message, bot, e)
def handleNoneAdmit(message,bot):
    try:
        replyMsg = """لطفا صبر کنید تا ادمین های ما بتونن تو اولین فرصت حساب کاربری شما را تایید کنند.❤️😉
    """
        bot.send_message(message.chat.id
            ,replyMsg,
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as e:
        handleError(message, bot, e)
def handleCancelAuthorization(message,bot):
    try:
        replyMsg = """خیلی ممنون از شما درخواست شما با موفقیت لغو شد. اگر میخواهید دوباره حساب کاربری بسازید لطفا /start را وارد نمایید . 
    
    ممنون از اینکه به ربات ما سر زدید❤️
    """

        bot.reply_to(message,
                     replyMsg,
                     reply_markup=ReplyKeyboardRemove()
        )
    except Exception as e:
        handleError(message, bot, e)
def handleBanned(message,bot):
    try:
        replyMsg = """متاسفانه اکانت شما به دلایل مختلفی از طریق ادمین ها مسدود شده هست🤦‍♂️ . برای اطلاعات بیشتر 
/help
را بزنید❤️
"""
        bot.reply_to(message,
                     replyMsg,
                     reply_markup=ReplyKeyboardRemove()
                     )

    except Exception as e:
        handleError(message, bot, e)
#--------------------------------------------------------------------------------- user --------------------------------------------------------------
def userLogedin(message,bot,user_data):
    try:
        configMsg = """کانفیگ های موجود برای شما"""
        historyMsg = """تاریخچه خرید های شما"""
        accountMsg = """اطلاعات حساب کاربری"""

        keyboard = InlineKeyboardMarkup(row_width=1)
        configButton = InlineKeyboardButton(text=configMsg, callback_data="user_see_configs")
        historyButton = InlineKeyboardButton(text=historyMsg, callback_data="user_see_history")
        accountButton = InlineKeyboardButton(text=accountMsg, callback_data="user_see_account")
        keyboard.add(configButton,historyButton,accountButton)

        msg = f"""{user_data["name"]} عزیز \n\
به حساب کاربری خود خوش آمدید. از منو پایین میتوانید انتحاب کنید به کحا بروید.\n\
در صورت بروز مشکل و یا سوال داشتن میتوانید از\n\
/help\n\
استفاده کنید."""
        bot.send_message(message.chat.id,msg,reply_markup=keyboard)
    except Exception as e:
        handleError(message, bot, e)

def handleUserSeeConfigs(call,bot,api_prefix):
    try:
        user = User(api_prefix)
        result = user.getConfigs(call.message.chat.id)
        if result.status_code == 200 :
            result = result.json()
            configs = result["body"]["data"]

            msg = """کافیگ های شما به شرح زیر میباشد:\n\n\nبرای دیدن اطلاعات کامل تر رو هر کدام کلیک کنید"""

            keyboard = InlineKeyboardMarkup(row_width=1)
            for config in configs:
                configMsg = f"""template: {config["template_id"]} | price: {config["price"]}0000 IRR"""
                configButton = InlineKeyboardButton(text=configMsg, callback_data=f"get_template_{config['template_id']}")
                keyboard.add(configButton)

            backHomeButton = InlineKeyboardButton(text="بازگشت",callback_data="back_to_home")
            keyboard.add(backHomeButton)

            bot.send_message(call.message.chat.id, msg, reply_markup=keyboard)

        else:
            handleError(call.message, bot, "")


    except Exception as e:
        handleError(call.message, bot, e)

def handleSelectTemplate(call,bot,api_prefix,template_id):
    try:
        user = User(api_prefix)
        result = user.getTemplate(template_id)
        if result.status_code == 200:
            template = result.json()["body"]["data"]

            msg = """اطلاعات کانفیگ به صورت زیر است : \n\n\n\nدر صورت مورد قبول بودن میتوانید آن را بخرید. """
            daysLimitButton = InlineKeyboardButton(
                text=f"days limit : {template['days_limit'] if template['days_limit'] else '-'}",
                callback_data="none-selectable")
            dataLimitButton = InlineKeyboardButton(
                text=f"data limit : {template['data_limit'] if template['data_limit'] else '-'}",
                callback_data="none-selectable")
            userLimitButton = InlineKeyboardButton(
                text=f"user limit : {template['user_limit'] if template['user_limit'] else '-'}",
                callback_data="none-selectable")
            inBounds = InlineKeyboardButton(
                text=f"in bounds : {template['in_bounds'] if template['in_bounds'] else '-'}",
                callback_data="none-selectable")
            price = InlineKeyboardButton(
                text=f"price : {template['price']}0000 IRR",
                callback_data="none-selectable")
            back_to_see_config = InlineKeyboardButton(
                text=f"بازگشت",
                callback_data="back_to_see_config")
            buyBotton = InlineKeyboardButton(
                text=f"خرید",
                callback_data=f"buy_template_{template['template_id']}")
            keyboard = [
                [daysLimitButton,dataLimitButton],
                [userLimitButton,inBounds],
                [price],
                [buyBotton],
                [back_to_see_config]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(call.message.chat.id,msg,reply_markup=markup)

        else:
            handleError(call.message,bot,"")

    except Exception as e:
        handleError(call.message, bot, e)


def handleBuyTemplate(call,bot,api_prefix,template_id):
    try:
        markup = InlineKeyboardMarkup()
        button = InlineKeyboardButton("انصراف", callback_data='cancel_purchase')
        markup.add(button)
        msg = """لطفا یک نام برای کانفیگ خود وارد کنید . \n\n\n\n در صورت عدم تمایل برای خرید میتوانید انصراف را بزنید."""
        bot.send_message(call.message.chat.id,text=msg,reply_markup=markup)
        bot.register_next_step_handler(call.message,lambda msg: buyTemplateWithName(msg,bot,template_id,api_prefix))

    except Exception as e:
        handleError(call.message, bot, e)


def buyTemplateWithName(message,bot,template_id,api_prefix):
    try:
        user = User(api_prefix)

        configName = message.json['text']
        chat_id = message.chat.id

        result = user.purchase(chat_id=chat_id,template_id=template_id,config_name=configName)
        if result.status_code == 200:
            config = result.json()['body']['data']['config']

            msg = f"""کانفیگ شما : \n\
{config}\n\
\n\n\nنام کانفیگ شما : \n\
{configName}"""

            markup = InlineKeyboardMarkup()
            button = InlineKeyboardButton("تایید", callback_data='back_to_home')
            markup.add(button)
            bot.reply_to(message, text=msg, reply_markup=markup)

        else :
            handleError(message, bot, "")
    except Exception as e:
        handleError(message, bot, e)


def handleUserSeeHistory(call,bot,api_prefix):
    try:
        user = User(api_prefix)
        result = user.getHistory(call.message.chat.id).json()
        debt = result['body']['data']['debt']
        histories = result['body']['data']['history']
        for history in histories:
            msg = f"""{datetime.fromisoformat(history['created_at'][:-1])}"""

            keyboard = [
                [
                    InlineKeyboardButton(f"name:{history['name']}", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"days limit:{history['days_limit']}", callback_data='none-selectable'),
                    InlineKeyboardButton(f"data limit:{history['data_limit']}",callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"user limit:{history['user_limit']}",callback_data='none-selectable'),
                    InlineKeyboardButton(f"in bounds:{history['in_bounds']}",callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"price:{history['price']}", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"دیدن لینک کافینگ", callback_data=f'see_config_links_{history["id"]}')
                ]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(call.message.chat.id,msg,reply_markup=markup)

        msg = f"کل بدهی شما به ما: {debt}0000 IRR"
        bot.send_message(call.message.chat.id,msg)
        startController(call.message, bot, api_prefix)

    except Exception as e:
        handleError(call.message, bot, e)

def showConfigLinks(call,bot,api_prefix,id):
    try:
        user = User(api_prefix)
        result = user.getConfigLink(id)
        if result.status_code == 200:
            result = result.json()['body']['data']
            msg = f"""نام کانفیگ شما:\n\
{result['config_name']}
\n\n\n کانفیگ شما:\n\
{result['config']}"""

            markup = InlineKeyboardMarkup()
            button = InlineKeyboardButton("بازگشت", callback_data='back_to_home')
            markup.add(button)
            bot.reply_to(call.message,text=msg,reply_markup=markup)

        else:
            handleError(call.message, bot, '')
    except Exception as e:
        handleError(call.message, bot, e)


def handleUserSeeAccount(call,bot,api_prefix):
    try:
        auth = Authorization(api_prefix)
        result = auth.checkUser(call.message.chat.id)
        if result.status_code == 200:
            user = result.json()['body']['data']

            msg = f"""اطلاعات شما به صورت زیر است!!\n\n\n\

مقدار بدهی کل شما به ما : {user['debt']}0000 IRR"""

            keyboard = [
                [
                    InlineKeyboardButton(f"name : {user['name']}", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"username : {user['username']}", callback_data='none-selectable'),
                    InlineKeyboardButton(f"phone : {user['phone']}", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"rule : {user['rule']}", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"relevant Admin : {user['relevantAdmin'] if user['relevantAdmin'] else '---'}", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"بازگشت", callback_data=f'back_to_home')
                ]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(call.message.chat.id, msg, reply_markup=markup)

        else:
            handleError(call.message, bot, '')

    except Exception as e:
        handleError(call.message, bot, e)

#--------------------------------------------------------- manager -----------------------------------------------------------------------------
def managerLogedin(message,bot,user_data):
    try:
        configMsg = """کانفیگ های موجود برای شما"""
        historyMsg = """تاریخچه خرید های شما"""
        accountMsg = """اطلاعات حساب کاربری"""
        managerPanelMsg = """پنل مدیریتی"""
        keyboard = InlineKeyboardMarkup(row_width=1)
        configButton = InlineKeyboardButton(text=configMsg, callback_data="user_see_configs")
        historyButton = InlineKeyboardButton(text=historyMsg, callback_data="user_see_history")
        accountButton = InlineKeyboardButton(text=accountMsg, callback_data="user_see_account")
        managerPanelButton = InlineKeyboardButton(text=managerPanelMsg, callback_data="manager_panel")
        keyboard.add(configButton,historyButton,accountButton,managerPanelButton)

        msg = f"""{user_data["name"]} عزیز \n\
به حساب کاربری خود خوش آمدید. از منو پایین میتوانید انتحاب کنید به کحا بروید.\n\
در صورت بروز مشکل و یا سوال داشتن میتوانید از\n\
/help\n\
استفاده کنید."""
        bot.send_message(message.chat.id,msg,reply_markup=keyboard)
    except Exception as e:
        handleError(message, bot, e)
def managerPanel(call,bot,api_prefix):
    try:
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
        msg = f"""به پنل مدیریتی خوش آمدید .\n\n\
لظفا انتخاب کنید چه کاری میخواهید انجام بدهید"""
        keyboard = [
            [
                InlineKeyboardButton(f"کاربران", callback_data='manager-see-users')
            ],
            [
                InlineKeyboardButton(f"کاربران جدید", callback_data='manager-see-new-users'),
                InlineKeyboardButton(f"کاربران مسدود", callback_data='manager-see-spam-users')
            ],
            [
                InlineKeyboardButton(f"قالب ها", callback_data='manager-see-templates')
            ],
            [
                InlineKeyboardButton(f"قالب جدید", callback_data='manager-create-templates')
            ],
            [
                InlineKeyboardButton(f"بازگشت", callback_data=f'back_to_home')
            ]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(call.message.chat.id, msg, reply_markup=markup)
    except Exception as e:
        handleError(call.message, bot, e)
def managerSeeUsers(call,bot,api_prefix):
    try:
        manager = Manager(api_prefix)

        result = manager.getUsers(call.message.chat.id)

        if result.status_code == 200:
            result = result.json()
            users = result['body']['data']

            msg = """\n\n\nکاربران شما به شرح زیر میباشد : \n\n\n"""

            markup = InlineKeyboardMarkup(row_width=2)
            for user in users:
                userBotton = InlineKeyboardButton(text=f"{user['username']} | {user['rule']}",callback_data=f"manager-see-user-{user['chat_id']}")
                markup.add(userBotton)

            backToHomeButton = InlineKeyboardButton(f"بازگشت به پنل مدیریت", callback_data=f'back_to_manager_panel')

            markup.add(backToHomeButton)

            bot.send_message(call.message.chat.id,msg,reply_markup=markup)
        else:
            handleError(call.message, bot, '')

    except Exception as e:
        handleError(call.message, bot, e)
def managerSeeUser(call,bot,api_prefix,user_id):
    try:
        auth = Authorization(api_prefix)
        user = auth.checkUser(user_id)

        if user.status_code == 200:
            user = user.json()
            user = user['body']['data']
            msg = f"""اطلاعات کاربر به شرح زیر است : \n\n\n\
لطفا یکی از گزینه ها را انتخاب کنید"""

            keyboard = [
                [
                    InlineKeyboardButton(f"نام : {user['name']}", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"نام کاربری : {user['username']}", callback_data='none-selectable'),
                    InlineKeyboardButton(f"تلفن : {user['phone']}", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"بدهی : {user['debt']}0000 IRR", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"نوع :{user['rule']}", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"ادمین مربوطه : {user['relevantAdminUsername'] if user['relevantAdminUsername'] else '---'}", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"اختصاص دادن ادمین", callback_data=f'assign-admin-to-user-{user_id}')
                ],
                [
                        InlineKeyboardButton(f"بن", callback_data=f'bann-user-{user_id}'),
                        InlineKeyboardButton(f"تاریخچه", callback_data=f'see-user-history-{user_id}')
                ],
                [
                    InlineKeyboardButton(f"کاهش بدهی", callback_data=f'manager-reduce-user-debt-{user_id}')
                ],
                [
                    InlineKeyboardButton(f"قالب های اختصاص داده شده", callback_data=f'see-assigned-template-{user_id}'),
                    InlineKeyboardButton(f"اختصاص دادن قالب", callback_data=f'assign-template-to-user-{user_id}')
                ],
                [
                    InlineKeyboardButton(f"تبدیل به ادمین" if user['rule'] == 'user' else "تبدیل به کاربر", callback_data=(f'manager-alter-user-to-admin-{user_id}' if user['rule'] == 'user' else f'manager-alter-admin-to-user-{user_id}'))
                ],
                [
                    InlineKeyboardButton(f"بازگشت به پنل مدیریت", callback_data=f'back_to_manager_panel')
                ]
            ]

            markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(chat_id=call.message.chat.id, text=msg, reply_markup=markup)
        else:
            handleError(call.message, bot, '')
    except Exception as e:
        handleError(call.message, bot, e)
def assignAdminToUser(call,bot,api_prefix,user_id):
    try:
        manager = Manager(api_prefix)
        admins = manager.getAdmins(chat_id=call.message.chat.id)

        if admins.status_code == 200:
            admins = admins.json()['body']['data']

            msg = """لطفا ادمین مربوطه را انتخاب کنید:"""

            markup = InlineKeyboardMarkup(row_width=2)

            for admin in admins:
                adminButton = InlineKeyboardButton(text=f"{admin['username']}",callback_data=f"assign-template-to-user-final-{admin['chat_id']}-{user_id}")
                markup.add(adminButton)

            cancelButton = InlineKeyboardButton(text="انصراف",
                                               callback_data=f"manager-see-user-{user_id}")
            markup.add(cancelButton)
            bot.send_message(chat_id=call.message.chat.id,text=msg,reply_markup=markup)

        else:
            handleError(call.message, bot, '')
    except Exception as e:
        handleError(call.message, bot, e)
def assignAdminToUserFinal(call,bot,api_prefix,user_id,admin_id):
    try:
        manager = Manager(api_prefix)
        admins = manager.assignAdmin(chat_id=call.message.chat.id,user_id=user_id,admin_id=admin_id)

        if admins.status_code == 200:

            msg = """عملیات با موفقیت انجام شد"""

            markup = InlineKeyboardMarkup(row_width=2)

            backButton = InlineKeyboardButton(text="بازگشت",
                                               callback_data=f"manager-see-user-{user_id}")
            markup.add(backButton)
            bot.send_message(chat_id=call.message.chat.id,text=msg,reply_markup=markup)

        else:
            handleError(call.message, bot, '')
    except Exception as e:
        handleError(call.message, bot, e)
def bannUser(call,bot,api_prefix,user_id):
    try:
        manager = Manager(api_prefix)
        result = manager.bannUser(chat_id=call.message.chat.id,user_id=user_id)

        if result.status_code == 200:
            msg = """عملیات با موفقیت انجام شد"""

            markup = InlineKeyboardMarkup(row_width=2)

            backButton = InlineKeyboardButton(text="بازگشت به پنل مدیریت",
                                              callback_data=f"back_to_manager_panel")
            markup.add(backButton)
            bot.send_message(chat_id=call.message.chat.id, text=msg, reply_markup=markup)

        else:
            handleError(call.message, bot, '')
    except Exception as e:
        handleError(call.message, bot, e)
def managerSeeHistory(call,bot,api_prefix,user_id):
    try:
        user = User(api_prefix)
        result = user.getHistory(user_id)

        if result.status_code == 200 :
            result = result.json()
            debt = result['body']['data']['debt']
            histories = result['body']['data']['history']
            for history in histories:
                msg = f"""{datetime.fromisoformat(history['created_at'][:-1])}"""

                keyboard = [
                    [
                        InlineKeyboardButton(f"name:{history['name']}", callback_data='none-selectable')
                    ],
                    [
                        InlineKeyboardButton(f"days limit:{history['days_limit']}", callback_data='none-selectable'),
                        InlineKeyboardButton(f"data limit:{history['data_limit']}",callback_data='none-selectable')
                    ],
                    [
                        InlineKeyboardButton(f"user limit:{history['user_limit']}",callback_data='none-selectable'),
                        InlineKeyboardButton(f"in bounds:{history['in_bounds']}",callback_data='none-selectable')
                    ],
                    [
                        InlineKeyboardButton(f"price:{history['price']}0,000 IRR", callback_data='none-selectable')
                    ],
                ]
                markup = InlineKeyboardMarkup(keyboard)
                bot.send_message(call.message.chat.id,msg,reply_markup=markup)

            msg = f"کل بدهی کاربر به ما: {debt}0000 IRR"
            bot.send_message(call.message.chat.id,msg)
            managerSeeUser(call,bot,api_prefix,user_id)
        else:
            handleError(call.message, bot, '')
    except Exception as e:
        handleError(call.message, bot, e)
def managerAssignTemplate(call,bot,api_prefix,user_id):
    try:
        manager = Manager(api_prefix)
        result = manager.getTemplates(call.message.chat.id)

        if result.status_code == 200:
            result = result.json()
            templates = result['body']['data']

            markup = InlineKeyboardMarkup(row_width=2)

            for template in templates:

                templateButton = InlineKeyboardButton(text=f"{template['template_id']} | {template['price']}0,000 IRR",
                                                  callback_data=f"select-template-to-assign-user-{user_id}-{template['template_id']}")
                markup.add(templateButton)

            backButton = InlineKeyboardButton(text="بازگشت",
                                              callback_data=f"manager-see-user-{user_id}")

            markup.add(backButton)

            msg = """لطفا قالب مدنظر را انتخا کنید:"""
            bot.send_message(call.message.chat.id,msg,reply_markup=markup)

        else:
            handleError(call.message, bot, '')

    except Exception as e:
        handleError(call.message, bot, e)
def managerShowTemplateToAssignTemplate(call,bot,api_prefix,user_id,template_id):
    try:
        manager = Manager(api_prefix)
        result = manager.getTemplate(call.message.chat.id,template_id=template_id)

        if result.status_code == 200:
            result = result.json()
            template = result['body']['data']
            keyboard = [
                [
                    InlineKeyboardButton(f"name:{template['price']}0,000 IRR", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"days limit:{template['days_limit']}", callback_data='none-selectable'),
                    InlineKeyboardButton(f"data limit:{template['data_limit']}", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"user limit:{template['user_limit']}", callback_data='none-selectable'),
                    InlineKeyboardButton(f"in bounds:{template['in_bounds']}", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"تایید", callback_data=f"admit-assign-template-to-user-{user_id}-{template_id}")
                ],
                [
                    InlineKeyboardButton(text="بازگشت",callback_data=f"assign-template-to-user-{user_id}")
                ]
            ]
            markup = InlineKeyboardMarkup(keyboard)

            msg = """آیا قالب مورد تایید است؟"""
            bot.send_message(call.message.chat.id,msg,reply_markup=markup)

        else:
            handleError(call.message, bot, '')

    except Exception as e:
        handleError(call.message, bot, e)
def managerFinishAssignTemplate(call,bot,api_prefix,user_id,template_id):
    try:
        manager = Manager(api_prefix)
        result = manager.assignTemplate(chat_id=call.message.chat.id,user_id=user_id,template_id=template_id)

        if result.status_code == 200:
            markup = InlineKeyboardMarkup()

            backButton = InlineKeyboardButton(text="بازگشت", callback_data=f"manager-see-user-{user_id}")

            markup.add(backButton)
            msg = """عملیات با موفقیت انجام شد"""
            bot.send_message(call.message.chat.id,msg,reply_markup=markup)

        else:
            bot.reply_to(call.message,
                         """این قالب قبلا به کاربر اختصاص داده شده است.""")

    except Exception as e:
        handleError(call.message, bot, e)
def seeAssignedTemplate(call,bot,api_prefix,user_id):
    try:
        user = User(api_prefix)

        templates = user.getConfigs(user_id)

        if templates.status_code == 200:
            templates = templates.json()['body']['data']

            if len(templates) == 0 :
                bot.send_message(call.message.chat.id,"هیچ قالبی به کاربر اختصاص داده نشده")
            else:
                for template in templates:
                    msg = f"""id : {template['template_id']}"""

                    keyboard = [
                        [
                            InlineKeyboardButton(f"price:{template['price']}0,000 IRR", callback_data='none-selectable')
                        ],
                        [
                            InlineKeyboardButton(f"days limit:{template['days_limit']}",
                                                 callback_data='none-selectable'),
                            InlineKeyboardButton(f"data limit:{template['data_limit']}", callback_data='none-selectable')
                        ],
                        [
                            InlineKeyboardButton(f"user limit:{template['user_limit']}",
                                                 callback_data='none-selectable'),
                            InlineKeyboardButton(f"in bounds:{template['in_bounds']}", callback_data='none-selectable')
                        ],
                        [
                            InlineKeyboardButton(f"لغو تخصیص این قالب",callback_data=f"manager-cancel-assigned-template-{user_id}-{template['template_id']}")
                        ]

                    ]
                    markup = InlineKeyboardMarkup(keyboard)
                    bot.send_message(call.message.chat.id, msg, reply_markup=markup)

                managerSeeUser(call, bot, api_prefix, user_id)

        else:
            handleError(call.message, bot, '')
    except Exception as e:
        handleError(call.message, bot, e)
def managerCancelAssignedTemplate(call,bot,api_prefix,user_id,template_id):
    try:
        manager = Manager(api_prefix)
        response = manager.deleteAssignedTemplate(call.message.chat.id,user_id,template_id)

        if response.status_code == 200:
            msg = "عملیات با موفقیت انجام شد"
            backButton = InlineKeyboardButton("بازگشت",callback_data=f"manager-see-user-{user_id}")
            markup = InlineKeyboardMarkup()
            markup.add(backButton)
            bot.send_message(call.message.chat.id,msg,reply_markup=markup)
            bot.send_message(user_id,f"قالب با آیدی {template_id} به شما از تخصیص داده های شما حذف شد.")
        else:
            handleError(call.message, bot, '')
    except Exception as e:
        handleError(call.message, bot, e)
def managerReduceUserDebt(call,bot,api_prefix,user_id):
    try:
        markup = InlineKeyboardMarkup()
        cancelButton = InlineKeyboardButton('انصراف',callback_data=f"manager-see-user-{user_id}")
        markup.add(cancelButton)
        msg = "لطفا مقدار قیمت را برای کاهش وارد کنید : \n\n\nبرای لغو عملیات انصراف را بزنید"
        bot.send_message(call.message.chat.id,text=msg,reply_markup=markup)
        bot.register_next_step_handler(call.message,lambda msg: reduceUserDebt(msg,bot,api_prefix,user_id))
    except Exception as e:
        handleError(call.message, bot, e)
def reduceUserDebt(message,bot,api_prefix,user_id):
    try:
        amount = str(message.json['text'])
        if amount.isdigit():
            amount = int(amount)
            amount = amount / 10000

            admin = Admin(api_prefix)

            response = admin.reduceUserDebt(message.chat.id,user_id=user_id,amount=amount)
            if response.status_code == 200 :
                markup = InlineKeyboardMarkup()
                cancelButton = InlineKeyboardButton('بازگشت', callback_data=f"manager-see-user-{user_id}")
                markup.add(cancelButton)
                msg = "عملیات با موفقیت انجام شد"
                bot.send_message(message.chat.id, text=msg, reply_markup=markup)
            else:
                handleError(message,bot,'')

        else :
            markup = InlineKeyboardMarkup()
            cancelButton = InlineKeyboardButton('انصراف', callback_data=f"manager-see-user-{user_id}")
            markup.add(cancelButton)
            msg = "لطفا مقدار قیمت را برای کاهش وارد تنها به صورت عدد به ریال کنید : \n\n\nبرای لغو عملیات انصراف را بزنید"
            bot.send_message(message.chat.id, text=msg, reply_markup=markup)
            bot.register_next_step_handler(message, lambda msg: reduceUserDebt(msg, bot, api_prefix, user_id))
    except Exception as e:
        handleError(message, bot, e)
def managerPromoteToAdmin(call, bot, api_prefix, user_id):
    try:
        manager = Manager(api_prefix)
        response = manager.alterUser(call.message.chat.id,user_id=user_id,rule="admin")
        if response.status_code == 200 :
            markup = InlineKeyboardMarkup()
            cancelButton = InlineKeyboardButton('بازگشت', callback_data=f"back_to_manager_panel")
            markup.add(cancelButton)
            msg = "عملیات با موفقیت انجام شد"
            bot.send_message(call.message.chat.id, text=msg, reply_markup=markup)
            bot.send_message(user_id,"وضعیت شما به ادمین تغییر پیدا کرد")
        else:
            handleError(call.message,bot,'')

    except Exception as e:
        handleError(call.message, bot, e)
def managerPromoteToUser(call, bot, api_prefix, user_id):
    try:
        manager = Manager(api_prefix)
        response = manager.alterUser(call.message.chat.id,user_id=user_id,rule="user")
        if response.status_code == 200 :
            markup = InlineKeyboardMarkup()
            cancelButton = InlineKeyboardButton('بازگشت', callback_data=f"back_to_manager_panel")
            markup.add(cancelButton)
            msg = "عملیات با موفقیت انجام شد"
            bot.send_message(call.message.chat.id, text=msg, reply_markup=markup)
            bot.send_message(user_id,"وضعیت شما به کاربر تغییر پیدا کرد")
        else:
            handleError(call.message,bot,'')

    except Exception as e:
        handleError(call.message, bot, e)
def managerSeeNewUsers(call,bot,api_prefix):
    try:
        manager = Manager(api_prefix)
        newUsers = manager.getNoneAdmitUsers(call.message.chat.id)

        if newUsers.status_code == 200:
            newUsers = newUsers.json()['body']['data']
            markup = InlineKeyboardMarkup()
            for user in newUsers:
                userButton = InlineKeyboardButton(f"{user['username']}",callback_data=f"manager-see-new-user-{user['chat_id']}")
                markup.add(userButton)
            backButton = InlineKeyboardButton('بازگشت', callback_data=f"back_to_manager_panel")
            markup.add(backButton)
            msg = "لطفا کاربر را انتخاب کنید : "
            bot.send_message(call.message.chat.id,msg,reply_markup=markup)
        else:
            handleError(call.message, bot, '')

    except Exception as e:
        handleError(call.message, bot, e)
def managerSeeNewUser(call,bot,api_prefix,user_id):
    try:
        user = User(api_prefix)
        userData= user.getUser(user_id)

        if userData.status_code == 200:
            userData = userData.json()['body']['data']

            keyBoard = [
                [
                    InlineKeyboardButton(text=f"{userData['name']}",callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"username : {userData['username']}", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"phone : {userData['phone']}", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f'تایید این کاربر',callback_data=f'manager-admit-new-user-{user_id}')
                ],
                [
                    InlineKeyboardButton('بازگشت', callback_data=f"back_to_manager_panel")
                ]
            ]

            markup = InlineKeyboardMarkup(keyBoard)
            msg = "اگر اطلاعات کاربر مورد تایید است لطفا آن را تایید کنید."
            bot.send_message(call.message.chat.id,msg,reply_markup=markup)
        else:
            handleError(call.message, bot, '')

    except Exception as e:
        handleError(call.message, bot, e)
def managerAdmitNewUser(call,bot,api_prefix,user_id):
    try:
        manager = Manager(api_prefix)
        response = manager.admitNewUser(call.message.chat.id,user_id)
        if response.status_code == 200:
            msg = """عملیات با موفقیت انجام شد"""
            markup = InlineKeyboardMarkup()
            backButton = InlineKeyboardButton(text='بازگشت', callback_data=f"back_to_manager_panel")
            markup.add(backButton)
            bot.send_message(call.message.chat.id,msg,reply_markup=markup)
            bot.send_message(user_id,"اکانت شما با موقیت تایید شد")

        else:
            handleError(call.message, bot, '')

    except Exception as e:
        handleError(call.message, bot, e)
def managerSeeSpamUsers(call,bot,api_prefix):
    try:
        manager = Manager(api_prefix)
        spamUsers = manager.getSpamUsers(call.message.chat.id)

        if spamUsers.status_code == 200:
            spamUsers = spamUsers.json()['body']['data']
            markup = InlineKeyboardMarkup()
            for user in spamUsers:
                userButton = InlineKeyboardButton(f"{user['username']}",callback_data=f"manager-see-spam-user-{user['chat_id']}")
                markup.add(userButton)
            backButton = InlineKeyboardButton('بازگشت', callback_data=f"back_to_manager_panel")
            markup.add(backButton)
            msg = "لطفا کاربر را انتخاب کنید : "
            bot.send_message(call.message.chat.id,msg,reply_markup=markup)
        else:
            handleError(call.message, bot, '')

    except Exception as e:
        handleError(call.message, bot, e)
def managerSeeSpamUser(call,bot,api_prefix,user_id):
    try:
        user = User(api_prefix)
        userData= user.getUser(user_id)

        if userData.status_code == 200:
            userData = userData.json()['body']['data']

            keyBoard = [
                [
                    InlineKeyboardButton(text=f"{userData['name']}",callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"username : {userData['username']}", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"phone : {userData['phone']}", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f'حذف مسدودیت',callback_data=f'manager-unbann-user-{user_id}')
                ],
                [
                    InlineKeyboardButton('بازگشت', callback_data=f"back_to_manager_panel")
                ]
            ]

            markup = InlineKeyboardMarkup(keyBoard)
            msg = "اگر اطلاعات کاربر مورد قبول است میتوانید مسدودیت آن را حذف کنید."
            bot.send_message(call.message.chat.id,msg,reply_markup=markup)
        else:
            handleError(call.message, bot, '')

    except Exception as e:
        handleError(call.message, bot, e)
def managerUnbanUser(call,bot,api_prefix,user_id):
    try:
        manager = Manager(api_prefix)
        response = manager.unbannUser(call.message.chat.id,user_id)
        if response.status_code == 200:
            msg = """عملیات با موفقیت انجام شد"""
            markup = InlineKeyboardMarkup()
            backButton = InlineKeyboardButton(text='بازگشت', callback_data=f"back_to_manager_panel")
            markup.add(backButton)
            bot.send_message(call.message.chat.id,msg,reply_markup=markup)
            bot.send_message(user_id,"اکانت شما بااز مسدودیت درآمد شد")

        else:
            handleError(call.message, bot, '')

    except Exception as e:
        handleError(call.message, bot, e)
def managerSeeTemplates(call,bot,api_prefix):
    try:
        manager = Manager(api_prefix)
        templates = manager.getTemplates(call.message.chat.id)
        if templates.status_code == 200:
            templates = templates.json()['body']['data']
            markup = InlineKeyboardMarkup()
            for template in templates:
                markup.add(InlineKeyboardButton(f"id : {template['template_id']} | price : {template['price']}0,000 IRR",callback_data=f"manager-see-template-{template['template_id']}"))
            markup.add(InlineKeyboardButton('بازگشت',callback_data="back_to_manager_panel"))
            bot.send_message(call.message.chat.id,"برای دیدن قالب روی آن کلیک کنید.",reply_markup=markup)
        else:
            handleError(call.message, bot, '')

    except Exception as e:
        handleError(call.message, bot, e)
def managerSeeTemplate(call,bot,api_prefix,template_id):
    try:
        manager = Manager(api_prefix)
        templates = manager.getTemplate(call.message.chat.id,template_id=template_id)

        if templates.status_code == 200:
            templates = templates.json()['body']['data']
            keyboard = [
                [
                    InlineKeyboardButton(f"id : {templates['template_id']}", callback_data='none-selectable'),
                ],
                [
                    InlineKeyboardButton(f"days limit : {templates['days_limit']}",callback_data='none-selectable'),
                    InlineKeyboardButton(f"data limit : {templates['data_limit']}",callback_data='none-selectable'),
                ],
                [
                    InlineKeyboardButton(f"price : {templates['price']}0,000 IRR", callback_data='none-selectable'),
                ],
                [
                    InlineKeyboardButton(f"user limit : {templates['user_limit']}", callback_data='none-selectable'),
                    InlineKeyboardButton(f"in bounds : {templates['in_bounds']}", callback_data='none-selectable'),
                ],
                [
                    InlineKeyboardButton(f"who created : {templates['whoCreated']}", callback_data='none-selectable'),
                    InlineKeyboardButton(f"parent template id : {templates['parent_template_id']}", callback_data='none-selectable'),
                ],
                [
                    InlineKeyboardButton(f"حذف",callback_data=f"manager-delete-template-{template_id}")
                ],
                [
                    InlineKeyboardButton(f"بازگشت", callback_data=f"back_to_manager_panel")
                ],
            ]
            markup = InlineKeyboardMarkup(keyboard)

            bot.send_message(call.message.chat.id,"اطلاعات قالب به صورت زیر است : ",reply_markup=markup)
        else:
            handleError(call.message, bot, '')

    except Exception as e:
        handleError(call.message, bot, e)
def managerDeleteTemplate(call,bot,api_prefix,template_id):
    try:
        manager = Manager(api_prefix)
        templates = manager.deleteTemplate(call.message.chat.id, template_id=template_id)

        if templates.status_code == 200:

            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(f"بازگشت", callback_data=f"back_to_manager_panel"))
            bot.send_message(call.message.chat.id, "عملیات با موفقیت انجام شد.", reply_markup=markup)
        else:
            handleError(call.message, bot, '')

    except Exception as e:
        handleError(call.message, bot, e)
def managerCreateTemplate(call,bot,api_prefix):
    try:
        markup = InlineKeyboardMarkup()
        button = InlineKeyboardButton("انصراف",callback_data=f"back_to_manager_panel")
        markup.add(button)
        msg = """لطفا days limit را وارد کنیدو\n\n\nدر صورت اینکه میخواهید خالی باشد خالی(با empty) را تایپ کنید.\n\n\nدرصورت عدم تمایل انصراف را بزنید."""
        bot.send_message(call.message.chat.id,text=msg,reply_markup=markup)
        bot.register_next_step_handler(call.message,lambda msg: managerCreateTemplateGetDataLimit(msg,bot,api_prefix))
    except Exception as e:
        handleError(call.message, bot, e)
def managerCreateTemplateGetDataLimit(message,bot,api_prefix):
    try:
        days_limit = str(message.json['text'])
        markup = InlineKeyboardMarkup()
        button = InlineKeyboardButton("انصراف",callback_data=f"back_to_manager_panel")
        markup.add(button)
        if days_limit == 'خالی' or days_limit == 'empty':
            days_limit = None
            msg = "لطفاdata limit (GB) را وارد کنید.\n\n\nدر صورت اینکه میخواهید خالی باشد خالی(با empty) را تایپ کنید.\n\n\nدرصورت عدم تمایل انصراف را بزنید"
            bot.send_message(message.chat.id,text=msg,reply_markup=markup)
            bot.register_next_step_handler(message,lambda msg: managerCreateTemplateGetUserLimit(msg,bot,api_prefix,days_limit))
        elif days_limit.isdigit():
            days_limit = int(days_limit)
            msg = "لطفا(GB) data limit را وارد کنید.\n\n\nدر صورت اینکه میخواهید خالی باشد خالی(با empty) را تایپ کنید.\n\n\nدرصورت عدم تمایل انصراف را بزنید"
            bot.send_message(message.chat.id,text=msg,reply_markup=markup)
            bot.register_next_step_handler(message,lambda msg: managerCreateTemplateGetUserLimit(msg,bot,api_prefix,days_limit))
        else:
            msg = "توجه!!!\n\n\nلطفا days limit را ''تنها به صورت عددی'' وارد کنید.\n\n\nدر صورت اینکه میخواهید خالی باشد خالی(با empty) را تایپ کنید.\n\n\nدرصورت عدم تمایل انصراف را بزنید"
            bot.send_message(message.chat.id, text=msg, reply_markup=markup)
            bot.register_next_step_handler(message, lambda msg: managerCreateTemplateGetDataLimit(msg,bot,api_prefix))
    except Exception as e:
        handleError(message, bot, e)
def managerCreateTemplateGetUserLimit(message,bot,api_prefix,days_limit):
    try:
        data_limit = str(message.json['text'])
        markup = InlineKeyboardMarkup()
        button = InlineKeyboardButton("انصراف",callback_data=f"back_to_manager_panel")
        markup.add(button)
        if data_limit == 'خالی' or data_limit == 'empty':
            data_limit = None
            msg = "لطفا user limit را وارد کنید.\n\n\nدر صورت اینکه میخواهید خالی باشد خالی(با empty) را تایپ کنید.\n\n\nدرصورت عدم تمایل انصراف را بزنید"
            bot.send_message(message.chat.id,text=msg,reply_markup=markup)
            bot.register_next_step_handler(message,lambda msg: managerCreateTemplateGetInBound(msg,bot,api_prefix,days_limit,data_limit))
        elif data_limit.isdigit():
            data_limit = int(data_limit)
            msg = "لطفا user limit را وارد کنید.\n\n\nدر صورت اینکه میخواهید خالی باشد خالی(با empty) را تایپ کنید.\n\n\nدرصورت عدم تمایل انصراف را بزنید"
            bot.send_message(message.chat.id,text=msg,reply_markup=markup)
            bot.register_next_step_handler(message,lambda msg: managerCreateTemplateGetInBound(msg,bot,api_prefix,days_limit,data_limit))
        else:
            msg = "توجه!!!\n\n\nلطفا(GB) data limit را ''تنها به صورت عددی'' وارد کنید.\n\n\nدر صورت اینکه میخواهید خالی باشد خالی(با empty) را تایپ کنید.\n\n\nدرصورت عدم تمایل انصراف را بزنید"
            bot.send_message(message.chat.id, text=msg, reply_markup=markup)
            bot.register_next_step_handler(message, lambda msg: managerCreateTemplateGetUserLimit(msg,bot,api_prefix,days_limit))
    except Exception as e:
        handleError(message, bot, e)
def managerCreateTemplateGetInBound(message,bot,api_prefix,days_limit,data_limit):
    try:
        user_limit = str(message.json['text'])
        markup = InlineKeyboardMarkup()
        button = InlineKeyboardButton("انصراف",callback_data=f"back_to_manager_panel")
        markup.add(button)
        if user_limit == 'خالی' or user_limit == 'empty':
            user_limit = None
            msg = "لطفا inbound را وارد کنید.\n\n\nدر صورت اینکه میخواهید خالی باشد خالی(با empty) را تایپ کنید.\n\n\nدرصورت عدم تمایل انصراف را بزنید"
            bot.send_message(message.chat.id,text=msg,reply_markup=markup)
            bot.register_next_step_handler(message,lambda msg: managerCreateTemplateGetPrice(msg,bot,api_prefix,days_limit,data_limit,user_limit))
        elif user_limit.isdigit():
            user_limit = int(user_limit)
            msg = "لطفا inbound را وارد کنید.\n\n\nدر صورت اینکه میخواهید خالی باشد خالی(با empty) را تایپ کنید.\n\n\nدرصورت عدم تمایل انصراف را بزنید"
            bot.send_message(message.chat.id,text=msg,reply_markup=markup)
            bot.register_next_step_handler(message,lambda msg: managerCreateTemplateGetPrice(msg,bot,api_prefix,days_limit,data_limit,user_limit))
        else:
            msg = "توجه!!!\n\n\nلطفا user limit را ''تنها به صورت عددی'' وارد کنید.\n\n\nدر صورت اینکه میخواهید خالی باشد خالی(با empty) را تایپ کنید.\n\n\nدرصورت عدم تمایل انصراف را بزنید"
            bot.send_message(message.chat.id, text=msg, reply_markup=markup)
            bot.register_next_step_handler(message, lambda msg: managerCreateTemplateGetInBound(msg,bot,api_prefix,days_limit))
    except Exception as e:
        handleError(message, bot, e)
def managerCreateTemplateGetPrice(message,bot,api_prefix,days_limit,data_limit,user_limit):
    try:
        in_bounds = str(message.json['text'])
        markup = InlineKeyboardMarkup()
        button = InlineKeyboardButton("انصراف",callback_data=f"back_to_manager_panel")
        markup.add(button)
        if in_bounds == 'خالی' or in_bounds == 'empty':
            in_bounds = None
            msg = "لطفا قیمت را وارد کنید.\n\n\nدرصورت عدم تمایل انصراف را بزنید"
            bot.send_message(message.chat.id,text=msg,reply_markup=markup)
            bot.register_next_step_handler(message,lambda msg: managerCreateTemplateFinal(msg,bot,api_prefix,days_limit,data_limit,user_limit,in_bounds))
        else :
            in_bounds = in_bounds
            msg = "لطفا قیمت را وارد کنید.\n\n\nدرصورت عدم تمایل انصراف را بزنید"
            bot.send_message(message.chat.id,text=msg,reply_markup=markup)
            bot.register_next_step_handler(message,lambda msg: managerCreateTemplateFinal(msg,bot,api_prefix,days_limit,data_limit,user_limit,in_bounds))
    except Exception as e:
        handleError(message, bot, e)
def managerCreateTemplateFinal(message,bot,api_prefix,days_limit,data_limit,user_limit,in_bounds):
    try:
        price = str(message.json['text'])
        markup = InlineKeyboardMarkup()
        button = InlineKeyboardButton("بازگشت", callback_data=f"back_to_manager_panel")
        markup.add(button)
        if price.isdigit():
            price = int(price)
            price = price / 10000
            manager = Manager(api_prefix)
            response = manager.addTemplate(message.chat.id,days_limit,data_limit,price,user_limit,in_bounds)
            if response.status_code == 200:
                msg = "عملیات با موفقیت انجام شد."
                bot.send_message(message.chat.id, text=msg, reply_markup=markup)
            else:
                handleError(message,bot,'')
        else:
            msg = "توجه!!!\n\n\nلطفا price را ''تنها به صورت عددی'' وارد کنید.\n\n\nدر صورت اینکه میخواهید خالی باشد خالی(با empty) را تایپ کنید.\n\n\nدرصورت عدم تمایل انصراف را بزنید"
            bot.send_message(message.chat.id, text=msg, reply_markup=markup)
            bot.register_next_step_handler(message, lambda msg: managerCreateTemplateFinal(msg, bot, api_prefix,
                                                                                                  days_limit,user_limit,in_bounds))
    except Exception as e:
        handleError(message, bot, e)
#----------------------------------------- admin ----------------------------------------
def adminLogedin(message,bot,user_data):
    try:
        configMsg = """کانفیگ های موجود برای شما"""
        historyMsg = """تاریخچه خرید های شما"""
        accountMsg = """اطلاعات حساب کاربری"""
        managerPanelMsg = """پنل ادمین"""
        keyboard = InlineKeyboardMarkup(row_width=1)
        configButton = InlineKeyboardButton(text=configMsg, callback_data="user_see_configs")
        historyButton = InlineKeyboardButton(text=historyMsg, callback_data="user_see_history")
        accountButton = InlineKeyboardButton(text=accountMsg, callback_data="user_see_account")
        managerPanelButton = InlineKeyboardButton(text=managerPanelMsg, callback_data="admin_panel")
        keyboard.add(configButton,historyButton,accountButton,managerPanelButton)

        msg = f"""{user_data["name"]} عزیز \n\
به حساب کاربری خود خوش آمدید. از منو پایین میتوانید انتحاب کنید به کحا بروید.\n\
در صورت بروز مشکل و یا سوال داشتن میتوانید از\n\
/help\n\
استفاده کنید."""
        bot.send_message(message.chat.id,msg,reply_markup=keyboard)
    except Exception as e:
        handleError(message, bot, e)
def adminPanel(call,bot,api_prefix):
    try:
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
        msg = f"""به پنل مدیریتی خوش آمدید .\n\n\
لظفا انتخاب کنید چه کاری میخواهید انجام بدهید"""
        keyboard = [
            [
                InlineKeyboardButton(f"کاربران", callback_data='admin-see-users')
            ],
            [
                InlineKeyboardButton(f"قالب ها ساخته شده", callback_data='admin-see-templates')
            ],
            [
                InlineKeyboardButton(f"قالب جدید", callback_data='admin-create-templates')
            ],
            [
                InlineKeyboardButton(f"بازگشت", callback_data=f'back_to_home')
            ]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(call.message.chat.id, msg, reply_markup=markup)
    except Exception as e:
        handleError(call.message, bot, e)
def adminCreateTemplate(call,bot,api_prefix):
    try:
        admin = Admin(api_prefix)

        result = admin.getAdminTemplates(call.message.chat.id)

        if result.status_code == 200:
            result = result.json()
            templates = result['body']['data']

            msg = """\n\n\nقالب شما به شرح زیر میباشد : \n\n\n"""

            markup = InlineKeyboardMarkup(row_width=2)

            for template in templates:
                userBotton = InlineKeyboardButton(text=f"{template['template_id']} | price : {template['price']}0,000 IRR",callback_data=f"admin-get-price-create-template-{template['template_id']}")
                markup.add(userBotton)

            backToHomeButton = InlineKeyboardButton(f"بازگشت به پنل ادمین", callback_data=f'back_to_admin_panel')

            markup.add(backToHomeButton)

            bot.send_message(call.message.chat.id,msg,reply_markup=markup)
        else:
            handleError(call.message, bot, '')
    except Exception as e:
        handleError(call.message, bot, e)
def adminGetPriceCreateTemplate(call,bot,api_prefix,template_id):
    try:
        admin = Admin(api_prefix)
        template = admin.getTemplate(call.message.chat.id,template_id)
        if template.status_code == 200:
            template = template.json()['body']['data']
            keyboard = [
                [
                    InlineKeyboardButton(f"id : {template['template_id']}",callback_data="none-selectable")
                ],
                [
                    InlineKeyboardButton(f"days limit : {template['days_limit'] if template['days_limit'] else '---'}",callback_data="none-selectable"),
                    InlineKeyboardButton(f"data limit : {template['data_limit'] if template['data_limit'] else '---'}",callback_data="none-selectable"),
                ],
                [
                    InlineKeyboardButton(f"price : {template['price']}0,000 IRR",callback_data="none-selectable"),
                ],
                [
                    InlineKeyboardButton(f"user limit : {template['user_limit'] if template['user_limit'] else '---'}", callback_data="none-selectable"),
                    InlineKeyboardButton(f"in bounds : {template['in_bounds'] if template['in_bounds'] else '---'}", callback_data="none-selectable"),
                ],
                [
                    InlineKeyboardButton(f"انصراف", callback_data=f'back_to_admin_panel')
                ]
            ]

            msg = "لطفا قیمت جدید خود را وارد کنید\n\n\nدرصورت عدم تمایل انصراف را بزنید."
            markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(call.message.chat.id,msg,reply_markup=markup)
            bot.register_next_step_handler(call.message,lambda msg : adminCreateTamplateFinal(msg,bot,api_prefix,template_id))
        else:
            handleError(call.message,bot,'')
    except Exception as e:
        handleError(call.message, bot, e)
def adminCreateTamplateFinal(message,bot,api_prefix,template_id):
    try:
        price = str(message.json['text'])
        backToHomeButton = InlineKeyboardButton(f"انصراف", callback_data=f'back_to_admin_panel')
        markup = InlineKeyboardMarkup()
        markup.add(backToHomeButton)
        if price.isdigit():
            price = int(price)
            price = price / 10000
            admin = Admin(api_prefix)
            response = admin.addTemplate(message.chat.id,template_id,price)
            if response.status_code == 200:
                msg = "عملیات با موفقیت انجام شد"
                bot.send_message(message.chat.id,msg,reply_markup=markup)
            else :
                handleError(message,bot,'')
        else:
            msg = "توجه!!!\n\n\nلطفا قیمت جدید خود را تنها به صورت عدد وارد کنید\n\n\nدرصورت عدم تمایل انصراف را بزنید."
            bot.send_message(message.chat.id,msg,reply_markup=markup)
            bot.register_next_step_handler(message,lambda msg : adminCreateTamplateFinal(message,bot,api_prefix,template_id))
    except Exception as e:
        handleError(message, bot, e)
def adminSeeTemplates(call,bot,api_prefix):
    try:
        admin = Admin(api_prefix)

        result = admin.getCustomTemplate(call.message.chat.id)

        if result.status_code == 200:
            result = result.json()
            templates = result['body']['data']

            msg = """\n\n\nقالب های شما به شرح زیر میباشد : \n\n\n"""

            markup = InlineKeyboardMarkup(row_width=2)

            for template in templates:
                userBotton = InlineKeyboardButton(text=f"{template['template_id']} | price : {template['price']}0,000 IRR",callback_data=f"admin-see-template-{template['template_id']}")
                markup.add(userBotton)

            backToHomeButton = InlineKeyboardButton(f"بازگشت به پنل ادمین", callback_data=f'back_to_admin_panel')

            markup.add(backToHomeButton)

            bot.send_message(call.message.chat.id,msg,reply_markup=markup)
        else:
            handleError(call.message, bot, '')
    except Exception as e:
        handleError(call.message, bot, e)
def adminSeeTemplate(call,bot,api_prefix,template_id):
    try:
        admin = Admin(api_prefix)
        template = admin.getTemplate(call.message.chat.id,template_id)
        if template.status_code == 200:
            template = template.json()['body']['data']
            keyboard = [
                [
                    InlineKeyboardButton(f"id : {template['template_id']}",callback_data="none-selectable")
                ],
                [
                    InlineKeyboardButton(f"days limit : {template['days_limit'] if template['days_limit'] else '---'}",callback_data="none-selectable"),
                    InlineKeyboardButton(f"data limit : {template['data_limit'] if template['data_limit'] else '---'}",callback_data="none-selectable"),
                ],
                [
                    InlineKeyboardButton(f"price : {template['price']}0,000 IRR",callback_data="none-selectable"),
                ],
                [
                    InlineKeyboardButton(f"user limit : {template['user_limit'] if template['user_limit'] else '---'}", callback_data="none-selectable"),
                    InlineKeyboardButton(f"in bounds : {template['in_bounds'] if template['in_bounds'] else '---'}", callback_data="none-selectable"),
                ],
                [
                    InlineKeyboardButton(f"حذف", callback_data=f"admin-delete-template-{template['template_id']}")
                ],
                [
                    InlineKeyboardButton(f"بازگشت به پنل ادمین", callback_data=f'back_to_admin_panel')
                ]
            ]

            msg = "اطلاعات قالب به صورت زیر است. در صورت نیاز میتوانید آن را حذف کنید یا به پنل مدیریتی بازگردید."
            markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(call.message.chat.id,msg,reply_markup=markup)
        else:
            handleError(call.message,bot,'')
    except Exception as e:
        handleError(call.message, bot, e)
def adminDeleteTemplate(call,bot,api_prefix,template_id):
    try:
        admin = Admin(api_prefix)
        response = admin.deleteTempalte(call.message.chat.id,template_id)
        if response.status_code == 200:
            keyboard = [
                [
                    InlineKeyboardButton(f"بازگشت به پنل ادمین", callback_data=f'back_to_admin_panel')
                ]
            ]

            msg = "عملیات با موفقیت انجام شد."
            markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(call.message.chat.id,msg,reply_markup=markup)
        else:
            handleError(call.message,bot,'')
    except Exception as e:
        handleError(call.message, bot, e)

def adminReduceUserDebt(call,bot,api_prefix,user_id):
    try:
        markup = InlineKeyboardMarkup()
        cancelButton = InlineKeyboardButton('بازگشت', callback_data=f"admin-see-user-{user_id}")
        markup.add(cancelButton)
        msg = "لطفا مقدار بدهی پرداخت شده این کاربر را وارد کنید."
        bot.send_message(call.message.chat.id,msg,reply_markup=markup)
        bot.register_next_step_handler(call.message,lambda msg: adminReduceUserDebtFinal(msg, bot, api_prefix, user_id))
    except Exception as e:
        handleError(call.message, bot, e)
def adminReduceUserDebtFinal(message,bot,api_prefix,user_id):
    try:
        price = str(message.json['text'])

        if price.isdigit():
            price = int(price) / 10000
            admin = Admin(api_prefix)
            response = admin.reduceUserDebt(message.chat.id,user_id,price)
            if response.status_code == 200:
                markup = InlineKeyboardMarkup()
                cancelButton = InlineKeyboardButton('بازگشت', callback_data=f"admin-see-user-{user_id}")
                markup.add(cancelButton)
                msg = "عملیات با موفقیت انجام شد."
                bot.send_message(message.chat.id, msg, reply_markup=markup)
            else:
                handleError(message,bot,'')
        else:
            markup = InlineKeyboardMarkup()
            cancelButton = InlineKeyboardButton('بازگشت', callback_data=f"admin-see-user-{user_id}")
            markup.add(cancelButton)
            msg = "توجه!!!\n\nلطفا مقدار بدهی پرداخت شده این کاربر را تنها به صورت عددی وارد کنید."
            bot.send_message(message.chat.id,msg,reply_markup=markup)
            bot.register_next_step_handler(message,lambda msg: adminCreateTamplateFinal(msg, bot, api_prefix, user_id))
    except Exception as e:
        handleError(message, bot, e)

def adminSeeUsers(call,bot,api_prefix):
    try:
        admin = Admin(api_prefix)

        result = admin.getUsers(call.message.chat.id)

        if result.status_code == 200:
            result = result.json()
            users = result['body']['data']

            msg = """\n\n\nکاربران شما به شرح زیر میباشد : \n\n\n"""

            markup = InlineKeyboardMarkup(row_width=2)
            for user in users:
                userBotton = InlineKeyboardButton(text=f"{user['username']} | {user['rule']}",callback_data=f"admin-see-user-{user['chat_id']}")
                markup.add(userBotton)

            backToHomeButton = InlineKeyboardButton(f"بازگشت به پنل ادمین", callback_data=f'back_to_admin_panel')

            markup.add(backToHomeButton)

            bot.send_message(call.message.chat.id,msg,reply_markup=markup)
        else:
            handleError(call.message, bot, '')

    except Exception as e:
        handleError(call.message, bot, e)

def adminSeeUser(call,bot,api_prefix,user_id):
    try:
        auth = Authorization(api_prefix)
        user = auth.checkUser(user_id)

        if user.status_code == 200:
            user = user.json()
            user = user['body']['data']
            msg = f"""اطلاعات کاربر به شرح زیر است : \n\n\n\
لطفا یکی از گزینه ها را انتخاب کنید"""

            keyboard = [
                [
                    InlineKeyboardButton(f"نام : {user['name']}", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"نام کاربری : {user['username']}", callback_data='none-selectable'),
                    InlineKeyboardButton(f"تلفن : {user['phone']}", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"بدهی : {user['debt']}0000 IRR", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"نوع :{user['rule']}", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"تاریخچه خرید ها از قالب شما", callback_data=f'admin-see-history-user-{user_id}')
                ],
                [
                    InlineKeyboardButton(f"کاهش بدهی", callback_data=f'admin-reduce-user-debt-{user_id}')
                ],
                [
                    InlineKeyboardButton(f"قالب های اختصاص داده شده از طرف شما", callback_data=f'admin-see-assigned-template-{user_id}'),
                    InlineKeyboardButton(f"اختصاص دادن قالب", callback_data=f'admin-assign-template-to-user-{user_id}')
                ],
                [
                    InlineKeyboardButton(f"بازگشت به پنل مدیریت", callback_data=f'back_to_admin_panel')
                ]
            ]

            markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(chat_id=call.message.chat.id, text=msg, reply_markup=markup)
        else:
            handleError(call.message, bot, '')
    except Exception as e:
        handleError(call.message, bot, e)
def adminAssignTemplateToUser(call,bot,api_prefix,user_id):
    try:
        markup = InlineKeyboardMarkup()
        admin = Admin(api_prefix)
        respones = admin.getCustomTemplateForAssign(call.message.chat.id,user_id)

        if respones.status_code == 200:
            templates = respones.json()['body']['data']
            for template in templates:
                button = InlineKeyboardButton(text=f"id : {template['template_id']} | price {template['price']}0,000 IRR",callback_data=f"admin-show-template-to-assign-{user_id}-{template['template_id']}")
                markup.add(button)

        cancelButton = InlineKeyboardButton('بازگشت', callback_data=f"admin-see-user-{user_id}")
        markup.add(cancelButton)
        msg = "لطفا قالب مدنظر را اتخاب کنید"
        bot.send_message(call.message.chat.id,msg,reply_markup=markup)
    except Exception as e:
        handleError(call.message, bot, e)

def adminShowTemplateToAssign(call,bot,api_prefix,user_id,template_id):
    try:
        admin = Admin(api_prefix)
        respones = admin.getTemplate(call.message.chat.id,template_id)

        if respones.status_code == 200:
            template = respones.json()['body']['data']
            keyboard = [
                [
                    InlineKeyboardButton(f"id : {template['template_id']}",callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"days limit : {template['days_limit']}", callback_data='none-selectable'),
                    InlineKeyboardButton(f"data limit : {template['data_limit']}", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"price : {template['price']}", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"user limit : {template['user_limit']}", callback_data='none-selectable'),
                    InlineKeyboardButton(f"in bounds : {template['in_bounds']}", callback_data='none-selectable')
                ],
                [
                    InlineKeyboardButton(f"تایید", callback_data=f"admin-final-assign-template-{user_id}-{template_id}")
                ],
                [
                    InlineKeyboardButton('بازگشت', callback_data=f"admin-see-user-{user_id}")
                ]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            msg = "آیا قالب زیر مورد تایید است؟"
            bot.send_message(call.message.chat.id,msg,reply_markup=markup)
        else:
            handleError(call.message,bot,'')
    except Exception as e:
        handleError(call.message, bot, e)

def adminFinalAssignTemplate(call,bot,api_prefix,user_id,template_id):
    try:
        admin = Admin(api_prefix)
        respones = admin.assignTemplate(call.message.chat.id,user_id,template_id)

        if respones.status_code == 200:
            keyboard = [
                [
                    InlineKeyboardButton('بازگشت', callback_data=f"admin-see-user-{user_id}")
                ]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            msg = "عملیات با موفقیت انجام شد"
            bot.send_message(call.message.chat.id,msg,reply_markup=markup)
        else:
            handleError(call.message,bot,'')
    except Exception as e:
        handleError(call.message, bot, e)

def adminSeeUserHistory(call,bot,api_prefix,user_id):
    try:
        admin = Admin(api_prefix)
        response = admin.getPurchaseFromCustomTemplate(call.message.chat.id,user_id)
        if response.status_code == 200:
            templates = response.json()['body']['data']
            for template in templates:
                msg = f"تاریخ : {datetime.fromisoformat(template['created_at'][:-1])}"
                keyboard = [
                    [
                        InlineKeyboardButton(f"config name : {template['name']}",callback_data="none-selectable")
                    ],
                    [
                        InlineKeyboardButton(f"days limit : {template['days_limit'] if template['days_limit'] else '---'}",callback_data="none-selectable"),
                        InlineKeyboardButton(f"data limit : {template['data_limit'] if template['data_limit'] else '---'}", callback_data="none-selectable")
                    ],
                    [
                        InlineKeyboardButton(f"price : {template['price']}0,000 IRR", callback_data="none-selectable")
                    ],
                    [
                        InlineKeyboardButton(f"user limit : {template['user_limit'] if template['user_limit'] else '---'}", callback_data="none-selectable"),
                        InlineKeyboardButton(f"in bounds : {template['in_bounds'] if template['in_bounds'] else '---'}", callback_data="none-selectable")
                    ],
                ]
                markup = InlineKeyboardMarkup(keyboard)
                bot.send_message(call.message.chat.id,msg,reply_markup=markup)
            adminSeeUser(call,bot,api_prefix,user_id)
        else :
            handleError(call.message,bot,'')
    except Exception as e:
        handleError(call.message, bot, e)

def adminSeeAssignedTemplate(call,bot,api_prefix,user_id):
    try:
        admin = Admin(api_prefix)
        response = admin.getAssignedTemplate(call.message.chat.id,user_id)
        if response.status_code == 200:
            templates = response.json()['body']['data']
            for template in templates:
                msg = f"اطلاعات قالب:\n\n\n\
                id : {template['template_id']}\
                درصورت نیاز میتوانید آن را حذف کنید"
                keyboard = [
                    [
                        InlineKeyboardButton(f"days limit : {template['days_limit'] if template['days_limit'] else '---'}",callback_data="none-selectable"),
                        InlineKeyboardButton(f"data limit : {template['data_limit'] if template['data_limit'] else '---'}", callback_data="none-selectable")
                    ],
                    [
                        InlineKeyboardButton(f"price : {template['price']}0,000 IRR", callback_data="none-selectable")
                    ],
                    [
                        InlineKeyboardButton(f"user limit : {template['user_limit'] if template['user_limit'] else '---'}", callback_data="none-selectable"),
                        InlineKeyboardButton(f"in bounds : {template['in_bounds'] if template['in_bounds'] else '---'}", callback_data="none-selectable")
                    ],
                    [
                        InlineKeyboardButton(f"حذف", callback_data=f"admin-delete-assignment-{user_id}-{template['template_id']}")
                    ],
                ]
                markup = InlineKeyboardMarkup(keyboard)
                bot.send_message(call.message.chat.id,msg,reply_markup=markup)
            adminSeeUser(call,bot,api_prefix,user_id)
        else :
            handleError(call.message,bot,'')
    except Exception as e:
        handleError(call.message, bot, e)

def adminDeleteAssignment(call,bot,api_prefix,user_id,template_id):
    try:
        admin = Admin(api_prefix)
        response = admin.deleteAssignment(call.message.chat.id,user_id,template_id)
        if response.status_code == 200:
            msg = f"عملیات با موفقیت انجام شد."
            keyboard = [
                [
                    InlineKeyboardButton('بازگشت', callback_data=f"admin-see-user-{user_id}")
                ]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            bot.reply_to(call.message,msg,reply_markup=markup)
        else :
            handleError(call.message,bot,'')
    except Exception as e:
        handleError(call.message, bot, e)

def handleError(message,bot,e):
    print('\033[91m'+str(e)+'\033[0m')
    bot.reply_to(message,
                 """متاسفانه مشکلی برای ربات پیش آمده . 😢 \nلطفا بعدا دوباره به ما سر بزنید یا با پشتیبانی تماس بگیرید!! 🫠❤️""")

