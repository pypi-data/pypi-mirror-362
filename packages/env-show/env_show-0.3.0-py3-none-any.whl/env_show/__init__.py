# env_show/__init__.py
import sys
from fastapi import FastAPI
from .router import env_router

# --- WARNING: This is a monkey-patching technique and is generally NOT recommended. ---
# It modifies the behavior of the FastAPI class globally.
# It is fragile and depends on import order and FastAPI's internal implementation.

# Store a reference to the original FastAPI.__init__ method
_original_fastapi_init = FastAPI.__init__

def _patched_fastapi_init(self, *args, **kwargs):
    """
    Our custom __init__ method for FastAPI.
    It calls the original __init__ and then includes our env_router.
    """
    # Call the original FastAPI.__init__ to ensure the app is properly initialized
    _original_fastapi_init(self, *args, **kwargs)

    # Automatically include our env_router into the newly created FastAPI app instance
    try:
        self.include_router(env_router)
        print("env_show: Successfully injected /env endpoint via monkey-patching.")
    except Exception as e:
        # Log any errors during injection, but don't crash the user's app
        print(f"env_show: Error injecting /env endpoint: {e}", file=sys.stderr)

# Replace the original FastAPI.__init__ with our patched version
FastAPI.__init__ = _patched_fastapi_init

# You can add a print statement here to confirm that env_show was loaded
# print("env_show package loaded and FastAPI.__init__ patched.")

# This makes env_router available if someone *does* choose to import it explicitly,
# though the goal of this approach is to make it unnecessary.
# from .router import env_router
