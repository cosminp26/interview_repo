from .base_page import BasePage

class CheckoutPage(BasePage):
    FIRST_NAME_INPUT = "[data-test='firstName']"
    LAST_NAME_INPUT = "[data-test='lastName']"
    POSTAL_CODE_INPUT = "[data-test='postalCode']"
    CONTINUE_BUTTON = "[data-test='continue']"
    CANCEL_BUTTON = "[data-test='cancel']"
    FINISH_BUTTON = "[data-test='finish']"
    ERROR_MESSAGE = "[data-test='error']"
    SUBTOTAL_LABEL = ".summary_subtotal_label"
    TAX_LABEL = ".summary_tax_label"
    TOTAL_LABEL = ".summary_total_label"
    
    def fill_info_and_continue(self, first, last, zipc):
        self.page.locator(self.FIRST_NAME_INPUT).fill(first)
        self.page.locator(self.LAST_NAME_INPUT).fill(last)
        self.page.locator(self.POSTAL_CODE_INPUT).fill(zipc)
        self.page.locator(self.CONTINUE_BUTTON).click()

    def subtotal_text(self):
        return self.page.locator(self.SUBTOTAL_LABEL).inner_text()

    def tax_text(self):
        return self.page.locator(self.TAX_LABEL).inner_text()

    def total_text(self):
        return self.page.locator(self.TOTAL_LABEL).inner_text()

    def click_finish(self):
        self.page.locator(self.FINISH_BUTTON).click()

    def error_text(self):
        return self.page.locator(self.ERROR_MESSAGE).inner_text()

    def cancel_checkout(self):
        self.page.locator(self.CANCEL_BUTTON).click()