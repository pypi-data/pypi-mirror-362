import re
from abc import abstractmethod
from typing import List


class ChainCommand():
    def __init__(self):
        self.output = ""

    # 开始链式调用
    @abstractmethod
    def start_chain(self, delay=1):
        pass

    # 结束链式调用
    @abstractmethod
    def end_chain(self):
        pass

    # 期望上个命令的链式调用的结果，单个字符串，或正则
    def expect_output(self, expectation, regex: bool = False):
        if regex:
            pattern = re.compile(expectation)
            match = pattern.search(self.output)
            if match is None:
                raise Exception(f"未匹配到期望结果,期望:{expectation},实际:{self.output}")
            return self

        if expectation not in self.output:
            raise Exception(f"未匹配到期望结果,期望:{expectation},实际:{self.output}")
        return self

    # 期望上个命令的链式调用的结果，多个字符串，或正则
    def expect_outputs(self, expectations: List, regex: bool = False):
        if regex:
            for expectation in expectations:
                pattern = re.compile(expectation)
                match = pattern.search(self.output)
                if match is not None:
                    return self

            raise Exception(f"未匹配到期望结果,期望:{expectations},实际:{self.output}")

        for expectation in expectations:
            if expectation in self.output:
                return self

        raise Exception(f"未匹配到期望结果,期望:{expectations},实际:{self.output}")

    def is_hit_target(self, result, expectations: List, regex: bool = False):
        if regex:
            for expectation in expectations:
                pattern = re.compile(expectation)
                match = pattern.search(result)
                if match is not None:
                    return self

            # raise Exception(f"未匹配到期望结果,期望:{expectations},实际:{result}")
            return None

        for expectation in expectations:
            if expectation in result:
                return self
        return None
        # raise Exception(f"未匹配到期望结果,期望:{expectations},实际:{result}")

    def match_regex(self, regex, result):
        pattern = re.compile(regex)
        return pattern.search(result)
