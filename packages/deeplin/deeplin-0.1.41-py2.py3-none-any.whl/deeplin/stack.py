from typing import List, Optional, Tuple, Union

import torch


def select_part(value: torch.Tensor, start_index: torch.LongTensor, offset: torch.LongTensor):
    # not include the last element
    max_offset = offset.max().item()
    return select_part_lower_than_max_offset(value, start_index, max_offset)


def select_part_lower_than_max_offset(value: torch.Tensor, start_index: torch.LongTensor, max_offset: int):
    B, L = value.size(0), value.size(1)
    rest_shape = tuple(value.size()[2:]) if len(value.size()) > 2 else ()
    end = start_index + max_offset
    mask = torch.arange(L).unsqueeze(0).expand(B, L)
    mask_low = mask < end.unsqueeze(1)
    mask_high = mask >= start_index.unsqueeze(1)
    mask = mask_low & mask_high
    # logger.info(f"{value.size()}, {start_index.size()}, {max_offset}, {mask.size()}")
    while len(mask.shape) < len(value.shape):
        mask = mask.unsqueeze(-1)
    selected_value = torch.masked_select(value, mask)
    selected_value = selected_value.view(B, max_offset, *rest_shape)
    return selected_value


class Stack(object):
    """
    Batch of stacks implemented in PyTorch.

    Parameters:
        batch_size (int): batch size
        stack_size (int): max stack size
        shape (tuple of int, optional): shape of each value in the stack
        dtype (torch.dtype, optional): dtype
        device (torch.device, optional): device
    """

    def __init__(
        self,
        batch_size: int,
        stack_size: int,
        *shape: Optional[Tuple],
        dtype: Optional[torch.dtype] = None,
        device: Optional[torch.device] = None,
    ):
        self.stack = torch.zeros(batch_size, stack_size, *shape, dtype=dtype, device=device)
        self.SP = torch.zeros(batch_size, dtype=torch.long, device=device)
        self.batch_size = batch_size
        self.stack_size = stack_size
        self.shape = shape
        self.dtype = dtype
        self.device = device

    def copy_from(self, other: "Stack"):
        self.stack.copy_(other.stack)
        self.SP.copy_(other.SP)
        self.batch_size = other.batch_size
        self.stack_size = other.stack_size
        self.shape = other.shape
        self.dtype = other.dtype
        self.device = other.device

    def copy_stack_from(self, stack: torch.Tensor):
        stack_size = stack.size(1)
        self.stack[:, :stack_size] = stack

    def push_one_number(self, mask: torch.BoolTensor, value: int):
        value = torch.full((mask.sum(),), value, dtype=torch.long, device=mask.device)
        self.push(mask, value)

    def push(self, mask: torch.BoolTensor, value: torch.Tensor):
        # mask  (B,), M = sum(mask)
        # value (M, *shape)
        if (self.SP[mask] >= self.stack_size).any():
            raise ValueError("Stack overflow")
        self.stack[mask, self.SP[mask]] = value
        self.SP[mask] += 1

    def push_sequence_of_values(self, mask: torch.BoolTensor, values: List[torch.Tensor]):
        # mask   (B,), M = sum(mask)
        # values [(M, *shape), ...]
        if (self.SP[mask] + len(values) > self.stack_size).any():
            raise ValueError("Stack overflow")
        for i, value in enumerate(values):
            self.stack[mask, self.SP[mask] + i] = value
        self.SP[mask] += len(values)

    def push_multi_lens_values_concatenated(self, mask: torch.BoolTensor, length: torch.LongTensor, values: torch.Tensor):
        # mask   (B,), M = sum(mask)
        # length (M,) = [S1, S2, ...], where S1, S2, ... ( < stack_size) are the lengths of the values
        # values (S, *shape) = cat([(S1, *shape), (S2, *shape)...], dim=0), where S = sum(S1, S2, ...)
        if (self.SP[mask] + length > self.stack_size).any():
            raise ValueError("Stack overflow")
        start_index = torch.cat([torch.zeros(1, dtype=torch.long, device=self.stack.device), length.cumsum(dim=0)[:-1]])
        for i, (ok, l, start) in enumerate(zip(mask, length, start_index)):
            if not ok:  # then length is 0, so we skip
                continue
            self.stack[i, self.SP[i] : self.SP[i] + l] = values[start : start + l]
        self.SP[mask] += length

    def push_multi_lens_values_paded(self, mask: torch.BoolTensor, values: torch.Tensor):
        # mask   (B,), M = sum(mask)
        # values (M, S, *shape) = stack([(S1, *shape), (S2, *shape)...], dim=0), where S = max(S1, S2, ...)
        if (self.SP[mask] + values.size(1) > self.stack_size).any():
            raise ValueError("Stack overflow")
        self.stack[mask, self.SP[mask] : self.SP[mask] + values.size(1)] = values
        self.SP[mask] += values.size(1)

    def push_multi_lens_values(self, mask: torch.BoolTensor, length: torch.LongTensor, values: List[torch.Tensor]):
        # mask   (B,), M = sum(mask)
        # length (M,) = [S1, S2, ...], where S1, S2, ... ( < stack_size) are the lengths of the values
        # values [(S1, *shape), (S2, *shape)...], len(values) == M
        # logger.info(f"{self.SP.shape}, {self.SP[mask].shape}, {length.shape} | {self.SP[mask]}, {length}")
        if (self.SP[mask] + length > self.stack_size).any():
            raise ValueError("Stack overflow")
        for i, (ok, l, value) in enumerate(zip(mask, length, values)):
            if not ok:
                continue
            self.stack[i, self.SP[i] : self.SP[i] + l] = value
        self.SP[mask] += length

    def prepend(self, mask: torch.BoolTensor, value: torch.Tensor):
        # mask  (B,), M = sum(mask)
        # value (M, *shape), where M = sum(mask) or M = 1
        if (self.SP[mask] >= self.stack_size).any():
            raise ValueError("Stack overflow")
        self.stack[mask, 1 : self.SP[mask] + 1] = self.stack[mask, : self.SP[mask]]
        self.stack[mask, 0] = value
        self.SP[mask] += 1

    def prepop(self, mask: torch.BoolTensor=None, length: int = 1):
        # mask   (B,)
        # length (int)
        if mask is None:
            mask = torch.ones(self.batch_size, dtype=torch.bool, device=self.stack.device)
        if (self.SP[mask] < length).any():
            raise ValueError("Stack underflow")
        start_index = torch.full_like(self.SP, length)
        offset = self.SP - length
        rest_values = select_part(self.stack, start_index, offset)
        self.stack[mask, :offset.max()] = rest_values[mask]
        self.SP[mask] -= length

    def prepop_multi_lens(self, mask: torch.BoolTensor, length: torch.LongTensor):
        # mask   (B,), M = sum(mask)
        # length (M,) = [S1, S2, ...], where S1, S2, ... ( < stack_size) are the lengths of the values
        if (self.SP[mask] < length).any():
            raise ValueError("Stack underflow")
        for i, (ok, l) in enumerate(zip(mask, length)):
            if not ok:
                continue
            self.stack[i, : self.SP[i] - l] = self.stack[i, l:]
        self.SP[mask] -= length

    def pop(self, mask: Optional[torch.BoolTensor] = None):
        # mask  (B,)
        return self.pop_fixed_length(mask, 1)

    def pop_multi_lens(self, mask: Optional[torch.BoolTensor], length: torch.LongTensor):
        # mask   (B,), M = sum(mask)
        # length (M,) = [S1, S2, ...], where S1, S2, ... ( < stack_size) are the lengths of the values
        if (self.SP[mask] < length).any():
            raise ValueError("Stack underflow")
        for i, (ok, l) in enumerate(zip(mask, length)):
            if not ok:
                continue
            self.SP[i] -= l
        if mask is None:
            mask = torch.ones(self.batch_size, dtype=torch.bool, device=self.stack.device)
        self.SP[mask] -= length
        max_length = length.max()
        return self.stack[mask, self.SP[mask] : self.SP[mask] + max_length]

    def pop_fixed_length(self, mask: Optional[torch.BoolTensor] = None, length: int = 1):
        # mask   (B,), M = sum(mask)
        # length (int)
        if (self.SP[mask] < length).any():
            raise ValueError("Stack underflow")
        if mask is None:
            mask = torch.ones(self.batch_size, dtype=torch.bool, device=self.stack.device)
        self.SP[mask] -= length
        return self.stack[mask, self.SP[mask] : self.SP[mask] + length]

    def replace(self, mask: torch.BoolTensor, value: torch.Tensor):
        # mask  (B,), M = sum(mask)
        # value (M, *shape), where M = sum(mask) or M = 1
        if (self.SP[mask] < 1).any():
            raise ValueError("Stack underflow")
        self.stack[mask, self.SP[mask] - 1] = value

    def replace_multi_lens(self, mask: torch.BoolTensor, length: torch.LongTensor, values: List[torch.Tensor]):
        # mask   (B,), M = sum(mask)
        # length (M,) = [S1, S2, ...], where S1, S2, ... ( < stack_size) are the lengths of the values
        # values [(S1, *shape), (S2, *shape)...], len(values) == M
        if (self.SP[mask] < length).any():
            raise ValueError("Stack underflow")
        for i, (ok, l, value) in enumerate(zip(mask, length, values)):
            if not ok:
                continue
            self.stack[i, self.SP[i] - l : self.SP[i]] = value

    def replace_fixed_length(self, mask: torch.BoolTensor, length: int, value: torch.Tensor):
        # mask  (B,), M = sum(mask)
        # value (M, *shape), where M = sum(mask) or M = 1
        if (self.SP[mask] < length).any():
            raise ValueError("Stack underflow")
        self.stack[mask, self.SP[mask] - length : self.SP[mask]] = value

    def top(self, mask: Optional[torch.BoolTensor] = None):
        # mask  (B,), M = sum(mask)
        if (self.SP < 1).any():
            raise ValueError("Stack is empty")
        if mask is None:
            mask = torch.ones(self.batch_size, dtype=torch.bool, device=self.stack.device)
        return self.stack[mask, self.SP[mask] - 1]

    def __len__(self):
        return self.SP

    @property
    def capacity(self):
        return self.stack_size - self.SP

    @property
    def max_size(self):
        return self.SP.max()

    @property
    def size(self):
        return self.SP

    def data(self, crop_size: Optional[int] = None, drop_top_elements: bool = False):
        if crop_size is not None:
            if drop_top_elements:
                return self.stack[:, :crop_size]
            else:
                # drop bottom elements
                max_offset = self.SP.max().item()
                start_index = torch.zeros_like(self.SP)
                if crop_size < max_offset:
                    max_offset = crop_size
                    start_index = torch.where(self.SP > crop_size, self.SP - crop_size, start_index)
                return select_part_lower_than_max_offset(self.stack, start_index, max_offset)
        return self.stack[:, : self.SP.max()]

    def full(self) -> torch.BoolTensor:
        return self.SP >= self.stack_size

    def exist_full(self):
        return self.full().any().item()

    def all_full(self):
        return self.full().all().item()

    def where_not_full(self):
        return self.SP < self.stack_size

    def clear(self):
        self.SP.zero_()

    def data_at(self, index: Union[torch.LongTensor, int]):
        return self.stack[:, index]
