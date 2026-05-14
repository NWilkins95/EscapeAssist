import asyncio
import threading

# Create a single event loop in a background thread to run all async workflows
if "loop" not in globals():
    loop = asyncio.new_event_loop()
    thread = threading.Thread(target=loop.run_forever, daemon=True)
    thread.start()

# Helper function to run async workflows from sync Streamlit code
def run_async(coro):
    return asyncio.run_coroutine_threadsafe(coro, loop).result()