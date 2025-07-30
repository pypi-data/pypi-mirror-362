from _balder.executor.executor_tree import ExecutorTree
from balderplugin.junit import JunitPlugin
from balder import BalderPlugin


class TestValidationPlugin(BalderPlugin):


    def session_finished(self, executor_tree: ExecutorTree):

        assert executor_tree.testsummary().success == 1
