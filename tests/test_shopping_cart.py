import pytest

class TestShoppingCart:
    """Test suite for shopping cart functionality."""
    
    @pytest.fixture(autouse=True)
    def setup(self, logged_in_user):
        pass
    
    def test_add_single_item_to_cart(self, inventory_page, cart_page, cart_cleanup):
        items_name = ["Sauce Labs Backpack"]
        
        inventory_page.add_item_by_name(items_name[0])
        assert inventory_page.cart_badge_count() == 1
        
        inventory_page.open_cart()
        assert cart_page.has_item(items_name[0])

    def test_add_multiple_items_to_cart(self, inventory_page, cart_page, cart_cleanup):
        items = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
        
        for item in items:
            inventory_page.add_item_by_name(item)
        
        assert inventory_page.cart_badge_count() == len(items)
        
        inventory_page.open_cart()
        for item in items:
            assert cart_page.has_item(item)
    
    def test_remove_item_from_cart(self, inventory_page, cart_page, cart_cleanup):
        """Verify removing items from cart updates badge and contents."""
        items = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
        
        for item in items:
            inventory_page.add_item_by_name(item)
        assert inventory_page.cart_badge_count() == 2
        
        inventory_page.open_cart()
        cart_page.remove_item("Sauce Labs Bike Light")
        
        inventory_page.open_cart()
        assert inventory_page.cart_badge_count() == 1
        assert cart_page.has_item("Sauce Labs Backpack")
        assert not cart_page.has_item("Sauce Labs Bike Light")
    
    def test_remove_item_from_inventory_page(self, inventory_page):
        item_name = "Sauce Labs Backpack"
        
        inventory_page.add_item_by_name(item_name)
        assert inventory_page.cart_badge_count() == 1
        
        inventory_page.remove_item_by_name(item_name)
        assert inventory_page.cart_badge_count() == 0