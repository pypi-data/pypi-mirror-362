import requests
import json
import time
from typing import Optional, Dict, Any
import getpass
import os
import sys
from threading import Thread, Event

BASE_URL = "http://139.59.5.84"  # DigitalOcean droplet IP
TOKEN_PATH = os.path.expanduser("~/.guidera_jwt.json")

STREAMING_STATUS_PREFIXES = [
    "Picking best model for you",
    "Checking compliance and generating response",
    "Running policy checks",
    "Running compliance checks"
]

def _is_status_line(line: str) -> bool:
    for prefix in STREAMING_STATUS_PREFIXES:
        if line.strip().startswith(prefix):
            return True
    return False

class Client:
    """
    Client for interacting with the Tilantra Model Swap Router API (fast version).
    Usage:
        guidera_client = Client()  # Will prompt for email/password if not provided and no valid token exists
        response = guidera_client.generate(prompt, prefs, cp_tradeoff_parameter)
    """
    def __init__(self, email: str = None, password: str = None, auth_token: Optional[str] = None, api_base_url: str = BASE_URL):
        self.api_base_url = api_base_url.rstrip("/")
        self.email = email
        self.password = password
        self.auth_token = None
        self.token_exp = None
        # Try to load cached token
        self._load_jwt()
        if not self.auth_token or not self._token_valid():
            # Prompt for credentials if not provided
            if not self.email:
                self.email = input("Enter your email: ")
            if not self.password:
                self.password = getpass.getpass("Enter your password: ")
            self.login()

    def _jwt_file_path(self):
        return TOKEN_PATH

    def _load_jwt(self):
        try:
            with open(self._jwt_file_path(), "r") as f:
                data = json.load(f)
                token = data.get("token")
                exp = data.get("exp")
                if token and exp and exp > time.time():
                    self.auth_token = token
                    self.token_exp = exp
        except Exception:
            pass

    def _save_jwt(self, token, exp):
        with open(self._jwt_file_path(), "w") as f:
            json.dump({"token": token, "exp": exp}, f)
        self.auth_token = token
        self.token_exp = exp

    def _clear_jwt(self):
        try:
            os.remove(self._jwt_file_path())
        except Exception:
            pass
        self.auth_token = None
        self.token_exp = None

    def _token_valid(self):
        return self.auth_token is not None and self.token_exp and self.token_exp > time.time()

    def login(self) -> str:
        """Login and get authentication token"""
        login_url = f"{self.api_base_url}/users/login"
        login_data = {
            "email": self.email,
            "password": self.password
        }
        try:
            response = requests.post(login_url, json=login_data)
            if response.status_code == 200:
                result = response.json()
                token = result.get("token")
                exp = result.get("exp", int(time.time()) + 2 * 3600)  # 2 hours default if not provided
                if token:
                    self._save_jwt(token, exp)
                    return token
                else:
                    raise Exception("Login failed: No token in response")
            else:
                raise Exception(f"Login failed with status {response.status_code}: {response.text}")
        except Exception as e:
            raise Exception(f"Login error: {str(e)}")

    def generate(
        self,
        prompt: str,
        prefs: Optional[Dict[str, Any]] = None,
        cp_tradeoff_parameter: float = 0.7,
        compliance_enabled: bool = True,
        stream: bool = True,
    ) -> None:
        """
        Generate a response from the backend. For main.py, only a single prompt is sent.
        If the token is invalid (401), prompt for login and retry once.
        Prints the response as a single block (no streaming).
        Shows a static line and a spinner line while waiting for the response.
        Suppresses streaming progress/status lines from the printed response.
        """
        if not self._token_valid():
            self.login()
        generate_url = f"{self.api_base_url}/generate"
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
        request_data = {
            "prompt": prompt,
            "prefs": prefs or {},
            "cp_tradeoff_parameter": cp_tradeoff_parameter,
            "compliance_enabled": compliance_enabled
        }

        def spinner_line(stop_event):
            spinner_chars = ['|', '/', '-', '\\']
            idx = 0
            sys.stdout.write("Picking the best model and generating compliance report.... ")
            sys.stdout.flush()
            while not stop_event.is_set():
                sys.stdout.write(f"\rPicking the best model and generating compliance report.... {spinner_chars[idx % len(spinner_chars)]}")
                sys.stdout.flush()
                idx += 1
                time.sleep(0.1)
            sys.stdout.write("\rPicking the best model and generating compliance report.... ✔\n")
            sys.stdout.flush()

        try:
            # Print the static line
            print("Generating your response...")
            stop_event = Event()
            t = Thread(target=spinner_line, args=(stop_event,))
            t.start()
            response = requests.post(generate_url, json=request_data, headers=headers, stream=False)
            stop_event.set()
            t.join()
            if response.status_code == 200:
                # Filter out streaming status lines
                lines = response.text.splitlines()
                filtered = [line for line in lines if not _is_status_line(line)]
                print("\n".join(filtered))
                return
            elif response.status_code == 401:
                self._clear_jwt()
                print("Session expired or invalid. Please log in again.")
                self.email = input("Enter your email: ")
                self.password = getpass.getpass("Enter your password: ")
                self.login()
                headers["Authorization"] = f"Bearer {self.auth_token}"
                stop_event.clear()
                t = Thread(target=spinner_line, args=(stop_event,))
                print("Generating your response...")
                t.start()
                response = requests.post(generate_url, json=request_data, headers=headers, stream=False)
                stop_event.set()
                t.join()
                if response.status_code == 200:
                    lines = response.text.splitlines()
                    filtered = [line for line in lines if not _is_status_line(line)]
                    print("\n".join(filtered))
                    return
                else:
                    print(f"Error: HTTP {response.status_code}: {response.text}")
                    return
            else:
                print(f"Error: HTTP {response.status_code}: {response.text}")
                return
        except Exception as e:
            print(f"Error: {str(e)}")
            return