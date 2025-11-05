import pytest

class TestUIElements:
    
    def test_cart_badge_visibility(self, logged_in_user, inventory_page):
        assert inventory_page.cart_badge_count() == 0
        
        inventory_page.add_item_by_name("Test.allTheThings() T-Shirt (Red)")
        assert inventory_page.cart_badge_count() == 1
        
        inventory_page.remove_item_by_name("Test.allTheThings() T-Shirt (Red)")
        assert inventory_page.cart_badge_count() == 0
    
    def test_menu_navigation(self, logged_in_user, inventory_page):
        inventory_page.open_burger_menu()
        
        assert inventory_page.is_logout_link_visible(), "Logout link should be visible when menu is open"
        
        inventory_page.close_burger_menu()
        
        assert inventory_page.is_logout_link_visible(), "Logout link should be visible when menu is closed"
        
        inventory_page.logout()
        assert not inventory_page.is_loaded(), "Logout link should not be visible when menu is closed"