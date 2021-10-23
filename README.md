
# Online Shop App

MeShop is a simple e-commerce Progressive Web App.


## Screenshots

![App Screenshot](https://s4.uupload.ir/files/git_2jl.png)

### Product View
![App Screenshot](https://s4.uupload.ir/files/screenshot_(115)_4udu.png)

### Cart View
![App Screenshot](https://s4.uupload.ir/files/screenshot_(116)_zeyi.png)

### Payment View
![App Screenshot](https://s4.uupload.ir/files/screenshot_(117)_cej.png)

### Order View
![App Screenshot](https://s4.uupload.ir/files/screenshot_(118)_qwcq.png)

### Change Address View
![App Screenshot](https://s4.uupload.ir/files/screenshot_(119)_ne2.png)


### Register/Login View
![App Screenshot](https://s4.uupload.ir/files/login_n1lf.png)

## Run Locally

Clone the project

```bash
  git clone https://github.com/ashkanzare/DjangoShoppingAppProject.git
```

Modify the sample .sample-env file with your database, sms, ... settings and rename it to .env
```bash
  mv .sample-env .env
  vim .env
```

Go to the project directory

```bash
  cd DjangoShoppingAppProject
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Migrate models to database

```bash
  python manage.py migrate

```

Run the server

```bash
  python manage.py runserver
```  

Open http://127.0.0.1:8000/ in browser