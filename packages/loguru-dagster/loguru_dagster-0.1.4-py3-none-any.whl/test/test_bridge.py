import pytest
from loguru import logger
from loguru_dagster import dagster_context_sink, with_loguru_logger


class MockDagsterContext:
    """Simulates Dagster's context.log interface with debug logging capabilities."""
    def __init__(self):
        self.log_history = []

    class log:
        def __init__(self):
            self.log_history = []

        @staticmethod
        def debug(msg): 
            print("[dagster.debug]", msg)
            return {"level": "debug", "message": msg}

        @staticmethod
        def info(msg): 
            print("[dagster.info]", msg)
            return {"level": "info", "message": msg}

        @staticmethod
        def warning(msg): 
            print("[dagster.warning]", msg)
            return {"level": "warning", "message": msg}

        @staticmethod
        def error(msg): 
            print("[dagster.error]", msg)
            return {"level": "error", "message": msg}

        @staticmethod
        def critical(msg):
            print("[dagster.critical]", msg)
            return {"level": "critical", "message": msg}


@pytest.fixture
def setup_logger():
    """Fixture to setup and cleanup logger for each test."""
    yield
    logger.remove()  # Cleanup after test

def test_dagster_context_sink_basic_logging(capfd, setup_logger):
    """Test that dagster_context_sink routes basic logs correctly."""
    context = MockDagsterContext()
    sink = dagster_context_sink(context)

    logger.remove()
    logger.add(sink, level="DEBUG")

    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")

    captured = capfd.readouterr()
    assert "[dagster.debug] Debug message" in captured.out
    assert "[dagster.info] Info message" in captured.out
    assert "[dagster.warning] Warning message" in captured.out
    assert "[dagster.error] Error message" in captured.out

def test_dagster_context_sink_with_structured_logging(capfd, setup_logger):
    """Test structured logging with extra fields."""
    context = MockDagsterContext()
    sink = dagster_context_sink(context)

    logger.remove()
    logger.add(sink, level="DEBUG")

    # Test structured logging with extra fields
    logger.bind(user="test_user", action="login").info("User login attempt")
    logger.bind(error_code=500).error("Server error occurred")
    
    captured = capfd.readouterr()
    assert "[dagster.info] User login attempt" in captured.out
    assert "[dagster.error] Server error occurred" in captured.out

def test_dagster_context_sink_different_log_levels(capfd, setup_logger):
    """Test various log levels including TRACE and CRITICAL."""
    context = MockDagsterContext()
    sink = dagster_context_sink(context)

    logger.remove()
    logger.add(sink, level="TRACE")

    test_messages = [
        (logger.trace, "Trace level message"),
        (logger.debug, "Debug level message"),
        (logger.info, "Info level message"),
        (logger.success, "Success message"),
        (logger.warning, "Warning level message"),
        (logger.error, "Error level message"),
        (logger.critical, "Critical level message"),
    ]

    for log_func, message in test_messages:
        log_func(message)

    captured = capfd.readouterr()
    assert "[dagster.debug] Trace level message" in captured.out
    assert "[dagster.debug] Debug level message" in captured.out
    assert "[dagster.info] Info level message" in captured.out
    assert "[dagster.info] Success message" in captured.out
    assert "[dagster.warning] Warning level message" in captured.out
    assert "[dagster.error] Error level message" in captured.out
    assert "[dagster.critical] Critical level message" in captured.out


class DagsterOperations:
    """Class for simulating different Dagster operations."""
    
    def __init__(self, context):
        self.context = context
    
    @with_loguru_logger
    def successful_op(self):
        logger.info("Operation completed successfully!")
        return True

    @with_loguru_logger
    def failing_op(self):
        logger.error("Operation failed!")
        raise ValueError("Operation failed")

    @with_loguru_logger
    def complex_op(self):
        logger.debug("Starting complex operation...")
        logger.info("Processing data")
        logger.warning("Resource usage high")
        logger.success("Data processing complete")
        return "Success"

    def get_context(self):
        return self.context


def test_with_loguru_logger_decorator_success(capfd, setup_logger):
    """Test the @with_loguru_logger decorator with successful operation."""
    context = MockDagsterContext()
    test_ops = DagsterOperations(context)

    result = test_ops.successful_op()
    assert result is True

    captured = capfd.readouterr()
    assert "[dagster.info] Operation completed successfully!" in captured.out


def test_with_loguru_logger_decorator_failure(capfd, setup_logger):
    """Test the @with_loguru_logger decorator with failing operation."""
    context = MockDagsterContext()
    test_ops = DagsterOperations(context)

    with pytest.raises(ValueError, match="Operation failed"):
        test_ops.failing_op()

    captured = capfd.readouterr()
    assert "[dagster.error] Operation failed!" in captured.out


