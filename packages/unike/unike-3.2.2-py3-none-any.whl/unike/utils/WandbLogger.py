# coding:utf-8
#
# unike/utils/WandbLogger.py
#
# created by LuYF-Lemon-love <luyanfeng_nlp@qq.com> on Jan 1, 2024
# updated by LuYF-Lemon-love <luyanfeng_nlp@qq.com> on Feb 24, 2024
#
# 该脚本定义了 WandbLogger 类.

"""
WandbLogger - 使用 Weights and Biases 记录实验结果。
"""

import typing
import wandb
import swanlab
from typing import Literal
from accelerate import Accelerator
from types import SimpleNamespace

class WandbLogger:

    """使用 `Weights and Biases <https://docs.wandb.ai/>`_ 记录实验结果。"""

    def __init__(self,
        project: str ="pybind11-ke",
        name: str = "transe",
        config: dict[str, typing.Any] | None = None,
        endpoint: Literal['wandb', 'swanlab'] = 'wandb'):

        """创建 WandbLogger 对象。
        
        :param project: wandb 的项目名称
        :type project: str
        :param name: wandb 的 run name
        :type name: str
        :param config: wandb 的项目配置如超参数。
        :type config: dict[str, typing.Any] | None
        :param endpoint: 使用 wandb 还是 swanlab 记录实验结果
        :type endpoint: Literal['wandb', 'swanlab']
        """
        self.project = project
        self.name = name
        self.endpoint = endpoint
        self.config: SimpleNamespace = SimpleNamespace(**config)
        
        self.accelerator = False
        self.logger = None

    def init(self):
        """初始化日志"""
        if not self.accelerator:         
            if self.endpoint == 'wandb':
                wandb.init(project=self.project, name=self.name, config=self.config.__dict__)
                self.logger = wandb
            elif self.endpoint == 'swanlab':
                swanlab.init(project=self.project, name=self.name, config=self.config.__dict__)
                self.logger = swanlab
    
    def set_accelerator(self, accelerator: Accelerator):
        """设置 Accelerator 对象
        
        :param accelerator: Accelerator 对象
        :type accelerator: Accelerator
        """
        self.logger = accelerator
        self.accelerator = True

    def log(self, *args, **kwargs):
        """记录日志"""
        self.logger.log(*args, **kwargs)
    
    def finish(self):
        """关闭日志"""
        if self.accelerator:
            self.logger.end_training()
        else:
            self.logger.finish()