from datetime import datetime

from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import Model
from peewee import Proxy
from peewee import TextField

db_proxy = Proxy()


class Base(Model):
    class Meta:
        database = db_proxy


class Account(Base):
    STATUSES = [('active', 'Active'),
                ('suspended', 'Suspended'),
                ('closed', 'Closed')]

    owner = ForeignKeyField('self', related_name='sub_acounts')
    sid = CharField(max_length=34, unique=True)
    friendly_name = CharField(max_length=64)
    type = CharField(choices=('Trial', 'Full'), default='Trial')
    status = CharField(choices=STATUSES, default='active')
    auth_token = CharField()
    uri = CharField()
    date_created = DateTimeField()
    date_updated = DateTimeField()

    class Meta:
        db_table = 'accounts'


class Application(Base):
    account = ForeignKeyField(Account, related_name='applications')
    sid = CharField(max_length=34, unique=True)
    friendly_name = CharField(max_length=64)
    voice_url = CharField()
    voice_method = CharField(choices=('GET', 'POST'), default='POST')
    voice_fallback_url = CharField()
    voice_fallback_method = CharField(choices=('GET', 'POST'), default='POST')
    status_callback = CharField()
    status_callback_method = CharField(choices=('GET', 'POST'), default='POST')
    voice_caller_id_lookup = BooleanField(default=False)
    sms_url = CharField()
    sms_method = CharField(choices=('GET', 'POST'), default='POST')
    sms_fallback_url = CharField()
    sms_fallback_method = CharField(choices=('GET', 'POST'), default='POST')
    sms_status_callback = CharField()
    message_status_callback = CharField()
    uri = CharField()
    date_created = DateTimeField(default=datetime.utcnow)

    class Meta:
        db_table = 'applications'


class PhoneNumber(Base):
    account = ForeignKeyField(Account, related_name='phone_numbers')
    sid = CharField(max_length=34, unique=True)
    date_created = DateTimeField()
    date_updated = DateTimeField()
    friendly_name = CharField(max_length=64)
    phone_number = CharField()
    application = ForeignKeyField(Application, related_name='phone_numbers')

    class Meta:
        db_table = 'phone_numbers'


class Message(Base):
    account = ForeignKeyField(Account, related_name='messages')
    sid = CharField(max_length=34, unique=True)
    date_created = DateTimeField()
    date_updated = DateTimeField()
    date_sent = DateTimeField()
    sender = ForeignKeyField(PhoneNumber, related_name='messages_sent')
    receiver = ForeignKeyField(PhoneNumber, related_name='messages_received')
    body = TextField()
    num_media = IntegerField()
    num_segments = IntegerField()
    status = CharField()
    error_code = CharField()
    error_message = CharField()
    direction = CharField()
    price = CharField()
    price_unit = CharField()

    class Meta:
        db_table = 'messages'

class Call(Base):
    account = ForeignKeyField(Account, realted_name='calls')
    parent = ForeignKeyField('self', related_name='calls')
    sid = CharField(max_length=34, unique=True)
    date_created = DateTimeField()
    date_updated = DateTimeField()
    sender = ForeignKeyField(PhoneNumber, related_name='calls_made')
    receipient = ForeignKeyField(PhoneNumber, related_name='calls_received')
    start_time = DateTimeField()
    end_time = DateTimeField()
