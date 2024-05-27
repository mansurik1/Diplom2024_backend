from app.store.bot.utils.redis_ import redis_get_data

def is_auth(chat_id):

    return bool(redis_get_data(f"{chat_id}:info"))
