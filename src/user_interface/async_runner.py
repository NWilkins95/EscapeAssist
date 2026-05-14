import asyncio
import threading

# Shared event loop for async workflows
if "loop" not in globals():
    loop = asyncio.new_event_loop()
    thread = threading.Thread(target=loop.run_forever, daemon=True)
    thread.start()

# Run async work from sync code
def run_async(coro):
    """
    Run a coroutine on the shared background event loop.
    """
    return asyncio.run_coroutine_threadsafe(coro, loop).result()