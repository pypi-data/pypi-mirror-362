import requests
import time

def test_connection():
    url = 'https://atukpostgrest.clubwise.com/'
    try:
        start = time.perf_counter()
        response = requests.head(url, timeout=5)
        end = time.perf_counter()
        response_time = end - start
        if response.status_code < 400:
            return True, f"Server is reachable (status code: {response.status_code})",  round(response_time,2)
        else:
            return False, f"Server responded, but with error status code: {response.status_code}",  round(response_time,2)
    except requests.exceptions.ConnectionError:
        return False, "Failed to connect: Server unreachable."
    except requests.exceptions.Timeout:
        return False, f"Connection timed out after {timeout} seconds."
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"