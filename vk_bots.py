from transitions import MachineError


class VkBot:
    def __init__(self, vk_session, vk_session_api, get_random_id, keyboard):
        """
                The VkBot class contains all the logic behind how the bot works with the Vkontakte api.

                Parameters:
                    vk_session (VkApi class instance): Imported from vk_api.
                    vk_session_api (VkApiMethod instance) : Allows API methods to be called as normal classes.
                    get_random_id (func) : Get random int32 number (signed). Imported from vk_api.utils
                    keyboard (module) : Imported from vk_api keyboard module.
        """
        self.vk_session = vk_session
        self.get_random_id = get_random_id
        self.keyboard = keyboard
        self.vk_session_api = vk_session_api
        self.blue_button = self.keyboard.VkKeyboardColor.PRIMARY
        self.white_button = self.keyboard.VkKeyboardColor.SECONDARY
        self.green_button = self.keyboard.VkKeyboardColor.POSITIVE
        self.red_button = self.keyboard.VkKeyboardColor.NEGATIVE
        self.start_commands = ['начать', 'start']
        self.commands = {}
        self.event_params = {'from_user': False}
        self.states_buttons = {}
        self.products_info = {}
        self.owner_id = ''

    def get_event(self, event):
        """
                The get_event method gets the event from VkBotLongPoll and parses it to event_params variable.
                Then calls a transition trigger depending on the event information.

                Parameters:
                    event (Event class instance): Event from VkBotLongPoll.

                Returns:
                    None
        """
        if event.raw.get('type') == 'message_new':
            self.event_params = {'from_user': True,
                                 'type': 'message_new',
                                 'event_id': event.raw.get('event_id'),
                                 'user_id': int(event.object.message.get('from_id')),
                                 'peer_id': int(event.object.message.get('peer_id')),
                                 'conversation_message_id': int(event.object.message.get('conversation_message_id')),
                                 'msg': event.object.message.get('text')}
            try:
                msg = self.event_params.get('msg')
                if msg.lower() in self.start_commands:
                    self.start()
                elif msg in self.commands:
                    trigger = self.commands.get(msg)
                    self.trigger(trigger)
                else:
                    self.tired()
                    self.recuperate()
            except MachineError as machine_error:
                print('Machine Error :', machine_error.__repr__())

    def create_keyboard(self, buttons=[]):
        """
                The create_keyboard method creates the keyboard from given buttons.

                Parameters:
                    buttons (list): List of dictionaries containing parameters for each button.

                Returns:
                    keyboard_new (json): Keyboard parameters
        """
        if buttons:
            keyboard_new = self.keyboard.VkKeyboard(one_time=False, inline=False)
            button_count = 0
            for button in buttons:
                button_count += 1
                keyboard_new.add_button(label=button.get('label'),
                                        color=button.get('color'),
                                        payload=button.get('payload'))
                if button_count < len(buttons):
                    keyboard_new.add_line()
            keyboard_new = keyboard_new.get_keyboard()
        else:
            keyboard_new = self.keyboard.VkKeyboard.get_empty_keyboard()
        return keyboard_new

    def send_msg(self, message, media_id=int(), buttons=None):
        """
                The send_msg method gets the parameters of the message and sends it with photo and keyboard if any,
                to the user using messages.send() method from vk_api.

                Parameters:
                    message (str): Message text
                    media_id (int): Id of the uploaded photo.
                    buttons (list): List of dictionaries containing parameters for each button.

                Returns:
                    None
        """
        random_id = self.get_random_id()
        if media_id:
            attachment = 'photo' + str(self.owner_id) + '_' + str(media_id)
        else:
            attachment = ''
        self.vk_session_api.messages.send(user_id=self.event_params.get('from_id'),
                                          peer_id=self.event_params.get('peer_id'),
                                          random_id=random_id,
                                          message=message,
                                          attachment=attachment,
                                          keyboard=self.create_keyboard(buttons=buttons)
                                          )

    def reply(self):
        """
                The reply method creates the reply messages with photo and buttons if any and send it to user using
                the send_msg() method.

                Returns:
                    None
        """
        state = self.state
        if state in self.products_info:
            product_info = self.products_info.get(state)
            product_label = product_info.get('product_label')
            product_media_id = product_info.get('product_media_id')
            # product_img_path = product_info.get('product_img_path')
            product_description = product_info.get('product_description')
            text = product_label + '\n' + product_description
        else:
            product_media_id = 0
            text = 'Выбирай, все вкусное и свежее'
        buttons = self.states_buttons.get(self.state)
        self.send_msg(message=text, media_id=product_media_id, buttons=buttons)

    def state_asleep(self):
        """
                The state_asleep method is called when the bot enters the asleep state and informs the user
                that the bot has stopped.

                Returns:
                    None
        """
        if self.event_params.get('type') == 'message_new':
            message = 'Я не понял о чем идет речь. Пойду позову человека.\n' \
                      'А сам тем временем отдохну. Засыпаю..\n' \
                      'Если захочешь пообщаться, отправь "Начать" или "Start".'
        elif self.event_params.get('type') == 'message_event':
            message = 'Раз я больше не нужен, пойду отдохну.\n' \
                      'Засыпаю..'
        self.send_msg(message=message)


if __name__ == '__main__':
    pass
