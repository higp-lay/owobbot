from database import insert_server

start_message = 'Thank you for inviting this bot into your server!\nThe default prefix of this bot is \'owob\'\nYou may discover more commands by running \'owob help\''

already_in_database = 'Thank you for inviting this bot into your server again!\nYou may reuse the settings that you have set previously\nOr, you may enter \'owob reset\' to reset your settings'

length_of_id = 18

default_settings = {
    'prefix' : 'owob',
}

def set_starter_default(db, server_id):
    objects = (server_id, default_settings['prefix'], '')
    insert_server(db, objects)