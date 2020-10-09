from pusher import pusher
from models.modules.core import app

pusher_client = pusher.Pusher(
  app_id = app.config['PUSHER_APP_ID'],
  key = app.config['PUSHER_APP_KEY'],
  secret = app.config['PUSHER_APP_SECRET'],
  cluster = app.config['PUSHER_APP_CLUSTER'],
  ssl = app.config['PUSHER_USE_SSL']
)


def send_event_to_channel(channel_name, event_name, payload):
    try:
        pusher_client.trigger(channel_name, event_name, payload)
    except Exception as e:
        raise str(e)