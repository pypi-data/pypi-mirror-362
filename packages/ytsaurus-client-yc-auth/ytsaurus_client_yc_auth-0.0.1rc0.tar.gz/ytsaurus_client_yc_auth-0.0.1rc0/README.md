PyPI библиотека с реализацией авторизации YT клиента через IAM токен.

Устновка: `pip install ytsaurus-client-yc-auth`.

Зависит от `ytsaurus-client`, т.к. способы авторизации реализованы в классах-наследниках класса `yt.wrapper.http_driver.TokenAuth`.

IAM токен может быть сгенерирован тремя способами:
- C помощью утилиты `yc`. 
- С помощью oAuth токена.
- С помощью сервера метаданных.

В данный момент в классе `yc_managed_ytsaurus_auth.IamTokenAuth` реализованы способы авторизации через `yc` и сервер метаданных.

Класс может быть сконфигурирован следующими опциональными параметрами:
- `profile` - имя профиля в `yc`.
- `source` - предпочитаемый источник токена, возможные значения – `cli` (утилита `yc`), `metadata`. Если не задано, то сначала проверяется наличие утилиты `yc`, если установлена – используется она, иначе используется сервер метаданных.

# Проверка работы авторизации

Через Python YT wrapper:

```py
import yt.wrapper as yt
yt.YtClient(
    proxy='https://%CID%.proxy.ytsaurus.yandexcloud.net', 
    config={
        'auth_class': {
            'module_name': 'yc_managed_ytsaurus_auth', 
            'class_name': 'IamTokenAuth', 
            'config': {
                'profile': 'prod-fed',  # optional
                'source': 'cli',  # optional
            },
        },
    },
).list('/')
```

С использованием helper-функции:
```py
import yt.wrapper as yt
from yc_managed_ytsaurus_auth import with_iam_token_auth
config = {
    # изначальное наполнение конфига; конфига может не быть
}
yt.YtClient(
    proxy='https://%CID%.proxy.ytsaurus.yandexcloud.net', 
    config=with_iam_token_auth(
        config=config,  # optional
        profile='prod-fed',  # optional
        source='cli',  # optional
    ),
).list('/')
```

Через YT CLI:
```bash
YT_PROXY="https://%CID%.proxy.ytsaurus.yandexcloud.net" \
YT_CONFIG_PATCHES="{"auth_class"={"module_name"="yc_managed_ytsaurus_auth"; "class_name"="IamTokenAuth"};}" \
yt list /
```

# Публикация пакета

Установка зависимостей для сборки:
```bash
pip install build twine
```

Сборка и публикация пакета:
```bash
python -m build && python -m twine upload dist/*
```