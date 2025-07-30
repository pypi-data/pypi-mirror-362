# from constants import DEFAULT_GREETING, MINUTE_INTERVAL, USER_STATUS_MESSAGE

from fastapi import FastAPI, Request
from sherlock_ai import get_logger, set_request_id
import uuid
from sherlock_ai import log_performance, monitor_memory, monitor_resources, hardcoded_value_detector
from sherlock_ai.analysis import smart_check
# from tests.helper_nested import helper_nested
logger = get_logger('ApiLogger')


def create_app():
    app = FastAPI()

    @app.middleware('http')
    # @log_performance
    # @monitor_memory
    # @monitor_resources
    async def request_id_middleware(request: Request, call_next):
        request_id = set_request_id()
        request.state.request_id = request_id
        logger.info(f'Request started')
        response = await call_next(request)
        logger.info(f'Request completed')
        response.headers['X-Request-ID'] = request_id
        return response

    @app.get('/health')
    @log_performance
    @monitor_memory
    @monitor_resources
    def health_check():
        try:
            # helper_nested(1)
            logger.info('Health check')
            print(1 / 0)
            return {'message': 'OK'}
        except Exception as e:
            logger.error(f'Error in health check: {e}')

    @app.get('/greet')
    @smart_check
    async def greet_user(name: str):
        greeting = 'Hello, World!'
        timeout = 60
        response = 'Processed'
        return {'message': greeting, 'processed': response, 'timeout': timeout}
    return app


app = create_app()
