from typing import List, Tuple, Optional

def binary_search(arr: List[float], target: float) -> Tuple[int, Optional[float]]:
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None
    
    while left <= right:
        iterations += 1
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return iterations, arr[mid]
        elif arr[mid] < target:
            left = mid + 1
        else:
            upper_bound = arr[mid]
            right = mid - 1
    
    return iterations, upper_bound


sorted_floats = [0.5, 1.2, 2.3, 3.7, 4.4, 5.9, 7.8]
target_value = 3.5

result = binary_search(sorted_floats, target_value)
print(result)
