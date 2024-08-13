# Онлайн магазин (бэк)

#### Описание
Проект для Сарафан

# Содержание

1. [О проекте](#project)

1.1 [Используемых технологий в проекте](#technologies-project)

2. [Подготовка к запуску](#start)

2.1 [Настройка poetry](#poetry)

2.2 [Настройка переменных окружения](#env)

3. [Запуск приложения](#run-app)

3.1 [Запуск проекта локально](#run-local)

3.2 [Джанго команды](#commands)

4 [Структура эндпоинтов](#urls)

<br><br>

# 1. О проекте <a id="project"></a>

## 1.1 Используемые технологии в проекте<a id="technologies-project"></a>:

[![Python][Python-badge]][Python-url]

[![Poetry][Poetry-badge]][Poetry-url]

[![Django][Django-badge]][Django-url]

# 2. Подготовка к запуску <a id="start"></a>

Примечание: для работы над проектом необходим Python не ниже версии 3.11.

Также необходимо установить Poetry (не ниже 1.6.0).

## 2.1. Poetry (инструмент для работы с виртуальным окружением и сборки пакетов)<a id="poetry"></a>:

Poetry - это инструмент для управления зависимостями и виртуальными окружениями, также может использоваться для сборки пакетов. В этом проекте Poetry необходим для дальнейшей разработки приложения, его установка <b>обязательна</b>.<br>



<details>

<summary>

Как скачать и установить?

</summary>



### Установка:



Установите poetry, не ниже версии 1.5.0 следуя [инструкции с официального сайта](https://python-poetry.org/docs/#installation).

<details>

<summary>

Команды для установки:

</summary>



Если у Вас уже установлен менеджер пакетов pip, то можно установить командой:



>  *pip install poetry==1.6.0*



Если по каким-то причинам через pip не устанавливается,

то для UNIX-систем и Bash on Windows вводим в консоль следующую команду:



>  *curl -sSL https://install.python-poetry.org | python -*



Для WINDOWS PowerShell:



>  *(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -*



</details>

<br>

После установки перезапустите оболочку и введите команду



> poetry --version



Если установка прошла успешно, вы получите ответ в формате



> Poetry (version 1.6.0)



P.S.: Если при попытке проверить версию возникает ошибка об отсутствии исполняемого файла

(poetry), необходимо после установки добавить его в Path Вашей системы

(пути указаны по ссылке на официальную инструкцию по установке чуть выше.)



Для дальнейшей работы введите команду:



> poetry config virtualenvs.in-project true



Выполнение данной команды необходимо для создания виртуального окружения в

папке проекта. Конфгурация является не обязательной. Поумолчанию poetry развернёт

виртуальное окружение в корневой директории диска в директории Cache/virtualenv/...

Что бы узнать конкретно куда установлено виртуальное окружение

> poetry env info --path

После предыдущей команды создаём виртуальное окружение нашего проекта с

помощью команды:


> poetry install


Зависимости для создания окружения берутся из файлов poetry.lock (приоритетнее)

и pyproject.toml

<details>

<summary>

Порядок работы после настройки

</summary>



<br>



Чтобы активировать виртуальное окружение, введите команду:



> poetry shell



Существует возможность запуска скриптов и команд с помощью команды без

активации окружения:



> poetry run <script_name>.py



_Примеры:_



> poetry run python script_name>.py

>

> poetry run pytest

>

> poetry run black

</details>
</details>

## 2.2. Настройка переменных окружения <a id="env"></a>

Перед запуском проекта необходимо создать копию файла

```.env.example```, назвав его ```.env``` cкопировав всё содержимое.


# 3. Запуск приложения <a id="run-app"></a>



##### Клонировать репозиторий

```shell

git  clone  https://github.com/zaritskiiAA/sarafan.git

```

или по ssh

```shell

git  clone  git@github.com:zaritskiiAA/sarafan.git

```
##### Перейти в директорию



```shell

cd  sarafan

```

## 3.1. Запуск проекта локально <a id="run-local"></a>

1. После клонирования проекта перейдите в корневую директорию проекта при помощи консоли.
```bash
cd  adaptive_hockey_federation
```

2. Cтянуть миграции и инициализировать файл с базой данных.
```bash
poetry run python manage.py migrate
```
3. Запустить локалхост
```bash
poetry run python manage.py runserver
```

## 3.2  Джанго команды <a id="commands"></a>

1. Для создания супер-пользователя выполните команду. Будет создан супер-пользователь
с кредами указанными в .env

```bash
poetry run python manage.py fill-test-db -super
```

2. Для наполнения базы данных тестовыми данными.

```bash
poetry run python manage.py fill-test-db -f
```

3. Для наполнения корзины конкретного пользователя

```bash
poetry run python manage.py fill-test-db -c -id <указать id пользователя>
```
4. Обнулить базу данных
```bash
poetry run python manage.py flush
```
5. Ознакомиться с кастомными командами 
```bash
poetry run python manage.py --help
```

## Структура эндпоинтов <a id="urls"></a>

admin/ - админ панель

users/register - GET/POST регистрация пользователя по username и password
users/login - GET/POST авторизация пользователя в системе по jwt-token, username, password
users/logout - POST выход из системы
users/refresh - POST обновление access-token

products/ - GET посмотреть все продукты
products/category/ - GET посмотреть все категории и их подкатегории 
products/cart/<int:user_id>/ GET - посмотреть свою корзину
products/cart/<int:user_id>/change/ GET/POST- обновить количество продуктов, добавить продукт, удалить продукт
products/cart/<int:user_id>/delete/ - POST очистить корзину 




<!-- MARKDOWN LINKS & BADGES -->

[Python-url]: https://www.python.org/downloads/release/python-3110/

[Python-badge]: https://img.shields.io/badge/python-v3.11-yellow?style=for-the-badge&logo=python



[Poetry-url]: https://python-poetry.org/

[Poetry-badge]: https://img.shields.io/badge/poetry-blue?style=for-the-badge&logo=poetry


[Django-url]: https://docs.djangoproject.com/en/4.2/releases/4.2.6/

[Django-badge]: https://img.shields.io/badge/Django-v4.2.6-008000?logo=django&style=for-the-badge


