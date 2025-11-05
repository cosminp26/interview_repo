class TestAuthentication:
    
    def test_successful_login(self, login_page, inventory_page, credentials):
        login_page.login(credentials["username"], credentials["password"])
        assert inventory_page.is_loaded(), "User should be redirected to inventory page after successful login"
    
    def test_invalid_login_shows_error(self, login_page):
        login_page.login("invalid_user", "wrong_password")
        
        error_message = login_page.error_text()
        assert "Epic sadface" in error_message, "Error message should be displayed for invalid credentials"

    def test_logout_clears_session(self, login_page, inventory_page, page, credentials, base_url, cart_cleanup):
        login_page.login(credentials["username"], credentials["password"])
        
        assert inventory_page.is_loaded()
        inventory_page.add_item_by_name("Sauce Labs Backpack")
        assert inventory_page.cart_badge_count() == 1
        
        inventory_page.logout()
        
        page.goto(base_url, wait_until="domcontentloaded")
        login_page.login(credentials["username"], credentials["password"])
        assert inventory_page.is_loaded()
        assert inventory_page.cart_badge_count() == 1, "Cart should not be empty after logout and re-login"

    def test_logout_keeps_user_session(self, login_page, inventory_page, page, credentials, base_url, cart_cleanup):
        login_page.login(credentials["username"], credentials["password"])
        
        assert inventory_page.is_loaded()
        inventory_page.add_item_by_name("Sauce Labs Onesie")
        assert inventory_page.cart_badge_count() == 1
        
        inventory_page.logout()
        
        page.goto(base_url, wait_until="domcontentloaded")
        login_page.login(credentials["username"], credentials["password"])
        assert inventory_page.is_loaded()
        assert inventory_page.cart_badge_count() == 1, "Cart shouldn't be empty after logout and re-login with same user"

    def test_logout_clears_cart_for_different_user(self, login_page, inventory_page, page, credentials, base_url, cart_cleanup):
        # This test is expected to fail - I think there is a bug :)
        login_page.login(credentials["username"], credentials["password"])
        
        assert inventory_page.is_loaded()
        inventory_page.add_item_by_name("Sauce Labs Backpack")
        assert inventory_page.cart_badge_count() == 1
        
        inventory_page.logout()
        
        login_page.login("visual_user", "secret_sauce")
        assert inventory_page.is_loaded()
        assert inventory_page.cart_badge_count() == 0, "Cart should be empty for a different user after logout and re-login"

    def test_locked_out_user_cannot_login(self, login_page):
        login_page.login("locked_out_user", "secret_sauce")
        error_message = login_page.error_text()
        assert "user has been locked out" in error_message, "Locked out user should see an error message upon login attempt"