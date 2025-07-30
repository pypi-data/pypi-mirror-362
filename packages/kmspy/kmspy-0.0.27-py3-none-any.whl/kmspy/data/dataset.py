from __future__ import annotations


from collections import defaultdict
import copy
from itertools import product
import logging
import random
import re
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, Set

import numpy as np

from .prefetch_generator import PrefetchGenerator
from ..utils import is_available
from ..utils._proxy_class import ObservableList


logger = logging.getLogger(__name__)


class Dataset:
    """
    """
    
    def __init__(self, data: List[Dict[str, Any]] = None, *args, **kwargs) -> None:
        self.ignore_keys_for_statistics = kwargs.get("ignore_keys_for_statistics", set())
        if isinstance(self.ignore_keys_for_statistics, list):
            self.ignore_keys_for_statistics = set(self.ignore_keys_for_statistics)
        self.data = ObservableList()
        if data is None:
            pass
        else:
            if isinstance(data, list):
                if data:
                    if isinstance(data[0], dict):
                        pass
                    else:
                        raise(ValueError("각각의 요소는 dict 타입이어야 합니다."))
            else:
                raise(ValueError("data는 list 타입이어야 합니다."))

        self.data.extend(data) if data is not None else None
        self._num_data = None
        self._statistics = None
    
    def update_states(func):
        def wrapper(self, *args, **kwargs):
            if self._num_data is None or self._statistics is None or self.data.has_changed:
                self._get_statistics()
                self._num_data = len(self.data)
                self.data.has_changed = False
            return func(self, *args, **kwargs)
        return wrapper            

    def shuffle(self):
        random.shuffle(self.data)

    def append(self, data: Dict[str, Any]) -> None:
        self.data.append(data)

    def drop(self, condition: function) -> Dataset:
        return self.filter(lambda x: not condition(x))

    def filter(self, condition: function) -> Dataset:
        return Dataset(list(filter(condition, self.data)), ignore_keys_for_statistics=copy.deepcopy(self.ignore_keys_for_statistics))

    def merge(self, key: str, values: Union[List[str], Tuple[str]], sort: bool = True, remain: bool = False, prefix: str = "old") -> Dataset:
        if isinstance(values, (list, tuple)):
            if sort:
                values = sorted([str(v) for v in values])
            new_values = "+".join(values)
            new_data = [{k: (new_values if (key == k and d[k] in values) else d[k]) for k in d.keys()} for d in self.data]
            if remain:
                for td, d in zip(new_data, self.data):
                    td[f"{prefix}_{key}"] = d[key]
            return Dataset(new_data, ignore_keys_for_statistics=copy.deepcopy(self.ignore_keys_for_statistics))
        else:
            raise TypeError("unsupported operand type(values) for merge")

    def _get_statistics(self):
        _statistics = defaultdict(lambda: defaultdict(int))
        for d in self.data:
            for k, v in d.items():
                if k in self.ignore_keys_for_statistics:
                    continue
                _statistics[k][v] += 1
        self._statistics = {k1: dict(v1) for k1, v1 in _statistics.items()}

    @update_states
    def statistics(self, keys: Optional[Union[List[str], Tuple[str], Set[str], str]] = None):
        if keys is not None and isinstance(keys, str):
            keys = set([keys])
        if keys is not None:
            tmp = {}
            for k in keys:
                tmp[k] = self._statistics[k]
            return tmp
        else:
            return self._statistics

    def combination_statistics(self, keys: Union[List[str], Tuple[str], Set[str]], views: Optional[Union[List[str], Tuple[str], Set[str], str]] = None) -> List[Dict[str, Any]]:
        def _cond(keys, values):
            def _wrapper(data):
                for k, v in zip(keys, values):
                    if data[k] == v:
                        pass
                    else:
                        b = False
                        break
                else:
                    b = True
                return b
            return _wrapper

        if not isinstance(keys, list):
            keys = list(keys)
        
        if views is not None:
            if isinstance(views, str):
                views = [views]
                
        _kvs = {k: list(v.keys()) for k, v in self.statistics(keys).items() if k in keys}

        combinations = _kvs[keys[0]]
        for i in range(len(keys)-1):
            combinations = ["\x1b".join(p) for p in product(combinations, _kvs[keys[i+1]])]
        combinations = [c.split("\x1b") for c in combinations]

        _statistics = []
        for c in combinations:
            ds = self.filter(_cond(keys, c))
            if ds.num_data > 0:
                _tmp = {k: v for k, v in zip(keys, c)}
                if views:
                    _ds_statistics = ds.statistics()
                    for v in views:
                        _tmp[v] = list(set(_ds_statistics[v]))
                _statistics.append(_tmp)
                _tmp["count"] = ds.num_data
        return _statistics
        
    def print_statistics(self, max_display: int = 10, keys: Optional[Union[List[str], Tuple[str], Set[str], str]] = None, print_all: bool = False):
        if print_all:
            max_display = int(1e10)
        _warn = True
        _statistics = self.statistics(keys)
        _repr = []
        for k, v in _statistics.items():
            _tmp = []
            for _i, (_k, _v) in enumerate(v.items()):
                if _i+1 == max_display+1:
                    if not print_all and _warn:
                        logger.warning(f"표시할 요소의 개수가 {max_display:d}개를 초과합니다. 모든 요소를 표시하려면 'print_all=True' 옵션을 사용하세요.")
                        _warn = False
                    _tmp.append("...")
                    break
                _tmp.append(f"{_k if _v == 1 else f'{_k}({_v})'}")
            _repr.append(f"{k}: {', '.join(_tmp)}")
        _repr = "\n".join(_repr)
        _repr = re.sub(r"^", " " * 4, _repr, 0, re.M)
        print(f"Dataset: {self.num_data}\n{_repr}")

    def __add__(self, other: Dataset) -> Dataset:
        cls = Dataset()
        cls.data.extend(copy.deepcopy(self.data))
        cls.data.extend(copy.deepcopy(other.data))
        cls.ignore_keys_for_statistics.add(copy.deepcopy(self.ignore_keys_for_statistics))
        cls.ignore_keys_for_statistics.add(copy.deepcopy(other.ignore_keys_for_statistics))
        return cls

    def __radd__(self, other: Dataset) -> Dataset:
        if not isinstance(other, Dataset):
            other = Dataset()
        return self + other

    def __getitem__(self, index: Union[int, slice]) -> Dataset:
        cls = Dataset()
        cls.ignore_keys_for_statistics.add(copy.deepcopy(self.ignore_keys_for_statistics))
        data = self.data[index]
        if isinstance(data, dict):
            cls.data.append(data)
        else:
            cls.data.extend(data)
        return cls

    def __len__(self) -> int:
        return self.num_data

    @property
    @update_states
    def num_data(self):
        return self._num_data

    def __repr__(self):
        return f"Dataset: {self.num_data}\n"

    def __iter__(self):
        return iter(self.data)


