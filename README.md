# Лабораторная работа №5 - Микросервисы, Docker, CI&CD 

Выполнили [Полыгалов Богдан](https://github.com/miamib34ch) и [Тетенова Алёна](https://github.com/alenatetenova)

[Остальные проекты по дисциплине](https://github.com/miamib34ch/HSE-SoftwareArchitecture)

## Постановка задания

**Тема:** Реализация архитектуры на основе сервисов (микросервисной архитектуры)  
**Цель работы:** Получить опыт работы организации взаимодействия сервисов с использованием контейнеров Docker

**Ожидаемые результаты:**
1. Как минимум два сервиса (модуля развертывания) упаковать в виде Docker-контейнеров.  
   (1 балл)
2. Реализовать микросервисвисную архитектуру для выбранного набора сервисов / Запустить контейнеры, показать работоспособность приложения, состоящего из взаимодействующих сервисов (запускать можно локально или на удаленной машине).  
   (3 балла)
3. Настроить непрерывную интеграцию и развертывание (развертывание - по возможности).  
   (4 балла)
4. Разработать интеграционные тесты и включить их в процесс непрерывной интеграции.  
   (2 балла)

## Docker
- Построение множества образов и запуск их контейнера:  
  - `docker-compose up --build` - запустить docker-compose.yml файл  
  - `docker-compose -f docker-compose-cd.yml up -d` - запустить определённый .yml файл  
- Управление образом:  
  - `docker build --no-cache -f Dockerfile -t imageTag_Name .`​​ - создать образ из конкретного Dockerfile без кэша  
  - `docker images | grep imageTag_Name` - найти идентификатор ранее созданного образа  
  - `​​docker rmi -f imageIdentificator` - удалить образ  
- Управление контейнером:  
  - `docker run -d --name containerName -p 8000:80 imageTag_Name` - создать контейнер из образа, в фоном режиме (-d) или в интерактивном (-it), с портами внешний:docker (-p int:int)  
  - `docker start containerName` - запустить контейнер  
  - `docker stop containerName` - остановить контейнер  
  - `docker ps -a` - список всех (-a) контейнеров  
  - `docker inspect containerName` - получение информации о контейнере в формате JSON  
  - `docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' сontainerName` - получить форматированную (-f) информацию о контейнере  
  - `​​docker container ls -n 5 | grep containerName` - найти идентификаторы ранее созданных контейнеров | с определённым именем  
  - `​​​docker cp filePath containerIdentificator:containerFilePath` - скопировать файл, параметры: из_чего во_что
  - ​`docker exec -it containerIdentificator bash` - зайти в контейнер  
  - `​​touch filePath` - создать файл в контейнере (предварительно нужно зайти в него)  
  - `​​echo "Some text" >> fileName` - скопировать текст в файл в контейнере (предварительно нужно зайти в него)  
  - `​​docker rm -vf containerIdentificator1 containerIdentificator2` - удалить контейнеры
 
## Отчёт
