from loguru import logger


async def retry_after_error(update, exception):
    logger.exception(f'RetryAfter: {exception} \nUpdate: {update}')
    return True
