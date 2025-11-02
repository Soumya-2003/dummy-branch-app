from flask import Flask, g, request
import logging
import sys
import time
from pythonjsonlogger import jsonlogger
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Latency', ['method', 'endpoint'])


from .config import Config

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config())
    
    
    log_handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(name)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S'
    )
    log_handler.setFormatter(formatter)
    app.logger.addHandler(log_handler)
    app.logger.setLevel(logging.INFO)

    # === REQUEST LOGGING & METRICS ===
    @app.before_request
    def before_request():
        g.start_time = time.time()

    @app.after_request
    def after_request(response):
        # Log request
        app.logger.info("request", extra={
            "method": request.method,
            "url": request.url,
            "status": response.status_code,
            "remote_addr": request.remote_addr,
        })

        # Record metrics
        latency = time.time() - g.start_time
        endpoint = request.endpoint or 'unknown'
        REQUEST_LATENCY.labels(request.method, endpoint).observe(latency)
        REQUEST_COUNT.labels(request.method, endpoint, response.status_code).inc()

        return response
    
    @app.route('/metrics')
    def metrics():
        return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

    # Lazy imports to avoid circular deps during app init
    from .routes.health import bp as health_bp
    from .routes.loans import bp as loans_bp
    from .routes.stats import bp as stats_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(loans_bp, url_prefix="/api")
    app.register_blueprint(stats_bp, url_prefix="/api")

    return app
