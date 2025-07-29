# coding:utf-8
#
# unike/config/HPOTrainer.py
#
# created by LuYF-Lemon-love <luyanfeng_nlp@qq.com> on Jan 2, 2024
# updated by LuYF-Lemon-love <luyanfeng_nlp@qq.com> on May 6, 2024
#
# 该脚本定义了并行训练循环函数.

"""
hpo_train - 超参数优化训练循环函数。
"""

import wandb
import typing
from ..utils import import_class
from ..module.model import TransE
from ..module.loss import MarginLoss
from ..module.strategy import NegativeSampling
from ..config import Trainer, Tester
from ..data import KGEDataLoader
from loguru import logger

def set_hpo_config(
	method: str = 'bayes',
	sweep_name: str = 'unike_hpo',
	metric_name: str = 'val/hits@10',
	metric_goal: str = 'maximize',
	data_loader_config: dict[str, dict[str, typing.Any]] = {},
	kge_config: dict[str, dict[str, typing.Any]] = {},
	loss_config: dict[str, dict[str, typing.Any]] = {},
	strategy_config: dict[str, dict[str, typing.Any]] = {},
	tester_config: dict[str, dict[str, typing.Any]] = {},
	trainer_config: dict[str, dict[str, typing.Any]] = {}) -> dict[str, dict[str, typing.Any]]:

	"""设置超参数优化范围。
	
	:param method: 超参数优化的方法，``grid`` 或 ``random`` 或 ``bayes``
	:type param: str
	:param sweep_name: 超参数优化 sweep 的名字
	:type sweep_name: str
	:param metric_name: 超参数优化的指标名字
	:type metric_name: str
	:param metric_goal: 超参数优化的指标目标，``maximize`` 或 ``minimize``
	:type metric_goal: str
	:param data_loader_config: :py:class:`unike.data.KGEDataLoader` 的超参数优化配置
	:type data_loader_config: dict
	:param kge_config: :py:class:`unike.module.model.Model` 的超参数优化配置
	:type kge_config: dict
	:param loss_config: :py:class:`unike.module.loss.Loss` 的超参数优化配置
	:type loss_config: dict
	:param strategy_config: :py:class:`unike.module.strategy.Strategy` 的超参数优化配置
	:type strategy_config: dict
	:param tester_config: :py:class:`unike.config.Tester` 的超参数优化配置
	:type tester_config: dict
	:param trainer_config: :py:class:`unike.config.Trainer` 的超参数优化配置
	:type trainer_config: dict
	:returns: 超参数优化范围
	:rtype: dict
	"""

	sweep_config: dict[str, str] = {
		'method': method,
		'name': sweep_name
	}

	metric: dict[str, str] = {
		'name': metric_name,
		'goal': metric_goal
	}

	parameters_dict: dict[str, dict[str, typing.Any]] | None = {}
	parameters_dict.update(data_loader_config)
	parameters_dict.update(kge_config)
	parameters_dict.update(loss_config)
	parameters_dict.update(strategy_config)
	parameters_dict.update(tester_config)
	parameters_dict.update(trainer_config)

	sweep_config['metric'] = metric
	sweep_config['parameters'] = parameters_dict

	return sweep_config

def set_hpo_hits(
    new_hits: list[int] = [1, 3, 10]):
	
	"""设置 Hits 指标。
	
	:param new_hits: 准备报告的指标 Hit@N 的列表，默认为 [1, 3, 10], 表示报告 Hits@1, Hits@3, Hits@10
	:type new_hits: list[int]
    """
	
	tmp = Tester.hits
	Tester.hits = new_hits
	logger.info(f"Hits@N 指标由 {tmp} 变为 {Tester.hits}")

def start_hpo_train(
	config: dict[str, dict[str, typing.Any]] | None = None,
	project: str = "pybind11-ke-sweeps",
	count: int = 2):

	"""开启超参数优化。
	
	:param config: wandb 的超参数优化配置。
	:type config: dict
	:param project: 项目名
	:type param: str
	:param count: 进行几次尝试。
	:type count: int
	"""

	wandb.login()

	sweep_id = wandb.sweep(config, project=project)

	wandb.agent(sweep_id, hpo_train, count=count)

