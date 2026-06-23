import multiprocessing

bind = "0.0.0.0:8000"
# Gunicorn recommends (2 * cores) + 1 workers
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
# Logging configuration
accesslog = "-"
errorlog = "-"
loglevel = "info"
# Timeout settings
keepalive = 5
timeout = 30
