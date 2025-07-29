"""HTML report generator for records logs."""
import os
import jinja2
import json

from t_utils.const_utils import EMPOWER_RUN_LINK, work_item

from ..models.records_logs import RecordLog

current_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(current_dir, "report_template.html"), encoding="utf-8") as f:
    template_str = f.read()


def _convert_logs_to_records(records_logs_data: dict[str, RecordLog]) -> list:
    """Convert records_logs_data to the list of dicts expected by the new_report.html template."""
    records = []
    for record_id, record_log in records_logs_data.items():
        # Compose the events list from traces and status_updates
        events = []
        # Merge and sort traces and status_updates by timestamp
        traces = getattr(record_log, "traces", [])
        status_updates = getattr(record_log, "status_updates", [])
        merged_events = [(t.timestamp, "trace", t) for t in traces] + [
            (s.timestamp, "status", s) for s in status_updates
        ]
        merged_events.sort(key=lambda x: x[0])
        for timestamp, kind, event in merged_events:
            if kind == "trace":
                events.append(
                    {
                        "type": "trace",
                        "action": getattr(event, "action", None),
                        "reason": getattr(event, "reason", None),
                        "timestamp": event.timestamp.isoformat() if hasattr(event, "timestamp") else None,
                        "image": getattr(event, "html_image_path", None),
                        "fieldsUpdated": getattr(event, "dict_updates", {}),
                        "technicalDetails": getattr(event, "traceback", None),
                    }
                )
            elif kind == "status":
                events.append(
                    {
                        "type": "status",
                        "action": "Status Update",
                        "timestamp": event.timestamp.isoformat() if hasattr(event, "timestamp") else None,
                        "fieldsUpdated": {
                            "status": {
                                "from": getattr(event, "old_status", ""),
                                "from_color": getattr(event, "old_status_color", ""),
                                "to": getattr(event, "new_status", ""),
                                "to_color": getattr(event, "new_status_color", ""),
                            }
                        },
                        "technicalDetails": getattr(event, "traceback", None),
                    }
                )
        records.append(
            {
                "id": record_id,
                "type": getattr(record_log, "record", ""),
                "time": "",
                "status": getattr(record_log, "status", ""),
                "statusColor": getattr(record_log, "status_color", ""),
                "events": events,
            }
        )
    return records


def generate_enhanced_html(records_logs_data: dict[str, RecordLog]) -> str:
    """Generate an enhanced HTML report using the new_report.html template and Alpine.js."""
    admin_code = work_item.get("metadata", {}).get("process", {}).get("adminCode", "")
    process_name = work_item.get("metadata", {}).get("process", {}).get("name", "")

    full_process_name = f"{admin_code} - {process_name}" if admin_code and process_name else process_name or admin_code
    report_name = f'Records Report for "{full_process_name}"' if full_process_name else "Records Report"

    records = _convert_logs_to_records(records_logs_data)
    records_json = json.dumps(records, default=str)
    env = jinja2.Environment(autoescape=True)

    html = env.from_string(template_str).render(
        records_json=records_json, run_link=EMPOWER_RUN_LINK, report_name=report_name
    )
    return html
