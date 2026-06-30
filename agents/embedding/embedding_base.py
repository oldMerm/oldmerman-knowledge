"""Description
向量化服务公共父类限定

Date: 2026-6-29
Created by oldmerman
"""
from abc import ABC, abstractmethod
from typing import List,  Dict, Tuple
import logging
import time
from agents.embedding.embedding_common import EmbeddingsGetterParam, EmbeddingsResponseParam

logger = logging.getLogger(__name__)

class BaseEmbeddingAdapter(ABC):
    """
    向量化适配器基类 - 固定流程骨架
    策略：异常隔离 + 占位处理
    """

    # 重试配置（子类可覆盖）
    MAX_RETRIES = 3
    INITIAL_RETRY_DELAY = 1  # 秒
    RETRY_BACKOFF = 2  # 退避倍数

    def get_simple_embeddings(self, param: EmbeddingsGetterParam) -> EmbeddingsResponseParam:
        """
        统一获取用于query的向量化数据，追求响应速度
        """
        client = self._get_client(param)
        response = self._send_request(client, param.doc, param)
        embeddings, usage, model = self._parse_response(response)
        return EmbeddingsResponseParam(
            model_name=model,
            data=embeddings
        )


    def get_embeddings(self, param: EmbeddingsGetterParam) -> EmbeddingsResponseParam:
        """
        模板方法：定义统一流程，子类只需实现差异点
        """
        # 1. 前置校验
        self._validate_param(param)

        # 2. 获取客户端（差异点）
        client = self._get_client(param)

        # 3. 分批处理
        batch_size = self._get_batch_size()
        texts = param.doc
        batches = [texts[i:i + batch_size] for i in range(0, len(texts), batch_size)]

        logger.info(f"开始处理 {len(texts)} 条文本，分 {len(batches)} 批，每批 {batch_size} 条")

        # 存储结果
        all_embeddings = []
        failed_batch_indices = []  # 记录失败批次索引
        failed_batch_details = []  # 记录失败详情
        total_prompt_tokens = 0
        total_completion_tokens = 0
        total_tokens = 0
        model_name = None

        # 4. 逐批处理（异常隔离）
        for batch_idx, batch in enumerate(batches):
            try:
                # 带重试的发送
                response = self._send_with_retry(client, batch, param)

                if response is None:
                    # 重试全部失败
                    raise Exception(f"批次 {batch_idx + 1} 重试 {self.MAX_RETRIES} 次均失败")

                # 解析响应
                embeddings, usage, model = self._parse_response(response)

                # 累加成功结果
                all_embeddings.extend(embeddings)
                total_prompt_tokens += usage.get("prompt_tokens", 0)
                total_completion_tokens += usage.get("completion_tokens", 0)
                total_tokens += usage.get("total_tokens", 0)
                if model_name is None:
                    model_name = model

                logger.debug(f"批次 {batch_idx + 1}/{len(batches)} 成功，条数: {len(batch)}")

            except Exception as e:
                # 异常隔离：记录失败，但不中断流程
                failed_batch_indices.append(batch_idx)
                failed_batch_details.append({
                    "batch_index": batch_idx,
                    "batch_size": len(batch),
                    "error": str(e)
                })

                # 补占位向量（保持总长度一致，便于上层处理）
                all_embeddings.extend([None] * len(batch))

                logger.error(f"批次 {batch_idx + 1}/{len(batches)} 失败: {str(e)}")

        # 5. 记录失败统计
        if failed_batch_indices:
            logger.warning(
                f"处理完成，共 {len(failed_batch_indices)}/{len(batches)} 个批次失败，"
                f"失败索引: {failed_batch_indices}"
            )
        else:
            logger.info(f"处理完成，全部 {len(batches)} 个批次成功")

        # 6. 构建返回结果
        return EmbeddingsResponseParam(
            model_name=model_name,
            data=all_embeddings,  # 包含 None 占位
            tokens={
                "prompt_tokens": total_prompt_tokens,
                "completion_tokens": total_completion_tokens,
                "total_tokens": total_tokens
            },
            failed_batches=failed_batch_indices,
            failed_details=failed_batch_details
        )

    @abstractmethod
    def _get_client(self, param: EmbeddingsGetterParam):
        """初始化厂商客户端"""
        pass

    @abstractmethod
    def _send_request(self, client, batch: List[str], param: EmbeddingsGetterParam):
        """发送请求并返回原始响应"""
        pass

    @abstractmethod
    def _parse_response(self, response) -> Tuple[List[List[float]], Dict[str, int], str]:
        """
        解析响应
        返回: (embeddings, usage_dict, model_name)
        usage_dict: {"prompt_tokens": int, "completion_tokens": int, "total_tokens": int}
        """
        pass

    def _get_batch_size(self) -> int:
        """默认批次大小，子类可重写"""
        return 50

    def _validate_param(self, param: EmbeddingsGetterParam) -> None:
        """参数校验，子类可重写增强"""
        if not param.doc:
            raise ValueError("输入文本列表不能为空")
        if len(param.doc) == 0:
            raise ValueError("文本列表为空")
        if not param.api_key:
            raise ValueError("API Key 不能为空")

    def _get_retry_config(self) -> Dict[str, int]:
        """获取重试配置，子类可重写"""
        return {
            "max_retries": self.MAX_RETRIES,
            "initial_delay": self.INITIAL_RETRY_DELAY,
            "backoff": self.RETRY_BACKOFF
        }

    def _send_with_retry(self, client, batch: List[str], param: EmbeddingsGetterParam):
        """
        带指数退避重试的发送
        返回: 响应对象，若全部失败返回 None
        """
        retry_config = self._get_retry_config()
        max_retries = retry_config["max_retries"]
        initial_delay = retry_config["initial_delay"]
        backoff = retry_config["backoff"]

        last_exception = None

        for attempt in range(max_retries):
            try:
                # 调用子类实现的发送方法
                response = self._send_request(client, batch, param)
                return response

            except Exception as e:
                last_exception = e

                if attempt == max_retries - 1:
                    # 最后一次重试失败
                    logger.error(
                        f"批次重试 {max_retries} 次全部失败，"
                        f"最后错误: {str(e)}"
                    )
                    return None

                # 计算退避延迟
                delay = initial_delay * (backoff ** attempt)
                logger.warning(
                    f"第 {attempt + 1} 次发送失败，{delay:.2f}s 后重试: {str(e)}"
                )
                time.sleep(delay)

        return None

