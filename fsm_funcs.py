import os
from dotenv import load_dotenv
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType, VkBotEvent, VkBotMessageEvent
from vk_api.utils import get_random_id
from vk_api import keyboard
from transitions import Machine, State, MachineError
from vk_bots import VkBot


# https://vk.com/buns_and_cakes

load_dotenv()
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
GROUP_ID = os.getenv('GROUP_ID')
API_VERSION = '5.130'

vk_session = vk_api.VkApi(token=ACCESS_TOKEN, api_version=API_VERSION)
vk_session_api = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)

vk_bot = VkBot(vk_session, vk_session_api, get_random_id, keyboard)

STATES = [
          State(name='start_point'),
          State(name='asleep', on_enter=['state_asleep']),
          State(name='categories', on_enter=['state_categories']),
          State(name='category_1', on_enter=['state_category_1']),
          State(name='cat_1_item_1', on_enter=['state_cat_1_item_1']),
          State(name='cat_1_item_2', on_enter=['state_cat_1_item_2']),
          State(name='category_2', on_enter=['state_category_2']),
          State(name='cat_2_item_1', on_enter=['state_cat_2_item_1']),
          State(name='cat_2_item_2', on_enter=['state_cat_2_item_2']),
          State(name='cat_2_item_3', on_enter=['state_cat_2_item_3']),
          State(name='category_3', on_enter=['state_category_3']),
          State(name='cat_3_item_1', on_enter=['state_cat_3_item_1']),
          State(name='cat_3_item_2', on_enter=['state_cat_3_item_2']),
          State(name='category_4', on_enter=['state_category_4']),
          State(name='cat_4_item_1', on_enter=['state_cat_4_item_1']),
          State(name='cat_4_item_2', on_enter=['state_cat_4_item_2']),
          State(name='cat_4_item_3', on_enter=['state_cat_4_item_3']),
          ]
TRANSITIONS = [{'trigger': 'recuperate', 'source': 'asleep', 'dest': 'start_point'},
               {'trigger': 'tired',
                'source': ['categories',
                           'category_1',
                           'cat_1_item_1',
                           'cat_1_item_2',
                           'category_2',
                           'cat_2_item_1',
                           'cat_2_item_2',
                           'cat_2_item_3',
                           'category_3',
                           'cat_3_item_1',
                           'cat_3_item_2',
                           'category_4',
                           'cat_4_item_1',
                           'cat_4_item_2',
                           'cat_4_item_3',
                           ],
                'dest': 'asleep'},
               {'trigger': 'start', 'source': '*', 'dest': 'categories'},
               {'trigger': 'category_1', 'source': 'categories', 'dest': 'category_1'},
               {'trigger': 'cat_1_item_1', 'source': 'category_1', 'dest': 'cat_1_item_1'},
               {'trigger': 'back', 'source': 'cat_1_item_1', 'dest': 'category_1'},
               {'trigger': 'cat_1_item_2', 'source': 'category_1', 'dest': 'cat_1_item_2'},
               {'trigger': 'back', 'source': 'cat_1_item_2', 'dest': 'category_1'},
               {'trigger': 'back', 'source': 'category_1', 'dest': 'categories'},
               {'trigger': 'category_2', 'source': 'categories', 'dest': 'category_2'},
               {'trigger': 'cat_2_item_1', 'source': 'category_2', 'dest': 'cat_2_item_1'},
               {'trigger': 'back', 'source': 'cat_2_item_1', 'dest': 'category_2'},
               {'trigger': 'cat_2_item_2', 'source': 'category_2', 'dest': 'cat_2_item_2'},
               {'trigger': 'back', 'source': 'cat_2_item_2', 'dest': 'category_2'},
               {'trigger': 'cat_2_item_3', 'source': 'category_2', 'dest': 'cat_2_item_3'},
               {'trigger': 'back', 'source': 'cat_2_item_3', 'dest': 'category_2'},
               {'trigger': 'back', 'source': 'category_2', 'dest': 'categories'},
               {'trigger': 'category_3', 'source': 'categories', 'dest': 'category_3'},
               {'trigger': 'cat_3_item_1', 'source': 'category_3', 'dest': 'cat_3_item_1'},
               {'trigger': 'back', 'source': 'cat_3_item_1', 'dest': 'category_3'},
               {'trigger': 'cat_3_item_2', 'source': 'category_3', 'dest': 'cat_3_item_2'},
               {'trigger': 'back', 'source': 'cat_3_item_2', 'dest': 'category_3'},
               {'trigger': 'back', 'source': 'category_3', 'dest': 'categories'},
               {'trigger': 'category_4', 'source': 'categories', 'dest': 'category_4'},
               {'trigger': 'cat_4_item_1', 'source': 'category_4', 'dest': 'cat_4_item_1'},
               {'trigger': 'back', 'source': 'cat_4_item_1', 'dest': 'category_4'},
               {'trigger': 'cat_4_item_2', 'source': 'category_4', 'dest': 'cat_4_item_2'},
               {'trigger': 'back', 'source': 'cat_4_item_2', 'dest': 'category_4'},
               {'trigger': 'cat_4_item_3', 'source': 'category_4', 'dest': 'cat_4_item_3'},
               {'trigger': 'back', 'source': 'cat_4_item_3', 'dest': 'category_4'},
               {'trigger': 'back', 'source': 'category_4', 'dest': 'categories'},
               ]


def run_vk_bot_machine():
    vk_bot_machine = Machine(vk_bot, states=STATES, transitions=TRANSITIONS, initial='start_point')
    for event in longpoll.listen():
        try:
            print('=' * 300)
            print('Type :', str(event.type))
            # print('Object :' + event.object.__str__())
            print('vk_bot_machine in state: ', vk_bot.state)
            print('raw: ', str(event.raw))
            if event.object.get('peer_id') in vk_bot.user_states:
                vk_bot_machine.get_state(vk_bot.user_states.get(event.object.get('peer_id')))  # doesn't work?:(
            vk_bot.get_event(event)
        except Exception as error:
            print('-' * 150)
            print('Error :' + error.__repr__())
            print('-' * 150)
        print('end event state: ' + vk_bot.state)
        print('=' * 300)
        print()


if __name__ == '__main__':
    run_vk_bot_machine()
