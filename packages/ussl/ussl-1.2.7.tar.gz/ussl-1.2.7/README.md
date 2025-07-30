# USSL - USSC SOAR SCRIPT LIB

<!-- Оглавление -->
## Оглавление
- [1. Описание](#описание)
    - [Установка](#установка)
- [2. Взаимодействие с внешними системами](#взаимодействие-с-внешними-системами)
    - [Доступные методы модуля ussl.protocol](#доступные-методы-модуля-usslprotocol)
    - [Доступные на данный момент транспорты](#доступные-на-данный-момент-транспорты)
- [3. Взаимодействие с USSC SOAR](#взаимодействие-с-ussc-soar)
    - [Использование ussl.postprocessing в скриптах](#использование-usslpostprocessing-в-скриптах)
    - [Расширения BaseFunction для работы со скриптами](#расширения-basefunction-для-работы-со-скриптами)

<!-- /Оглавление -->

<!-- Описание -->
## Описание:

Библиотека разработана для упрощения работы с сетевыми устройствами, а также для расширения возможностей USSC SOAR.

### Установка

Установка через PyPI:
> `pip install ussl`


<!-- /Описание -->


<!-- Взаимодействие с внешними системами -->
## Взаимодействие с внешними системами:
Для упрощения взаимодействия с различными системами в модуле ussl.transport реализован единый интерфейс. На вход он принимает объект Protocol, содержащий данные о подключении и объект (или список объектов) Query, содержащий данные о команде, которую необходимо выполнить; в качестве ответа возвращается объект Responce.
<br>
<details>
  <summary>Поля объекта Protocol</summary>

    Общие для всех интерфейсов поля:
        host: ip-адрес или имя хоста, к которому необходимо подключиться;
        username: имя пользователя, под которым необходимо подключиться;
        password: пароль от указанного пользователя;
        interface: интерфейс, к которому необходимо подключиться (ssh, winrm, и т.д.);
        port: порт, на котором работает интерфейс;
        query: команда или набор команд, которые необходимо выполнить;
        encoding: кодировка запроса;
        decoding: кодировка ответа;
        window_width: ширина окна консоли (влияет на форматирование ответа).

    Поля, специфичные для winrm:
        domain: имя домена к которому необходимо подключиться;
        scheme: схема подключения (http или https);
        path: путь до WS-Management;
        transport: протокол аутентификации.

    Поля, специфичные для ssh:
        clean_timeout: таймаут очищения канала;
        look_for_keys: включить или отключить аутентификацию по ключам;
        auth_timeout: таймаут авторизации;
        timeout: таймаут соединения;
        pem_file: значение закрытого ключа авторизации от указанного пользователя.

</details>
<details>
  <summary>Поля объекта Query</summary>

    command: содержит командe, которую необходимо выполнить;
    timeout: содержит время, отведенное на выпонение команды;
    shell_type: содержит тип команды (cmd, powershell, и т.д.);
    sudo: содержит пароль от супер пользователя или enable.

</details>
<details>
  <summary>Поля объекта Responce</summary>
  
    result: содержит результат выполнения переданной команды;
    stdout: содержится форматированный ответ от целевой системы;
    stderr: содержится ошибка выполнения переданной команды;
    status_code: содержится статус код выполнения переданной команды.

</details>
<br>
Из особенностей поведения можно выделить следующее:

- При передаче списка Query в Responce попадёт вывод последней команды или, если в ходе выполнения произошла ошибка, вывод ошибки с соответствующим статусом;

- ...

### Доступные методы модуля ussl.protocol:

 ```python
from ussl.protocol import WinRMProtocol
from ussl.model import ProtocolData, Query

protocol = ProtocolData(...)
winrm_conn = WinRMProtocol(protocol)
winrm_conn.connect()
winrm_conn.execute(Query('ping 123.123.123.123', sudo='sudo_password'))
winrm_conn.execute('ping 123.123.123.123')
 ```

### Доступные на данный момент транспорты:

* WinRM
* SSH
* LDAP
___
<!-- /Взаимодействие с внешними системами -->


<!-- Взаимодействие с USSC SOAR -->

## Взаимодействие с USSC SOAR:

Для упрощения взаимодействия с USSC SOAR был разработан модуль ussl.postprocessing. Он берёт на себя работу с вводом/выводом данных в скриптах, переназначение ключей объектов, а также форматирование значений объектов, передаваемых в скрипт стандратным образом.


### Использование ussl.postprocessing в скриптах

Для того чтобы использовать возможности ussl.postprocessing достаточно при создании скрипта выполнить несколько условий, а именно:

- Создать класс с произвольным именем
- Унаследоваться от класса ussl.posprocessing.base.BaseFunction
- В поля класса *secrets_model* и *inputs_model* передать marshmallow-схемы, предназначеные для валидации данных
- Реализовать метод *function*
- Для вывода ошибок использовать исключения из модуля exceptions
- Вывести из метода словарь с результатом выполнения и сообщение
- В конце скрипта создать экземпляр созданного класса

```python
from typing import Type, Tuple
from ussl.postprocessing.base import BaseFunction
from ussl.exceptions import ExecutionError
from marshmallow import Schema, fields

class InputSchema(Schema):
    name: str = fields.String(required=True)

class NewFunction(BaseFunction):
    inputs_model: Type[Schema] = InputSchema        # Передаём схему для валидирования входных данных скрипта
    secrets_model: Type[Schema] = None              # Означает отсутствие секретов, используемых в этом скрипте
    def function(self) -> Tuple[dict, str]:       
        ...                                         # Прописываем операции скрипта
        result_key = self.input_json.get('name')    # Забираем из входящих данных необходимую информацию
        if result_key == 'unknown_user':
          raise ExecutionError("User is unknown")   # Выводим ошибку из скрипта 
        return {"result_key": result_key}, "Успешно"# Выводим успешное завершение
    

NewFunction()
```
_Output:_
```
{
  "user": "user", 
  "result": "Успешно", 
  "result_key": "user"
}

Process finished with exit code 0
```

### Расширения BaseFunction для работы со скриптами

#### DEBUG_MODE
Флаг, указывающий на необходимость вывода всего Stacktrace из скрипта при обнаружении ошибки, кроме ошибок валидации данных.
Используется для дебага скрипта на стэнде.
```python
from typing import Tuple
from ussl.postprocessing.base import BaseFunction
from ussl.exceptions import ExecutionError

class NewFunction(BaseFunction):
    DEBUG_MODE = True
    def function(self) -> Tuple[dict, str]:       
        raise ExecutionError("Script if failed")
    

NewFunction()
```

_Output:_
```
Traceback (most recent call last):
  File "<...>", line 6, in <module>
    raise ExecutionError("Script if failed")
<...>.ExecutionError: Command execution error: Script if failed.

Process finished with exit code 1
```


#### RETURN_CODE_IGNORE 
Необходим для успешного завершения программы даже при обнаружении ошибки.

```python
from typing import Tuple
from ussl.postprocessing.base import BaseFunction
from ussl.exceptions import ExecutionError

class NewFunction(BaseFunction):
    RETURN_CODE_IGNORE = True
    def function(self) -> Tuple[dict, str]:       
        raise ExecutionError("Script if failed")
    

NewFunction()
```
_Output:_
```
{"error": "Command execution error: Script if failed."}

Process finished with exit code 0
```