import json
import sys

sys.path.append('.myenv/lib/python3.6/site-packages')
import mysql.connector

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handle_lookup(event, context):
    logger.info(str(event))

    hostname = '--host--'
    username = '--user--'
    password = '--pass--'
    database = '--database--'
    
    main_ingredient = event['currentIntent']['slots']['main_ingredient']
    cooking_time = event['currentIntent']['slots']['cooking_time']
    
    cnx = mysql.connector.connect(user=username, password=password, host=hostname, database=database)
    cursor = cnx.cursor(buffered=True)
    query = 'select * from recipes where main_ingredient = %s and cooking_time <=%s'#.format(main_ingredient, cooking_time)
    cursor.execute(query, (main_ingredient, cooking_time))
    
    reply = "\n*Here's what I found:*\n"
    for r in cursor:
        logger.info(r)
        recipe = "\n- *{}* which requires the ingredients: {}".format(r[1], r[3])
        reply = reply + recipe
    
    return {
        'sessionAttributes': event['sessionAttributes'],
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
                'contentType': 'PlainText',
                'content': 'Here\'s a recipe for ' + main_ingredient + ' taking ' + cooking_time + "\n\n== " + reply
            }
        }
    }
