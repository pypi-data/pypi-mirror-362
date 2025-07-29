from enum import Enum


class StudyStatus(str, Enum):
    wait = "wait"
    running = "running"
    done = "done"
    not_found = "not_found"
