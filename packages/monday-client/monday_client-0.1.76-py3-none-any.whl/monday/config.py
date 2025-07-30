# This file is part of monday-client.
#
# Copyright (C) 2024 Leet Cyber Security <https://leetcybersecurity.com/>
#
# monday-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# monday-client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with monday-client. If not, see <https://www.gnu.org/licenses/>.

"""
Configuration management for monday-client.

This module provides a centralized configuration system for the MondayClient,
allowing for easy management of timeouts, proxies, and other HTTP settings.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


@dataclass
class HTTPConfig:
    """
    HTTP-specific configuration options.

    This class encapsulates all HTTP-related configuration that can be
    passed to aiohttp.ClientSession.
    """

    timeout: int = 30
    """Request timeout in seconds."""

    connect_timeout: int = 10
    """Connection timeout in seconds."""

    read_timeout: int = 30
    """Read timeout in seconds."""

    write_timeout: int = 30
    """Write timeout in seconds."""

    proxy: str | None = None
    """Proxy URL (e.g., 'http://proxy.example.com:8080')."""

    proxy_auth: tuple[str, str] | None = None
    """Proxy authentication as (username, password) tuple."""

    ssl_verify: bool = True
    """Whether to verify SSL certificates."""

    ssl_cert: str | None = None
    """Path to SSL certificate file."""

    ssl_key: str | None = None
    """Path to SSL private key file."""

    ssl_ca_cert: str | None = None
    """Path to CA certificate file."""

    ssl_password: str | None = None
    """Password for SSL private key."""

    max_connections: int = 100
    """Maximum number of connections in the connection pool."""

    max_connections_per_host: int = 10
    """Maximum connections per host."""

    keepalive_timeout: int = 30
    """Keep-alive timeout in seconds."""

    tcp_nodelay: bool = True
    """Enable TCP_NODELAY."""

    tcp_keepalive: bool = True
    """Enable TCP keepalive."""

    tcp_keepalive_count: int = 3
    """TCP keepalive probe count."""

    tcp_keepalive_idle: int = 60
    """TCP keepalive idle time in seconds."""

    tcp_keepalive_interval: int = 10
    """TCP keepalive interval in seconds."""

    use_dns_cache: bool = True
    """Use DNS cache."""

    dns_cache_ttl: int = 300
    """DNS cache TTL in seconds."""

    dns_cache_size: int = 100
    """DNS cache size."""

    def _validate_timeouts(self) -> None:
        """Validate timeout-related configuration."""
        timeouts = [
            ('timeout', self.timeout),
            ('connect_timeout', self.connect_timeout),
            ('read_timeout', self.read_timeout),
            ('write_timeout', self.write_timeout),
        ]
        for name, value in timeouts:
            if value <= 0:
                error_msg = f'{name} must be positive'
                raise ValueError(error_msg)

    def _validate_connection_settings(self) -> None:
        """Validate connection-related configuration."""
        settings = [
            ('max_connections', self.max_connections),
            ('max_connections_per_host', self.max_connections_per_host),
            ('keepalive_timeout', self.keepalive_timeout),
            ('tcp_keepalive_count', self.tcp_keepalive_count),
            ('tcp_keepalive_idle', self.tcp_keepalive_idle),
            ('tcp_keepalive_interval', self.tcp_keepalive_interval),
            ('dns_cache_ttl', self.dns_cache_ttl),
            ('dns_cache_size', self.dns_cache_size),
        ]
        for name, value in settings:
            if value <= 0:
                error_msg = f'{name} must be positive'
                raise ValueError(error_msg)

    def _validate_proxy(self) -> None:
        """Validate proxy configuration."""
        if self.proxy:
            try:
                urlparse(self.proxy)
            except Exception as e:
                error_msg = f'Invalid proxy URL: {e}'
                raise ValueError(error_msg) from e

    def _validate_ssl_files(self) -> None:
        """Validate SSL file paths."""
        ssl_files = [
            ('ssl_cert', self.ssl_cert),
            ('ssl_key', self.ssl_key),
            ('ssl_ca_cert', self.ssl_ca_cert),
        ]
        for name, path in ssl_files:
            if path and not Path(path).exists():
                error_msg = f'{name} file does not exist: {path}'
                raise ValueError(error_msg)

    def validate(self) -> None:
        """Validate configuration values."""
        self._validate_timeouts()
        self._validate_connection_settings()
        self._validate_proxy()
        self._validate_ssl_files()


@dataclass
class RateLimitConfig:
    """
    Rate limiting configuration.
    """

    rate_limit_seconds: int = 60
    """Default rate limit window in seconds."""

    max_retries: int = 4
    """Maximum number of retry attempts."""

    retry_delay_base: float = 1.0
    """Base delay for exponential backoff."""

    retry_delay_max: float = 60.0
    """Maximum delay for exponential backoff."""

    retry_delay_factor: float = 2.0
    """Exponential backoff factor."""

    jitter: bool = True
    """Add jitter to retry delays."""

    jitter_factor: float = 0.1
    """Jitter factor (0.0 to 1.0)."""

    respect_retry_after: bool = True
    """Respect Retry-After headers from server."""

    def validate(self) -> None:
        """Validate configuration values."""
        # Validate positive values
        positive_values = [
            ('rate_limit_seconds', self.rate_limit_seconds),
            ('retry_delay_base', self.retry_delay_base),
            ('retry_delay_max', self.retry_delay_max),
            ('retry_delay_factor', self.retry_delay_factor),
        ]
        for name, value in positive_values:
            if value <= 0:
                error_msg = f'{name} must be positive'
                raise ValueError(error_msg)

        # Validate non-negative values
        if self.max_retries < 0:
            error_msg = 'max_retries must be non-negative'
            raise ValueError(error_msg)

        # Validate jitter factor
        if not 0.0 <= self.jitter_factor <= 1.0:
            error_msg = 'jitter_factor must be between 0.0 and 1.0'
            raise ValueError(error_msg)


@dataclass
class CacheConfig:
    """
    Caching configuration.
    """

    enabled: bool = False
    """Whether caching is enabled."""

    cache_type: str = 'memory'
    """Cache type: 'memory', 'redis', 'file'."""

    ttl: int = 300
    """Default TTL in seconds."""

    max_size: int = 1000
    """Maximum number of cached items."""

    redis_url: str | None = None
    """Redis URL for Redis cache."""

    cache_dir: str | None = None
    """Directory for file cache."""

    def validate(self) -> None:
        """Validate configuration values."""
        # Validate positive values
        positive_values = [
            ('ttl', self.ttl),
            ('max_size', self.max_size),
        ]
        for name, value in positive_values:
            if value <= 0:
                error_msg = f'{name} must be positive'
                raise ValueError(error_msg)

        # Validate cache type
        valid_types = ('memory', 'redis', 'file')
        if self.cache_type not in valid_types:
            error_msg = f'cache_type must be one of: {", ".join(valid_types)}'
            raise ValueError(error_msg)

        # Validate cache-specific requirements
        if self.cache_type == 'redis' and not self.redis_url:
            error_msg = 'redis_url is required for Redis cache'
            raise ValueError(error_msg)
        if self.cache_type == 'file' and not self.cache_dir:
            error_msg = 'cache_dir is required for file cache'
            raise ValueError(error_msg)


@dataclass
class LoggingConfig:
    """
    Logging configuration.
    """

    level: str = 'INFO'
    """Logging level."""

    format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    """Log format string."""

    file: str | None = None
    """Log file path."""

    max_size: int = 10 * 1024 * 1024  # 10MB
    """Maximum log file size in bytes."""

    backup_count: int = 5
    """Number of backup log files."""

    json_format: bool = False
    """Use JSON format for logs."""

    include_timestamp: bool = True
    """Include timestamp in log messages."""

    def validate(self) -> None:
        """Validate configuration values."""
        # Validate log level
        valid_levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        if self.level.upper() not in valid_levels:
            error_msg = f'level must be one of: {valid_levels}'
            raise ValueError(error_msg)

        # Validate positive values
        if self.max_size <= 0:
            error_msg = 'max_size must be positive'
            raise ValueError(error_msg)

        # Validate non-negative values
        if self.backup_count < 0:
            error_msg = 'backup_count must be non-negative'
            raise ValueError(error_msg)


@dataclass
class MetricsConfig:
    """
    Metrics configuration.
    """

    enabled: bool = False
    """Whether metrics collection is enabled."""

    metrics_type: str = 'prometheus'
    """Metrics type: 'prometheus', 'statsd', 'datadog'."""

    endpoint: str | None = None
    """Metrics endpoint URL."""

    interval: int = 60
    """Metrics collection interval in seconds."""

    tags: dict[str, str] = field(default_factory=dict)
    """Default tags for metrics."""

    def validate(self) -> None:
        """Validate configuration values."""
        # Validate positive values
        if self.interval <= 0:
            error_msg = 'interval must be positive'
            raise ValueError(error_msg)

        # Validate metrics type
        valid_types = ('prometheus', 'statsd', 'datadog')
        if self.metrics_type not in valid_types:
            error_msg = f'metrics_type must be one of: {", ".join(valid_types)}'
            raise ValueError(error_msg)


@dataclass
class MondayConfig:
    """
    Complete configuration for MondayClient.

    This class centralizes all configuration options for the MondayClient,
    making it easier to manage and extend configuration options.
    """

    api_key: str
    """The API key for authenticating with the monday.com API."""

    url: str = 'https://api.monday.com/v2'
    """The endpoint URL for the monday.com API."""

    version: str | None = None
    """The monday.com API version to use. If None, will automatically fetch the current version."""

    headers: dict[str, Any] = field(default_factory=dict)
    """Additional HTTP headers used for API requests."""

    http: HTTPConfig = field(default_factory=HTTPConfig)
    """HTTP-specific configuration."""

    rate_limit: RateLimitConfig = field(default_factory=RateLimitConfig)
    """Rate limiting configuration."""

    cache: CacheConfig = field(default_factory=CacheConfig)
    """Caching configuration."""

    logging: LoggingConfig = field(default_factory=LoggingConfig)
    """Logging configuration."""

    metrics: MetricsConfig = field(default_factory=MetricsConfig)
    """Metrics configuration."""

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if not self.api_key:
            error_msg = 'api_key is required'
            raise ValueError(error_msg)

        try:
            urlparse(self.url)
        except Exception as e:
            error_msg = f'Invalid URL: {e}'
            raise ValueError(error_msg) from e

        self.http.validate()
        self.rate_limit.validate()
        self.cache.validate()
        self.logging.validate()
        self.metrics.validate()

    @classmethod
    def from_env(cls) -> 'MondayConfig':
        """Create configuration from environment variables."""
        return cls(
            api_key=os.environ['MONDAY_API_KEY'],
            url=os.environ.get('MONDAY_URL', 'https://api.monday.com/v2'),
            version=os.environ.get('MONDAY_VERSION'),
            headers={},
            http=HTTPConfig(
                timeout=int(os.environ.get('MONDAY_TIMEOUT', '30')),
                connect_timeout=int(os.environ.get('MONDAY_CONNECT_TIMEOUT', '10')),
                proxy=os.environ.get('MONDAY_PROXY'),
                proxy_auth=(
                    (os.environ['MONDAY_PROXY_USER'], os.environ['MONDAY_PROXY_PASS'])
                    if os.environ.get('MONDAY_PROXY_USER')
                    and os.environ.get('MONDAY_PROXY_PASS')
                    else None
                ),
                ssl_verify=os.environ.get('MONDAY_SSL_VERIFY', 'true').lower()
                == 'true',
                ssl_cert=os.environ.get('MONDAY_SSL_CERT'),
                ssl_key=os.environ.get('MONDAY_SSL_KEY'),
                ssl_ca_cert=os.environ.get('MONDAY_SSL_CA_CERT'),
                max_connections=int(os.environ.get('MONDAY_MAX_CONNECTIONS', '100')),
                max_connections_per_host=int(
                    os.environ.get('MONDAY_MAX_CONNECTIONS_PER_HOST', '10')
                ),
            ),
            rate_limit=RateLimitConfig(
                rate_limit_seconds=int(
                    os.environ.get('MONDAY_RATE_LIMIT_SECONDS', '60')
                ),
                max_retries=int(os.environ.get('MONDAY_MAX_RETRIES', '4')),
                retry_delay_base=float(
                    os.environ.get('MONDAY_RETRY_DELAY_BASE', '1.0')
                ),
                retry_delay_max=float(os.environ.get('MONDAY_RETRY_DELAY_MAX', '60.0')),
            ),
            cache=CacheConfig(
                enabled=os.environ.get('MONDAY_CACHE_ENABLED', 'false').lower()
                == 'true',
                cache_type=os.environ.get('MONDAY_CACHE_TYPE', 'memory'),
                ttl=int(os.environ.get('MONDAY_CACHE_TTL', '300')),
                max_size=int(os.environ.get('MONDAY_CACHE_MAX_SIZE', '1000')),
                redis_url=os.environ.get('MONDAY_REDIS_URL'),
                cache_dir=os.environ.get('MONDAY_CACHE_DIR'),
            ),
            logging=LoggingConfig(
                level=os.environ.get('MONDAY_LOG_LEVEL', 'INFO'),
                file=os.environ.get('MONDAY_LOG_FILE'),
                json_format=os.environ.get('MONDAY_LOG_JSON', 'false').lower()
                == 'true',
            ),
            metrics=MetricsConfig(
                enabled=os.environ.get('MONDAY_METRICS_ENABLED', 'false').lower()
                == 'true',
                metrics_type=os.environ.get('MONDAY_METRICS_TYPE', 'prometheus'),
                endpoint=os.environ.get('MONDAY_METRICS_ENDPOINT'),
                interval=int(os.environ.get('MONDAY_METRICS_INTERVAL', '60')),
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary for serialization."""
        return {
            'api_key': self.api_key,
            'url': self.url,
            'version': self.version,
            'headers': self.headers,
            'http': {
                'timeout': self.http.timeout,
                'connect_timeout': self.http.connect_timeout,
                'read_timeout': self.http.read_timeout,
                'write_timeout': self.http.write_timeout,
                'proxy': self.http.proxy,
                'proxy_auth': self.http.proxy_auth,
                'ssl_verify': self.http.ssl_verify,
                'ssl_cert': self.http.ssl_cert,
                'ssl_key': self.http.ssl_key,
                'ssl_ca_cert': self.http.ssl_ca_cert,
                'ssl_password': self.http.ssl_password,
                'max_connections': self.http.max_connections,
                'max_connections_per_host': self.http.max_connections_per_host,
                'keepalive_timeout': self.http.keepalive_timeout,
                'tcp_nodelay': self.http.tcp_nodelay,
                'tcp_keepalive': self.http.tcp_keepalive,
                'tcp_keepalive_count': self.http.tcp_keepalive_count,
                'tcp_keepalive_idle': self.http.tcp_keepalive_idle,
                'tcp_keepalive_interval': self.http.tcp_keepalive_interval,
                'use_dns_cache': self.http.use_dns_cache,
                'dns_cache_ttl': self.http.dns_cache_ttl,
                'dns_cache_size': self.http.dns_cache_size,
            },
            'rate_limit': {
                'rate_limit_seconds': self.rate_limit.rate_limit_seconds,
                'max_retries': self.rate_limit.max_retries,
                'retry_delay_base': self.rate_limit.retry_delay_base,
                'retry_delay_max': self.rate_limit.retry_delay_max,
                'retry_delay_factor': self.rate_limit.retry_delay_factor,
                'jitter': self.rate_limit.jitter,
                'jitter_factor': self.rate_limit.jitter_factor,
                'respect_retry_after': self.rate_limit.respect_retry_after,
            },
            'cache': {
                'enabled': self.cache.enabled,
                'cache_type': self.cache.cache_type,
                'ttl': self.cache.ttl,
                'max_size': self.cache.max_size,
                'redis_url': self.cache.redis_url,
                'cache_dir': self.cache.cache_dir,
            },
            'logging': {
                'level': self.logging.level,
                'format': self.logging.format,
                'file': self.logging.file,
                'max_size': self.logging.max_size,
                'backup_count': self.logging.backup_count,
                'json_format': self.logging.json_format,
                'include_timestamp': self.logging.include_timestamp,
            },
            'metrics': {
                'enabled': self.metrics.enabled,
                'metrics_type': self.metrics.metrics_type,
                'endpoint': self.metrics.endpoint,
                'interval': self.metrics.interval,
                'tags': self.metrics.tags,
            },
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'MondayConfig':
        """Create configuration from dictionary."""
        http_data = data.get('http', {})
        rate_limit_data = data.get('rate_limit', {})
        cache_data = data.get('cache', {})
        logging_data = data.get('logging', {})
        metrics_data = data.get('metrics', {})

        return cls(
            api_key=data['api_key'],
            url=data.get('url', 'https://api.monday.com/v2'),
            version=data.get('version'),
            headers=data.get('headers', {}),
            http=HTTPConfig(**http_data),
            rate_limit=RateLimitConfig(**rate_limit_data),
            cache=CacheConfig(**cache_data),
            logging=LoggingConfig(**logging_data),
            metrics=MetricsConfig(**metrics_data),
        )
