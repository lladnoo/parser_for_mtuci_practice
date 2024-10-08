# Парсинг Вакансий career.habr.com

Это веб-приложение занимается парсингом вакансий с career.habr.com и их сохранение в базу данных SQLite. Функционал позволяет сортировать данные для парсинга и так же сортировать уже сохраненые данные, помимо этого отображается количество вакансий в базе данных.

## Использованные библиотеки

- Requests
- BeautifulSoup
- Sqlite3
- Argparse
- Os
- Flask
- Subprocess
- Threading

## ИНСТРУКЦИЯ К ЗАПУСКУ

### 1) Клонирование репозитория
```bash
git clone https://github.com/lladnoo/parser_for_mtuci_practice
```

### 2) Постройка Docker контейнеров

```bash
cd parser_for_mtuci_practice
docker-compose up --build
```

### 3) Запуск Docker контейнера и веб-приложения

После запуска контейнера перейдите в браузер по адресу: http://127.0.0.1:5000

## Инструкция по использованию сайта

### ВАЖНО
Города, должности и навыки нужно писать c большой буквы! (Если написать должность с маленькой буквы, будут выданы не все вакансии).

Изначально база данных пустая.

### ПАРСИНГ

Нажимая на ≡ Вы открываете настройки парсера. Здесь Вы можете выбрать параметры для добычи данных:

1. В графе "Город" можно указать нужные Вам города через запятую <i>(Для удаленной работы следует указать "Можно удаленно")</i>.
В этой же графе можно указать желаемый рабочий день <i>("Полный рабочий день" или "Неполный рабочий день")</i>.
2. В графе "Должность" следует указывать желаемые должности через запятую <i>(например "Системный администратор")</i>.
3. В графе "Навыки" нужно указать Ваш уровень <i>(Senior, Middle, Junior)</i> или же Ваш язык программирования.
Если Вы не зададите никаких параметров, то в базу данных будут записаны все вакансии с сайта.
Парсинг может длиться более пяти минут. Рекомендуется не взаимодействовать с сайтом в это время.
После парсинга требуется обновление базы. Для этого нажмите "Поиск" на главном экране.

### РАБОТА С БАЗОЙ ДАННЫХ

Фильтры в базе данных работают так же как в парсере. Они расположены на главной странице.
1. В графе "Город" можно указать нужные Вам города через запятую <i>(Для удаленной работы следует указать "Можно удаленно")</i>.
В этой же графе можно указать желаемый рабочий день <i>("Полный рабочий день" или "Неполный рабочий день")</i>.
2. В графе "Должность" следует указывать желаемые должности через запятую <i>(например "Системный администратор")</i>.
3. В графе "Навыки" нужно указать Ваш уровень <i>(Senior, Middle, Junior)</i> или же Ваш язык программирования.
Если Вы не зададите никаких параметров, то в таблице будут отображены все вакансии.

Работу выполнил:

    Кананыхин Д. С. БВТ2307