def test_with_loguru_logger_decorator_complex(capfd, setup_logger):
    """Test the @with_loguru_logger decorator with complex logging scenario."""
    context = MockDagsterContext()
    test_ops = DagsterOperations(context)

    result = test_ops.complex_op()
    assert result == "Success"

    captured = capfd.readouterr()
    assert "[dagster.debug] Starting complex operation..." in captured.out
    assert "[dagster.info] Processing data" in captured.out
    assert "[dagster.warning] Resource usage high" in captured.out
    assert "[dagster.info] Data processing complete" in captured.out


def test_mixed_logging_systems(capfd, setup_logger):
    """Test mixing Dagster's native logging with Loguru logging."""
    test_ctx = DagsterTestContext()

    class MixedLogger:
        def __init__(self, context):
            self.context = context

        @with_loguru_logger
        def mixed_logging_op(self):
            # Direct Dagster logging
            self.context.log.info("Direct Dagster log")
            # Loguru logging
            logger.info("Loguru log")
            # Mixed in sequence
            self.context.log.debug("Dagster debug")
            logger.debug("Loguru debug")
            return "Mixed logging complete"

        def get_context(self):
            return self.context

    mixed_logger = MixedLogger(test_ctx.context)
    result = mixed_logger.mixed_logging_op()
    assert result == "Mixed logging complete"

    captured = capfd.readouterr()
    assert "[dagster.info] Direct Dagster log" in captured.out
    assert "[dagster.info] Loguru log" in captured.out
    assert "[dagster.debug] Dagster debug" in captured.out
    assert "[dagster.debug] Loguru debug" in captured.out


def test_nested_operations_logging(capfd, setup_logger):
    """Test nested operations with both logging systems."""
    test_ctx = DagsterTestContext()

    class NestedLogger:
        def __init__(self, test_ctx):
            self.context = test_ctx.context
            self.test_ops = test_ctx.test_ops

        @with_loguru_logger
        def nested_op(self):
            logger.info("Starting nested operation")
            self.test_ops.complex_op()  # This already has logging
            logger.info("Nested operation complete")
            return True

        def get_context(self):
            return self.context

    nested_logger = NestedLogger(test_ctx)
    result = nested_logger.nested_op()
    assert result is True

    captured = capfd.readouterr()
    assert "[dagster.info] Starting nested operation" in captured.out
    assert "[dagster.debug] Starting complex operation..." in captured.out
    assert "[dagster.info] Processing data" in captured.out
    assert "[dagster.warning] Resource usage high" in captured.out
    assert "[dagster.info] Data processing complete" in captured.out
    assert "[dagster.info] Nested operation complete" in captured.out


def test_exception_handling_with_logging(capfd, setup_logger):
    """Test exception handling with both logging systems."""
    test_ctx = DagsterTestContext()

    class ExceptionLogger:
        def __init__(self, context):
            self.context = context

        @with_loguru_logger
        def exception_op(self):
            try:
                logger.info("Starting risky operation")
                raise ValueError("Simulated error")
            except ValueError as e:
                logger.error(f"Caught error: {str(e)}")
                self.context.log.error(f"Dagster also logged: {str(e)}")
            finally:
                logger.info("Cleanup in finally block")

        def get_context(self):
            return self.context

    exception_logger = ExceptionLogger(test_ctx.context)
    exception_logger.exception_op()
    captured = capfd.readouterr()
    assert "[dagster.info] Starting risky operation" in captured.out
    assert "[dagster.error] Caught error: Simulated error" in captured.out
    assert "[dagster.error] Dagster also logged: Simulated error" in captured.out
    assert "[dagster.info] Cleanup in finally block" in captured.out


def test_structured_logging_with_context(capfd, setup_logger):
    """Test structured logging with context data in both systems."""
    test_ctx = DagsterTestContext()

    class StructuredLogger:
        def __init__(self, context):
            self.context = context

        @with_loguru_logger
        def structured_log_op(self):
            # Loguru structured logging
            logger.bind(
                operation_id="12345",
                user_id="user123",
                environment="test"
            ).info("Operation started with context")

            # Add some processing simulation
            logger.bind(
                duration_ms=150,
                items_processed=100
            ).success("Processing complete")

            return "Structured logging test complete"

        def get_context(self):
            return self.context

    structured_logger = StructuredLogger(test_ctx.context)
    result = structured_logger.structured_log_op()
    assert result == "Structured logging test complete"

    captured = capfd.readouterr()
    assert "[dagster.info] Operation started with context" in captured.out
    assert "[dagster.info] Processing complete" in captured.out


