# coding: utf-8
from adapter_client import models as db
from adapter_client.core.domain import model
from m3_ext.ui import all_components as ext
from m3_ext.ui.containers.forms import ExtFieldSet
from m3_ext.ui.icons import Icons
from objectpack import ui


class EditWindow(ui.ModelEditWindow):

    model = db.Config
    field_fabric_params = {
        'field_list': [
            'adapter_address',
            'app_mnemonics',
            'send_request_retry_time',
            'send_request_retry_count',
            'find_request_retry_time',
            'get_request_retry_time',
        ]
    }

    def _init_components(self):
        super()._init_components()

        self._main_params_fieldset = ExtFieldSet(
            title='Основное', layout='form', label_width=200
        )
        self._requests_params_fieldset = ExtFieldSet(
            title='Параметры отправки запросов', layout='form', label_width=200
        )

    def _do_layout(self):
        super()._do_layout()

        self._main_params_fieldset.items[:] = [
            self.field__adapter_address,
            self.field__app_mnemonics
        ]
        self._requests_params_fieldset.items[:] = [
            self.field__send_request_retry_time,
            self.field__send_request_retry_count,
            self.field__find_request_retry_time,
            self.field__get_request_retry_time,
        ]
        self.form.items[:] = [
            self._main_params_fieldset,
            self._requests_params_fieldset
        ]

    def set_params(self, params):
        super().set_params(params)

        self.title = self.model._meta.verbose_name
        self.width = 480
        self.height = 'auto'


class JournalEntryListWindow(ui.BaseListWindow):

    def set_params(self, params, *args, **kwargs):
        super().set_params(params, *args, **kwargs)
        self.grid.top_bar.button_edit.text = 'Просмотр'
        self.grid.top_bar.button_edit.icon_cls = Icons.APPLICATION_VIEW_DETAIL


class JournalEntryEditWindow(ui.ModelEditWindow):

    model = db.JournalEntry
    field_fabric_params = dict(
        field_list=[
            'address',
            'timestamp',
            'type',
            'request',
            'response',
        ],
        keep_field_list_order=True,
    )

    def _init_components(self):
        super()._init_components()
        self.field__message_status = ext.ExtStringField(
            label=model.MessageMetadataInterface.status.title,
            anchor='100%',
        )
        self.field__message_type = ext.ExtStringField(
            label=model.Message.message_type.title,
            anchor='100%',
        )
        self.field__message_attachments = ext.ExtTextArea(
            label=model.Message.attachments.title,
            anchor='100%',
        )

    def _do_layout(self):
        super()._do_layout()
        self.form.items.insert(0, self.field__message_status)
        self.form.items[:] = [
            self.field__message_status,
            self.field__message_type,
            *self.form.items,
            self.field__message_attachments,
        ]

    def set_params(self, params):
        super().set_params(params)
        self.title = self.title[:-len('Редактирование')] + 'Просмотр'
        self.width = 800
        self.buttons.remove(self.save_btn)
        self.cancel_btn.text = 'Ок'
        for field in self.form.items:
            field.read_only = True

        self.field__request.height = self.field__response.height = 250

        self.field__message_status.value = params['message_status']
        self.field__message_type.value = params['message_type']
        self.field__message_attachments.value = params['message_attachments']
