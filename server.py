import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from src.api.main import app
except Exception:
    print("FAILED TO START APP", file=sys.stderr)
    traceback.print_exc()
    sys.exit(1)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