def test_log_level_inheritance(capfd, setup_logger):
    """Test log level inheritance and filtering."""
    test_ctx = DagsterTestContext()

    class LevelLogger:
        def __init__(self, context):
            self.context = context

        @with_loguru_logger
        def level_test_op(self):
            logger.trace("This should not appear")  # Should be filtered out
            logger.debug("Debug message should appear")
            logger.info("Info message should appear")
            logger.success("Success should map to info")
            logger.warning("Warning message should appear")
            logger.error("Error message should appear")
            logger.critical("Critical message should appear")

        def get_context(self):
            return self.context

    level_logger = LevelLogger(test_ctx.context)
    level_logger.level_test_op()
    captured = capfd.readouterr()
    
    assert "This should not appear" not in captured.out
    assert "[dagster.debug] Debug message should appear" in captured.out
    assert "[dagster.info] Info message should appear" in captured.out
    assert "[dagster.info] Success should map to info" in captured.out
    assert "[dagster.warning] Warning message should appear" in captured.out
    assert "[dagster.error] Error message should appear" in captured.out
    assert "[dagster.critical] Critical message should appear" in captured.out


def test_concurrent_operations_logging(capfd, setup_logger):
    """Test logging behavior with concurrent operations."""
    import threading
    import time
    test_ctx = DagsterTestContext()

    class ConcurrentLogger:
        def __init__(self, context):
            self.context = context

        @with_loguru_logger
        def concurrent_op(self, op_id):
            logger.info(f"Operation {op_id} started")
            time.sleep(0.1)  # Simulate some work
            logger.info(f"Operation {op_id} completed")
            return op_id

        def get_context(self):
            return self.context

    concurrent_logger = ConcurrentLogger(test_ctx.context)

    # Run multiple operations concurrently
    threads = []
    for i in range(3):
        thread = threading.Thread(
            target=concurrent_logger.concurrent_op, 
            args=(f"thread-{i}",)
        )
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    captured = capfd.readouterr()
    
    # Check that all operations were logged
    for i in range(3):
        assert f"[dagster.info] Operation thread-{i} started" in captured.out
        assert f"[dagster.info] Operation thread-{i} completed" in captured.out


def test_log_formatting_consistency(capfd, setup_logger):
    """Test consistency of log formatting between Dagster and Loguru."""
    test_ctx = DagsterTestContext()

    class FormatLogger:
        def __init__(self, context):
            self.context = context

        @with_loguru_logger
        def format_test_op(self):
            # Test different message formats
            logger.info("Simple message")
            logger.info("Message with {}", "placeholder")
            logger.info("Message with {name}", name="named placeholder")
            logger.info("Message with multiple {} {}", "placeholders", "here")
            
            # Test with different data types
            logger.info("Number: {}", 42)
            logger.info("Boolean: {}", True)
            logger.info("List: {}", [1, 2, 3])
            logger.info("Dict: {}", {"key": "value"})

        def get_context(self):
            return self.context

    format_logger = FormatLogger(test_ctx.context)
    format_logger.format_test_op()
    captured = capfd.readouterr()
    
    assert "[dagster.info] Simple message" in captured.out
    assert "[dagster.info] Message with placeholder" in captured.out
    assert "[dagster.info] Message with named placeholder" in captured.out
    assert "[dagster.info] Message with multiple placeholders here" in captured.out
    assert "[dagster.info] Number: 42" in captured.out
    assert "[dagster.info] Boolean: True" in captured.out
    assert "[dagster.info] List: [1, 2, 3]" in captured.out
    assert "[dagster.info] Dict: {'key': 'value'}" in captured.out


def test_error_context_preservation(capfd, setup_logger):
    """Test that error context and stack traces are preserved."""
    test_ctx = DagsterTestContext()

    class CustomError(Exception):
        pass

    class ErrorLogger:
        def __init__(self, context):
            self.context = context

        @with_loguru_logger
        def nested_error(self):
            raise CustomError("Nested error occurred")

        @with_loguru_logger
        def error_context_op(self):
            try:
                logger.info("Starting operation that will fail")
                self.nested_error()
            except CustomError as e:
                logger.error(f"An error occurred in the nested operation: {str(e)}")
                self.context.log.error(f"Dagster also logged error: {str(e)}")
                return "Error handled"

        def get_context(self):
            return self.context

    error_logger = ErrorLogger(test_ctx.context)
    result = error_logger.error_context_op()
    assert result == "Error handled"

    captured = capfd.readouterr()
    assert "[dagster.info] Starting operation that will fail" in captured.out
    assert "[dagster.error] An error occurred in the nested operation: Nested error occurred" in captured.out
    assert "[dagster.error] Dagster also logged error: Nested error occurred" in captured.out


class DagsterTestContext:
    """Helper class to manage context for test functions."""
    def __init__(self):
        self.context = MockDagsterContext()
        self.test_ops = DagsterOperations(self.context)

    def get_context(self):
        return self.context
