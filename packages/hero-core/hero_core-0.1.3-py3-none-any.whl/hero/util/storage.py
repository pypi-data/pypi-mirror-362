import os
from hero.util import log, function
import json


class Storage:
    def __init__(self, dir: str):
        self.dir = dir
        self.local_storage = "__local_storage.md"
        self.local_storage_path = os.path.join(self.dir, self.local_storage)
        self.storage_dict = {}
        self.initial_storage_dict = {
            "task_history_tail": 0,
            "compressed_task_history_tail": 0,
        }

        if not os.path.exists(self.local_storage_path):
            function.write_file(
                self.dir,
                self.local_storage,
                json.dumps(self.initial_storage_dict),
            )
        else:
            self.storage_dict = json.loads(
                function.read_file(self.dir, self.local_storage)
            )
            self._fix_storage_dict()
            log.debug(f"storage_dict: {self.storage_dict}")

    def _fix_storage_dict(self):
        """
        Fix the storage dict if it is not complete.
        """
        for key, value in self.initial_storage_dict.items():
            if key not in self.storage_dict:
                self.storage_dict[key] = value

    def _write_local_storage(self, key: str, value: str):
        """
        Append the value to the storage dict.
        """
        self.storage_dict[key] = value
        function.write_file(self.dir, self.local_storage, json.dumps(self.storage_dict))

    def _read_local_storage(self, key: str) -> str:
        """
        Read the value from the storage dict.
        """
        return str(self.storage_dict.get(key, self.initial_storage_dict.get(key, "")))

    def read(self, key: str) -> str:
        """
        Read the value from the storage dict.
        """
        return self._read_local_storage(key)

    def write(self, key: str, value: str):
        """
        Write the value to the storage dict.
        """
        self._write_local_storage(key, value)
