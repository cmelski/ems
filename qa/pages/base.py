from qa.utilities.logging_utils import logger_utility
from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page):
        self.page = page

    def find_table_header_index(self, table_locator, header_text: str) -> int:
        headers = table_locator.locator("thead th")
        header_texts = headers.all_inner_texts()

        if header_text not in header_texts:
            raise AssertionError(
                f"Table header '{header_text}' not found. "
                f"Headers present: {header_texts}"
            )

        return header_texts.index(header_text)

    def find_table_cells_for_specific_column(self, table_locator, index: int, entity) -> list:
        cell_values = []
        empty_row = table_locator.locator('tbody tr.empty-state')
        expect(empty_row).to_have_count(0, timeout=5000)
        table_rows = table_locator.locator('tbody tr')
        table_rows_count = table_rows.count()
        for i in range(table_rows_count):
            row_cells = table_rows.nth(i).locator('td')
            cell = row_cells.nth(index).inner_text().strip()
            cell_values.append(cell)
        logger_utility().info(f'cell values: {cell_values}')
        return cell_values

    def find_table_cell_value(self, index: int, row):
        cells = row.locator('td')
        cell = cells.nth(index).inner_text()
        return cell

    def find_row_to_action(self, table_locator, item_details: tuple, entity_text: str):
        item_id = item_details[0]
        logger_utility().info(f'{entity_text} to find: {item_details}')
        table_rows = table_locator.locator('tbody')
        row_to_action = table_rows.locator(f'tr[data-{entity_text}-id="{item_id}"]')
        expect(row_to_action).to_have_count(1, timeout=5000)
        logger_utility().info(f'{entity_text}: {item_details} found.')
        return row_to_action

    def verify_new_item_in_table(self, table_locator, values, entity_text: str):
        table_rows = table_locator.locator('tbody tr')
        new_row = table_rows.filter(has_text=values[0])
        expect(new_row).to_be_visible()
        table_rows_count = table_rows.count()
        values_formatted = [item.lower() if isinstance(item, str) else item for item in values]
        logger_utility().info(f'new {entity_text} values: {values_formatted}')
        for i in range(table_rows_count):
            row_cells = table_rows.nth(i).locator('td').all_inner_texts()
            row_cells_formatted = [item.lower() if isinstance(item, str) else item for item in row_cells]
            logger_utility().info(f'{entity_text} row values: {row_cells_formatted}')
            if all(item in row_cells_formatted for item in values_formatted):
                logger_utility().info(f'New {entity_text}: {values} found in UI {entity_text} table')
                item_id = int(table_rows.nth(i).get_attribute(f'data-{entity_text}-id'))
                if entity_text == 'note':
                    item_description = values[1]
                else:
                    item_description = values[0]
                return item_id, item_description

        return 0

    def verify_item_not_in_table(self, item_details, table_locator, entity_text):
        item_id = item_details[0]
        logger_utility().info(f'{entity_text} details: {item_details}')
        table_rows = table_locator.locator('tbody')
        row =table_rows.locator(f'tr[data-{entity_text}-id="{item_id}"]')
        # check count = 0 is better than checking not to be visible to ensure the row
        # isn't just hidden
        expect(row).to_have_count(0)
        return True

    def delete_item(self, row, entity_text):
        row.get_by_title('Delete').click()
        logger_utility().info(f'{entity_text} deleted.')

    def cycle_status(self, row, entity):

        if entity == 'task':
            row.get_by_title("Cycle status").click()
        elif entity == 'bill' or entity == 'expense':
            row.get_by_title("Toggle paid").click()
        elif entity == 'asset':
            row.get_by_title('Cycle asset status').click()

    def click(self, selector, *args):
        if args:
            self.page.locator(selector).filter(has_text=args[0]).click()
            logger_utility().info(f'{selector} clicked with value: {args[0]}')
        else:
            self.page.locator(selector).click()
            logger_utility().info(f'{selector} clicked')

    def fill(self, selector, value):
        self.page.locator(selector).fill(value)
        logger_utility().info(f'{selector} filled with value: {value}')

    def fill_fields(self, fields: list[dict]) -> None:
        for index, field in enumerate(fields, start=1):
            selector = field["selector"]
            value = field["value"]
            field_type = field.get("type", "text")

            logger_utility().info(
                f"Step {index}: Filling {selector} with value: {value}"
            )

            if field_type in ("text", "date"):
                self.page.fill(selector, value)

            elif field_type == "select":
                self.page.select_option(selector, value)

            else:
                raise ValueError(f"Unsupported field type: {field_type}")


    def get_table_row_cells(self, row):

        row_cells = row.locator('td').all_inner_texts()
        return row_cells




