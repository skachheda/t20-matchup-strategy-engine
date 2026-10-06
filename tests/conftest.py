import subprocess
import time
import pytest
import requests

@pytest.fixture(scope="session", autouse=True)
def run_streamlit_app():
    # Start streamlit server in background
    cmd = ["streamlit", "run", "app/app.py", "--server.port", "8501", "--server.headless", "true"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Polling wait until server is reachable
    max_wait = 15
    start_time = time.time()
    server_ready = False

    while time.time() - start_time < max_wait:
        try:
            res = requests.get("http://localhost:8501")
            if res.status_code == 200:
                server_ready = True
                break
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)

    if not server_ready:
        process.kill()
        raise RuntimeError("Streamlit server failed to start within 15 seconds.")

    yield

    # Cleanup: shut down the server process
    process.terminate()
    process.wait()