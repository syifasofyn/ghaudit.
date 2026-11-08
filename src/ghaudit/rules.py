import re
from dataclasses import dataclass

SHA_RE = re.compile(r"^[0-9a-f]{40}$")


@dataclass
class Finding:
    rule: str
    severity: str
    file: str
    message: str


def check_unpinned_actions(path, workflow):
    findings = []
    for job_name, job in (workflow.get("jobs") or {}).items():
        for step in job.get("steps") or []:
            uses = step.get("uses")
            if not uses or uses.startswith("./") or uses.startswith("docker://"):
                continue
            _, _, ref = uses.partition("@")
            if not SHA_RE.match(ref):
                findings.append(Finding(
                    rule="unpinned-action",
                    severity="MEDIUM",
                    file=path,
                    message=f"Job '{job_name}': '{uses}' tidak di-pin ke commit SHA",
                ))
    return findings