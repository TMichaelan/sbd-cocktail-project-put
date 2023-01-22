# SBD Cocktail Project


## ✨ Start the DB in Docker

> 👉 **Step 1** - Download the code from the GH repository (using `GIT`) 

```bash
$ git clone https://github.com/TMichaelan/SBD-Cocktail-Project.git
$ cd SBD-Cocktail-Project
```

<br />

> 👉 **Step 2** - Start the APP in `Docker`

```bash
$ docker-compose up --build 
```

Visit `http://localhost:5085` in your browser. The app should be up & running.

```bash
$ via pgAdmin or same connect to the database, insert .sql script
```


<br />


## ✨ Manual Build

> Download the code 

```bash
$ git clone https://github.com/TMichaelan/SBD-Cocktail-Project.git
$ cd SBD-Cocktail-Project
```

<br />


### 👉 Set Up for `Windows` 


```
$ pip3 install -r requirements.txt
```

<br />

> Start the app

```bash
$ python run.py
```

At this point, the app runs at `http://127.0.0.1:5000/`. 

<br />

### 👉 Create Users


- Start the app via `python run.py`
- Access the `registration` page and create a new user:
  - `http://127.0.0.1:5000/register`
- Access the `sign in` page and authenticate
  - `http://127.0.0.1:5000/login`

<br />


