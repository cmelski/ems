from qa.pages.base import BasePage
from qa.utilities.logging_utils import logger_utility
from playwright.sync_api import Page, expect


class DashboardPage:

    def __init__(self, page):
        self.page = page
        self.base_actions = BasePage(page)
        self.page_heading_1 = page.locator('h1')
        self.page_title = page.locator('#section-title')
        self.open_tasks = page.locator('#stat-tasks')
        self.sidebar_nav = page.locator('.sidebar-nav div')
        self.activity_table = page.locator('#section-dashboard table')
        self.empty_activity_log = self.activity_table.locator('.empty-state')

    def click_sidebar_menu(self, entity):
        self.sidebar_nav.filter(has_text=entity).click()

    def find_activity_log(self, item_details: tuple, activity_text, entity_text):
        item_id = item_details[0]
        logger_utility().info(f'{entity_text} activity logs to find: {item_details}')
        table_rows = self.activity_table.locator('tbody')
        rows_to_find = table_rows.locator(f'tr[data-activity-id="{item_id}"]').filter(has_text=activity_text)
        expect(rows_to_find).to_have_count(1)
        logger_utility().info(f'{entity_text}: {item_details} found in Recent Activity table with note "{activity_text}".')
        return True

    def count_open_tasks_activity_table(self):
        header_index = self.base_actions.find_table_header_index(self.activity_table,
                                                                 header_text='STATUS')
        rows = self.base_actions.find_table_cells_for_specific_column(self.activity_table,header_index, 'tasks')
        count_open = 0
        for row in rows:
            if row == 'PENDING' or row == 'IN-PROGRESS':
                count_open += 1
        return count_open




