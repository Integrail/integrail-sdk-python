from .agent import *
from .execution import *
from .memory import *
from .node import *

class IntegrailCloudApi(BaseApi):
    def __init__(self, options: dict):
        super().__init__(options)
        self.agent = CloudAgentApi(self.options)
        self.node = CloudNodeApi(self.options)
        self.category = CloudCategoryApi(self.options)
        self.memory = CloudMemoryApi(self.options)