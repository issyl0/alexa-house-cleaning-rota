def alexa_handler(event, context):
    request = event['request']

    # called when invoked with no values - early exit
    if request['type'] == 'LaunchRequest':
        return get_welcome_response()

    if request['type'] == 'IntentRequest':
        intent = request['intent']

        if intent['name'] == 'HouseCleaningRota':
            return make_response(
                get_cleaning_rota_status(intent),
                card_title='Lookup'
            )
        elif intent['name'] == 'AMAZON.HelpIntent':
            return get_welcome_response()
        elif intent['name'] in ('AMAZON.StopIntent', 'AMAZON.CancelIntent'):
            return make_response(
                'Thank you for using House Cleaning Rota',
                card_title='Goodbye',
            )

    # default catch all in case nothing else matches
    return make_response("Sorry, I didn't understand that request")

def get_welcome_response():
    welcome = """
              Welcome to the House Cleaning Rota Alexa skill. You can
              ask me which week of the rota it is, and find out what
              jobs each person has to do.
              """

    return make_response(
        welcome,
        card_title='Welcome',
        reprompt_text=welcome,
        should_end_session=False
    )

def _get_cleaning_rota(intent):
    slots = intent.get('slots')
    speech_output = None

    if slots:
        cleaning_rota = slots['HouseCleaningRota'].get('value')

        if cleaning_rota:
            week = check_week
            all_jobs = check_all_jobs

            speech_output = 'It is week ' + week + '. Jack must: ' +
            all_jobs['jack'] '. Phil must: ' + all_jobs['phil'] + '.
            Isabell must: ' + all_jobs['isabell'] + '.'
	else:
	    speech_output = 'Ask me to check the house cleaning rota.'

    return speech_output

def check_week:
    import requests

    week = 'Unknown'

    r = requests.get('https://house-cleaning-rota.herokuapp.com/week.json')
    week = r.json()['week']

    return week

def check_all_jobs:
    import requests

    jobs = ''

    r = requests.get('https://house-cleaning-rota.herokuapp.com/jobs.json')
    jobs = r.json()

    return jobs

def make_response(text, card_title='Thanks', should_end_session=True,
                  reprompt_text=None):
    response = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': text,
            },
            'card': {
                'type': 'Simple',
                'title': card_title,
                'content': text
            },
            'shouldEndSession': should_end_session
        }
    }

    if reprompt_text:
        response['reprompt'] = {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        }

    return response
