import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))

STATISTICS_TOKEN = str(os.getenv('STATISTICS_TOKEN'))

LOGS_BASE_PATH = "./"

admins = [
    os.getenv('ADMIN_ID')
]

ip = os.getenv('ip')

aiogram_redis = {
    'host': ip
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}

DATABASE = str(os.getenv('DATABASE'))

PGUSER = str(os.getenv('PGUSER'))

PGPASSWORD = str(os.getenv('PGPASSWORD'))

db_host = ip

POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@{db_host}/{DATABASE}"

faculties = {
    'FAIS': 'https://abiturient.gstu.by/sites/default/files/images/tax-faculties/fais.jpeg',
    'GEF': 'https://abiturient.gstu.by/sites/default/files/images/tax-faculties/gef.jpeg',
    'MTF': 'https://abiturient.gstu.by/sites/default/files/images/tax-faculties/mtf.jpeg',
    'EF': 'https://abiturient.gstu.by/sites/default/files/images/tax-faculties/ef.jpeg',
    'MSF': 'https://abiturient.gstu.by/sites/default/files/images/tax-faculties/msf.jpeg'
}

ERROR = 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/apple/237/pensive-face_1f614.png'
FAIS = 'https://abiturient.gstu.by/sites/default/files/images/tax-faculties/fais.jpeg'
GEF = 'https://abiturient.gstu.by/sites/default/files/images/tax-faculties/gef.jpeg'
MTF = 'https://abiturient.gstu.by/sites/default/files/images/tax-faculties/mtf.jpeg'
EF = 'https://abiturient.gstu.by/sites/default/files/images/tax-faculties/ef.jpeg'
MSF = 'https://abiturient.gstu.by/sites/default/files/images/tax-faculties/msf.jpeg'

PREPOD_PIC = 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/apple/237/teacher_1f9d1-200d-1f3eb.png'
PREPOD_PIC2 = 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/apple/237/teacher-light-skin-tone_1f9d1-1f3fb-200d-1f3eb.png'
PREPOD_PIC3 = 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/apple/237/teacher-medium-light-skin-tone_1f9d1-1f3fc-200d-1f3eb.png'
PREPOD_PIC4 = 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/apple/237/teacher-medium-skin-tone_1f9d1-1f3fd-200d-1f3eb.png'
PREPOD_PIC5 = 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/apple/237/teacher-medium-dark-skin-tone_1f9d1-1f3fe-200d-1f3eb.png'
PREPOD_PIC6 = 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/apple/237/teacher-dark-skin-tone_1f9d1-1f3ff-200d-1f3eb.png'

PREPODS = [
    PREPOD_PIC, PREPOD_PIC2, PREPOD_PIC3, PREPOD_PIC4
]

week_correction = 0
