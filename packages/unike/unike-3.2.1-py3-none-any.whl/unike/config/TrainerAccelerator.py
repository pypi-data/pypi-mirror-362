# coding:utf-8
#
# unike/config/TrainerAccelerator.py
#
# created by LuYF-Lemon-love <luyanfeng_nlp@qq.com> on Apr 12, 2024
# updated by LuYF-Lemon-love <luyanfeng_nlp@qq.com> on Apr 27, 2024
#
# 该脚本定义了并行训练循环函数.

"""
利用 accelerate 实现并行训练。
"""

from typing import Any, List
from accelerate import Accelerator
from ..utils import WandbLogger

def accelerator_prepare(*args: List[Any], wandb_logger: WandbLogger = None) -> List[Any]:

	"""
	由于分布式并行依赖于 `accelerate <https://github.com/huggingface/accelerate>`_ ，因此，需要利用 Accelerator 为分布式训练准备对象。
	
	例子::

		dataloader, model, accelerator = accelerator_prepare(
		    dataloader,
		    model
		)

	:param args: :py:class:`unike.data.KGEDataLoader` 和 :py:class:`unike.module.strategy.Strategy` 。
	:type args: typing.List[typing.Any]
	:param wandb_logger: :py:class:`unike.utils.WandbLogger` 对象
	:type wandb_logger: :py:class:`unike.utils.WandbLogger`
	:returns: 包装好的对象列表和 Accelerator() 对象。
	:rtype: typing.List[typing.Any]
	"""
	if wandb_logger:
		accelerator = Accelerator(log_with=wandb_logger.endpoint)
		accelerator.init_trackers(
			project_name=wandb_logger.project,
			config=wandb_logger.config.__dict__,
			init_kwargs={
				wandb_logger.endpoint: {
					'name': wandb_logger.name
				}
			}
		)
	else:
		accelerator = Accelerator()
	
	result = accelerator.prepare(*args)
	result = list(result)
	result.append(accelerator)
	return result