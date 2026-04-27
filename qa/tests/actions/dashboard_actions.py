from qa.tests.pages.dashboard import DashboardPage
from qa.tests.pages.base import BasePage


class DashboardActions:
    def __init__(self, page):
        self.page = page
        self.dashboard_page = DashboardPage(page)
        self.base_page = BasePage(page)

    def navigate_to_panel(self, panel):
        self.dashboard_page.click_sidebar_menu(panel)
