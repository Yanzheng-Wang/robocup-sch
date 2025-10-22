from abc import ABC, abstractmethod

class StateMachine(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def planTasks(self):
        """计划任务：子类实现具体的任务规划逻辑"""
        pass