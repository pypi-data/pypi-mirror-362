import time
from datetime import datetime
from contextlib import contextmanager
from ..engines.spark import Spark

@contextmanager
def timer(phase: str = "Elapsed time", test_item: str = '', engine: str = None):
    if not hasattr(timer, "results"):
        timer.results = []

    iteration = sum(1 for result in timer.results if result[0] == phase and result[1] == test_item) + 1

    if isinstance(engine, Spark):
        engine.spark.sparkContext.setJobDescription(f"{phase} - {test_item} [i:{iteration}]")

    start = time.time()
    start_datetime = datetime.now()
    success = True
    error_message = None
    error_type = None

    try:
        yield
    except Exception as e:
        success = False
        error_message = str(e)
        error_type = type(e).__name__  # Capture the error type
        print(f"Error during {phase} - {test_item}... {error_type}: {error_message}")
        
    finally:
        end = time.time()
        duration = int((end - start) * 1000)
        print(f"{phase} - {test_item}{f' [i:{iteration}]' if iteration > 1 else ''}: {(duration / 1000):.2f} seconds")
        if isinstance(engine, Spark):
            engine.spark.sparkContext.setJobDescription(None)
        timer.results.append((phase, test_item, start_datetime, duration, iteration, success, f"{error_type}: {error_message}" if error_message else ''))

def _clear_results():
    if hasattr(timer, "results"):
        timer.results = []

timer.clear_results = _clear_results