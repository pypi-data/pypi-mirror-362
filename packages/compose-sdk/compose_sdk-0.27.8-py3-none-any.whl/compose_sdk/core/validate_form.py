# type: ignore
import datetime

from .ui.types import INTERACTION_TYPE, TYPE, Table
from .file import File
from .static_tree import StaticTree
from .json import JSON
from .run_hook_function import RunHookFunction


class ValidateForm:
    def __init__(self, run_hook_function: RunHookFunction):
        self.run_hook_function = run_hook_function

    @staticmethod
    def hydrate_form_data(form_data, component_tree, temp_files):
        hydrated = {}
        temp_files_to_delete = []

        for key, data in form_data.items():
            try:
                if (
                    isinstance(data, list)
                    and "fileId" in data[0]
                    and isinstance(data[0]["fileId"], str)
                ):
                    hydrated[key] = [
                        File(
                            temp_files[file["fileId"]],
                            file["fileName"],
                            file["fileType"],
                        )
                        for file in data
                    ]
                    temp_files_to_delete.extend([file["fileId"] for file in data])
                elif (
                    isinstance(data, dict)
                    and "value" in data
                    and "type" in data
                    and len(data) == 2
                ):
                    if data["type"] == TYPE.INPUT_DATE:
                        if data["value"] is None:
                            hydrated[key] = None
                        else:
                            hydrated[key] = datetime.date(
                                data["value"]["year"],
                                data["value"]["month"],
                                data["value"]["day"],
                            )
                    elif data["type"] == TYPE.INPUT_TIME:
                        if data["value"] is None:
                            hydrated[key] = None
                        else:
                            hydrated[key] = datetime.time(
                                data["value"]["hour"],
                                data["value"]["minute"],
                            )
                    elif data["type"] == TYPE.INPUT_DATE_TIME:
                        if data["value"] is None:
                            hydrated[key] = None
                        else:
                            hydrated[key] = datetime.datetime(
                                data["value"]["year"],
                                data["value"]["month"],
                                data["value"]["day"],
                                data["value"]["hour"],
                                data["value"]["minute"],
                            )
                    elif data["type"] == TYPE.INPUT_JSON:
                        try:
                            hydrated[key] = JSON.parse(data["value"])
                        except Exception:
                            hydrated[key] = data["value"]
                    elif data["type"] == TYPE.INPUT_TABLE:
                        component = StaticTree.find_component.by_id(component_tree, key)

                        if (
                            component is not None
                            and component["type"] == TYPE.INPUT_TABLE
                        ):
                            if (
                                component["model"]["properties"].get("selectMode")
                                == Table.SelectionReturn.ID
                                or component["model"]["properties"].get("selectMode")
                                == Table.SelectionReturn.INDEX
                            ):
                                hydrated[key] = data["value"]
                            else:
                                primary_key = component["model"]["properties"].get(
                                    "primaryKey", None
                                )

                                if primary_key is None:
                                    rows = [
                                        component["model"]["properties"]["data"][idx]
                                        for idx in data["value"]
                                    ]
                                else:
                                    primary_key_map = {}

                                    for value in data["value"]:
                                        primary_key_map[value] = True

                                    rows = [
                                        row
                                        for row in component["model"]["properties"][
                                            "data"
                                        ]
                                        if row[primary_key] in primary_key_map
                                    ]

                                hydrated[key] = rows
                        else:
                            raise Exception(
                                "An error occurred while trying to hydrate a table input: could not find the table within the component tree"
                            )
                    else:
                        hydrated[key] = data["value"]
                else:
                    hydrated[key] = data
            except Exception:
                hydrated[key] = data

        return hydrated, temp_files_to_delete

    async def get_form_input_errors(self, form_data, static_layout):
        input_errors = {}
        has_errors = False

        for component_id, data in form_data.items():
            input_component = StaticTree.find_component.by_id(
                static_layout, component_id
            )

            if (
                input_component is None
                or input_component["interactionType"] != INTERACTION_TYPE.INPUT
                or input_component["hooks"]["validate"] is None
            ):
                continue

            validator_func = input_component["hooks"]["validate"]
            validator_response = await self.run_hook_function.execute(
                validator_func, data
            )

            if isinstance(validator_response, str):
                has_errors = True
                input_errors[component_id] = validator_response
            elif validator_response is False:
                has_errors = True
                input_errors[component_id] = "Invalid value"

        if has_errors:
            return input_errors

        return None

    async def get_form_error(self, component, form_data):
        if component["hooks"]["validate"] is None:
            return None

        validator_func = component["hooks"]["validate"]
        validator_response = await self.run_hook_function.execute(
            validator_func, form_data
        )

        if isinstance(validator_response, str):
            return validator_response
        elif validator_response is False:
            return "Invalid value"

        return None
