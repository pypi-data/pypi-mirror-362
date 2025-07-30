from prometheus_client import Counter, Histogram, Gauge
from contextlib import contextmanager
from time import perf_counter
from typing import Optional
from weakref import WeakSet

_scraper_clients = WeakSet()

scraper_requests_response_time = Histogram(
    name="scraper_requests_response_time",
    documentation="Time requests to scraper sources took",
    labelnames=["scraper_id"],
)

scraper_requests_count = Counter(
    name="scraper_requests_count",
    documentation="Total count of requests per source",
    labelnames=["scraper_id"],
)

httpx_pool_connections = Gauge(
    name="httpx_pool_connections",
    documentation="Total number of HTTPX connections in all scraper pools",
)

httpx_scraper_client_count = Gauge(
    name="httpx_scraper_client_count",
    documentation="Number of active scraper clients",
)


def register_scraper_client(client):
    _scraper_clients.add(client)


def request_response_received(*, scraper_id: str, response_time: float):
    labels = dict(scraper_id=scraper_id)

    scraper_requests_count.labels(**labels).inc()
    scraper_requests_response_time.labels(**labels).observe(response_time)


@contextmanager
def request_timer(scraper_id: Optional[str] = None):
    try:
        response_time = -perf_counter()
        yield
    finally:
        response_time += perf_counter()
    if scraper_id:
        request_response_received(
            scraper_id=scraper_id,
            response_time=response_time,
        )


scraper_datapoints = Histogram(
    name="scraper_datapoints",
    documentation="Number of data points found by a scraper per run",
    labelnames=["scraper_id", "data_type"],
)


def datapoints_found(*, data_type: str, amount: int, scraper_id: str = None):
    labels = dict(scraper_id=scraper_id, data_type=data_type)
    scraper_datapoints.labels(**labels).observe(amount)


def _get_total_connections():
    total = 0
    for client in _scraper_clients:
        try:
            total += len(client._transport._pool.connections)
        except AttributeError:
            continue
    return total


def _get_client_count():
    count = 0
    for client in _scraper_clients:
        try:
            _ = client._transport._pool.connections
            count += 1
        except AttributeError:
            continue
    return count


httpx_pool_connections.set_function(_get_total_connections)
httpx_scraper_client_count.set_function(_get_client_count)
