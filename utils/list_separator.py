from typing import List, Any

class ListSeparator:
    @staticmethod
    def chunk_array(arr: List[Any], chunk_size: int) -> List[List[Any]]:
        """
        将一个长度为 n 的数组切分为长度为 x 的若干个子数组

        Args:
            arr: 要切分的原始数组
            chunk_size: 每个子数组的长度（最后一块可能小于该值）

        Returns:
            切分后的二维数组列表
        """
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")

        if not arr:
            return []

        return [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]

    @staticmethod
    def merge_chunks(chunks: List[List[Any]]) -> List[Any]:
        """
        将切分后的子数组合并回原始数组

        Args:
            chunks: 二维数组列表（由 chunk_array 生成的）

        Returns:
            合并后的一维数组
        """
        if not chunks:
            return []

        return [item for sublist in chunks for item in sublist]