import requests
import time
import logging
from jaeger_client import Config
from flask_opentracing import FlaskTracing
from flask import Flask
from os import getenv
from opentracing.propagation import Format
from opentracing.ext import tags

JAEGER_HOST = getenv('JAEGER_HOST', 'localhost')
USER_API = getenv('USER_API', 'localhost:5001') 

if __name__ == '__main__':
    app = Flask(__name__)
    log_level = logging.DEBUG
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)

    # Create configuration object with enabled logging and sampling of all requests.
    config = Config(config={'sampler': {'type': 'const', 'param': 1},
                            'logging': True,
                            'local_agent':
                            {'reporting_host': JAEGER_HOST}},
                    service_name="account-service")
    jaeger_tracer = config.initialize_tracer()
    tracing = FlaskTracing(jaeger_tracer)

    @app.route('/create-account')
    @tracing.trace()
    def create_account():
        # Extract the span information for request object.
        with jaeger_tracer.start_active_span(
                'creating-account') as scope:
            # Perform business rules
            scope.span.log_kv({'event': 'creating-account'})

            user_service_url = "http://{}/save-user".format(USER_API)
            app.logger.info('user_api {}'.format(USER_API))

            #Inject current trace
            current_span = scope.span
            current_span.set_tag(tags.HTTP_URL, user_service_url)
            current_span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_CLIENT)

            headers = {}
            jaeger_tracer.inject(current_span, Format.HTTP_HEADERS, headers)

            # Make the actual request to webserver.
            user_response = requests.get(user_service_url, headers=headers)
            time.sleep(1)

            return "account created"

    app.run(debug=True, host='0.0.0.0', port=5000)
