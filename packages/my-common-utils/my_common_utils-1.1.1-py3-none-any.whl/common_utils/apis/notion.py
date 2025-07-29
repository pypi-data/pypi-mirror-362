from notion_client import Client
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

from common_utils.config import secret, load_config_yaml
from common_utils.logger import create_logger


class NotionClient:
    """Wrapper for the Notion API. Loads data from a database.

    Attributes:
        api: NotionClient object
        projects_db: List of all projects from the projects database (config)
        project_names: dict, project ids as keys, project names as values
    """

    def __init__(self, notion_secret=None):
        if not notion_secret:
            notion_secret = secret("NOTION_SECRET")
        assert notion_secret, "Could not load NOTION_SECRET from variable or .env"
        self.log = create_logger("Notion")
        self.api = Client(auth=secret("NOTION_SECRET"))

    def _get_title(self, page, property_name) -> str:
        return page["properties"][property_name]["title"][0]["plain_text"]

    def _get_emoji(self, page) -> str:
        return page["icon"]["emoji"]

    def _get_plaintext(self, page, property_name) -> str:
        plain_texts = [item["plain_text"] for item in page["properties"][property_name]["rich_text"]]
        return "".join(plain_texts)

    def _get_number(self, page, property_name) -> float:
        return page["properties"][property_name]["number"]

    def _get_select(self, page, property_name) -> object:
        select = page["properties"][property_name]["select"]
        return select

    def _get_select_name(self, page, property_name) -> str:
        select = page["properties"][property_name]["select"]["name"]
        return select

    def _get_multi_select(self, page, property_name) -> list[object]:
        multiselect = page["properties"][property_name]["multi_select"]
        return multiselect

    def _get_multi_select_names(self, page, property_name) -> list[str]:
        multiselect = page["properties"][property_name]["multi_select"]
        return [item["name"] for item in multiselect]

    def _get_date(self, task, property_name) -> tuple[str, str]:
        """Returns the start and end dates as strings of a task, empty if a date is not set"""
        date_property = task["properties"][property_name]["date"]
        start_date, end_date = None, None
        if date_property is not None and date_property["start"] is not None:
            start_date = date_property["start"]
        if date_property is not None and date_property["end"] is not None:
            end_date = date_property["end"]
        return start_date, end_date

    def get_properties(self, page, property_mapping) -> dict:
        """ Returns all properties of a page using the property_mapping """
        properties = {"id": page["id"]}
        for name, property_type in property_mapping.items():
            try:
                match property_type:
                    case "title": properties[name] = self._get_title(page, name)
                    case "emoji": properties[name] = self._get_emoji(page)
                    case "content_simple": properties[name] = self.get_page_content(page["id"], "simple")
                    case "content_markdown": properties[name] = self.get_page_content(page["id"], "markdown")
                    case "text": properties[name] = self._get_plaintext(page, name)
                    case "number": properties[name] = self._get_number(page, name)
                    case "select": properties[name] = self._get_select(page, name)
                    case "select_name": properties[name] = self._get_select_name(page, name)
                    case "multi_select": properties[name] = self._get_multi_select(page, name)
                    case "multi_select_names": properties[name] = self._get_multi_select_names(page, name)
                    case "date":
                        start_date, end_date = self._get_date(page, name)
                        properties[name] = start_date
                        properties[name + "_end"] = end_date
                    case _: properties[name] = page["properties"][property_type]
            except Exception as e:
                properties[name] = None
        return properties

    def get_database(self, database_id: str, properties_mapping: dict[str, str], filter={}, sort={}) -> pd.DataFrame:
        """Returns dataframe with data from a specific database.

        Args:
            database_id: Notion ID of the database
            properties_mapping: Mapping of database properties to their types.
                Example: {"Name": "title", "Status": "select"}
                Types: title, emoji, text, number, select, select_name,
                       multi_select, multi_select_names, date
            filter: Filter for the database query
            sort: Sorting for the database query

        Returns:
            pd.DataFrame: Dataframe with all tasks and their properties
        """

        all_entries = pd.DataFrame()
        query_parameter = {}
        if filter:
            query_parameter["filter"] = filter
        if sort:
            query_parameter["sorts"] = sort
        query = self.api.databases.query(database_id, **query_parameter)["results"]
        for page in query:
            properties = self.get_properties(page, properties_mapping)
            all_entries = all_entries._append(properties, ignore_index=True)
        return all_entries

    def get_multiple_databases(self, db_config_dict: dict[dict]) -> dict[str, pd.DataFrame]:
        with ThreadPoolExecutor(max_workers=2) as executor:
            thread_list = {}
            results = {}
            for name, db_config in db_config_dict.items():
                thread = executor.submit(self.get_database, **db_config)
                thread_list[name] = thread
            for name, thread in thread_list.items():
                results[name] = thread.result()
        return results

    def _get_text_part_plaintext(self, text_part: dict) -> str:
        if 'text' in text_part:
            return text_part['text']['content']
        elif 'mention' in text_part:
            if 'link_mention' in text_part['mention']:
                return text_part['mention']['link_mention']['href']
        else:
            return ""

    def get_page_content(self, page_id: str, parse_mode: str) -> str:
        assert parse_mode in ['markdown', 'simple'], "parse_mode must be 'markdown' or 'simple'"
        blocks = self.api.blocks.children.list(block_id=page_id)
        numbered_list_count = 1
        entire_text = ""
        for block in blocks['results']:
            try:
                if numbered_list_count > 1 and block['type'] != 'numbered_list_item':
                    numbered_list_count = 1
                match block['type']:
                    case 'paragraph':
                        text = ''.join([self._get_text_part_plaintext(text_part) for text_part in
                                        block['paragraph']['rich_text']])
                    case 'heading_1' | 'heading_2' | 'heading_3':
                        text = ''.join([text_part['text']['content'] for text_part in
                                        block[block['type']]['rich_text']])
                        heading_level = int(block['type'].split('_')[1])
                        text = f"{'#' * heading_level} {text}" if parse_mode == 'markdown' else f"*{text}*"
                    case 'bookmark':
                        url = block['bookmark']['url']
                        text = f"{url}"
                    case 'bulleted_list_item':
                        text = ''.join([self._get_text_part_plaintext(text_part) for text_part in
                                        block['bulleted_list_item']['rich_text']])
                        text = f"- {text}" if parse_mode == 'markdown' else f"• {text}"
                    case 'numbered_list_item':
                        text = ''.join([self._get_text_part_plaintext(text_part) for text_part in
                                        block['numbered_list_item']['rich_text']])
                        text = f"{numbered_list_count}. {text}"
                        numbered_list_count += 1
                    case 'quote':
                        text = ''.join(
                            [self._get_text_part_plaintext(text_part) for text_part in
                             block['quote']['rich_text']])
                        text = f"> {text}" if parse_mode == 'markdown' else f"\"**{text}**\""
                    case 'code':
                        text = block['code']['text']
                        text = f"```{text}```"
                    case 'to_do':
                        text = block['to_do']['text']
                        text = f"[ ] {text}"
                    case 'toggle':
                        text = block['toggle']['text']
                    case 'child_page':
                        text = f"_{block['child_page']['title']}_"
                    case 'divider':
                        text = "---" if parse_mode == 'markdown' else ""
                    case 'callout':
                        text = block['callout']['text']
                        text = f"**{text}**"
                    case _:
                        text = ""
                entire_text += f"{text}\n"
            except Exception as e:
                print(e)
        if parse_mode == 'simple':
            entire_text = entire_text.replace("https://", "")
        return entire_text

    def add_property(self, prop_type, value):
        match prop_type:
            case 'title': return {"title": [{"text": {"content": value}}]}
            case 'number': return {"number": value}
            case 'text': return {"rich_text": [{"text": {"content": value}}]}
            case 'date': return {"date": {"start": value}}
            case 'select': return {"select": {"name": value}}
            case 'multi_select': return {"multi_select": [{"name": item} for item in value]}
            case 'checkbox': return {"checkbox": value}
            case 'url': return {"url": value}
            case 'email': return {"email": value}
            case 'phone_number': return {"phone_number": value}
            case 'formula': return {"formula": {"expression": value}}
            case 'relation': return {"relation": value}
            case 'rollup': return {"rollup": {"relation": value}}
            case _: raise ValueError(f"Unsupported property type: {prop_type}")

    def create_db_entry(self, database_id, properties=None, data=None, properties_mapping=None):
        """Creates a new entry in a database.

        Currently only supports title, text, number, select, multi_select, date, url, email,
        phone_number, formula, relation, rollup, checkbox

        Args:
            database_id: Notion ID of the database
            properties: Dict with properties and their values
                Example: {"Name": {"type": "title", "value": "My task"},
                          "Status": {"type": "select", "value": "In Progress"}}
            """
        assert properties or (data and properties_mapping), "Either properties or data and properties_mapping must be set"
        if data and properties_mapping:
            properties = self._convert_data_to_notion_properties(data, properties_mapping)
        notion_properties = {}
        for key, prop in properties.items():
            notion_properties[key] = self.add_property(prop['type'], prop['value'])
        try:
            self.api.pages.create(parent={"database_id": database_id}, properties=notion_properties)
        except Exception as e:
            print("An error occurred:", e)

    @staticmethod
    def _convert_data_to_notion_properties(data: dict | pd.Series, properties_mapping: dict) -> dict:
        # TODO: integrate into my-common-utils, automatically detect type from notion database schema
        notion_properties = {}
        for key, value in data.items():
            try:
                entry_type = properties_mapping[key]
                try:
                    value = float(value)
                except ValueError:
                    pass
                notion_properties[key] = {'type': entry_type, 'value': value}
            except KeyError:
                pass
        return notion_properties


if __name__ == "__main__":
    from dotenv import load_dotenv
    from common_utils.config import load_config_yaml
    load_dotenv()
    notion = NotionClient()
    config = load_config_yaml("config.yml")
    db_config_dict = config["NOTION_DATABASES"]
    fitness_creation_dict = db_config_dict["fitness"]
    fitness_df = notion.create_db_entry(**fitness_creation_dict)




    print()
