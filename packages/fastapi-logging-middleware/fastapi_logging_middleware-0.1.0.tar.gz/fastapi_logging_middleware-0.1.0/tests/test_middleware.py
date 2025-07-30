import io
import logging
from unittest.mock import AsyncMock, MagicMock, patch

import colorama
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from logging_middleware import GoStyleLoggingMiddleware


class TestGoStyleLoggingMiddleware:
    @pytest.fixture
    def output_buffer(self):
        return io.StringIO()

    @pytest.fixture
    def middleware(self, app, output_buffer):
        return GoStyleLoggingMiddleware(app, output=output_buffer)

    def test_middleware_initialization(self, app, output_buffer):
        middleware = GoStyleLoggingMiddleware(app, output=output_buffer)

        assert middleware.app == app
        assert middleware.output == output_buffer

        uvicorn_access_logger = logging.getLogger("uvicorn.access")
        assert uvicorn_access_logger.disabled is True
        assert uvicorn_access_logger.propagate is False

    def test_middleware_initialization_default_output(self, app):
        middleware = GoStyleLoggingMiddleware(app)
        assert isinstance(middleware.output, colorama.ansitowin32.StreamWrapper)

    def test_format_duration_microseconds(self):
        result = GoStyleLoggingMiddleware._format_duration(0.5)
        assert result == "500µs"

    def test_format_duration_milliseconds(self):
        result = GoStyleLoggingMiddleware._format_duration(50.123)
        assert result == "50.1ms"

    def test_format_duration_seconds(self):
        result = GoStyleLoggingMiddleware._format_duration(1500.0)
        assert result == "1.50s"

    def test_get_client_ip_from_client(self):
        scope = {"client": ("192.168.1.1", 8000), "headers": []}

        ip = GoStyleLoggingMiddleware._get_client_ip(scope)
        assert ip == "192.168.1.1"

    def test_get_client_ip_from_x_forwarded_for(self):
        scope = {"headers": [(b"x-forwarded-for", b"10.0.0.1, 192.168.1.1"), (b"host", b"example.com")]}

        ip = GoStyleLoggingMiddleware._get_client_ip(scope)
        assert ip == "10.0.0.1"

    def test_get_client_ip_from_x_real_ip(self):
        scope = {"headers": [(b"x-real-ip", b"10.0.0.2"), (b"host", b"example.com")]}

        ip = GoStyleLoggingMiddleware._get_client_ip(scope)
        assert ip == "10.0.0.2"

    def test_get_client_ip_unknown(self):
        scope = {"headers": []}

        ip = GoStyleLoggingMiddleware._get_client_ip(scope)
        assert ip == "unknown"

    @pytest.mark.parametrize(
        "status_code,expected_color",
        [
            (200, GoStyleLoggingMiddleware._STATUS_COLORS[range(200, 300)]),
            (301, GoStyleLoggingMiddleware._STATUS_COLORS[range(300, 400)]),
            (404, GoStyleLoggingMiddleware._STATUS_COLORS[range(400, 500)]),
            (500, GoStyleLoggingMiddleware._STATUS_COLORS[range(500, 600)]),
            (100, GoStyleLoggingMiddleware._DEFAULT_COLOR),
        ],
    )
    def test_get_status_color_parametrized(self, status_code, expected_color):
        middleware = GoStyleLoggingMiddleware(MagicMock())
        color = middleware._get_status_color(status_code)
        assert color == expected_color

    @pytest.mark.parametrize(
        "method,expected_color",
        [
            ("GET", GoStyleLoggingMiddleware._METHOD_COLORS["GET"]),
            ("POST", GoStyleLoggingMiddleware._METHOD_COLORS["POST"]),
            ("UNKNOWN", GoStyleLoggingMiddleware._DEFAULT_COLOR),
        ],
    )
    def test_get_method_color_parametrized(self, method, expected_color):
        middleware = GoStyleLoggingMiddleware(MagicMock())
        color = middleware._get_method_color(method)
        assert color == expected_color

    def test_build_log_message_basic(self):
        middleware = GoStyleLoggingMiddleware(MagicMock())

        scope = {
            "type": "http",
            "method": "GET",
            "path": "/test",
            "query_string": b"",
            "client": ("127.0.0.1", 8000),
            "headers": [],
        }

        with patch("logging_middleware.middleware.datetime") as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2023-01-01 12:00:00.000000"

            message = middleware._build_log_message(scope, 200, 10.5)

            assert "2023-01-01 12:00:00.000000" in message
            assert "200" in message
            assert "10.5ms" in message
            assert "127.0.0.1" in message
            assert "GET" in message
            assert '"/test"' in message

    def test_build_log_message_with_query_string(self):
        middleware = GoStyleLoggingMiddleware(MagicMock())

        scope = {
            "type": "http",
            "method": "GET",
            "path": "/test",
            "query_string": b"param=value",
            "client": ("127.0.0.1", 8000),
            "headers": [],
        }

        with patch("logging_middleware.middleware.datetime") as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2023-01-01 12:00:00.000000"

            message = middleware._build_log_message(scope, 200, 10.5)
            assert '"/test?param=value"' in message

    def test_log_message_output(self, output_buffer):
        middleware = GoStyleLoggingMiddleware(MagicMock(), output=output_buffer)

        test_message = "Test log message"
        middleware._log_message(test_message)

        output = output_buffer.getvalue()
        assert test_message in output

    @pytest.mark.asyncio
    async def test_middleware_call_non_http(self, middleware, output_buffer):
        mock_app = AsyncMock()
        middleware.app = mock_app

        scope = {"type": "websocket"}
        receive = AsyncMock()
        send = AsyncMock()

        await middleware(scope, receive, send)

        mock_app.assert_called_once_with(scope, receive, send)
        assert output_buffer.getvalue() == ""

    @pytest.mark.asyncio
    async def test_middleware_call_successful_request(self, middleware, output_buffer):
        mock_app = AsyncMock()
        middleware.app = mock_app

        scope = {
            "type": "http",
            "method": "GET",
            "path": "/test",
            "query_string": b"",
            "client": ("127.0.0.1", 8000),
            "headers": [],
        }

        receive = AsyncMock()
        send = AsyncMock()

        async def mock_send_wrapper(message):
            if message["type"] == "http.response.start":
                message["status"] = 200
            await send(message)

        with patch.object(middleware, "_build_log_message", return_value="Test log"):
            await middleware(scope, receive, send)

        mock_app.assert_called_once()
        output = output_buffer.getvalue()
        assert "Test log" in output

    @pytest.mark.asyncio
    async def test_middleware_call_with_exception(self, middleware, output_buffer):
        mock_app = AsyncMock()
        mock_app.side_effect = Exception("Test exception")
        middleware.app = mock_app

        scope = {
            "type": "http",
            "method": "GET",
            "path": "/test",
            "query_string": b"",
            "client": ("127.0.0.1", 8000),
            "headers": [],
        }

        receive = AsyncMock()
        send = AsyncMock()

        with pytest.raises(Exception, match="Test exception"):
            await middleware(scope, receive, send)

        output = output_buffer.getvalue()
        assert "Request failed after" in output
        assert "Test exception" in output

    def test_integration_with_fastapi_successful_request(self, app, output_buffer):
        app.add_middleware(GoStyleLoggingMiddleware, output=output_buffer)

        with TestClient(app) as client:
            response = client.get("/")
            assert response.status_code == 200
            assert response.json() == {"message": "Hello World"}

        output = output_buffer.getvalue()
        assert "200" in output
        assert "GET" in output
        assert '"/"' in output

    def test_integration_with_fastapi_error_request(self, app, output_buffer):
        app.add_middleware(GoStyleLoggingMiddleware, output=output_buffer)

        with TestClient(app) as client:
            response = client.get("/error")
            assert response.status_code == 404

        output = output_buffer.getvalue()
        assert "404" in output
        assert "GET" in output
        assert '"/error"' in output

    def test_integration_with_fastapi_different_methods(self, app, output_buffer):
        app.add_middleware(GoStyleLoggingMiddleware, output=output_buffer)

        with TestClient(app) as client:
            response = client.get("/")
            assert response.status_code == 200

            response = client.post("/create")
            assert response.status_code == 200

            response = client.put("/update")
            assert response.status_code == 200

            response = client.delete("/delete")
            assert response.status_code == 200

        output = output_buffer.getvalue()
        assert "GET" in output
        assert "POST" in output
        assert "PUT" in output
        assert "DELETE" in output

    def test_integration_with_fastapi_slow_request(self, app, output_buffer):
        app.add_middleware(GoStyleLoggingMiddleware, output=output_buffer)

        with TestClient(app) as client:
            response = client.get("/slow")
            assert response.status_code == 200

        output = output_buffer.getvalue()
        assert "200" in output
        assert "ms" in output or "s" in output

    @pytest.mark.asyncio
    async def test_send_wrapper_status_capture(self, middleware):
        mock_app = AsyncMock()
        middleware.app = mock_app

        scope = {
            "type": "http",
            "method": "GET",
            "path": "/test",
            "query_string": b"",
            "client": ("127.0.0.1", 8000),
            "headers": [],
        }

        receive = AsyncMock()
        send = AsyncMock()

        async def mock_app_func(scope, receive, send_wrapper):
            await send_wrapper({"type": "http.response.start", "status": 201})
            await send_wrapper({"type": "http.response.body", "body": b"Test body"})

        middleware.app = mock_app_func

        with patch.object(middleware, "_build_log_message") as mock_build:
            mock_build.return_value = "Test log"
            await middleware(scope, receive, send)

            mock_build.assert_called_once()
            call_args = mock_build.call_args
            assert call_args[0][1] == 201

    def test_uvicorn_logging_setup(self):
        uvicorn_access_logger = logging.getLogger("uvicorn.access")
        uvicorn_access_logger.disabled = False
        uvicorn_access_logger.propagate = True

        GoStyleLoggingMiddleware._setup_uvicorn_logging()

        assert uvicorn_access_logger.disabled is True
        assert uvicorn_access_logger.propagate is False

        uvicorn_logger = logging.getLogger("uvicorn")
        assert uvicorn_logger.level == logging.INFO

    def test_empty_scope_handling(self):
        middleware = GoStyleLoggingMiddleware(MagicMock())

        scope = {}

        client_ip = middleware._get_client_ip(scope)
        assert client_ip == "unknown"

    def test_malformed_headers_handling(self):
        middleware = GoStyleLoggingMiddleware(MagicMock())

        scope = {
            "headers": [
                (b"x-forwarded-for", b""),
                (b"x-real-ip", b"invalid-ip"),
                (b"malformed", "not-bytes"),
            ]
        }

        client_ip = middleware._get_client_ip(scope)
        assert client_ip == "invalid-ip"

    def test_very_long_duration_formatting(self):
        duration_ms = 3600000.0
        result = GoStyleLoggingMiddleware._format_duration(duration_ms)
        assert result == "3600.00s"

    def test_very_small_duration_formatting(self):
        duration_ms = 0.0001
        result = GoStyleLoggingMiddleware._format_duration(duration_ms)
        assert result == "0µs"

    def test_negative_duration_formatting(self):
        duration_ms = -5.0
        result = GoStyleLoggingMiddleware._format_duration(duration_ms)
        assert result == "-5000µs"

    def test_missing_scope_fields(self):
        middleware = GoStyleLoggingMiddleware(MagicMock())

        scope = {"type": "http"}

        with patch("logging_middleware.middleware.datetime") as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2023-01-01 12:00:00.000000"
            message = middleware._build_log_message(scope, 200, 10.0)

            assert "2023-01-01 12:00:00.000000" in message
            assert "200" in message
            assert "10.0ms" in message
            assert "GET" in message
            assert "unknown" in message
            assert '"/"' in message

    def test_extremely_long_path(self):
        middleware = GoStyleLoggingMiddleware(MagicMock())

        long_path = "/very/long/path/" + "segment/" * 100
        scope = {
            "type": "http",
            "method": "GET",
            "path": long_path,
            "query_string": b"",
            "client": ("127.0.0.1", 8000),
            "headers": [],
        }

        with patch("logging_middleware.middleware.datetime") as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2023-01-01 12:00:00.000000"

            message = middleware._build_log_message(scope, 200, 10.0)
            assert long_path in message

    def test_special_characters_in_query_string(self):
        middleware = GoStyleLoggingMiddleware(MagicMock())

        scope = {
            "type": "http",
            "method": "GET",
            "path": "/test",
            "query_string": b"param=value%20with%20spaces&special=!@#$%^&*()",
            "client": ("127.0.0.1", 8000),
            "headers": [],
        }

        with patch("logging_middleware.middleware.datetime") as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2023-01-01 12:00:00.000000"

            message = middleware._build_log_message(scope, 200, 10.0)
            assert "param=value%20with%20spaces&special=!@#$%^&*()" in message

    @pytest.mark.asyncio
    async def test_exception_during_send(self):
        output_buffer = io.StringIO()
        mock_app = AsyncMock()
        middleware = GoStyleLoggingMiddleware(mock_app, output=output_buffer)

        scope = {
            "type": "http",
            "method": "GET",
            "path": "/test",
            "query_string": b"",
            "client": ("127.0.0.1", 8000),
            "headers": [],
        }

        receive = AsyncMock()
        send = AsyncMock()
        send.side_effect = Exception("Send failed")

        async def mock_app_func(scope, receive, send_wrapper):
            await send_wrapper({"type": "http.response.start", "status": 200})

        mock_app.side_effect = mock_app_func

        with pytest.raises(Exception, match="Send failed"):
            await middleware(scope, receive, send)

    @pytest.mark.asyncio
    async def test_multiple_response_start_messages(self):
        output_buffer = io.StringIO()
        mock_app = AsyncMock()
        middleware = GoStyleLoggingMiddleware(mock_app, output=output_buffer)

        scope = {
            "type": "http",
            "method": "GET",
            "path": "/test",
            "query_string": b"",
            "client": ("127.0.0.1", 8000),
            "headers": [],
        }

        receive = AsyncMock()
        send = AsyncMock()

        async def mock_app_func(scope, receive, send_wrapper):
            await send_wrapper({"type": "http.response.start", "status": 200})
            await send_wrapper({"type": "http.response.start", "status": 404})
            await send_wrapper({"type": "http.response.body", "body": b"test"})

        mock_app.side_effect = mock_app_func

        await middleware(scope, receive, send)

        log_output = output_buffer.getvalue()
        assert "404" in log_output

    def test_output_buffer_exception_handling(self):
        class FailingBuffer:
            def write(self, text):
                raise IOError("Buffer write failed")

            def flush(self):
                raise IOError("Buffer flush failed")

        failing_buffer = FailingBuffer()
        middleware = GoStyleLoggingMiddleware(MagicMock(), output=failing_buffer)

        with pytest.raises(IOError):
            middleware._log_message("test message")

    def test_ipv6_address_handling(self):
        middleware = GoStyleLoggingMiddleware(MagicMock())

        scope = {"client": ("2001:db8::1", 8000), "headers": []}

        ip = middleware._get_client_ip(scope)
        assert ip == "2001:db8::1"

    def test_forwarded_for_multiple_ips(self):
        middleware = GoStyleLoggingMiddleware(MagicMock())

        scope = {
            "headers": [
                (b"x-forwarded-for", b"203.0.113.1, 198.51.100.1, 192.0.2.1"),
            ]
        }

        ip = middleware._get_client_ip(scope)
        assert ip == "203.0.113.1"

    def test_forwarded_for_with_spaces(self):
        middleware = GoStyleLoggingMiddleware(MagicMock())

        scope = {
            "headers": [
                (b"x-forwarded-for", b"  203.0.113.1  ,  198.51.100.1  "),
            ]
        }

        ip = middleware._get_client_ip(scope)
        assert ip == "203.0.113.1"

    @pytest.mark.asyncio
    async def test_middleware_with_streaming_response(self):
        output_buffer = io.StringIO()
        app = FastAPI()

        @app.get("/stream")
        async def stream_endpoint():
            def generate():
                for i in range(3):
                    yield f"chunk {i}\n"

            from fastapi.responses import StreamingResponse

            return StreamingResponse(generate(), media_type="text/plain")

        app.add_middleware(GoStyleLoggingMiddleware, output=output_buffer)

        with TestClient(app) as client:
            response = client.get("/stream")
            assert response.status_code == 200
            assert "chunk 0" in response.text
            assert "chunk 1" in response.text
            assert "chunk 2" in response.text

        log_output = output_buffer.getvalue()
        assert "200" in log_output
        assert '"/stream"' in log_output

    def test_status_code_edge_values(self):
        middleware = GoStyleLoggingMiddleware(MagicMock())

        edge_codes = [100, 199, 200, 299, 300, 399, 400, 499, 500, 599, 600, 999]

        for code in edge_codes:
            color = middleware._get_status_color(code)
            assert color is not None

            if 200 <= code < 300:
                assert color == middleware._STATUS_COLORS[range(200, 300)]
            elif 300 <= code < 400:
                assert color == middleware._STATUS_COLORS[range(300, 400)]
            elif 400 <= code < 500:
                assert color == middleware._STATUS_COLORS[range(400, 500)]
            elif 500 <= code < 600:
                assert color == middleware._STATUS_COLORS[range(500, 600)]
            else:
                assert color == middleware._DEFAULT_COLOR

    def test_unusual_http_methods(self):
        middleware = GoStyleLoggingMiddleware(MagicMock())

        unusual_methods = ["TRACE", "CONNECT", "CUSTOM", ""]

        for method in unusual_methods:
            color = middleware._get_method_color(method)
            if method in middleware._METHOD_COLORS:
                assert color == middleware._METHOD_COLORS[method]
            else:
                assert color == middleware._DEFAULT_COLOR

    @pytest.mark.asyncio
    async def test_middleware_with_custom_asgi_app(self):
        output_buffer = io.StringIO()

        async def custom_app(scope, receive, send):
            if scope["type"] == "http":
                await send(
                    {
                        "type": "http.response.start",
                        "status": 418,  # I'm a teapot
                        "headers": [[b"content-type", b"text/plain"]],
                    }
                )
                await send(
                    {
                        "type": "http.response.body",
                        "body": b"I'm a teapot",
                    }
                )

        middleware = GoStyleLoggingMiddleware(custom_app, output=output_buffer)

        scope = {
            "type": "http",
            "method": "GET",
            "path": "/tea",
            "query_string": b"",
            "client": ("127.0.0.1", 8000),
            "headers": [],
        }

        receive = AsyncMock()
        send = AsyncMock()

        await middleware(scope, receive, send)

        log_output = output_buffer.getvalue()
        assert "418" in log_output
        assert '"/tea"' in log_output

    def test_zero_duration(self):
        result = GoStyleLoggingMiddleware._format_duration(0.0)
        assert result == "0µs"

    def test_exactly_one_millisecond(self):
        result = GoStyleLoggingMiddleware._format_duration(1.0)
        assert result == "1.0ms"

    def test_exactly_one_second(self):
        result = GoStyleLoggingMiddleware._format_duration(1000.0)
        assert result == "1.00s"
