from .base_page import BasePage

class CheckoutCompletePage(BasePage):
    COMPLETE_HEADER = ".complete-header"
    CHECKOUT_COMPLETE_CONTAINER = ".checkout_complete_container"
    BACK_TO_PRODUCTS_BUTTON = "[data-test='back-to-products']"
    THANK_YOU_TEXT = "Thank you for your order!"
    
    def is_thank_you(self):
        return self.page.locator(self.COMPLETE_HEADER).filter(has_text=self.THANK_YOU_TEXT).is_visible()
    
    def is_loaded(self):
        return self.page.locator(self.CHECKOUT_COMPLETE_CONTAINER).is_visible() or self.is_thank_you()
    
    def back_to_inventory(self):
        self.page.locator(self.BACK_TO_PRODUCTS_BUTTON).click()