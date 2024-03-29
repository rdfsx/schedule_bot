from aiogram.types import Update
from aiogram.utils.markdown import hcode
from loguru import logger

from app.loader import dp


@dp.errors_handler()
async def errors_handler(update, exception):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param update:
    :param exception:
    :return: stdout logging
    """
    from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,
                                          CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                          MessageTextIsEmpty, RetryAfter,
                                          CantParseEntities, MessageCantBeDeleted, BadRequest)

    if isinstance(exception, CantDemoteChatCreator):
        logger.debug("Can't demote chat creator")
        return True

    if isinstance(exception, MessageNotModified):
        logger.debug('Message is not modified')
        return True
    if isinstance(exception, MessageCantBeDeleted):
        logger.debug('Message cant be deleted')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        logger.debug('Message to delete not found')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        logger.debug('MessageTextIsEmpty')
        return True

    if isinstance(exception, Unauthorized):
        logger.info(f'Unauthorized: {exception}')
        return True
    # TODO переделать
    text = "Вызвано необрабатываемое исключение. Перешлите это сообщение @rdfsx\n\n"
    if isinstance(exception, InvalidQueryID):
        error = f'InvalidQueryID: {exception} \nUpdate: {update}'
        logger.exception(error)
        await Update.get_current().message.answer(text + hcode(error))
        return True

    if isinstance(exception, TelegramAPIError):
        error = f'TelegramAPIError: {exception} \nUpdate: {update}'
        logger.exception(error)
        await Update.get_current().message.answer(text + hcode(error))
        return True
    if isinstance(exception, RetryAfter):
        error = f'RetryAfter: {exception} \nUpdate: {update}'
        logger.exception(error)
        await Update.get_current().message.answer(text + hcode(error))
        return True
    if isinstance(exception, CantParseEntities):
        error = f'CantParseEntities: {exception} \nUpdate: {update}'
        logger.exception(error)
        await Update.get_current().message.answer(text + hcode(error))
        return True
    if isinstance(exception, BadRequest):
        error = f'CantParseEntities: {exception} \nUpdate: {update}'
        logger.exception(error)
        await Update.get_current().message.answer(text + hcode(error))
        return True
    error = f'Update: {update} \n{exception}'
    logger.exception(error)
    await Update.get_current().message.answer(text + hcode(error))
