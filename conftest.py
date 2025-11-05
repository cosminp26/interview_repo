import os
from dotenv import load_dotenv
import pytest
from playwright.sync_api import sync_playwright

load_dotenv()

@pytest.fixture(scope="session")
def base_url():
    return os.environ.get("BASE_URL", "https://www.saucedemo.com")

@pytest.fixture(scope="session")
def credentials():
    return {
        "username": os.environ.get("USERNAME", "standard_user"),
        "password": os.environ.get("PASSWORD", "secret_sauce"),
    }

@pytest.fixture(scope="session")
def browser_name():
    return os.environ.get("BROWSER", "chromium")

@pytest.fixture(scope="session")
def headless():
    v = os.environ.get("HEADLESS", "true").lower()
    return v in ("1", "true", "yes")

@pytest.fixture(scope="session")
def pw(browser_name, headless):
    with sync_playwright() as p:
        browser = getattr(p, browser_name).launch(headless=headless)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()

@pytest.fixture
def page(pw, base_url):
    page = pw.new_page()
    page.goto(base_url, wait_until="domcontentloaded")
    return page

@pytest.fixture
def login_page(page):
    from pages.login_page import LoginPage
    return LoginPage(page)

@pytest.fixture  
def inventory_page(page):
    from pages.inventory_page import InventoryPage
    return InventoryPage(page)

@pytest.fixture
def cart_page(page):
    from pages.cart_page import CartPage
    return CartPage(page)

@pytest.fixture
def checkout_page(page):
    from pages.checkout_page import CheckoutPage
    return CheckoutPage(page)

@pytest.fixture
def complete_page(page):
    from pages.checkout_complete_page import CheckoutCompletePage
    return CheckoutCompletePage(page)

@pytest.fixture
def logged_in_user(login_page, inventory_page, credentials):
    login_page.login(credentials["username"], credentials["password"])
    assert inventory_page.is_loaded(), "User should be on inventory page after login"
    return {
        'login_page': login_page,
        'inventory_page': inventory_page
    }

@pytest.fixture
def cart_cleanup(inventory_page, cart_page):
    yield
    try:
        if cart_page.is_loaded():
            cart_page.continue_shopping()
        
        cart_count = inventory_page.cart_badge_count()
        if cart_count > 0:
            inventory_page.clear_all_cart_items()
    except Exception as e:
        print(f"Warning: Cart cleanup failed: {e}")

@pytest.fixture
def reset_to_inventory(inventory_page, cart_page, complete_page):
    yield
    try:
        if complete_page.is_loaded():
            complete_page.back_to_inventory()
        elif cart_page.is_loaded():
            cart_page.continue_shopping()
    except Exception as e:
        print(f"Warning: Navigation cleanup failed: {e}")

@pytest.fixture 
def full_checkout_cleanup(inventory_page, cart_page, complete_page):
    yield
    try:
        if complete_page.is_loaded():
            complete_page.back_to_inventory()
        elif cart_page.is_loaded():
            cart_page.continue_shopping()
        
        cart_count = inventory_page.cart_badge_count()
        if cart_count > 0:
            inventory_page.clear_all_cart_items()
    except Exception as e:
        print(f"Warning: Full checkout cleanup failed: {e}")