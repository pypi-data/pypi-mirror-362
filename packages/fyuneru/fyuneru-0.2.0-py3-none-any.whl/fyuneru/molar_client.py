from enum import Enum
from dataclasses import dataclass, field

import requests

from fyuneru.http_utils import find_labels, get_item_info, get_task_info


class MolarDomain(Enum):
    CN = "https://app.molardata.com/"
    OTHER = "https://app.abaka.ai/"


@dataclass
class MolarClient:
    token: str = field(default=None)
    domain: str = field(default=MolarDomain.CN.value)

    __required_structure = {
        "taskId": None,
        "exportMetadata": {"match": {"itemIds": None}},
    }

    def __validate_export_task(self, data, struct):
        if not isinstance(data, dict):
            return

        for key, value in struct.items():
            if key not in data:
                raise ValueError(f"Missing key: {key}")
            value = data[key]
            sub_struct = struct[key]
            self.__validate_export_task(value, sub_struct)

    def get_export_task(self, export_task: dict):
        self.__validate_export_task(export_task, self.__required_structure)
        origin_data = dict()
        origin_data["config"] = export_task["exportMetadata"]
        taskId = export_task["taskId"]
        itemIds = export_task["exportMetadata"]["match"]["itemIds"]
        while (task_info := self.get_task_info(taskId)) is None:
            continue
        origin_data["task"] = task_info.origin_data
        data = self.init_items(itemIds, taskId)
        origin_data["data"] = ...

    def process_item(
        self, item_id: str, task_id: str, session: requests.Session = None
    ):
        while (item_info := self.get_item_info(item_id=item_id)) is None:
            continue
        while (labels := self.find_labels(task_id=task_id, item_id=item_id)) is None:
            continue

    def init_items(self, item_ids: list[str], task_id: str): ...

    def get_task_info(
        self, task_id: str, session: requests.Session = None
    ) -> "MolarClient.TaskInfo":
        response_json = get_task_info(
            task_id=task_id, token=self.token, domain=self.domain, session=session
        )
        if not response_json:
            return None
        data = response_json.pop("data")
        return MolarClient.TaskInfo(
            uid=data["_id"],
            domain_id=data["domainId"],
            name=data["name"],
            type=data["type"],
            label_config=data["labelConfig"],
            label_alias=data["labelAlias"],
            origin_data=response_json,
        )

    def get_item_info(
        self, item_id: str, session: requests.Session = None
    ) -> "MolarClient.ItemInfo":
        response_json = get_item_info(
            item_id=item_id, token=self.token, domain=self.domain, session=session
        )
        if not response_json:
            return None
        data = response_json.pop("data")
        return MolarClient.ItemInfo(
            uid=data["_id"],
            task_id=data["taskId"],
            batch_id=data["packageInfo"]["_id"],
            info=data["info"],
            origin_data=data,
        )

    def find_labels(
        self, task_id: str, item_id: str, session: requests.Session = None
    ) -> list[dict]:
        response_json = find_labels(
            task_id=task_id,
            item_id=item_id,
            token=self.token,
            domain=self.domain,
            session=session,
        )
        if not response_json:
            return None
        return response_json.pop("data")

    @dataclass
    class TaskInfo:
        uid: str = field(default=None)
        domain_id: str = field(default=None)
        name: str = field(default=None)
        type: str = field(default=None)
        label_config: dict = field(default_factory=dict)
        label_alias: dict = field(default_factory=dict)
        origin_data: dict = field(default=None)

    @dataclass
    class ItemInfo:
        uid: str = field(default=None)
        task_id: str = field(default=None)
        batch_id: str = field(default=None)
        info: dict = field(default_factory=dict)
        origin_data: dict = field(default_factory=dict)

    @dataclass
    class LabelInfo:
        label_id: str = field(default=None)
        label_name: str = field(default=None)

    @dataclass
    class ExportTask:
        task_uid: str = field(default=None)
        item_ids: list[str] = field(default=None)
        task_alias: dict = field(default=None)
