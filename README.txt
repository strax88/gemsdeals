Приложение gemsdeals построено на фреймворке Django 3.1.6 и упаковано через docker desktop (Engine 20.10.2, Compose 1.27.4)

Для запуска приложения необходимо иметь установленными git, docker и docker-compose, а также выполнить следующие шаги:
 - открыть консоль/командную строку/powershell
 - ввести команду git clone https://github.com/strax88/gemsdeals.git
 - перейти в каталог ./gemsdeals
 - выполнить команду docker-compose up

Пример входного файла CSV:
customer,item,total,quantity,date
user01,Алмаз,248,4,2020-11-18 09:51:47.231461

Для отправки файла с данными необходимо иметь curl.
 - откройте консоль/командную строку/powershell
 - выполните команду curl -c cookie.txt http://localhost:8000/gemsdeals/loadcsv
 - перейдите в каталог, где была открыта консоль, найдите файл <cookie.txt>
 - поместите в данный каталог файл с данными: deals.csv
 - в файле найдите 64 значный ключ, например: JbMSY2AdVSCDib4Igr71Jrxs9jhETyW2Gh1CosFhUgC6kBsq5E1fs0Z2nSKVcDHn
 - выполните команду curl --cookie cookie.txt http://localhost:8000/gemsdeals/loadcsv -F myfile=@./deals.csv -H "X-CSRFToken: 64_ЗНАЧНЫЙ_КЛЮЧ_ИЗ_ФАЙЛА_cookie.txt":
	curl --cookie cookie.txt http://localhost:8000/gemsdeals/loadcsv -F myfile=@./deals.csv -H "X-CSRFToken: JbMSY2AdVSCDib4Igr71Jrxs9jhETyW2Gh1CosFhUgC6kBsq5E1fs0Z2nSKVcDHn"


Для визуального ознакомления после запуска приложения необходимо перейти на http://localhost:8000 или http://localhost:8000/gemsdeals
