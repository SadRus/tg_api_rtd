# Разработчикам библиотеки Tg API

В этом документе собраны те рекомендации и инструкции, которые необходимы разработчикам библиотеки Tg API, но бесполезны для прикладных программистов — пользователей Tg API.

## Содержимое

1. [Как развернуть local-окружение](#local-setup)
1. [Как вести разработку](#development)
    1. [Как обновить local-окружение](#update-local-env)
    1. [Как установить python-пакет в образ с Django](#add-python-package-to-django-image)
    1. [Как запустить линтеры Python](#run-python-linters)
    1. [Как запустить тесты](#run-tests)
    1. [Как собрать документацию Sphinx](#build-docs)
    1. [Как опубликовать свежую версию](#publish-on-pypi)

<a name="local-setup"></a>
## Как развернуть local-окружение

Для запуска ПО вам понадобятся консольный Git, Docker и Docker Compose. Инструкции по их установке ищите на официальных сайтах:

- [Install Docker Desktop](https://www.docker.com/get-started/)
- [Install Docker Compose](https://docs.docker.com/compose/install/)

Склонируйте репозиторий.

В репозитории используются хуки pre-commit, чтобы автоматически запускать линтеры и автотесты. Перед началом разработки установите [pre-commit package manager](https://pre-commit.com/).

В корне репозитория запустите команду для настройки хуков:

```shell
$ pre-commit install
```

В последующем при коммите автоматически будут запускаться линтеры и автотесты. Есть линтеры будет недовольны, или автотесты сломаются, то коммит прервётся с ошибкой.

Скачайте и соберите докер-образы с помощью Docker Сompose:

```shell
$ docker compose pull --ignore-buildable
$ docker compose build
```

В репозиторий добавлен Makefile, который поможет упростить и/или автоматизировать часть рутинных команд в процессе разработки
Для того чтобы посмотреть список доступных команд введите:

``
make help
``

Вы получите похожий вывод
```
Available targets:
build                          Собирает докер-образ
up                             Запускает докер-контейнер
clean                          Очищает все volume в соответствии с docker-compose
linter                         Запускает python линтеры
test                           Запускает python-тесты
help                           Отображает список доступных целей и их описания
build-docs                     Запускает сборку документации Sphinx
publish-on-pypi                Публикует библиотеку на PyPI
```

<a name="development"></a>
## Как вести разработку

<a name="update-local-env"></a>
### Как обновить local-окружение

Чтобы обновить local-окружение до последней версии подтяните код из центрального окружения и пересоберите докер-образы:

``` shell
$ git pull
$ docker compose build
```

<a name="add-python-package-to-django-image"></a>
### Как установить python-пакет в образ

В качестве менеджера пакетов для образа используется [Poetry](https://python-poetry.org/docs/).

Конфигурационные файлы Poetry `pyproject.toml` и `poetry.lock` проброшены в контейнер в виде volume, поэтому изменения зависимостей внутри контейнера попадают и наружу в git-репозиторий.

Вот пример как добавить в зависимости библиотеку asks. Запустите все контейнеры. Подключитесь к уже работающему контейнеру `tg-api` и внутри запустите команду `poetry add asks`. Затем выйдите из контейнера и остановить работу контейнеров:

```shell
$ docker compose up -d
$ docker compose exec tg-api bash
container:$ poetry add asks
container:$ exit
$ docker compose down
```

Конфигурационные файлы `pyproject.toml` и `poetry.lock` обновятся не только внутри контейнера, но и в репозитории благодаря настроенным docker volumes. Осталось только закоммитить изменения.

Чтобы все новые контейнеры также получали свежий набор зависимостей не забудьте обновить докер-образ:

```shell
$ docker compose build tg-api
```

Аналогичным образом можно удалять python-пакеты.

<a name="run-python-linters"></a>
### Как запустить линтеры Python

Линтеры запускаются в отдельном docker-контейнере, а код подключается к нему с помощью volume. Например, чтобы проверить линтером код в каталогах `tg_api` и `tests` запустите команду:

```shell
$ docker compose run --rm py-linters flake8 /tg_api/ /tests/
[+] Building 0.0s (0/0)
[+] Building 0.0s (0/0)
/tg_api/client.py:23:121: E501 line too long (148 > 120 characters)
1
```
Цифра в конце `1` -- это количество найденных линтером ошибок форматирования кода.


Запустить mypy:
```shell
$ docker compose run --rm py-linters mypy /tg_api/ /tests/
Success: no issues found in 11 source files
```

Того же результата -- запустить и pytest, и mypy вмеcте -- можно добиться с помощью make:

```shell
$ make linter
flake8 /tg_api/ /tests/
0
mypy /tg_api/ /tests/
Success: no issues found in 11 source files
```

Тот же образ с линтером можно использовать, чтобы подсветить ошибки форматирования прямо внутри IDE. Вот пример настройки Sublime Text с предустановленными плагинами [SublimeLinter](http://www.sublimelinter.com/en/stable/) и [SublimeLinter-flake8](https://packagecontrol.io/packages/SublimeLinter-flake8):

```jsonc
// project settings file
{
    "settings": {
        // specify folder where docker-compose.yaml file placed to be able to launch `docker compose`
        "SublimeLinter.linters.flake8.working_dir": "/path/to/repo/",
        "SublimeLinter.linters.flake8.executable": ["docker", "compose", "run", "--rm", "py-linters", "flake8"],
    },
}
```

<a name="run-tests"></a>
### Как запустить тесты

В репозитории используются автотесты [pytest](https://docs.pytest.org/). Запустить их можно так:

```shell
$ docker compose run --rm tg-api pytest
=========================== test session starts ===========================
platform linux -- Python 3.11.4, pytest-7.3.2, pluggy-1.2.0
cachedir: /pytest_cache_dir
rootdir: /opt/app
configfile: pyproject.toml
plugins: httpx-0.22.0, anyio-3.7.0
collected 6 items

test_asend.py ..                                                                                                       [ 33%]
test_types.py ....                                                                                                     [100%]

============================================================= 6 passed in 0.22s==============================================
```

Того же результата можно добиться с помощью make:

```shell
$ make test
...
```

Если вы чините поломанный тест, часто его запускаете и не хотите ждать когда отработают остальные, то можно запускать их по-отдельности. При этом полезно включать опцию `-s`, чтобы pytest не перехватывал вывод в консоль и выводил все сообщения. Пример для теста `test_update_parsing` из файла `tests/test_types.py`:

```shell
$ docker compose run --rm tg-api pytest -s test_asend.py::test_httpx_mocking
```

Подробнее про [Pytest usage](https://docs.pytest.org/en/6.2.x/usage.html).

<a name="build-docs"></a>
### Как собрать документацию Sphinx

Документация в репозитории собирается с помощью Sphinx и публикуется на ReadTheDocs. Этот сервис сам скачивает репозиторий и запускает сборку на своих серверах. Для публикации свежей версии документации достаточно изменить код в main-ветке центрального репозитория, зайти в личный кабинет ReadTheDocs и нажать кнопку.

Новую сборку документации можно проверить на своей машине ещё до публикации на ReadTheDocs и до коммита. Sphinx со всеми зависимостями установлен в отладочный докер-образ. Запустить сборку можно командой:

```shell
$ docker compose run --rm tg-api bash -c "cd sphinx_docs; make html"
...
build succeeded.

The HTML pages are in build/html.
```

Того же результата можно добиться с помощью make:

```shell
$ make build-docs
...
```

В результате сборки в репозиториии появится набор HTML-файлов в каталоге `sphinx_docs/build/index.html`. Индексный HTML лежит в файле `sphinx_docs/build/index.html` — откройте его в браузере.

<a name="publish-on-pypi"></a>
### Как опубликовать свежую версию

Для публикации библиотеки на PyPI вам понадобится [Twine](https://twine.readthedocs.io/en/stable/index.html). Установите его на свою машину по [официальной инструкции](https://twine.readthedocs.io/en/stable/index.html).

- Обновите информацию о релизе в файле [CHANGES.md](./CHANGES.md)
- Обновите версию пакета в [pyproject.toml](./pyproject.toml)
- Запустите финальное тестирование, сборку и публикацию:

```shell
$ make publish-on-pypi
```
