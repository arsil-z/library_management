import logging

from logging.config import dictConfig

from flask import current_app as app, request

from src.common.routes import ASSIGNMENT_ROUTES


def setup_application():
    _setup_logs()
    _setup_routes()
    # _setup_tables()


def _setup_logs():
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(pathname)s:%(lineno)d: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })
    logging.basicConfig(level=logging.DEBUG)
    _setup_api_logs()


def _setup_routes():
    for api_route in ASSIGNMENT_ROUTES:
        app.add_url_rule(api_route[0], view_func=api_route[1].as_view(api_route[0]))


def _setup_api_logs():
    def log_requests():
        try:
            logging.info('\n\n=============================================')
            logging.info(f'>>{request}')
            logging.info(f'>>Request Headers: {request.headers}')
            logging.info(f'>>Request Data: {(request.data or "")[:20000]}')
            logging.info(f'>>Request Params: {request.args}')
            logging.info('-------------------------------------------------')
        except Exception as err:
            logging.exception(f'>>Request Error: {err}')

    def log_responses(response):
        try:
            logging.info('-------------------------------------------------')
            logging.info(f'>>{response}')
            logging.info(f'>>Response headers: {response.headers}')
            logging.info(f'>>Response data: {(response.data or "")[:20000]}')
        except Exception as err:
            logging.exception(f'>>Response Error: {err}')

        return response

    app.before_request(log_requests)
    app.after_request(log_responses)


def _setup_tables():
    from src.sql import Base, engine
    Base.metadata.create_all(engine)
