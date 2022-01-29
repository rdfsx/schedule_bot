from aiogram.utils.callback_data import CallbackData


day_week_inline = CallbackData('week', 'day', 'this_or_next')

other_week_inline = CallbackData('other', 'day', 'this_or_next', 'group_id')

teacher_inline = CallbackData('teacher', 'user_id', 'teacher_id', 'rating')

delete_teacher_rating = CallbackData('delete', 'user_id', 'teacher_id')

teacher_schedule = CallbackData('schedule', 'teacher_id', 'this_or_next')

message_for_admin = CallbackData('admin', 'from_user_id', 'message_id')

group_subgroups = CallbackData('subgroup', 'number')
