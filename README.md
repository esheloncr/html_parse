To run this project:
1. Clone repository
2. Run install.sh
3. Run "run.sh"
install.sh will install all requirements then make and apply migrations.
Available urls:
http://domen/page/all - show all records from DB
http://domen/page/number - show record by id(by example http://domen/page/2)
http://domen/page/ - Send POST with body which contains url parameter. By example: {url: "http://google.com"}
