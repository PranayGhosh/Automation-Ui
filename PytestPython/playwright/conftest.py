from playwright.sync_api import Playwright
import pytest
from playwright.sync_api import Page
import time
import base64

BASE_URL = "https://dev.xaquaudp.io"

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "args": ["--start-maximized"],
    }

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "no_viewport": True,
    }


@pytest.fixture
def xaquaLogin(page: Page):
    page.goto("https://dev.xaquaudp.io/login")
    page.get_by_label("USER ID").fill("Pranay")
    # time.sleep(5)
    page.get_by_role("button", name="Continue").click()
    # time.sleep(5)
    page.get_by_label("Password", exact=True).fill("Kolkata@#7531")
    # time.sleep(5)
    page.locator("#v2-terms").check()
    # time.sleep(5)
    page.get_by_role("button", name="Sign In").click()
    # time.sleep(5)
    return page

def pytest_addoption(parser):
    parser.addoption(
        "--create-wf", action="store_true", default=False, help="Create a new workflow instead of selecting an existing one"
    )

@pytest.fixture
def should_create_wf(request):
    return request.config.getoption("--create-wf")


@pytest.fixture
def get_token(playwright: Playwright):
    # Encode username:password as HTTP Basic Auth
    credentials = base64.b64encode(b"Pranay:Kolkata@#7531").decode("utf-8")
    
    api_request_context = playwright.request.new_context(
        base_url="https://xaqua-udp-core-sec-api-dev.xaquaudp.io",
        extra_http_headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/json"
        }
    )
    
    response = api_request_context.post(
        "/user/auth",
        data={"shortExp": False, "checkSession": False}
    )
    
    assert response.ok, f"HTTP Error: {response.status} {response.text()}"
    res_json = response.json()
    assert res_json.get("code") == 0, f"Auth Error: {res_json}"
    
    jwt_token = res_json.get("data", {}).get("jwt")
    print(f"\n[SUCCESS] JWT Token Retrieved: {jwt_token}")
    return jwt_token





