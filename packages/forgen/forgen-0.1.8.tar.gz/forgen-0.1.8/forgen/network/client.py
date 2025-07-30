from flask import request


def get_client_ip():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
    else:
        ip = request.remote_addr
    return ip
