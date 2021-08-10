import multiprocessing

from pizza_store.settings import settings

wsgi_app = "pizza_store.app:app"
bind = f"{settings.SERVER_HOST}:{settings.SERVER_PORT}"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
