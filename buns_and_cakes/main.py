import os
from dotenv import load_dotenv
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from db_adapter import Categories
from bot_setup import bot_init


load_dotenv()
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
GROUP_ID = os.getenv('GROUP_ID')
API_VERSION = os.getenv('API_VERSION')
OWNER_ID = os.getenv('OWNER_ID')


def run_vk_bot_machine():
    """
            The run_vk_bot_machine function creates the VkApi class instance as vk_session, then pass it to
            bot_init function for initial setup. After it creates VkBotLongPoll class instance and runs VkBotLongPoll
            listen() loop. Every event in VkBotLongPoll listen() loop is then passed to the get_event method of VkBot
            class.

            Returns:
                None
    """
    vk_session = vk_api.VkApi(token=ACCESS_TOKEN)
    vk_bot = bot_init(session=vk_session, categories=Categories)
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)
    vk_bot.owner_id = OWNER_ID
    for event in longpoll.listen():
        try:
            vk_bot.get_event(event)
        except Exception as error:
            print('Error :', error.__repr__())


if __name__ == '__main__':
    run_vk_bot_machine()
