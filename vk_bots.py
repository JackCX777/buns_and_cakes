import json
import pickle
from transitions import MachineError

# from vk_api import keyboard
# import vk_api
# import os
# from dotenv import load_dotenv
# load_dotenv()
# ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
# API_VERSION = '5.130'
# vk_session = vk_api.VkApi(token=ACCESS_TOKEN, api_version=API_VERSION)
# vk_session_api = vk_session.get_api()



class VkBot:
    def __init__(self, vk_session, vk_session_api, get_random_id, keyboard):
        self.vk_session = vk_session
        self.get_random_id = get_random_id
        self.keyboard = keyboard
        self.vk_session_api = vk_session_api
        self.blue_button = self.keyboard.VkKeyboardColor.PRIMARY
        self.white_button = self.keyboard.VkKeyboardColor.SECONDARY
        self.green_button = self.keyboard.VkKeyboardColor.POSITIVE
        self.red_button = self.keyboard.VkKeyboardColor.NEGATIVE
        self.start_commands = ['начать', 'start']
        self.event_params = {'from_user': False}
        self.user_states_to_save = ['categories', 'category_1', 'cat_1_item_1', 'cat_1_item_2', 'category_2',
                                    'cat_2_item_1', 'cat_2_item_2', 'cat_2_item_3', 'category_3', 'cat_3_item_1',
                                    'cat_3_item_2', 'category_4', 'cat_4_item_1', 'cat_4_item_2', 'cat_4_item_3',
                                    ]
        self.user_states = {}

    def get_event(self, event):
        if event.raw.get('type') == 'message_new':
            self.event_params = {'from_user': True,
                                 'type': 'message_new',
                                 'event_id': event.raw.get('event_id'),
                                 'user_id': int(event.object.message.get('from_id')),
                                 'peer_id': int(event.object.message.get('peer_id')),
                                 'conversation_message_id': int(event.object.message.get('conversation_message_id')),
                                 'msg': event.object.message.get('text').lower()
                                 }
            try:
                if self.event_params.get('msg') in self.start_commands:
                    self.start()
                else:
                    self.tired()
                    self.recuperate()
            except MachineError as machine_error:
                print('-' * 150)
                print('Machine Error :' + machine_error.__repr__())
                print('-' * 150)
        elif event.raw.get('type') == 'message_event':
            self.event_params = {'from_user': False,
                                 'type': 'message_event',
                                 'event_id': event.object.event_id,
                                 'user_id': int(event.object.get('user_id')),
                                 'peer_id': int(event.object.get('peer_id')),
                                 'conversation_message_id': int(event.object.get('conversation_message_id')),
                                 'event_data': json.dumps(event.object.payload),
                                 }
            trigger = json.loads(self.event_params.get('event_data')).get('trigger')
            try:
                self.trigger(trigger)
            except MachineError as machine_error:
                print('-' * 150)
                print('Machine Error :' + machine_error.__repr__())
                print('-' * 150)
        user = self.event_params.get('user_id')
        user_state = self.state
        if user_state in self.user_states_to_save:
            self.user_states[user] = user_state
        else:
            if user in self.user_states:
                del self.user_states[user]
        print('user_states: ', self.user_states)

    def create_keyboard(self, hide=False, buttons={}):
        if hide:
            keyboard_new = self.keyboard.VkKeyboard.get_empty_keyboard()
        else:
            keyboard_new = self.keyboard.VkKeyboard(one_time=False, inline=True)
            button_count = 0
            for button in buttons:
                button_count += 1
                keyboard_new.add_callback_button(label=buttons.get(button).get('label'),
                                                 color=buttons.get(button).get('color'),
                                                 payload=buttons.get(button).get('payload'))
                if button_count < len(buttons):
                    keyboard_new.add_line()
            keyboard_new = keyboard_new.get_keyboard()
        return keyboard_new

    def send_msg(self,
                 message,
                 owner_id=int(),
                 media_id=int(),
                 keyboard_params=None
                 ):
        random_id = self.get_random_id()
        if owner_id and media_id:
            attachment = 'photo' + str(owner_id) + '_' + str(media_id)
        else:
            attachment = ''
        self.vk_session_api.messages.send(user_id=self.event_params.get('from_id'),
                                          peer_id=self.event_params.get('peer_id'),
                                          random_id=random_id,
                                          message=message,
                                          keyboard=self.create_keyboard(hide=keyboard_params.get('hide'),
                                                                        buttons=keyboard_params.get('buttons'))
                                          )

    def edit_msg(self, message, keyboard_params=None):
        self.vk_session_api.messages.edit(peer_id=self.event_params.get('peer_id'),
                                          conversation_message_id=self.event_params.get(
                                             'conversation_message_id'),
                                          message=message,
                                          keyboard=self.create_keyboard(hide=keyboard_params.get('hide'),
                                                                       buttons=keyboard_params.get(
                                                                           'buttons'))
                                          )

    def state_asleep(self, keyboard_params={}):
        keyboard_params['hide'] = True
        if self.event_params.get('type') == 'message_new':
            message = 'Я не понял о чем идет речь. Пойду позову человека.\n' \
                      'А сам тем временем отдохну. Засыпаю..\n' \
                      'Если захочешь пообщаться, отправь "Начать" или "Start".'
        elif self.event_params.get('type') == 'message_event':
            message = 'Раз я больше не нужен, пойду отдохну.\n' \
                      'Засыпаю..'
        self.send_msg(message=message, keyboard_params=keyboard_params)

    def state_categories(self, keyboard_params={}):
        keyboard_params['hide'] = False
        buttons = {'category_1': {'label': 'Булочки',
                                  'color': self.green_button,
                                  'payload': {'trigger': 'category_1'}},
                   'category_2': {'label': 'Хлеб',
                                  'color': self.green_button,
                                  'payload': {'trigger': 'category_2'}},
                   'category_3': {'label': 'Пирожки',
                                  'color': self.green_button,
                                  'payload': {'trigger': 'category_3'}},
                   'category_4': {'label': 'Кексы',
                                  'color': self.green_button,
                                  'payload': {'trigger': 'category_4'}},
                   }
        keyboard_params['buttons'] = buttons
        message = 'Категории продуктов'
        if self.event_params.get('type') == 'message_new':
            self.send_msg(message, keyboard_params=keyboard_params)
        elif self.event_params.get('type') == 'message_event':
            self.edit_msg(message, keyboard_params=keyboard_params)

    def state_category_1(self, keyboard_params={}):
        keyboard_params['hide'] = False
        buttons = {'cat_1_item_1': {'label': 'Булочка с кремом',
                            'color': self.green_button,
                            'payload': {'trigger': 'cat_1_item_1'}},
                   'cat_1_item_2': {'label': 'Булочка в глазури',
                            'color': self.green_button,
                            'payload': {'trigger': 'cat_1_item_2'}},
                   'back': {'label': 'Назад',
                            'color': self.red_button,
                            'payload': {'trigger': 'back'}},
                   }
        keyboard_params['buttons'] = buttons
        message = 'Булочки'
        self.edit_msg(message, keyboard_params=keyboard_params)

    def state_cat_1_item_1(self, keyboard_params={}):
        keyboard_params['hide'] = False
        buttons = {'back': {'label': 'Назад',
                            'color': self.red_button,
                            'payload': {'trigger': 'back'}},
                   }
        keyboard_params['buttons'] = buttons
        message = 'Булочка с кремом'
        self.edit_msg(message, keyboard_params=keyboard_params)

    def state_cat_1_item_2(self, keyboard_params={}):
        keyboard_params['hide'] = False
        buttons = {'back': {'label': 'Назад',
                            'color': self.red_button,
                            'payload': {'trigger': 'back'}},
                   }
        keyboard_params['buttons'] = buttons
        message = 'Булочка в глазури'
        self.edit_msg(message, keyboard_params=keyboard_params)

    def state_category_2(self, keyboard_params={}):
        keyboard_params['hide'] = False
        buttons = {'cat_2_item_1': {'label': 'Хлеб зерновой',
                            'color': self.green_button,
                            'payload': {'trigger': 'cat_2_item_1'}},
                   'cat_2_item_2': {'label': 'Хлебные булочки',
                            'color': self.green_button,
                            'payload': {'trigger': 'cat_2_item_2'}},
                   'cat_2_item_3': {'label': 'Хлеб деревенский',
                                    'color': self.green_button,
                                    'payload': {'trigger': 'cat_2_item_3'}},
                   'back': {'label': 'Назад',
                            'color': self.red_button,
                            'payload': {'trigger': 'back'}},
                   }
        keyboard_params['buttons'] = buttons
        message = 'Хлеб'
        self.edit_msg(message, keyboard_params=keyboard_params)

    def state_cat_2_item_1(self, keyboard_params={}):
        keyboard_params['hide'] = False
        buttons = {'back': {'label': 'Назад',
                            'color': self.red_button,
                            'payload': {'trigger': 'back'}},
                   }
        keyboard_params['buttons'] = buttons
        message = 'Хлеб зерновой'
        self.edit_msg(message, keyboard_params=keyboard_params)

    def state_cat_2_item_2(self, keyboard_params={}):
        keyboard_params['hide'] = False
        buttons = {'back': {'label': 'Назад',
                            'color': self.red_button,
                            'payload': {'trigger': 'back'}},
                   }
        keyboard_params['buttons'] = buttons
        message = 'Хлебные булочки'
        self.edit_msg(message, keyboard_params=keyboard_params)

    def state_cat_2_item_3(self, keyboard_params={}):
        keyboard_params['hide'] = False
        buttons = {'back': {'label': 'Назад',
                            'color': self.red_button,
                            'payload': {'trigger': 'back'}},
                   }
        keyboard_params['buttons'] = buttons
        message = 'Хлеб деревенский'
        self.edit_msg(message, keyboard_params=keyboard_params)

    def state_category_3(self, keyboard_params={}):
        keyboard_params['hide'] = False
        buttons = {'cat_3_item_1': {'label': 'Пирожок с мясом',
                            'color': self.green_button,
                            'payload': {'trigger': 'cat_3_item_1'}},
                   'cat_3_item_2': {'label': 'Пирожок с яблоком',
                            'color': self.green_button,
                            'payload': {'trigger': 'cat_3_item_2'}},
                   'back': {'label': 'Назад',
                            'color': self.red_button,
                            'payload': {'trigger': 'back'}},
                   }
        keyboard_params['buttons'] = buttons
        message = 'Пирожки'
        self.edit_msg(message, keyboard_params=keyboard_params)

    def state_cat_3_item_1(self, keyboard_params={}):
        keyboard_params['hide'] = False
        buttons = {'back': {'label': 'Назад',
                            'color': self.red_button,
                            'payload': {'trigger': 'back'}},
                   }
        keyboard_params['buttons'] = buttons
        message = 'Пирожок с мясом'
        self.edit_msg(message, keyboard_params=keyboard_params)

    def state_cat_3_item_2(self, keyboard_params={}):
        keyboard_params['hide'] = False
        buttons = {'back': {'label': 'Назад',
                            'color': self.red_button,
                            'payload': {'trigger': 'back'}},
                   }
        keyboard_params['buttons'] = buttons
        message = 'Пирожок с яблоком'
        self.edit_msg(message, keyboard_params=keyboard_params)

    def state_category_4(self, keyboard_params={}):
        keyboard_params['hide'] = False
        buttons = {'cat_4_item_1': {'label': 'Брауни',
                            'color': self.green_button,
                            'payload': {'trigger': 'cat_4_item_1'}},
                   'cat_4_item_2': {'label': 'Кекс',
                            'color': self.green_button,
                            'payload': {'trigger': 'cat_4_item_2'}},
                   'cat_4_item_3': {'label': 'Маффин',
                                    'color': self.green_button,
                                    'payload': {'trigger': 'cat_4_item_3'}},
                   'back': {'label': 'Назад',
                            'color': self.red_button,
                            'payload': {'trigger': 'back'}},
                   }
        keyboard_params['buttons'] = buttons
        message = 'Кексы'
        self.edit_msg(message, keyboard_params=keyboard_params)

    def state_cat_4_item_1(self, keyboard_params={}):
        keyboard_params['hide'] = False
        buttons = {'back': {'label': 'Назад',
                            'color': self.red_button,
                            'payload': {'trigger': 'back'}},
                   }
        keyboard_params['buttons'] = buttons
        message = 'Брауни'
        self.edit_msg(message, keyboard_params=keyboard_params)

    def state_cat_4_item_2(self, keyboard_params={}):
        keyboard_params['hide'] = False
        buttons = {'back': {'label': 'Назад',
                            'color': self.red_button,
                            'payload': {'trigger': 'back'}},
                   }
        keyboard_params['buttons'] = buttons
        message = 'Кекс'
        self.edit_msg(message, keyboard_params=keyboard_params)

    def state_cat_4_item_3(self, keyboard_params={}):
        keyboard_params['hide'] = False
        buttons = {'back': {'label': 'Назад',
                            'color': self.red_button,
                            'payload': {'trigger': 'back'}},
                   }
        keyboard_params['buttons'] = buttons
        message = 'Маффин'
        self.edit_msg(message, keyboard_params=keyboard_params)


if __name__ == '__main__':
    pass
