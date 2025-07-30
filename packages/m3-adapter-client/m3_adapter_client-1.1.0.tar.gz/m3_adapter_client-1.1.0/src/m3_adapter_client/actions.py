# coding: utf-8
from itertools import chain

from objectpack.actions import ObjectPack

from adapter_client import models as db
from adapter_client.core import services
from django.db.models import Case
from django.db.models import CharField
from django.db.models import F
from django.db.models import Value
from django.db.models import When

from .permissions import PERM_GROUP__SMEV_REQUEST_LOG
from .ui import EditWindow
from .ui import JournalEntryEditWindow
from .ui import JournalEntryListWindow


class BasePack(ObjectPack):

    model = db.Config

    def get_row(self, _):
        return services.load_config()

    def save_row(self, obj, *args, **kwargs):
        return services.write_config(obj)


class Pack(BasePack):

    edit_window = EditWindow

    def declare_context(self, action):
        if action in (
            self.edit_window_action, self.save_action
        ):
            return {
                self.id_param_name: {
                    'type': 'int_or_none',
                    'default': None
                }
            }

    def extend_menu(self, menu):
        return menu.administry(
            menu.SubMenu(
                'Адаптер СМЭВ',
                menu.Item(
                    'Настройки клиента',
                    self.edit_window_action
                )
            )
        )


class JournalPack(ObjectPack):

    model = db.JournalEntry

    select_related = (
        'message',
    )

    edit_window = JournalEntryEditWindow
    list_window = JournalEntryListWindow
    can_delete = False

    columns = [
        dict(
            header='Клиентский идентификатор запроса',
            data_index='message_client_id',
        ),
        dict(
            header='Идентификатор запроса СМЭВ 3 (MessageID)',
            data_index='message_smev3_id',
        ),
        dict(
            header='Дата создания',
            data_index='timestamp',
        ),
        dict(
            header='Статус запроса',
            data_index='message_status'
        )
    ]

    def __init__(self):
        super().__init__()
        self.need_check_permission = True
        self.get_rbac_rule_data = None
        self.perm_code = PERM_GROUP__SMEV_REQUEST_LOG
        for action in self.actions:
            action.perm_code = 'view'

    def get_rows_query(self, request, context):
        """Добавляет аннотацию полей сообщения."""
        result = super().get_rows_query(request, context).annotate(
            message_status=Case(
                *chain.from_iterable(
                    (
                        When(**{f'{lookup}__status': code}, then=Value(name))
                        for code, name
                        in model_cls._meta.get_field('status').choices
                    ) for lookup, model_cls in (
                        ('message__incomingmessage', db.IncomingMessage),
                        ('message__outgoingmessage', db.OutgoingMessage),
                    )
                ),
                output_field=CharField()
            ),
            message_smev3_id=F('message__message_id'),
            message_client_id=F('message__client_id'),
            message_type=F('message__message_type'),
            message_attachments=F('message__attachments'),
        )
        return result

    def declare_context(self, action):
        ctx = super().declare_context(action)
        if action is self.edit_window_action:
            ctx[self.id_param_name] = dict(type=int)
        return ctx

    def get_edit_window_params(self, params, request, context):
        result = super().get_edit_window_params(params, request, context)
        result.update(
            self.get_rows_query(request, context).values(
                'message_status',
                'message_type',
                'message_attachments'
            ).get(
                id=getattr(context, self.id_param_name)
            )
        )
        return result

    def extend_menu(self, menu):
        return menu.administry(
            menu.SubMenu(
                'Адаптер СМЭВ',
                menu.Item(
                    'Журнал сообщений',
                    self.list_window_action,
                )
            )
        )
