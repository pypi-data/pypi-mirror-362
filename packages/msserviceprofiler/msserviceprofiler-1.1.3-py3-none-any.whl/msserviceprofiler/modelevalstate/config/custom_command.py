# -*- coding: utf-8 -*-
# Copyright (c) Huawei Technologies Co., Ltd. 2023-2024. All rights reserved.
import os
import shutil
from loguru import logger
from pydantic import BaseModel
from msserviceprofiler.msguard import Rule
 
 
class BenchmarkCommandConfig(BaseModel):
    dataset_path: str = ""
    dataset_type: str = ""
    model_name: str = ""
    model_path: str = ""
    test_type: str = "client"
    max_output_len: str = ""
    http: str = "http://127.0.0.1:1025"
    management_http: str = "http://127.0.0.1:1026"
    warmup_size: str = "1"
    tokenizer: str = "True"
 
 
class BenchmarkCommand:
    def __init__(self, benchmark_command_config: BenchmarkCommandConfig):
        self.process = shutil.which("benchmark")
        self.benchmark_command_config = benchmark_command_config
 
    @property
    def command(self):
        if not Rule.input_file_read.is_satisfied_by(self.benchmark_command_config.dataset_path):
            logger.error("the file of dataset_path is not safe, please check")
            return None
        
        return [self.process,
                "--DatasetPath", self.benchmark_command_config.dataset_path,
                "--DatasetType", self.benchmark_command_config.dataset_type,
                "--ModelName", self.benchmark_command_config.model_name,
                "--ModelPath", self.benchmark_command_config.model_path,
                "--TestType", self.benchmark_command_config.test_type,
                "--MaxOutputLen", self.benchmark_command_config.max_output_len,
                "--Http", self.benchmark_command_config.http,
                "--ManagementHttp", self.benchmark_command_config.management_http,
                "--Concurrency", "$CONCURRENCY",
                "--RequestRate", "$REQUESTRATE",
                "--WarmupSize", self.benchmark_command_config.warmup_size,
                "--Tokenizer", self.benchmark_command_config.tokenizer]
 
 
class VllmBenchmarkCommandConfig(BaseModel):
    backend: str = "vllm"
    host: str = "127.0.0.1"
    port: str = "6379"
    model: str = ""
    served_model_name: str = ""
    dataset_name: str = ""
    dataset_path: str = ""
    num_prompts: str = ""
 
 
class VllmBenchmarkCommand:
    def __init__(self, benchmark_command_config: VllmBenchmarkCommandConfig):
        self.benchmark_command_config = benchmark_command_config
 
    @property
    def command(self):
        if not Rule.input_file_read.is_satisfied_by(self.benchmark_command_config.dataset_path):
            logger.error("the file of dataset_path is not safe, please check")
            return None
        return ["python", self.benchmark_command_config.serving,
                "--backend", self.benchmark_command_config.backend,
                "--host", self.benchmark_command_config.host,
                "--port", self.benchmark_command_config.port,
                "--model", self.benchmark_command_config.model,
                "--served-model-name", self.benchmark_command_config.served_model_name,
                "--dataset-name", self.benchmark_command_config.dataset_name,
                "--dataset-path", self.benchmark_command_config.dataset_path,
                "--num-prompts", self.benchmark_command_config.num_prompts,
                "--max-concurrency", "$MAXCONCURRENCY",
                "--request-rate", "$REQUESTRATE",
                "--result-dir", "$MODEL_EVAL_STATE_VLLM_CUSTOM_OUTPUT",
                "--save-result"]
 
 
class MindieCommandConfig(BaseModel):
    pass
 
 
class MindieCommand:
    def __init__(self, command_config: MindieCommandConfig):
        self.command_config = command_config
 
    @property
    def command(self):
        mindie_service_default_path: str = "/usr/local/Ascend/mindie/latest/mindie-service"
        mindie_service_path: str = os.getenv("MIES_INSTALL_PATH", mindie_service_default_path)
        mindie_command_path: str = os.path.join(mindie_service_path, "bin", "mindieservice_daemon")
        return [mindie_command_path]
 
 
class VllmCommandConfig(BaseModel):
    host: str = "127.0.0.1"
    port: str = "6379"
    model: str = ""
    served_model_name: str = ""
 
 
class VllmCommand:
    def __init__(self, command_config: VllmCommandConfig):
        self.process = shutil.which("vllm")
        self.command_config = command_config
 
    @property
    def command(self):
        return [self.process, "serve",
                self.command_config.model,
                "--served-model-name", self.command_config.served_model_name,
                "--host", self.command_config.host,
                "--port", self.command_config.port,
                "--max-num-batched-tokens", "$MAX_NUM_BATCHED_TOKENS",
                "--max-num-seqs", "$MAX_NUM_SEQS"]