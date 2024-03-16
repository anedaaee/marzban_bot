import json

from dotenv import dotenv_values
import telebot
import os
import requests
from botController.botController import *

env_vars = dotenv_values(".env")
token = env_vars["BOT_TOKEN"]
# api_prefix = env_vars["BACKEND_URL"]
api_prefix = os.environ.get('BACKEND_URL') 
#initialize bot
bot = telebot.TeleBot(token)



@bot.message_handler(commands=['start'])
def start_bot(message):
    try:
        startController(message,bot,api_prefix)
    except Exception as e:
        handleError(message,bot,e)


@bot.message_handler(content_types=['contact'])
def shared_contact(message):
    try:
        sharedContact(message,bot,api_prefix)
    except Exception as e:
        handleError(message,bot,e)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    try:
        if call.data == "user_see_configs" :
            handleUserSeeConfigs(call,bot,api_prefix)
        elif call.data == "user_see_history" :
            handleUserSeeHistory(call, bot, api_prefix)
        elif call.data == "user_see_account":
            handleUserSeeAccount(call,bot,api_prefix)
        elif call.data == "manager_panel":
            managerPanel(call, bot, api_prefix)
        elif call.data == "back_to_home":
            startController(message=call.message,bot=bot,api_prefix=api_prefix)
        elif call.data == "back_to_see_config":
            handleUserSeeConfigs(call=call,bot=bot,api_prefix=api_prefix)
        elif call.data == "cancel_purchase":
            startController(message=call.message, bot=bot, api_prefix=api_prefix)
        elif str(call.data).startswith("get_template_"):
            template_id = json.loads(str(call.data).split("_").pop())
            handleSelectTemplate(call=call,bot=bot,api_prefix=api_prefix,template_id=template_id)
        elif str(call.data).startswith("buy_template_"):
            template_id = json.loads(str(call.data).split("_").pop())
            handleBuyTemplate(call=call, bot=bot, api_prefix=api_prefix, template_id=template_id)
        elif str(call.data).startswith("see_config_links_"):
            id = json.loads(str(call.data).split("_").pop())
            showConfigLinks(call=call, bot=bot, api_prefix=api_prefix, id=id)
        elif call.data == 'manager-see-users':
            managerSeeUsers(call=call,bot=bot,api_prefix=api_prefix)
        elif call.data == 'back_to_manager_panel':
            managerPanel(call, bot, api_prefix)
        elif str(call.data).startswith("manager-see-user-"):
            user_id = json.loads(str(call.data).split("-").pop())
            managerSeeUser(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id)
        elif str(call.data).startswith("assign-admin-to-user-"):
            user_id = json.loads(str(call.data).split("-").pop())
            assignAdminToUser(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id)
        elif str(call.data).startswith("assign-template-to-user-final-"):
            data = str(call.data).split("-")
            user_id = data.pop()
            admin_id = data.pop()
            assignAdminToUserFinal(call=call,bot=bot,api_prefix=api_prefix,user_id=user_id,admin_id=admin_id)
        elif str(call.data).startswith("bann-user-"):
            data = str(call.data).split("-")
            user_id = data.pop()
            bannUser(call=call,bot=bot,api_prefix=api_prefix,user_id=user_id)
        elif str(call.data).startswith("see-user-history-"):
            data = str(call.data).split("-")
            user_id = data.pop()
            managerSeeHistory(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id)
        elif str(call.data).startswith("assign-template-to-user-"):
            data = str(call.data).split("-")
            user_id = data.pop()
            managerAssignTemplate(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id)
        elif str(call.data).startswith("select-template-to-assign-user-"):
            data = str(call.data).split("-")
            template_id = data.pop()
            user_id = data.pop()
            managerShowTemplateToAssignTemplate(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id,template_id=template_id)
        elif str(call.data).startswith("admit-assign-template-to-user-"):
            data = str(call.data).split("-")
            template_id = data.pop()
            user_id = data.pop()
            managerFinishAssignTemplate(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id,template_id=template_id)
        elif str(call.data).startswith("see-assigned-template-"):
            data = str(call.data).split("-")
            user_id = data.pop()
            seeAssignedTemplate(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id)
        elif str(call.data).startswith("manager-cancel-assigned-template-"):
            data = str(call.data).split("-")
            template_id = data.pop()
            user_id = data.pop()
            managerCancelAssignedTemplate(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id,template_id=template_id)
        elif str(call.data).startswith("manager-reduce-user-debt-"):
            data = str(call.data).split("-")
            user_id = data.pop()
            managerReduceUserDebt(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id)
        elif str(call.data).startswith("manager-alter-user-to-admin-"):
            data = str(call.data).split("-")
            user_id = data.pop()
            managerPromoteToAdmin(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id)
        elif str(call.data).startswith("manager-alter-admin-to-user-"):
            data = str(call.data).split("-")
            user_id = data.pop()
            managerPromoteToUser(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id)
        elif call.data == "manager-see-new-users":
            managerSeeNewUsers(call=call, bot=bot, api_prefix=api_prefix)
        elif str(call.data).startswith("manager-see-new-user-"):
            data = str(call.data).split("-")
            user_id = data.pop()
            managerSeeNewUser(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id)
        elif str(call.data).startswith("manager-admit-new-user-"):
            data = str(call.data).split("-")
            user_id = data.pop()
            managerAdmitNewUser(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id)
        elif call.data == "manager-see-spam-users":
            managerSeeSpamUsers(call=call, bot=bot, api_prefix=api_prefix)
        elif str(call.data).startswith("manager-see-spam-user-"):
            data = str(call.data).split("-")
            user_id = data.pop()
            managerSeeSpamUser(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id)
        elif str(call.data).startswith("manager-unbann-user-"):
            data = str(call.data).split("-")
            user_id = data.pop()
            managerUnbanUser(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id)
        elif call.data == "manager-see-templates":
            managerSeeTemplates(call=call, bot=bot, api_prefix=api_prefix)
        elif str(call.data).startswith("manager-see-template-"):
            data = str(call.data).split("-")
            template_id = data.pop()
            managerSeeTemplate(call=call, bot=bot, api_prefix=api_prefix, template_id=template_id)
        elif str(call.data).startswith("manager-delete-template-"):
            data = str(call.data).split("-")
            template_id = data.pop()
            managerDeleteTemplate(call=call, bot=bot, api_prefix=api_prefix, template_id=template_id)
        elif call.data == "manager-create-templates":
            managerCreateTemplate(call=call, bot=bot, api_prefix=api_prefix)
        elif call.data == "admin_panel":
            adminPanel(call=call, bot=bot, api_prefix=api_prefix)
        elif call.data == "back_to_admin_panel":
            adminPanel(call=call, bot=bot, api_prefix=api_prefix)
        elif call.data == "admin-create-templates":
            adminCreateTemplate(call=call, bot=bot, api_prefix=api_prefix)
        elif str(call.data).startswith("admin-get-price-create-template-"):
            data = str(call.data).split("-")
            template_id = data.pop()
            adminGetPriceCreateTemplate(call=call, bot=bot, api_prefix=api_prefix, template_id=template_id)
        elif call.data == "admin-see-templates":
            adminSeeTemplates(call=call, bot=bot, api_prefix=api_prefix)
        elif str(call.data).startswith("admin-see-template-"):
            data = str(call.data).split("-")
            template_id = data.pop()
            adminSeeTemplate(call=call, bot=bot, api_prefix=api_prefix, template_id=template_id)
        elif str(call.data).startswith("admin-delete-template-"):
            data = str(call.data).split("-")
            template_id = data.pop()
            adminDeleteTemplate(call=call, bot=bot, api_prefix=api_prefix, template_id=template_id)
        elif call.data == "admin-see-users":
            adminSeeUsers(call=call, bot=bot, api_prefix=api_prefix)
        elif str(call.data).startswith("admin-see-user-"):
            data = str(call.data).split("-")
            user_id = data.pop()
            adminSeeUser(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id)
        elif str(call.data).startswith("admin-reduce-user-debt-"):
            data = str(call.data).split("-")
            user_id = data.pop()
            adminReduceUserDebt(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id)
        elif str(call.data).startswith("admin-assign-template-to-user-"):
            data = str(call.data).split("-")
            user_id = data.pop()
            adminAssignTemplateToUser(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id)
        elif str(call.data).startswith("admin-show-template-to-assign-"):
            data = str(call.data).split("-")
            template_id = data.pop()
            user_id = data.pop()
            adminShowTemplateToAssign(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id,template_id=template_id)
        elif str(call.data).startswith("admin-final-assign-template-"):
            data = str(call.data).split("-")
            template_id = data.pop()
            user_id = data.pop()
            adminFinalAssignTemplate(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id,template_id=template_id)
        elif str(call.data).startswith("admin-see-history-user-"):
            data = str(call.data).split("-")
            user_id = data.pop()
            adminSeeUserHistory(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id)
        elif str(call.data).startswith("admin-see-assigned-template-"):
            data = str(call.data).split("-")
            user_id = data.pop()
            adminSeeAssignedTemplate(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id)
        elif str(call.data).startswith("admin-delete-assignment-"):
            data = str(call.data).split("-")
            template_id = data.pop()
            user_id = data.pop()
            adminDeleteAssignment(call=call, bot=bot, api_prefix=api_prefix, user_id=user_id,template_id=template_id)
        print(call.data)


    except Exception as e:
        handleError(call.message,bot,e)

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    cancelTxt = "لغو احراز هویت"
    if message.text == cancelTxt :
        handleCancelAuthorization(message,bot)

    else:
        bot.reply_to(message, message.text)


print('start connection')
bot.infinity_polling()
print('close connection')

