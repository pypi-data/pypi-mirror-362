# uintlib

A simple, lightweight Python library providing fixed-size unsigned and signed integer types  
(`UInt8`, `Int8`, `UInt16`, `Int16`, `UInt32`, `Int32`, `UInt64`, `Int64`) with correct wrapping behavior  
and easy arithmetic operations. Perfect for network programming, binary protocols, emulation, and low-level data manipulation.

---

## Why?

Python's built-in integers are unbounded and do not overflow, which is convenient but not suitable for all use cases, especially when working with:

- Binary protocols requiring precise bit widths  
- Network packet parsing and construction  
- Emulators or hardware interfacing code  
- Embedded systems data serialization/deserialization  
- Situations where overflow behavior must match C, Rust, Go, or other languages

This library provides integer classes that behave like fixed-size integers in low-level languages, including overflow wrapping and bit masking.

---

## Features

- Fixed bit widths: 8, 16, 32, and 64 bits  
- Both unsigned (`UInt*`) and signed (`Int*`) types  
- Proper overflow wrapping on arithmetic operations (`+`, `-`)  
- Supports comparison operators (`==`, `!=`, `<`, `>`, etc.)  
- Intuitive constructor with automatic bit masking  
- Supports integer conversion via `int()`  
- Easy to extend or customize  
- Lightweight, no external dependencies  

---

## Installation

You can install from PyPI (once published) using:

    pip install uintlib

---

## Usage

```python
from uintlib.uint import UInt8, Int16, UInt32, Int64

a = UInt8(250)
b = UInt8(10)

print(a + b)          # UInt8(4) — wraps around at 255 (250 + 10 = 260 → 4)
print(int(a + b))     # 4 as Python int

x = Int16(-20000)
y = Int16(10000)

print(x + y)          # Int16(-10000) — correct 16-bit signed overflow
print(int(x + y))     # -10000

# Comparisons work as expected
print(a == UInt8(4))  # True
print(x < y)          # True
```
