# quiz_bot
 
Два чат-бота для Telegram и VK. Бот задает вопросы из базы данных викторины и проверяет ответы пользователей.


### Примеры ботов

Cсылки на примеры работающих ботов:

- [Бот](https://t.me/tg_space_pictures_bot) для Telegram
- [Бот](https://vk.com/public221134484) для VK (в сообщениях группе)


### Функционал ботов

Боты поддерживают следующие команды:

- "Новый вопрос" - Бот задает новый вопрос из базы данных викторины.
- "Сдаться" - Бот показывает правильный ответ на последний заданный вопрос и задает другой.
- "Мой счет" - Бот сообщает текущий счет пользователя. (В настоящее время эта функция не реализована)

### Запуск

Сперва необходимо клонировать репозиторий, выполнив команду:
```
$ git clone https://github.com/YuraML/quiz_bot.git
```
После копирования проекта запустите виртуальное окружение:

```
$ python3 -m venv env
$ source env/bin/activate
```

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```

Также для работы программы необходимо создать файл `.env`, заполненный следующим образом:

```
VK_TOKEN={Ваш токен бота VK}
TG_TOKEN={Ваш токен бота Telegram}
REDIS_HOST={Ваш адрес базы данных Redis}
REDIS_PORT={Ваш порт Redis, на сайте написан в адресе после двоеточия}
REDIS_PASSWORD={Ваш пароль от базы данных Redis}
```
В проекте используется база данных `Redis`. Получить ее можно [здесь](https://redis.com/).

### Запуск

Для запуска ботов введите в командную строку:

```console
python3 tg_bot.py
```
или
```console
python3 vk_bot.py
```

Вы можете использовать другие текстовые файлы для викторины. Поместите текстовый файл в каталог questions и в терминале введите команду:

```console
python3 tg_bot.py --path questions/{ваш_текстовый_файл.txt}
```
### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).

 
