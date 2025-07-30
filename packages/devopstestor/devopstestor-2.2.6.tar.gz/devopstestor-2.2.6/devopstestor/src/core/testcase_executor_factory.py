from testcase_executor import TestcaseExecutor

class TestcaseExecutorFactory():
    """
    Usine de TestcaseExecutor
    """
    def __init__(self, global_config, machines_factory):
        self.global_config = global_config
        self.machines_factory = machines_factory

    def create_testcase_executor(self, name, tags, default_target, **common_scenarios_args):
        return TestcaseExecutor(
            global_config=self.global_config,
            machines_factory=self.machines_factory,
            name=name,
            tags=tags,
            default_target=default_target,
            **common_scenarios_args
        )
