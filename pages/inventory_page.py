from .base_page import BasePage

class InventoryPage(BasePage):
    INVENTORY_LIST = ".inventory_list"
    INVENTORY_ITEM = ".inventory_item"
    ADD_TO_CART_BUTTON = "button:has-text('Add to cart')"
    REMOVE_BUTTON = "button:has-text('Remove')"
    SHOPPING_CART_LINK = ".shopping_cart_link"
    SHOPPING_CART_BADGE = ".shopping_cart_badge"
    BURGER_MENU_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"
    BURGER_MENU_CLOSE = "#react-burger-cross-btn"
    
    def is_loaded(self):
        return self.page.locator(self.INVENTORY_LIST).is_visible()

    def add_item_by_name(self, name):
        self.page.locator(self.INVENTORY_ITEM).filter(has_text=name).locator(self.ADD_TO_CART_BUTTON).first.click()

    def remove_item_by_name(self, name):
        self.page.locator(self.INVENTORY_ITEM).filter(has_text=name).locator(self.REMOVE_BUTTON).first.click()

    def open_cart(self):
        self.page.locator(self.SHOPPING_CART_LINK).click()

    def cart_badge_count(self):
        locator = self.page.locator(self.SHOPPING_CART_BADGE)
        return int(locator.inner_text()) if locator.count() > 0 else 0

    def clear_all_cart_items(self):
        remove_buttons = self.page.locator(self.REMOVE_BUTTON)
        count = remove_buttons.count()
        for i in range(count):
            if remove_buttons.first.is_visible():
                remove_buttons.first.click()
    
    def open_burger_menu(self):
        self.page.locator(self.BURGER_MENU_BUTTON).click()
    
    def close_burger_menu(self):
        self.page.locator(self.BURGER_MENU_CLOSE).click()
    
    def logout(self):
        self.open_burger_menu()
        self.page.locator(self.LOGOUT_LINK).click()
    
    def is_logout_link_visible(self):
        return self.page.locator(self.LOGOUT_LINK).is_visible()