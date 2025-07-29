import zipfile
import json
from pathlib import Path

from t_record import Status
from t_record.record import configure_records_tracing, dump_records, pack_sharable_zip
from tests.conftest import SimpleRecord


def test_record_lifecycle(tmp_storage_dir: Path, simple_record: SimpleRecord) -> None:
    configure_records_tracing(tmp_storage_dir)

    simple_record.status = simple_record.status
    simple_record.log_trace(action="start", reason="testing")
    dump_records()

    process_folder = next(tmp_storage_dir.glob("*/*"))
    assert (process_folder / "records_logs.json").exists()
    assert (process_folder / "records_report.html").exists()

    html_content = (process_folder / "records_report.html").read_text()
    assert "test123" in html_content

    zip_file = tmp_storage_dir / "out.zip"
    pack_sharable_zip(zip_file)
    assert zip_file.exists()
    with zipfile.ZipFile(zip_file) as zf:
        assert any("records_report.html" in n for n in zf.namelist())


def test_persistence_across_runs(tmp_storage_dir: Path, simple_record: SimpleRecord) -> None:
    # First run
    configure_records_tracing(tmp_storage_dir)
    rec = simple_record
    rec.status = Status.RUNNING
    rec.log_trace("first")
    dump_records()

    # Second run, continuing history
    configure_records_tracing(tmp_storage_dir)
    rec2 = simple_record
    rec2.status = Status.COMPLETED
    rec2.log_trace("second")
    dump_records()

    process_folder = next(tmp_storage_dir.glob("*/*"))
    json_file = process_folder / "records_logs.json"
    data = json.loads(json_file.read_text())
    assert len(data["data"][rec2.id]["traces"]) >= 3
    assert any(trace["action"] == "first" for trace in data["data"][rec2.id]["traces"])


def test_status_updates_logged(tmp_storage_dir: Path, simple_record: SimpleRecord) -> None:
    configure_records_tracing(tmp_storage_dir)
    record = simple_record
    record.status = Status.RUNNING
    record.log_trace("doing")
    dump_records()

    process_folder = next(tmp_storage_dir.glob("*/*"))
    data = json.loads((process_folder / "records_logs.json").read_text())
    assert record.id in data["data"]
