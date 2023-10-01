# ZF
Set of basic APIs for adding users, clients and advisors onto a financial system and purchase products. Entire code is built on top of Django framework.

Advisor
1. Register - POST http://localhost:8000/advisor/register/
2. Login - POST http://localhost:8000/advisor/login/
3. Add Client - POST http://localhost:8000/advisor/add_client/
4. Product Purchase - POST http://localhost:8000/advisor/product_purchase/

User
1. Register - POST http://localhost:8000/user/register/
2. Login - POST http://localhost:8000/user/login/

Admin
1. Register (Optional) - POST http://localhost:8000/administer/register/
2. Login (Optional) - POST http://localhost:8000/administer/login/
3. Create Product - POST http://localhost:8000/administer/create_product/

