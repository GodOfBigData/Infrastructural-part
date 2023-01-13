# Infrastructural-part
Infrastructural part

#О проекте:
Проект предназначен для процессинга событий, приходящих от датчиков Iot устройства. Данные с отрицательной температурой отфильтровываются.

#Инфраструктурные элементы системы: 
- датчики Iot устройства
- apache kafka;
- zookeeper;
- consumer;
- greenplum;
- apache airflow;
- redis;
- postgresql.

#Image системы:
- airflow;
- postgres:13;
- redis:latest;
- bitnami/zookeeper:latest;
- bitnami/kafka:latest;
- iot-device;
- consumer;
- greenplum.

#Контейнеры системы:
- airflow-worker_1
- airflow-webserver_1
- airflow-triggerer_1
- airflow-scheduler_1
- redis_1
- kafka_1
- greenplum
- zookeeper_1
- consumer
- postgres_1
- iot-device

Инструкция по разворачиванию системы. (Инструкция предполагает, что у вас на момент разворачивания системы уже установлены: docker, docker-compose, git)

Ниже буду приведены относительные пути директорий. Корнем будет являтся дирекотрия, в которой распологается docker-compose.yaml

Шаг 1. 
git pull проекта

Шаг2.
Переходим в директорию "./createImage/iotDevice". Запускаем команду: docker build -t iot-device . -f iotDevice.dockerfile

Шаг 3
Переходим в директорию "./createImage/consumer".  Запускаем команду: docker build -t consumer . -f consumer.dockerfile

Шаг 4
Переходим в директорию "./createImage/greenplum".  В файле 'setEnv.sh' прописываем имя бд, имя пользователя и пароль. Запускаем команду: docker build -t greenplum . -f greenplum.dockerfile

Шаг 5
Переходим в директорию "./createImage".  Запускаем команду: docker build -t airflow . -f airflow.dockerfile

Шаг 6
Переходим в директорию ./. Выполняем комунду: docker-compose up -d

Шаг 7
После того, как система запустилась необходимо перейти по адресу http://localhost:8080/dags/DEVICES/grid и активировать Даг

Для проверки работы системы, подключитесь к базе данных по адресу localhost:5434/iot_integration. Проверьте наличие данных в таблицах: 
- device_info_stg;
- device_info_dds.

#Минимальные системные требования 
IntelCore i3-9100 3.60GHz
8ГБ
8ГБ на твердотельном накопителе (SSD)
OS: Ubuntu 20.04+

#Требуемое программное обеспечение
Git 2.38.1+
Docker 20.10.21+
Docker-Compose 1.29.2+
Firefox 107.0.1+ или Google Ghrome 107.0.5304.122-1.1+

