from vk_api.utils import get_random_id
from vk_api import keyboard
from transitions import Machine, State
from vk_bots import VkBot


def bot_init(session, categories):
    """
            The bot_init function makes initial settings for an instance of the VkBot class and also creates
            an instance of the Machine class from the pytransitions/transitions library. The bot_init function then
            extracts category and product information from the database to fill in the values of button names,
            transitions, states etc.

            Parameters:
                session (VkApi class instance): Imported from vk_api.
                categories (Categories class instance): Imported from peewee.

            Returns:
                bot (VkBot class instance): Bot instance with configured states, transitions and product information
                from the database.
    """
    # Creating VkBot instance
    session_api = session.get_api()
    bot = VkBot(session, session_api, get_random_id, keyboard)

    # Creating Machine instance
    base_states = [State(name='start_point', on_enter=['reply']),
                   State(name='asleep', on_enter=['state_asleep']),
                   State(name='categories', on_enter=['reply'])]
    base_transitions = [{'trigger': 'recuperate', 'source': 'asleep', 'dest': 'start_point'},
                        {'trigger': 'tired', 'source': ['categories'], 'dest': 'asleep'},
                        {'trigger': 'start', 'source': '*', 'dest': 'categories'}]
    bot_machine = Machine(bot, states=base_states, transitions=base_transitions, initial='start_point')

    # Collecting information from the database
    states_buttons = {}
    states_buttons['categories'] = []
    for category in categories.select():
        category_name = category.name
        category_label = category.label
        state = State(name=category_name, on_enter=['reply'])
        bot_machine.add_states(states=state)
        bot_machine.add_transition(trigger=category_name, source='categories', dest=category_name)
        bot_machine.add_transition(trigger='back', source=category_name, dest='categories')
        bot_machine.add_transition(trigger='tired', source=category_name, dest='asleep')
        category_button = {'label': category_label,
                           'name': category_name,
                           'color': bot.green_button}
        states_buttons['categories'].append(category_button)
        bot.commands[category_label] = category_name
        states_buttons[category_name] = []
        for product in category.products:
            product_name = product.name
            product_label = product.label
            product_media_id = product.media_id
            product_img_path = product.img_path
            product_description = product.description
            bot.products_info[product_name] = {'product_label': product_label,
                                               'product_media_id': product_media_id,
                                               'product_img_path': product_img_path,
                                               'product_description': product_description}
            state = State(name=product_name, on_enter=['reply'])
            bot_machine.add_states(states=state)
            bot_machine.add_transition(trigger=product_name, source=category_name, dest=product_name)
            bot_machine.add_transition(trigger='back', source=product_name, dest=category_name)
            bot_machine.add_transition(trigger='tired', source=product_name, dest='asleep')
            category_product_button = {'label': product_label,
                                       'name': product_name,
                                       'color': bot.green_button}
            states_buttons[category_name].append(category_product_button)
            states_buttons[product_name] = []
            back_button = {'label': 'Назад',
                           'name': 'back',
                           'color': bot.red_button}
            states_buttons[product_name].append(back_button)
            bot.commands[product_label] = product_name
        states_buttons[category_name].append(back_button)
        bot.commands['Назад'] = 'back'
    bot.states_buttons = states_buttons
    return bot


if __name__ == '__main__':
    pass
