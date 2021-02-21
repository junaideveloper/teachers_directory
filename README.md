# Teachers Directory
## Running the Application
1. First, clone the repository to your local machine:
```
https://github.com/junaideveloper/teachers_directory.git
```
2. cd into the teachers_directory

3. Install the requirements:
```
pip install -r requirements.txt
```
4. Delete the existing db.sqlite3 file to clean the database

5.  Do the makemigrations and migrate command..
```
python manage.py makemigrations account
python manage.py makemigrations directory
python manage.py migrate

```
6. Create superuser
```
python manage.py createsuperuser
email : admin@gmail.com
username : admin
password : ****
Confirm password : ****

```
7. Run the application.
```
python manage.py runserver
```
8.Register User or  Login using the superuser to upload bulk data and Add teachers by selecting the Add Teachers button on the top left nav bar.
Upload the Teachers.csv file and teachers.zip file, then click upload button to insert data.
