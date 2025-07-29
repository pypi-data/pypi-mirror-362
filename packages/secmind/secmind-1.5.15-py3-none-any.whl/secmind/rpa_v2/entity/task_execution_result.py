from typing import Optional


class TaskExecutionResult:
    FIELD_NAME = 'task_execution_result'

    def __init__(self, success: bool = False, data: Optional[any] = None, log: Optional[str] = None,
                 stack: Optional[str] = None, msg: Optional[str] = None):
        self.success = success
        self.data = data
        self.log = log
        self.stack = stack
        self.msg = msg