def hpo_train(config: dict[str, typing.Any] | None = None):

	"""超参数优化训练循环函数。
	
	:param config: wandb 的项目配置如超参数。
	:type config: dict[str, typing.Any] | None
	"""
	
	with wandb.init(config = config):
		
		config = wandb.config

		# dataloader for training
		dataloader_class: type[KGEDataLoader] = import_class(f"unike.data.{config.dataloader}")
		dataloader = dataloader_class(
			in_path = config.in_path,
			ent_file = config.ent_file,
			rel_file = config.rel_file,
			train_file = config.train_file,
			valid_file = config.valid_file,
			test_file = config.test_file,
			batch_size = config.batch_size,
			neg_ent = config.neg_ent,
			test = True,
			test_batch_size = config.test_batch_size,
			type_constrain = config.type_constrain,
			num_workers = config.num_workers,
			train_sampler = import_class(f"unike.data.{config.train_sampler}"),
			test_sampler = import_class(f"unike.data.{config.test_sampler}")
		)

		# define the model
		model_class = import_class(f"unike.module.model.{config.model}")
		if config.model in ["TransE", "TransH"]:
			kge_model = model_class(
			    ent_tol = dataloader.get_ent_tol(),
			    rel_tol = dataloader.get_rel_tol(),
			    dim = config.dim,
			    p_norm = config.p_norm,
			    norm_flag = config.norm_flag
			)
		elif config.model == "TransR":
			transe = TransE(
				ent_tol = dataloader.get_ent_tol(),
				rel_tol = dataloader.get_rel_tol(),
				dim = config.dim,
				p_norm = config.p_norm,
				norm_flag = config.norm_flag
			)
			kge_model = model_class(
				ent_tol = dataloader.get_ent_tol(),
				rel_tol = dataloader.get_rel_tol(),
				dim_e = config.dim,
				dim_r = config.dim,
				p_norm = config.p_norm,
				norm_flag = config.norm_flag,
				rand_init = config.rand_init)
			model_e = NegativeSampling(
				model = transe,
				loss = MarginLoss(margin = config.margin_e)
			)
			trainer_e = Trainer(
				model = model_e,
				data_loader = dataloader.train_dataloader(),
				epochs = 1,
				lr = config.lr_e,
				opt_method = config.opt_method_e,
				use_gpu = config.use_gpu,
				device = config.device
			)
			trainer_e.run()
			parameters = transe.get_parameters()
			transe.save_parameters("./transr_transe.json")
			kge_model.set_parameters(parameters)
		elif config.model == "TransD":
			kge_model = model_class(
				ent_tol = dataloader.get_ent_tol(),
				rel_tol = dataloader.get_rel_tol(),
				dim_e = config.dim_e,
				dim_r = config.dim_r,
				p_norm = config.p_norm,
				norm_flag = config.norm_flag)
		elif config.model == "RotatE":
			kge_model = model_class(
				ent_tol = dataloader.get_ent_tol(),
				rel_tol = dataloader.get_rel_tol(),
				dim = config.dim,
				margin = config.margin,
				epsilon = config.epsilon)
		elif config.model in ["RESCAL", "DistMult", "HolE", "ComplEx", "Analogy", "SimplE"]:
			kge_model = model_class(
			    ent_tol = dataloader.get_ent_tol(),
			    rel_tol = dataloader.get_rel_tol(),
			    dim = config.dim)
		elif config.model == "RGCN":
			kge_model = model_class(
				ent_tol = dataloader.get_ent_tol(),
				rel_tol = dataloader.get_rel_tol(),
				dim = config.dim,
				num_layers = config.num_layers)
		elif config.model == "CompGCN":
			kge_model = model_class(
				ent_tol = dataloader.get_ent_tol(),
				rel_tol = dataloader.get_rel_tol(),
				dim = config.dim,
				opn = config.opn,
				fet_drop = config.fet_drop,
				hid_drop = config.hid_drop,
				margin = config.margin,
				decoder_model = config.decoder_model)

		# define the loss function
		loss_class = import_class(f"unike.module.loss.{config.loss}")
		if config.loss == 'MarginLoss':
			loss = loss_class(
				adv_temperature = config.adv_temperature,
				margin = config.margin
			)
		elif config.loss in ['SigmoidLoss', 'SoftplusLoss']:
			loss = loss_class(adv_temperature = config.adv_temperature)
		elif config.loss == 'RGCNLoss':
			loss = loss_class(
				model = kge_model,
				regularization = config.regularization
			)
		elif config.loss == 'CompGCNLoss':
			loss = loss_class(model = kge_model)
		
		# define the strategy
		strategy_class = import_class(f"unike.module.strategy.{config.strategy}")
		if config.strategy == 'NegativeSampling':
			model = strategy_class(
				model = kge_model,
				loss = loss,
				regul_rate = config.regul_rate,
				l3_regul_rate = config.l3_regul_rate
			)
		elif config.strategy == 'RGCNSampling':
			model = strategy_class(
				model = kge_model,
				loss = loss
			)
		elif config.strategy == 'CompGCNSampling':
			model = strategy_class(
				model = kge_model,
				loss = loss,
				smoothing = config.smoothing,
				ent_tol = dataloader.train_sampler.ent_tol
			)

		# test the model
		tester_class: type[Tester] = import_class(f"unike.config.{config.tester}")
		tester = tester_class(
			model = kge_model,
			data_loader = dataloader,
			prediction = config.prediction,
			use_tqdm = config.use_tqdm,
			use_gpu = config.use_gpu,
			device = config.device
		)

		# # train the model
		trainer_class: type[Trainer] = import_class(f"unike.config.{config.trainer}")
		trainer = trainer_class(
			model = model,
			data_loader = dataloader.train_dataloader(),
			epochs = config.epochs,
			lr = config.lr,
			opt_method = config.opt_method,
			use_gpu = config.use_gpu,
			device = config.device,
			tester = tester,
			test = True,
			valid_interval = config.valid_interval,
			log_interval = config.log_interval,
			save_path = config.save_path,
			use_early_stopping = config.use_early_stopping,
			metric = config.metric,
			patience = config.patience,
			delta = config.delta,
			wandb_logger = wandb_logger
		)
		trainer.run()