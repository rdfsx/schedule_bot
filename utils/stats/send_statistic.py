from .Message import Message


def send_statistics(loop, token, uid, message, user_type=None):
    if user_type is not None:
        msg = Message(
            api_key=token,
            platform="tg",
            version="0.1",
            user_id=uid,
            message=message
        )
    else:
        msg = Message(
            api_key=token,
            platform="tg",
            version="0.1",
            user_id=uid,
            message=message
        )
    loop.run_in_executor(None, msg.send)
