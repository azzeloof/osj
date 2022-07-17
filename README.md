# OpenJewelry
![Django CI](https://github.com/azzeloof/osj/actions/workflows/django.yml/badge.svg)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/open_jewelry.svg?style=social&label=Follow%20%40open_jewelry)](https://twitter.com/open_jewelry)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/K3K1DSJ1I)

OpenJewelry was designed to be the internet's home for wearable art of all kinds. It was built on the open-source framework Django, and all of its source code is available here. It is also very much a work in progress :)

The official site is at [https://open.jewelry](https://open.jewelry)

<div align="center">
<img src="assets/logo/osj-logo-full.svg" width="400" />
</div>

## Deployment Notes
If you want your own copy of OpenJewelry to mess around or contribute some bug fixes or new features, here's how you can get started:
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
 
