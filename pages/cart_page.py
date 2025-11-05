from .base_page import BasePage

class CartPage(BasePage):
    CART_LIST = ".cart_list"
    CART_CONTENTS_CONTAINER = ".cart_contents_container"
    CART_ITEM = ".cart_item"
    REMOVE_BUTTON = "button:has-text('Remove')"
    CHECKOUT_BUTTON = "[data-test='checkout']"
    CONTINUE_SHOPPING_BUTTON = "[data-test='continue-shopping']"
    
    def is_loaded(self):
        return self.page.locator(self.CART_LIST).is_visible() or self.page.locator(self.CART_CONTENTS_CONTAINER).is_visible()
    
    def has_item(self, name):
        return self.page.locator(self.CART_ITEM).filter(has_text=name).is_visible()

    def remove_item(self, name):
        self.page.locator(self.CART_ITEM).filter(has_text=name).locator(self.REMOVE_BUTTON).click()

    def click_checkout(self):
        self.page.locator(self.CHECKOUT_BUTTON).click()
    
    def continue_shopping(self):
        self.page.locator(self.CONTINUE_SHOPPING_BUTTON).click()