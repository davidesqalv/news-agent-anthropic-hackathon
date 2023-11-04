from typing import List


class Utils:
    @classmethod
    def is_list_with_all_numbers_up_to(cls, nums: List[int], max_num: int) -> bool:
        nums = sorted(nums)
        i = 0
        for num in nums:
            if num != i:
                return False
            i += 1
        return True
