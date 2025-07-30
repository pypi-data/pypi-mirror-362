production-request
===============================

author: BARS Group

Описание
--------

Позволяет логировать метрики запросов
(клиенсткое время, серверное время, время SQL) в production-средах


Установка
---------

Установка производится командой
-e git+https://stash.bars-open.ru/scm/budg/production_request.git@master#egg=production_request. 
При этом необходимо, чтобы при запуске *pip install* в качестве альтернативного 
index-url был указан http://pypi.bars-open.ru/simple/ 


Настройка
---------

Для подключения логирования необходимо:

1. В качестве *DATABASE_ENGINE* указать *production_request*
2. Добавить *ProductionRequestLoggingMiddleware* в перечень *MIDDLEWARE*
3. Подключить к рабочему столу *production_request_client.js* и *xhr_interceptor.js*
4. Зарегистрировать *ProductionRequestPack* в контроллере
5. Выполнить в инициализации шаблона рабочего стола функцию *startLogging*. 
Данная функция принимает на вход URL action'а *action_save_client_log* из предыдущего пункта
6. Если необходимо логировать celery-task, то в *CELERY_IMPORTS* нужно добавить *'production_request.celery_handlers'* 
    
