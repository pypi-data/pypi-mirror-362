"""Module for remote storage operations."""
import os.path
import shutil
import zipfile
from pathlib import Path

from t_utils.const_utils import EMPOWER_RUN_ID
from t_utils.robocloud_utils import RC_PROCESS_NAME

from .models.records_logs import RecordsLogs
from .utils.utils import SimpleFileLock, get_image_src_uri

HTML_FILE_NAME = "records_report.html"
IMAGES_FOLDER_NAME = "images"


class RemoteStorage:
    """Class to manage remote storage for records logs."""

    def __init__(self, root_folder_path: str | Path):
        """Initialize the RemoteStorage."""
        process_name = RC_PROCESS_NAME or "process_name"
        run_id = EMPOWER_RUN_ID or "run_id"
        self.root_path: Path = Path(root_folder_path) / process_name / run_id

    def get_records_logs(self, include_image_src_uri: bool = False) -> RecordsLogs:
        """Get all records for a given run_id."""
        json_file = self.root_path / "records_logs.json"

        if json_file.exists():
            records_logs = RecordsLogs.load_from_json_file(json_file)

            if include_image_src_uri:
                for record_log in records_logs.data.values():
                    for trace in record_log.traces:
                        if trace.image:
                            trace.image_src_uri = get_image_src_uri(str(self.root_path / trace.html_image_path))

            return records_logs
        else:
            return RecordsLogs()

    def get_global_records_logs(self) -> RecordsLogs:
        json_file = self.root_path / "records_logs.json"
        if json_file.exists():
            with open(json_file, "r", encoding="utf-8") as file:
                return RecordsLogs.model_validate_json(file.read())
        else:
            return RecordsLogs()

    def update_records_logs(self, new_records: RecordsLogs) -> None:
        """Safely merge local logs with global logs (parallel-safe)."""
        self.root_path.mkdir(parents=True, exist_ok=True)
        json_file = self.root_path / "records_logs.json"
        lock_file = self.root_path / "records_logs.json.lock"

        with SimpleFileLock(lock_file):
            existing_records = self.get_global_records_logs()

            for record_id, new_log in new_records.data.items():
                if record_id in existing_records.data:
                    existing_log = existing_records.data[record_id]
                    existing_log.traces.extend(new_log.traces)
                    existing_log.status_updates.extend(new_log.status_updates)

                    if existing_log.record != new_log.record:
                        existing_log.record = new_log.record
                    existing_log.status = new_log.status
                    existing_log.status_color = new_log.status_color
                else:
                    existing_records.data[record_id] = new_log

                for trace in new_log.traces:
                    if trace.image and os.path.exists(trace.image):
                        new_image_path = self.root_path / trace.html_image_path
                        new_image_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy(trace.image, new_image_path)

            with open(json_file, "w", encoding="utf-8") as file:
                file.write(existing_records.to_json_str())

    def save_html(self, html_content: str) -> Path:
        """Save HTML content to a file in the remote storage."""
        self.root_path.mkdir(parents=True, exist_ok=True)

        html_file = self.root_path / HTML_FILE_NAME
        html_file.write_text(html_content, encoding="utf-8")
        return html_file

    def get_zip(self, file_path: str) -> None:
        """Pack all records logs and images into a zip file."""
        with zipfile.ZipFile(file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Add HTML file
            zipf.write(self.root_path / HTML_FILE_NAME, arcname=os.path.basename(HTML_FILE_NAME))

            images_folder_path = self.root_path / IMAGES_FOLDER_NAME
            # Add all files from the images folder
            for root, _, files in os.walk(images_folder_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, os.path.dirname(images_folder_path))
                    zipf.write(full_path, arcname=arcname)
