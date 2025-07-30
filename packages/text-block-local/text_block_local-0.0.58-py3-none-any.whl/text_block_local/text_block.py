import json
import re
from datetime import datetime
from functools import lru_cache

from database_mysql_local.generic_crud import GenericCRUD
from database_mysql_local.point import Point
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.MetaLogger import MetaLogger
from person_local.persons_local import Person
from person_local.persons_local import PersonsLocal
from profile_local.profiles_local import ProfilesLocal
from user_context_remote.user_context import UserContext
from fields_local.fields_local import FieldsLocal

# TODO Identify duplicate text block, maybe using fingerprint, link them and logically delete similar to what we do with duplicate entities (group, event)

# TODO: move to constants
PERSON_TABLE = "person_table"
# TODO Use const enum from gender-local package
DEFAULT_GENDER_ID = 8  # = Prefer not to respond
MAX_ERRORS = 5
TEXT_BLOCK_COMPONENT_ID = 143
TEXT_BLOCK_COMPONENT_NAME = "text_block_local_python_package"
DEVELOPER_EMAIL = "akiva.s@circ.zone"
object1 = {
    'component_id': TEXT_BLOCK_COMPONENT_ID,
    'component_name': TEXT_BLOCK_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
user_context = UserContext()

# TODO: Group Name which starts with YYMMDD means they person attended event created by the user in this date, name and title of the event is YYMMDD.

class TextBlocks(GenericCRUD, metaclass=MetaLogger, object=object1):
    def __init__(self, text_block_id: int = None, is_test_data: bool = False):
        GenericCRUD.__init__(self, default_schema_name="text_block",
                             default_table_name="text_block_table",
                             default_view_table_name="text_block_view",
                             default_column_name="text_block_id",
                             is_test_data=is_test_data)
        self.text_block_id = text_block_id  # TODO: I don't think we should send this in the constructor
        self.currect_profile_id = None
        self.profile_id = None
        self.errors_count = 0
        self.profiles_local = ProfilesLocal()
        self.persons_local = PersonsLocal(is_test_data=is_test_data)
        self.fields_local = FieldsLocal(is_test_data=is_test_data)

    def process_text_blocks_updated_since_date(self, since_date: datetime) -> None:
        text_block_ids = self.select_multi_value_by_where(
            select_clause_value="text_block_type_id", where="updated_timestamp >= %s", params=(since_date,))
        print(text_block_ids)
        for text_block_id in text_block_ids:
            self.process_text_block_by_id(text_block_id)

    def process_text_block_by_id(self, text_block_id: int) -> None:
        """
        1. Retrieves the text and other details of the text block.
        2. Reformat the text if needed.
        3. Identifies and updates the text block type.
        4. Extract fields from the text based on the block type's regular expressions.
        5. Updates the text block with the extracted fields in JSON format.
        """

        self.text_block_id = text_block_id
        text, text_block_type_id, profile_id = self.get_text_block_details(text_block_id)

        if text_block_type_id is None:
            text_block_type_id = self.identify_and_update_text_block_type(text_block_id, text)

        fields_dict = self.extract_fields_from_text(text, text_block_type_id)
        self.update_text_block_fields(text_block_id, fields_dict)

        self.errors_count = 0

    @lru_cache
    def get_block_fields(self, text_block_type_id: int) -> list[dict]:
        """Retrieves regular expressions and field IDs based on the provided `text_block_type_id`."""
        # One field id can have multiple regexes
        block_fields = self.select_multi_dict_by_column_and_value(
            schema_name="field_text_block_type", view_table_name="field_text_block_type_view",
            select_clause_value="regex, field_id, index_in_regex, comment",
            column_name="text_block_type_id", column_value=text_block_type_id)
        return block_fields

    @lru_cache
    def get_regex_per_block_type_id(self, potential_regex_tuple: tuple = None) -> dict[int, str]:
        """Retrieves block type IDs and regular expressions from the database."""
        # TODO: we also have regexes in block_type_field_table, should we return those as well?
        if potential_regex_tuple:
            where = ("regex IN (" + ",".join(["%s"] * len(potential_regex_tuple)) + ")")
        else:
            where = None

        potential_block_type_ids = dict(self.select_multi_tuple_by_where(
            schema_name="text_block_type", view_table_name="text_block_type_regex_view",
            select_clause_value="text_block_type_id, regex", where=where, params=potential_regex_tuple))

        return potential_block_type_ids

    def get_block_types_dict(self) -> dict:
        """Retrieves block type IDs and names from the database."""
        block_types = dict(self.select_multi_tuple_by_where(
            schema_name="text_block_type", view_table_name="text_block_type_ml_view",
            select_clause_value="text_block_type_id, name"))

        return block_types

    def get_text_block_ids_types_dict(self) -> dict[int, tuple[int, str]]:
        """Retrieves text block IDs and types from the database."""
        select_clause_value = "text_block_id, text_block_type_id, text_without_empty_lines, text"
        result = self.select_multi_tuple_by_where(select_clause_value=select_clause_value)
        text_block_ids_types_dict = {}
        for text_block_id, type_id, text_without_empty_lines, text in result:
            if text_block_id in text_block_ids_types_dict:
                self.logger.warning(f"Duplicate text block ID: {text_block_id}")
            text_block_ids_types_dict[text_block_id] = (type_id, self.__clean_text(text_without_empty_lines, text))

        return text_block_ids_types_dict

    @staticmethod
    def __clean_text(text_without_empty_lines: str, text: str) -> str:
        cleaned_text = (text_without_empty_lines or text).replace("\n", " ")
        return cleaned_text

    @lru_cache
    def get_text_block_details(self, text_block_id: int) -> tuple:
        """Retrieves text and related details for a given text block ID."""

        query = "SELECT text_without_empty_lines, text, text_block_type_id, profile_id " \
        "FROM text_block.text_block_table " \
        "WHERE text_block_id=%s"
        self.cursor.execute(sql_statement=query, sql_parameters=(text_block_id,))
        result = self.cursor.fetchone()
        if not result:
            raise Exception(f"No text block found for ID: {text_block_id}")

        text, text_block_type_id, profile_id = self.__clean_text(result[0], result[1]), result[2], result[3]
        return text, text_block_type_id, profile_id

    @lru_cache
    def extract_fields_from_text(self, text: str, text_block_type_id: int) -> dict:
        """
        Extracts fields from the text based on the block type's regular expressions.
        text_block_profile_id is the profile_id of the profile which referred to in the specific text_block (not user_context.profile_id)
        """

        block_fields = self.get_block_fields(text_block_type_id)
        fields = self.fields_local.get_fields()
        fields_dict = {}

        for item_index, item in enumerate(block_fields):
            regex = item.get("regex")
            field_id = item.get("field_id")
            if not regex or not field_id:  # we have not defined those yet in the block_type_field_table
                continue
            try:
                re.compile(regex)
                matches = re.findall(regex,
                                     text)  # Example: ['linkedin.com/in/iangolding'], ['http://www.ravitlivni.com/']
            except re.error as exception:
                # We do not want to raise is such case, so we only send warning to fix the db.
                # TODO If it is a Metadata error in the database, we prefer the process to stop we fix it and continue from the same point
                self.logger.warning(f"Invalid regex: {regex}", object={
                    "exception": exception, "item": item})
                continue

            if not matches:
                continue
            field = fields[field_id]  # Example: 'Website'
            # Extend fields_dict if not exists
            if field not in fields_dict:
                fields_dict[field] = []
            for match in matches:
                if match not in fields_dict[field]:
                    fields_dict[field].append(match)

            # TODO: why do we need this loop? Can we proccess several fields at a time?
            #   (for example all person related fields should be processed together)
            for index, match in enumerate(matches):
                dict_to_organize = {field: matches}
                organized_fields_dict = self.__organize_fields_dict(dict_to_organize, text_block_type_id, index)
                self.process_and_update_field(
                    fields_dict=organized_fields_dict, field_id=field_id, index=item_index)

        return fields_dict

    # TODO Can we use table_definition_table generated using Sql2Code here because of performance?  # noqa: E501
    # TODO Can we generate SQL on logger_table to see how often we call this function? - We should call it one time in the lifetime of each process  # noqa: E501
    def process_and_update_field(self, fields_dict: dict, field_id: int, index: int) -> int | None:
        """Processes and updates the field."""
        # TODO: rewrite this method and break it down into smaller methods
        # Old version: https://github.com/circles-zone/text-block-local-python-package/blob/613e6cdbf5c5f54b40c37e4b479e0d48d820a03b/circles_text_block_local/text_block_microservice.py#L181

        select_clause_value = ("table_id, database_field_name, database_sub_field_name, "
                               "database_sub_field_value, processing_id, processing_database_field_name")
        field_info = self.fields_local.select_one_tuple_by_column_and_value(
            select_clause_value=select_clause_value,
            column_name="field_id", column_value=field_id)
        self.logger.info(object={"field_info": field_info})
        table_id, database_field_name, database_sub_field_name, database_sub_field_value, processing_id, processing_database_field_name = field_info
        field_name = self.fields_local.get_field_name_by_field_id(field_id)
        field_column_value = fields_dict.get(field_name)
        if isinstance(field_column_value, tuple):
            field_column_value = field_column_value[index]
        profile_id = self.__get_profile_id(fields_dict)

        # TODO: process fields with _original
        # processed_value = self.process_field(processing_id, match)

        # This is the same as selecting profile_mapping_table_id and using it to get the mapping table:
        # cursor.execute("SELECT `schema`, table_name, profile_mapping_table_id FROM database.table_definition_table WHERE id = %s", (table_id,))
        # (schema, table_name, profile_mapping_table_id) = (result[0], result[1], result[2])
        #
        # cursor.execute("SELECT `schema`, table_name FROM database.table_definition_table WHERE id = %s", (profile_mapping_table_id,))
        # (profile_mapping_table_schema, profile_mapping_table_name) = (result[0], result[1])

        query = """
            SELECT D1.`schema`                   AS `schema`,
                   D1.`table_name`               AS `table_name`,
                   D1.`view_name`                AS `view`,
                   D1.`profile_mapping_table_id` AS `profile_mapping_table_id`,
                   D2.`schema`                   AS `profile_mapping_table_schema`,
                   D2.`table_name`               AS `profile_mapping_table_name`,
                   D2.`view_name`                AS `profile_mapping_view_name`
            FROM `database`.`table_definition_table` AS D1
                     JOIN `database`.`table_definition_table` AS D2
                          ON D1.profile_mapping_table_id = D2.table_definition_id
            WHERE D1.table_definition_id = %s
        """
        self.cursor.execute(query, (table_id,))
        record = self.cursor.fetchone()
        if not record:
            self.logger.error("No table definition found for table_id", object={"table_id": table_id})
            return
        columns = ("schema, table_name, view_name, profile_mapping_table_id, profile_mapping_table_schema, "
                   "profile_mapping_table_name, profile_mapping_view_name")
        (schema, table_name, view_name, profile_mapping_table_id, profile_mapping_table_schema,
         profile_mapping_table_name, profile_mapping_view_name) = record
        dict_record = self.convert_to_dict(record, columns)
        # TODO In which cases do we use .copy()? - Let's make sure it is documented in the logger python local package README.md
        self.logger.info(object=dict_record.copy())
        if not schema or not profile_mapping_table_schema:
            self.logger.error("No schema found", object={
                "table_id": table_id, "schema": schema, "profile_mapping_table_schema": profile_mapping_table_schema})
            return
        if not all((table_name, view_name, profile_mapping_table_name, profile_mapping_view_name)):
            self.logger.warning("table_name or view_name missing, so I will guess the value",
                                object=dict_record.copy())
            table_name = table_name or schema + "_table"
            view_name = view_name or table_name.replace("_table", "_view")
            profile_mapping_table_name = profile_mapping_table_name or profile_mapping_table_schema + "_table"
            profile_mapping_view_name = profile_mapping_view_name or profile_mapping_table_name.replace(
                "_table", "_view")
        # TODO It is not always schema+"_id", I think it is better entiity_name + "_id", while entity_name is table_name - "_table
        select_clause_value = schema + "_id"
        if profile_id and profile_mapping_table_id:
            # Retrieve mapping ID for the profile
            if table_name == PERSON_TABLE:
                entity_id = self.select_one_value_by_column_and_value(
                    schema_name="profile", view_table_name="profile_view",
                    select_clause_value="main_person_id",
                    column_name="profile_id", column_value=profile_id)
            else:
                entity_id = self.select_one_value_by_column_and_value(
                    schema_name=schema, view_table_name=view_name, select_clause_value=select_clause_value,
                    column_name=database_field_name, column_value=field_column_value)
            if entity_id is None:
                # insert information from extracted fields
                if table_name == PERSON_TABLE:
                    entity_id = self.__add_person_to_db(fields_dict=fields_dict, index=index)
                else:
                    entity_id = self.insert_information_from_extracted_fields(
                        schema, table_name, database_field_name, field_column_value,
                        database_sub_field_name, database_sub_field_value)

            profile_mapping_id_name = profile_mapping_table_schema + "_id"

            mapping_id = self.select_one_value_by_where(
                schema_name=profile_mapping_table_schema, view_table_name=profile_mapping_view_name,
                select_clause_value=profile_mapping_id_name,
                where=f"profile_id=%s AND {select_clause_value}=%s", params=(profile_id, entity_id))
            if mapping_id is None:
                # update the profile_mapping table
                self.insert_profile_mapping(profile_id=profile_id, entity_id=entity_id,
                                            profile_mapping_table_schema=profile_mapping_table_schema,
                                            select_clause_value=select_clause_value,
                                            profile_mapping_table_name=profile_mapping_table_name)

            if table_name == PERSON_TABLE:
                return
            field_old = self.select_one_value_by_column_and_value(schema_name=schema, view_table_name=view_name,
                                                                  select_clause_value=database_field_name,
                                                                  column_name=select_clause_value,
                                                                  column_value=entity_id)

            if not field_old:
                return

            data_dict = {}
            if database_field_name and field_column_value:
                data_dict[database_field_name] = field_column_value
            if database_sub_field_name and database_sub_field_value:
                data_dict[database_sub_field_name] = database_sub_field_value
            if data_dict:
                self.update_by_column_and_value(schema_name=schema, table_name=table_name, data_dict=data_dict,
                                                column_name=select_clause_value, column_value=entity_id)

            if field_old != field_column_value:
                self.update_logger_with_old_and_new_field_value(field_id, field_old, field_column_value)

        else:  # no profile_id and profile_mapping_table_id
            # Populate the person/profile class for each profile processed
            person_id = self.__add_person_to_db(fields_dict=fields_dict, index=index)
            if person_id is None:
                self.logger.error("No person_id found for profile_id", object={"profile_id": profile_id})
                raise Exception("No person was inserted into the database.")

            profile_id = self.__add_profile_to_db(person_id=person_id, fields_dict=fields_dict, index=index)
            # insert information from extracted fieldss
            if table_name == PERSON_TABLE:
                entity_id = person_id
            else:
                entity_id = self.insert_information_from_extracted_fields(
                    schema, table_name, database_field_name, field_column_value,
                    database_sub_field_name, database_sub_field_value)

            # update the profile_mapping table
            if profile_mapping_table_schema and profile_mapping_table_name and schema and profile_id and entity_id:
                self.insert_profile_mapping(profile_id=profile_id, entity_id=entity_id,
                                            profile_mapping_table_schema=profile_mapping_table_schema,
                                            select_clause_value=select_clause_value,
                                            profile_mapping_table_name=profile_mapping_table_name)

    def update_text_block_fields(self, text_block_id: int, fields_dict: dict) -> None:
        """Updates the text block with the extracted fields in JSON format."""
        self.update_by_column_and_value(column_value=text_block_id,
                                        data_dict={"fields_extracted_json": json.dumps(fields_dict)})

    # TODO The text we send it the text in the text_block_id, just to save the SELECT? Please clarify https://github.com/circles-zone/text-block-local-python-package/commit/3765831dc34a70efcc701c8689be1c1a5679a9cd
    def identify_and_update_text_block_type(self, text_block_id: int, text: str) -> int:
        """Identifies and updates the text block type. Returns text_block_type_id"""

        text_block_type_id = self.identify_text_block_type(text, text_block_id)
        if text_block_type_id:
            self.update_by_column_and_value(column_value=text_block_id,
                                            data_dict={"text_block_type_id": text_block_type_id})

        return text_block_type_id

    @lru_cache
    def get_regex_tuple_by_text_block_id(self, text_block_id: int or None) -> tuple or None:
        if not text_block_id:
            return

        system = self.select_one_tuple_by_column_and_value(
            schema_name="text_block_type", view_table_name="text_block_type_view",
            select_clause_value="system_id, system_entity_id",
            column_name="text_block_type_id", column_value=text_block_id)
        if system:
            return self.get_regex_tuple_by_system(system[0], system[1])

    @lru_cache
    def get_regex_tuple_by_system(self, system_id: int, system_entity_id: int) -> tuple or None:
        # filter results with system_id and system_entity if possible
        where = "TRUE "
        params = ()
        if system_id:
            where += " AND system_id = %s "
            params += (system_id,)
        if system_entity_id:
            where += " AND system_entity_id = %s "
            params += (system_entity_id,)

        if params:
            regex_list = self.select_multi_value_by_where(
                schema_name="text_block_type", view_table_name="text_block_type_view",
                select_clause_value="regex", where=where, params=params)
            regex_tuple = tuple(regex for regex in regex_list if regex)
            return regex_tuple  # tuple is hashable and save memory, so we can cache it later

    @lru_cache
    def identify_text_block_type(self, text: str, text_block_id: int = None) -> int:
        """Identifies the text block type.
        If a text block ID is provided, it will first try to identify the block type based on its system ID and entity ID."""

        potential_regex_tuple = self.get_regex_tuple_by_text_block_id(text_block_id)
        potential_block_type_ids = self.get_regex_per_block_type_id(potential_regex_tuple=potential_regex_tuple)

        # classify block_type using regex
        for text_block_type_id, regex in potential_block_type_ids.items():
            try:
                re.compile(regex)  # cached by re
                match = re.search(regex, text)
                if match:
                    return text_block_type_id
            except (re.error, TypeError) as e:
                self.logger.exception(f"Invalid regex: {regex}", object=e)

        # if no block type id has been found by this point

    def identify_and_update_all_text_blocks(self) -> None:
        """Checks all text blocks and updates their block type if needed."""
        # For all text_blocks
        text_block_ids_types_dict = self.get_text_block_ids_types_dict()
        block_types_dict = self.get_block_types_dict()
        for text_block_type_id, (existing_block_type_id, text) in text_block_ids_types_dict.items():
            if existing_block_type_id:
                self.logger.info(f"\nOld block type id: {existing_block_type_id}, "
                                 f"'{block_types_dict[existing_block_type_id]}' for text block type id {text_block_type_id}")
            else:
                self.logger.info("Old block type id: None")

            # TODO: optimize by sending all ids, so we SELECT for all ids at once (get_regex_tuple_by_text_block_id is called a lot)
            new_block_type_id = self.identify_and_update_text_block_type(text_block_type_id, text)
            if new_block_type_id is not None:
                self.logger.info(f"Identified block type: {new_block_type_id}: {block_types_dict[new_block_type_id]}")
            else:
                self.logger.info(f"No block type identified for text block {text_block_type_id}")

    def update_logger_with_old_and_new_field_value(
            self, field_id: int, field_value_old: str, field_value_new: str) -> int:
        """Updates the logger with the old and new field value."""
        data_dict = {"field_id": field_id, "field_value_old": field_value_old, "field_value_new": field_value_new}
        logger_id = self.insert(schema_name="logger", table_name="logger_table", data_dict=data_dict)
        return logger_id

    # TODO move this method to PersonsLocal class if not exists
    def __add_person_to_db(self, fields_dict: dict, index: int) -> int:
        """Adds a person to the database."""
        person_id = None
        first_name = None
        last_name = None
        birthday_original = None
        email_address = None

        if "Name" in fields_dict:
            full_name = fields_dict.get("Name")
            if isinstance(full_name, tuple):
                full_name = full_name[index]
            if full_name:
                full_name = full_name.split(" ")
                first_name = full_name[0]
                if len(full_name) > 1:
                    last_name = full_name[-1]

        if "Email" in fields_dict:
            email_address = fields_dict.get("Email")
            if isinstance(email_address, tuple):
                email_address = email_address[index]
        if "Birthday" in fields_dict:
            birthday_original = fields_dict.get("Birthday")  # , [None])[0]
        if "First Name" in fields_dict:
            first_name = fields_dict.get("First Name")  # , [None])[0]
        else:
            self.logger.warning("No first name found in fields_dict", object={'fields_dict': fields_dict})
        if "Last Name" in fields_dict:
            last_name = fields_dict.get("Last Name")  # , [None])[0]
        else:
            self.logger.warning("No last name found in fields_dict", object={'fields_dict': fields_dict})
        # TODO: can we get more information from the fields_dict and add it to the person object?
        if (first_name and last_name) or (first_name and email_address):
            person_object = Person(first_name=first_name, last_name=last_name, birthday_original=birthday_original,
                                   main_email_address=email_address,
                                   last_coordinate=Point(0.0, 0.0))
            insert_result = self.persons_local.insert_if_not_exists(
                person=person_object)
            if insert_result:
                person_id = insert_result[0]

        return person_id

    # TODO move this method to ProfilesLocal class if not exists
    def __add_profile_to_db(self, person_id: int, index: int, fields_dict: dict = None) -> int or None:
        """Adds a profile to the database."""
        if not person_id:
            self.logger.warning("__add_profile_to_db: No person_id provided")
            return

        # TODO: can we get more information from the fields_dict and add it to the profile object?
        name = fields_dict.get("Name")
        if isinstance(name, tuple):
            name = name[index]
        profile_dict = {
            'visibility_id': 0,  # TODO: replace this magic number.
            'is_approved': 0,
            'stars': 0,
            'last_dialog_workflow_state_id': 1,
            'lang_code': user_context.get_effective_profile_preferred_lang_code_string(),
            'is_main': 0,
            'profile.name': name,
            'name_approved': 0,
        }
        profile_id = self.profiles_local.insert(
            profile_dict=profile_dict,
            main_person_id=person_id)

        return profile_id

    def insert_information_from_extracted_fields(
            self, schema: str, table_name: str, database_field_name: str,
            match: str, database_sub_field_name: str, database_sub_field_value: str) -> int:
        """Inserts information from extracted fields."""
        # TODO: there are 3 such sections. So A, can we reuse the code? B: original version inserted twice (probably mistake?):
        # sql = "INSERT IGNORE INTO %s.%s (%s) VALUES ('%s', %s, %s)" % (schema, table_name, database_field_name, match)
        # if database_sub_field_name and database_sub_field_value:
        #    sql = "INSERT IGNORE INTO %s.%s (%s, %s) VALUES ('%s', '%s', %s, %s)" % (schema, table_name, database_field_name, database_sub_field_name, match, database_sub_field_value)

        data_dict = {}
        if database_field_name and match:
            data_dict[database_field_name] = match
        if database_sub_field_name and database_sub_field_value:
            data_dict[database_sub_field_name] = database_sub_field_value
        entity_id = self.insert(ignore_duplicate=True, schema_name=schema, table_name=table_name, data_dict=data_dict)
        return entity_id

    # TODO move this method to ProfilesLocal class if not exists
    # TODO use the generic profile mapping method
    def insert_profile_mapping(self, *, profile_id: int = None, entity_id: int,
                               profile_mapping_table_schema: str,
                               select_clause_value: str, profile_mapping_table_name: str) -> int:
        """Inserts a profile mapping."""
        data_dict = {}
        if profile_id:
            data_dict["profile_id"] = profile_id
        if select_clause_value and entity_id:  # and profile_mapping_table_schema == "group_profile":
            data_dict[select_clause_value] = entity_id
        try:
            entity_id = self.insert(ignore_duplicate=True, schema_name=profile_mapping_table_schema,
                                    table_name=profile_mapping_table_name, data_dict=data_dict)
        except Exception as exception:  # TODO: remove
            self.logger.error("Failed to insert profile mapping",
                              object={"exception": exception, **locals()})
        return entity_id

    # TODO I think we should move this method to ProfilesLocal
    def __get_profile_id(self, fields_dict: dict) -> int:
        """Gets the profile ID."""
        # TODO: split this method into smaller methods
        profile_id = None
        if "Email" in fields_dict:
            email_address = fields_dict["Email"]
            # TODO email_address -> email_address_str
            if isinstance(email_address, tuple):
                email_address = self.__get_email_from_tuple(email_address)
            # Try to get profile_id from person_id
            person_id = self.persons_local.get_person_id_by_email_address_str(email_address)
            if person_id:
                profile_id = self.profiles_local.select_one_value_by_column_and_value(
                    view_table_name="profile_view", select_clause_value="profile_id",
                    column_name="main_person_id", column_value=person_id)
            # Try to get profile_id from contact_id
            if not profile_id:
                # get email_address_id
                email_address_id = self.select_one_value_by_column_and_value(
                    schema_name="email_address", view_table_name="email_address_view",
                    select_clause_value="email_address_id", column_name="email_address", column_value=email_address)
                if email_address_id:
                    # get contact_id
                    contact_id = self.select_one_value_by_column_and_value(
                        schema_name="contact_email_address", view_table_name="contact_email_address_view",
                        select_clause_value="contact_id", column_name="email_address_id", column_value=email_address_id)
                    if contact_id:
                        # get profile_id
                        profile_id = self.select_one_value_by_column_and_value(
                            schema_name="contact_profile", view_table_name="contact_profile_view",
                            select_clause_value="profile_id", column_name="contact_id", column_value=contact_id)
        elif "Phone Number" in fields_dict:
            phone_number = fields_dict["Phone Number"]
            # Try to get profile_id from contact_id
            results = self.select_multi_dict_by_where(
                schema_name="phone", view_table_name="phone_view",
                select_clause_value="phone_id, number_original, full_number_normalized",
                where="full_number_normalized=%s OR number_original=%s", params=(phone_number, phone_number))
            # choose any number_original, and if not found, take full_number_normalized
            phone_id = next((result["phone_id"] for result in results if result["number_original"]),
                            next((result["phone_id"] for result in results if result["full_number_normalized"]), None))
            if phone_id:
                # get contact_id
                contact_id = self.select_one_value_by_column_and_value(
                    schema_name="contact_phone", view_table_name="contact_phone_view",
                    select_clause_value="contact_id", column_name="phone_id", column_value=phone_id)
                if contact_id:
                    # get profile_id
                    profile_id = self.select_one_value_by_column_and_value(
                        schema_name="contact_profile", view_table_name="contact_profile_view",
                        select_clause_value="profile_id", column_name="contact_id", column_value=contact_id)
        elif "Person Id" in fields_dict:
            person_id = fields_dict["Person Id"]
            profile_id = self.profiles_local.select_one_value_by_column_and_value(
                view_table_name="profile_view", select_clause_value="profile_id",
                column_name="main_person_id", column_value=person_id)
        self.profile_id = profile_id or self.profile_id or self.select_one_value_by_column_and_value(
            select_clause_value="profile_id", column_value=self.text_block_id)
        return self.profile_id

    @lru_cache
    def __get_index_in_regex_to_field_id_mapping(self, text_block_type_id: int) -> dict or None:
        """Gets the index_in_regex to field_id mapping."""
        field_text_block_types_dicts = self.select_multi_dict_by_column_and_value(
            schema_name="field_text_block_type", view_table_name="field_text_block_type_view",
            select_clause_value="index_in_regex, field_id",
            column_name="text_block_type_id", column_value=text_block_type_id)
        if not field_text_block_types_dicts:
            return
        index_in_regex_to_field_id_mapping = {}
        for field_text_block_types_dict in field_text_block_types_dicts:
            if field_text_block_types_dict["index_in_regex"] is None:
                return
            index_in_regex_to_field_id_mapping[field_text_block_types_dict["index_in_regex"]] = \
                field_text_block_types_dict["field_id"]
        return index_in_regex_to_field_id_mapping


    def __organize_fields_dict(self, fields_dict: dict, text_block_type_id: int, current_match_index: int) -> dict:
        """Organizes the fields' dictionary."""
        organized_fields_dict = {}
        index_in_regex_to_field_id_mapping = self.__get_index_in_regex_to_field_id_mapping(text_block_type_id)
        if not index_in_regex_to_field_id_mapping:
            for key, matches in fields_dict.items():
                organized_fields_dict[key] = matches[current_match_index] if isinstance(matches, list) else matches
        else:
            for key, matches in fields_dict.items():
                for matches_index, match in enumerate(matches):
                    if matches_index != current_match_index:
                        continue
                    for match_index, item in enumerate(match):
                        field_id = index_in_regex_to_field_id_mapping.get(match_index)
                        if field_id:
                            field_name = self.__get_field_name_by_field_id(field_id)
                            organized_fields_dict[field_name] = match[match_index] if isinstance(match, list) else match
        return organized_fields_dict

    @staticmethod
    def __get_email_from_tuple(emails_tuple: tuple) -> str:
        for element in emails_tuple:
            if '@' in element:
                return element

    # def process_field(self, processing_id, match):
    #     pass
    #     if processing_id == 1: #birthday YYYY-MM-DD
    #
    #     else if processing_id ==2: #phone
    #
    #     return processed_value

    # old version
    # TODO This method replaced by? __add_profile_to_db(...) and __add_person_to_db(...)?
    # def create_person_profile(self, fields_dict: dict) -> int:
    #     """Creates a person and profile based on the provided fields."""
    #
    #     created_user_id = UserContext().get_effective_user_id()
    #     person_id = self.create_person(fields_dict)
    #     visibility_id = 0  # TODO: replace this magic number.
    #     self.set_schema(schema_name="profile")
    #     number = NumberGenerator.get_random_number("profile", "profile_view")
    #     data_dict = {}
    #     data_dict["number"] = number
    #     data_dict["main_person_id"] = person_id
    #     data_dict["visibility_id"] = visibility_id
    #     data_dict["created_user_id"] = created_user_id
    #     self.insert(table_name="profile_table", data_dict=data_dict)
    #
    #     profile_id = self.cursor.lastrowid()
    #
    #
    #     return profile_id
    #
    #
    # def create_person(self, fields_dict: dict) -> int:
    #     """Creates a person based on the provided fields."""
    #
    #     self.set_schema(schema_name="person")
    #     created_user_id = UserContext().get_effective_user_id()
    #     data_dict = {}
    #     number = NumberGenerator.get_random_number("person", "person_view")
    #     if "First Name" in fields_dict and "Last Name" in fields_dict:
    #         first_name = fields_dict["First Name"][0]
    #         last_name = fields_dict["Last Name"][0]
    #         data_dict["number"] = number
    #         data_dict["first_name"] = first_name
    #         data_dict["last_name"] = last_name
    #         data_dict["created_user_id"] = created_user_id
    #     elif "Birthday" in fields_dict:
    #         birthday = fields_dict["Birthday"][0]
    #         data_dict["number"] = number
    #         data_dict["birthday_original"] = birthday
    #         data_dict["created_user_id"] = created_user_id
    #     else:
    #         data_dict["number"] = number
    #         data_dict["created_user_id"] = created_user_id
    #     columns = ", ".join(data_dict.keys())
    #     values = ", ".join(["%s"] * len(data_dict.values()))
    #     self.cursor.execute(f"INSERT INTO person.person_table (last_coordinate, {columns}) "
    #                         # TODO Please DEFAULT_POINT constant from location-local-python repo
    #                         f"VALUES (POINT(0.0000, 0.0000), {values})", tuple(data_dict.values()))
    #     # POINT can't be parameterized
    #
    #     person_id = self.cursor.lastrowid()
    #
    #     return person_id
