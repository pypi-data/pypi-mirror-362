# coding: utf-8
PERM_GROUP__SMEV_REQUEST_LOG = 'request_log'
PERM__REQUEST_LOG__VIEW = PERM_GROUP__SMEV_REQUEST_LOG + '/view'

permissions = (
    (
        PERM__REQUEST_LOG__VIEW,
        'Просмотр Журнала запросов СМЭВ',
        'Просмотр Журнала запросов СМЭВ',
    ),
)

groups = {
    PERM_GROUP__SMEV_REQUEST_LOG: 'Адаптер СМЭВ',
}

partitions = {
    'Администрирование': (
        PERM_GROUP__SMEV_REQUEST_LOG,
    ),
}
