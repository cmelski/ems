from qa.pages.base import BasePage
from qa.utilities.logging_utils import logger_utility
from playwright.sync_api import Page, expect


class AssetPage:

    def __init__(self, page):
        self.page = page
        self.base_actions = BasePage(page)
        self.asset_table = page.locator('#section-assets table')
        self.add_asset_button = page.get_by_role("button", name="Add Asset")
        self.asset_name = page.locator('#asset-name')
        self.asset_type = page.locator('#asset-type')
        self.asset_value = page.locator('#asset-value')
        self.asset_beneficiary = page.locator('#asset-beneficiary')
        self.asset_location = page.locator('#asset-location')
        self.asset_status = page.locator('#asset-status')
        self.error_container = page.locator('#toasts')

    def find_asset_table_cell_value(self, row, column_text):
        column_index = self.base_actions.find_table_header_index(self.asset_table, column_text)
        cell_value = self.find_table_cell_value(column_index, row)
        return cell_value

    def find_asset_row_to_action(self, expense_details):
        return self.base_actions.find_row_to_action(self.asset_table, expense_details, 'asset')

    def cycle_asset_status(self, row):
        self.base_actions.cycle_status(row, 'asset')

    def find_table_cells_for_specific_column(self, column_text) -> list:
        column_index = self.base_actions.find_table_header_index(self.asset_table, column_text)

        return self.base_actions.find_table_cells_for_specific_column(self.asset_table,
                                                                      column_index, 'assets')

    def find_table_cell_value(self, index: int, row) -> str:
        return self.base_actions.find_table_cell_value(index, row)

    def click_add_asset(self, values: list):
        self.asset_name.fill(values[0])
        self.asset_type.select_option(values[1])
        self.asset_value.fill(values[2])
        self.asset_beneficiary.fill(values[3])
        self.asset_location.fill(values[4])
        self.asset_status.select_option(values[5])
        self.add_asset_button.click()

    def verify_new_asset_in_asset_table(self, values):
        return self.base_actions.verify_new_item_in_table(self.asset_table, values, 'asset')

    def verify_asset_not_in_asset_table(self, asset_details):
        return self.base_actions.verify_item_not_in_table(asset_details, self.asset_table, 'asset')

    def fill_asset_form_invalid(self):
        self.add_asset_button.click()

    def delete_asset(self, row):
        row.get_by_title('Delete').click()
        logger_utility().info('Asset deleted.')
