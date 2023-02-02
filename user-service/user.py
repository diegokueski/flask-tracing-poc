import time
import logging
from jaeger_client import Config
from flask_opentracing import FlaskTracing
from flask import Flask, request
from os import getenv
from opentracing.propagation import Format
from opentracing.ext import tags
JAEGER_HOST = getenv('JAEGER_HOST', 'localhost')
JAEGER_PORT = getenv('JAEGER_PORT', '14268')

if __name__ == '__main__':
    app = Flask(__name__)
    log_level = logging.DEBUG
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)
    app.logger.info('JAEGER_HOST {}'.format(JAEGER_HOST))
    app.logger.info('JAEGER_PORT {}'.format(JAEGER_PORT))

    # Create configuration object with enabled logging and sampling of all requests.
    config = Config(config={'sampler': {'type': 'const', 'param': 1},
                            'logging': True,
                            'local_agent':
                            {'reporting_host': JAEGER_HOST,'reporting_port': JAEGER_PORT}},
                    service_name="user-service")
    jaeger_tracer = config.initialize_tracer()
    tracing = FlaskTracing(jaeger_tracer)

    @app.route('/save-user')
    @tracing.trace()
    def save_user():
        # Extract the span information for request object.
        span_ctx = jaeger_tracer.extract(Format.HTTP_HEADERS, request.headers)
        span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_CLIENT}
        with jaeger_tracer.start_active_span('saving-user', child_of=span_ctx, tags=span_tags):
            #TODO: Save user in BD
            time.sleep(1.5)

            return "user saved"

    app.run(debug=True, host='0.0.0.0', port=5001)
