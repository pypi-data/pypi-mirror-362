"""Module for remote storage operations."""
import os.path
import shutil
import zipfile
from pathlib import Path

from t_utils.const_utils import EMPOWER_RUN_ID
from t_utils.robocloud_utils import RC_PROCESS_NAME

from .models.records_logs import RecordsLogs
from .utils.utils import SimpleFileLock


HTML_FILE_NAME = "records_report.html"
IMAGES_FOLDER_NAME = "images"


class RemoteStorage:
    """Class to manage remote storage for records logs."""

    def __init__(self, root_folder_path: str | Path):
        """Initialize the RemoteStorage."""
        process_name = RC_PROCESS_NAME or "process_name"
        run_id = EMPOWER_RUN_ID or "run_id"
        self.root_path: Path = Path(root_folder_path) / process_name / run_id

    def get_records_logs(self) -> RecordsLogs:
        """Get all records for a given run_id."""
        json_file = self.root_path / "records_logs.json"

        if json_file.exists():
            return RecordsLogs.load_from_json_file(json_file)
        else:
            return RecordsLogs()

    def update_records_logs(self, new_records: RecordsLogs) -> None:
        """Safely merge local logs with global logs (parallel-safe)."""
        self.root_path.mkdir(parents=True, exist_ok=True)
        json_file = self.root_path / "records_logs.json"
        lock_file = self.root_path / "records_logs.json.lock"

        with SimpleFileLock(lock_file):
            if json_file.exists():
                existing_records = RecordsLogs.load_from_json_file(json_file)
            else:
                existing_records = RecordsLogs()

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

            existing_records.save_to_json_file(json_file)

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
