# packager

Every new django app needs to be contained by a django project — even if the endgame of the app's developer is to make
the app available independently as a standalone package. `packager` is  simply a container for such apps that need a 
temporary place to live while they're actively being developed.


## Features
- Supports environment variables
- Supports running with docker in virtual environment
- Supports building with docker-compose
- Supports deployment with [`dokku`](http://dokku.viewdocs.io/dokku/getting-started/installation/)
- Supports remote media storage with S3 protocol
- Supports Django REST Framework
- Supports JWT Authentication
---

Built in house with
[django-clite](https://github.com/oleoneto/django-clite).

Developed and maintained by
[Leo Neto](https://github.com/oleoneto)
