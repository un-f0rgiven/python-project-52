### Hexlet tests and linter status:
[![Actions Status](https://github.com/un-f0rgiven/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/un-f0rgiven/python-project-52/actions)

[![Maintainability](https://codeclimate.com/github/un-f0rgiven/python-project-52/badges/gpa.svg)](https://codeclimate.com/github/un-f0rgiven/python-project-52/maintainability)

**Учебный проект - Менеджер задач**
Веб-сайт для администрирования задач. Позволяет создавать и удалять задачи, присваивать им статусы и метки.

### - Требования
OS Linux
Python 3.9>
Poetry 1.8>
PostgreSQL 14>

### - Переменные окружения
В проекте используются следующие переменные окружения:  
**- SECRET_KEY** - уникальный секретный ключ, используемый для криптографических операций, таких как шифрование данных и создание токенов.

**- Важно**: Необходимо использовать длинную и случайную строку для обеспечения безопасности вашего приложения. Не делитесь этим ключом публично!  

**- DATABASE_URL** - URL для подключения к базе данных. Содержит информацию о типе базы данных, имени пользователя, пароле, хосте и имени базы данных.  
**- Формат**: dialect://username:password@host:port/database  
    ```*dialect*: тип базы данных```  
    ```*username*: имя пользователя для подключения к базе данных```  
    ```*password*: пароль для доступа к базе данных```  
    ```*host*: адрес сервера базы данных```  
    ```*port*: порт для подключения к базе данных (по умолчанию для PostgreSQL - 5432)```  
    ```*database*: имя базы данных, к которой нужно подключиться```  
**- Пример использования**: DATABASE_URL='postgresql://user:password@localhost:5432/mydatabase'

### - Установка
1. Установка производится через команду **make install**
2. Запуск производится через команду **make dev**
3. Развёртывание производится с использованием gunicorn через команду **make start**
4. Порт для запуска можно изменить через установку переменной окружения PORT **export PORT=<укажите_значение_порта>**

**Демонстрация развёрнутого приложения**
https://task-manager-yoqv.onrender.com/