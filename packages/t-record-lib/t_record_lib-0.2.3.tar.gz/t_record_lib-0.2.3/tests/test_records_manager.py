from pathlib import Path

from t_record import Status
from t_record.records_manager import RecordsManager
from t_record.remote_storage import RemoteStorage
from tests.conftest import SimpleRecord


def test_storage_writes(tmp_storage_dir: Path) -> None:
    storage = RemoteStorage(tmp_storage_dir)
    logs = storage.get_records_logs()
    assert isinstance(logs.data, dict)


def test_register_and_update(tmp_storage_dir: Path, simple_record: SimpleRecord) -> None:
    mgr = RecordsManager(tmp_storage_dir)
    rec = simple_record
    rec._status_field = None
    mgr.register_record(rec)
    assert simple_record.id in mgr.local_records_logs.data

    mgr.update_status(rec, Status.COMPLETED)
    log = mgr.local_records_logs.data[simple_record.id]
    assert log.status == Status.COMPLETED


def test_merge_logs(tmp_storage_dir: Path, simple_record: SimpleRecord) -> None:
    mgr1 = RecordsManager(tmp_storage_dir)
    rec = simple_record
    mgr1.register_record(rec)
    mgr1.dump()

    # new manager simulating new run
    mgr2 = RecordsManager(tmp_storage_dir)
    assert rec.id in mgr2.global_records_logs.data
