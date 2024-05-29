# Django Starter with Ecommerce Basic

This is a django rest api with jwt based authentication. What are included:

- Custom `User` model with email and password based auth (no username)
- `Django Rest Framework` and `Simple JWT` for JWT based auth
- Automatic user `signup`, `login`, `reset password` with `Djoser`
- `SMTP` based email setup in `settings`
- Distinct `Profile` models based on user role, e.g. `MANAGER`, `CUSTOMER` etc.
- Basic `Product` model
- Basic `Order` model with `signals` to auto update cart items based on changes

Disclaimer: This is developed and tested in MacOS, should work out-of-the-box with Linux as well, and might need adjustments for windows in the shell script.

## Better to jump to [`How to start`](#how-to-start-if-you-are-for-the-first-time-with-this-repo) section, if you're here for the first time

Taking into consideration that you're already in a blank project directory of your preferred name.

- Clone the repo

```bash
git clone https://github.com/7shovon7/simplest-django-drf-starter-template .
```

- Run the init.sh script with your preferred `<your preferred app name>`

```bash
./init.sh <your preferred app name>
```

If you face permission error, allow the script execution permission

```bash
chmod +x init.sh
```

- Activate the virtual environment

```bash
source .venv/bin/activate
```

- Migrate and test run with `sqlite3` db

```bash
python3 manage.py makemigrations
# Migrate db
python3 manage.py migrate
# Run
python3 manage.py runserver
```

You're done!! Now jumpt to [DB](#db) section.

## How to start (If you are for the first time with this repo)

- Create a project directory

```bash
mkdir project-name
cd project-name
```

- Clone the repo in existing directory

```bash
git clone https://github.com/7shovon7/simplest-django-drf-starter-template .
```

- Search and replace the project app `catelyn_pet_shop` with your preferred name `<your preferred name>`

```bash
# Rename the main app
find . -type d -name 'catelyn_pet_shop' | while read dir; do mv "$dir" "$(dirname "$dir")/<your preferred name>"; done
# Replace the strings in different files
find . -type f -exec sed -i '' 's/catelyn_pet_shop/<your preferred name>/g' {} +
```

- Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

- Install the requirements

```bash
pip3 install -r requirements.txt
```

- Delete existing migration files

```bash
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
```

- Create .env and generate a secret

```bash
cp .env.example .env
echo ".env file created successfully. Feel free to make changes."

# Generate a 60-character long secret
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(60))')

# Update the SECRET_KEY in the .env file
sed -i '' "s/^SECRET_KEY=.*/SECRET_KEY=${SECRET_KEY}/" .env

echo "SECRET_KEY updated successfully"
```

- Create fresh migration files and migrate with `sqlite3` db

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

- Run and test the server

```bash
python3 manage.py runserver
```

- Start customizing the project by deleting the existing .git and init.sh script

```bash
echo "\nDeleting .git directory..."
rm -rf .git
# Self-destruction
echo "\nScript ran successfully. Deleting the script from this directory. If you need, pls try pulling the repo again."
rm -- "$0"
```

## DB

Inside the created .env file you'll get `DB_KEY=sqlite3`. To use postgres change this key to `DB_KEY=postgres` and update the postgres database details accordingly.
