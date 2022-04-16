# OpenJewelry

This is a Django project designed to be an online repository for opne-source jewelry designs. It is very much a work in progress.

## Deployment Notes
- Clone the repo
- Make a Pyhton virtual environment in the root directory (.env or similar, ideally pick something included in .gitignore)
- Enter the environment, and run `pip install -r requirements.txt`
- Create the following directories:
  - `osj-project/media`
    - `osj-project/media/files`
    - `osj-project/media/images`
    - `osj-project/media/profile_photos`
  - `osj-project/static`
- Enter `osj-project/`
- Copy `local_config.py.sample` to `local_config.py` and change contents as needed
- Set up database if needed
- Run:
  - `python manage.py makemigrations`
  - `python manage.py migrate`
  - `python manage.py collectstatic`
 - Set up production server if needed, or for development, run `python manage.py runserver`
 
