# Smart Mall

---

## About
У владельца торгового центра (далее. ТЦ) есть множество площадей, которые предприниматели арендуют под магазины, кафе и
т.д. При этом каждый расчётный период (например, месяц) арендаторы платят за занимаемое ими место.\
Однако часто происходит следующая ситуация: арендатор задерживает платеж за арендованное помещение, но продолжает им пользоваться.
Несмотря на его обещания погасить долг, владелец ТЦ не получает своих денег. В результате стороны договора не могут
урегулировать спор и обращаются в суд.\
Smart Mall автоматизирует процесс сбора платы за помещение, упрощая работу для арендатора и арендодателя.

---

## Technical specifications
Python version: 3.10.4\
Django version: 3.2.13\
Database: PostgreSQL 14.0\
Nginx version: 1.21

---

## Quick start
1. Install [docker compose](https://docs.docker.com/compose/install/)
2. Run ```docker-compose up -d --build```
3. Run ```docker-compose exec smart_mall_backend python manage.py migrate```
4. Run ```docker-compose exec smart_mall_backend python manage.py collectstatic```
5. Go to ```localhost```