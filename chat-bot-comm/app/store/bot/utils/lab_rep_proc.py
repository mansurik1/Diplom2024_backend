import json

from app.store.bot.utils.redis_ import redis_get_data, redis_save_data


def lab_rep_proc(chat_id: int, user_text: str = None):
    resp = redis_get_data(f"{chat_id}:lab_rep:resp")
    if resp is None:
        info = json.loads(redis_get_data(f"{chat_id}:info"))
        resp = {
            "lastname": info["lastname"],
            "alias": info["alias"]
        }
    else:
        resp = json.loads(resp)
    state = redis_get_data(f"{chat_id}:lab_rep")

    match state:
        case None:
            redis_save_data(f"{chat_id}:lab_rep", 1)

            return True

        case "1":
            resp["title"] = user_text
            redis_save_data(f"{chat_id}:lab_rep:resp", resp)
            redis_save_data(f"{chat_id}:lab_rep", 2)

            return 1

        case "2":
            resp["type"] = user_text
            redis_save_data(f"{chat_id}:lab_rep:resp", resp)
            redis_save_data(f"{chat_id}:lab_rep", 3)

            return 2

        case "3":
            resp["number"] = user_text
            redis_save_data(f"{chat_id}:lab_rep:resp", resp)
            redis_save_data(f"{chat_id}:lab_rep", 4)

            return 3

        case "4":
            return f"{resp['lastname']}_{resp['alias']}_{resp['title']}_{resp['type']}{resp['number']}"
