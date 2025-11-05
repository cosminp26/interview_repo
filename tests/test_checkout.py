import pytest
import re

def extract_price(price_text):
    return float(re.search(r"[-+]?[0-9]*\.?[0-9]+", price_text).group())

class TestCheckoutProcess:
    
    @pytest.fixture(autouse=True)
    def setup(self, logged_in_user):
        # setup fixture; only for clarity because is not used directly
        pass
    
    def test_checkout_single_item_success(self, inventory_page, cart_page, checkout_page, complete_page, full_checkout_cleanup):
        inventory_page.add_item_by_name("Sauce Labs Backpack")
        inventory_page.open_cart()
        cart_page.click_checkout()
        
        checkout_page.fill_info_and_continue("John", "Doe", "12345")
        
        subtotal = extract_price(checkout_page.subtotal_text())
        tax = extract_price(checkout_page.tax_text())
        total = extract_price(checkout_page.total_text())
        
        assert round(subtotal + tax, 2) == round(total, 2), "Total should equal subtotal plus tax"
        
        checkout_page.click_finish()
        assert complete_page.is_thank_you(), "Thank you message should appear after successful order"
    
    def test_checkout_multiple_items_success(self, inventory_page, cart_page, checkout_page, complete_page, full_checkout_cleanup):
        items = ["Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
        
        for item in items:
            inventory_page.add_item_by_name(item)
        
        inventory_page.open_cart()
        
        for item in items:
            assert cart_page.has_item(item)
        
        cart_page.click_checkout()
        
        checkout_page.fill_info_and_continue("Jane", "Smith", "90210")
        
        subtotal = extract_price(checkout_page.subtotal_text())
        tax = extract_price(checkout_page.tax_text())
        total = extract_price(checkout_page.total_text())
        
        assert round(subtotal + tax, 2) == round(total, 2), "Total should equal subtotal plus tax"
        
        checkout_page.click_finish()
        assert complete_page.is_thank_you(), "Thank you message should appear after successful order"
    
    def test_checkout_validation_empty_fields(self, inventory_page, cart_page, checkout_page, cart_cleanup):
        inventory_page.add_item_by_name("Sauce Labs Fleece Jacket")
        inventory_page.open_cart()
        cart_page.click_checkout()
        
        checkout_page.fill_info_and_continue("", "", "")
        
        error_message = checkout_page.error_text()
        assert "Error" in error_message, "Error message should appear for empty required fields"
        checkout_page.cancel_checkout()

    @pytest.mark.parametrize("first_name,last_name,postal_code", [
        ("", "Doe", "12345"),  # Missing first name
        ("John", "", "12345"),  # Missing last name  
        ("John", "Doe", ""),   # Missing postal code
    ])
    def test_checkout_validation_missing_individual_fields(self, first_name, last_name, postal_code, inventory_page, cart_page, checkout_page, cart_cleanup):
        inventory_page.add_item_by_name("Sauce Labs Backpack")
        inventory_page.open_cart()
        cart_page.click_checkout()
        
        checkout_page.fill_info_and_continue(first_name, last_name, postal_code)
        
        error_message = checkout_page.error_text()
        assert "Error" in error_message, f"Error should appear for missing field(s)"

        checkout_page.cancel_checkout()

