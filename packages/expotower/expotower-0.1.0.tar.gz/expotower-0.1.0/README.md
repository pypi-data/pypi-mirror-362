# Expotower

A tiny Python library for evaluating exponential towers.

## Example

```python
from expotower import expotower, log10_estimate, repeat

print(expotower(10, 20))             # 10^20
print(log10_estimate(10, 20, 30))    # ≈ log10 of result
print(repeat(10, 3))                 # 10^(10^10)