class DataLoader:
    def __init__(self, dataset: Dataset, shuffle: bool = False, batch_size: int = 1, collate_fn: Optional[Callable] = None, prefetch_factor: int = 1, num_workers: int = 1, format: Optional[str] = None, padding_value: int = 0, **kwargs) -> None:
        self.dataset = dataset
        self._shuffle = shuffle
        self._batch_size = batch_size
        self._collate_fn = collate_fn
        self._prefetch_factor = prefetch_factor
        self._num_workers = num_workers
        self.set_format(format)
        self._padding_value = padding_value

    def make_gen(self):
        if hasattr(self, "_gen"):
            if isinstance(self._gen, PrefetchGenerator) and self._gen._is_running:
                # 실행 중
                pass
            else:
                # stop된 상태
                self._gen = PrefetchGenerator(self.dataset.data, num_prefetch=self._prefetch_factor*self._batch_size, num_workers=self._num_workers, shuffle=self._shuffle, processing_func=self._collate_fn, name="DataLoader", start=True)
        else:
            # 최초 생성
            self._gen = PrefetchGenerator(self.dataset.data, num_prefetch=self._prefetch_factor*self._batch_size, num_workers=self._num_workers, shuffle=self._shuffle, processing_func=self._collate_fn, name="DataLoader", start=True)

    def set_format(self, format):
        self._format = format if format in {"tf", "tensorflow", "torch", "pytorch"} else "numpy"
        if self._format in {"tf", "tensorflow"}:
            if is_available("tensorflow"):
                import tensorflow as tf
            else:
                import tensorflow as tf  # raise
        elif self._format in {"torch", "pytorch"}:
            if is_available("torch"):
                import torch
            else:
                import torch  # raise

    def as_format(self, batch):
        if is_available("numpy"):
            ranks = [len(b) for b in batch]
            keys = [list(b.keys()) for b in batch]
            types = [[type(_b) for _b in b.values()] for b in batch]
            rank = np.unique(ranks)
            if len(rank) == 1:
                rank = rank[0]
                keys = keys[0]
                types = types[0]
                datas = [[] for _ in range(rank)]
                for b in batch:
                    for i in range(rank):
                        datas[i].append(b[keys[i]])
                for i, data in enumerate(datas):
                    if types[i] in {np.ndarray, list, tuple, int, float}:
                        max_shape = np.amax(np.array([np.shape(d) if hasattr(d, "__len__") else 1 for d in data]), axis=0)
                        min_shape = np.amin(np.array([np.shape(d) if hasattr(d, "__len__") else 1 for d in data]), axis=0)
                        if np.all(max_shape == min_shape):
                            datas[i] = np.array(data)
                        else:
                            padded_begin = np.zeros(max_shape.shape).astype(np.int32)
                            datas[i] = np.array([np.pad(d, np.stack((padded_begin, max_shape - np.shape(d))).T, constant_values=self._padding_value) for d in data])
                    elif types[i] is dict:
                        tmp_dict = {k: [] for k in data[0].keys()}
                        for d in data:
                            for k, v in d.items():
                                tmp_dict[k].append(v)
                        datas[i] = tmp_dict
                datas = {k: v for k, v in zip(keys, datas)}
            else:
                raise ValueError("collate_fn에서 출력하는 데이터의 개수가 동일하지 않습니다.")
        else:
            raise ModuleNotFoundError("numpy")
        if self._format == "tf":
            if is_available("tensorflow"):
                import tensorflow as tf
                for k, v in datas.items():
                    if isinstance(v, np.ndarray):
                        datas[k] = tf.convert_to_tensor(v)
            else:
                raise ModuleNotFoundError("tensorflow")
        elif self._format == "torch":
            if is_available("torch"):
                import torch
                for k, v in datas.items():
                    if isinstance(v, np.ndarray):
                        datas[k] = torch.tensor(v)
            else:
                raise ModuleNotFoundError("torch")
        return datas

    def reset_gen(self):
        self._gen.stop()
        del self._gen

    def __getitem__(self, index: Union[int, slice]):
        if isinstance(index, int):
            if self._collate_fn is not None:
                _data = self._collate_fn(self.dataset.data[index:(index+1)*self._batch_size])
            else:
                _data = self.dataset.data[index:(index+1)*self._batch_size]
            return self.as_format(_data)
        else:
            start = index.start if index.start else 0
            step = index.step if index.step else 1
            assert step == 1
            stop = index.stop
            new_slice = slice(start, stop*self._batch_size, step)
            _ds = DataLoader(dataset=self.dataset[new_slice], shuffle=self._shuffle, batch_size=self._batch_size, collate_fn=self._collate_fn, prefetch_factor=self._prefetch_factor, num_workers=self._num_workers, format=self._format, padding_value=self._padding_value)
            for _batch in _ds:
                yield _batch

    def __next__(self):
        data = []
        for _ in range(self._batch_size):
            try:
                _data = next(self._gen)
                # None 또는 빈 리스트 등의 값이 나오면 버림
                if _data:
                    data.append(_data)
            except StopIteration:
                if data:
                    return self.as_format(data)
                else:
                    raise StopIteration
        return self.as_format(data)

    def __iter__(self):
        self.make_gen()
        try:
            while True:
                yield self.__next__()
        except StopIteration:
            self.reset_gen()
        except GeneratorExit:
            self.reset_gen()

    def __len__(self):
        return self.dataset.num_data//self._batch_size + (0 if self.dataset.num_data%self._batch_size == 0 else 1)