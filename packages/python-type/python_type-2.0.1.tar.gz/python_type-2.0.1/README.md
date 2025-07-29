# Python Type Validator

A powerful, flexible, and easy-to-use Python decorator for runtime type validation. This library provides comprehensive type checking for function parameters and return values with detailed error messages and multiple configuration options.

## 🚀 Features

- **Runtime Type Validation**: Validates function parameters and return types at runtime
- **Type Hints Support**: Automatically uses Python type hints for validation
- **Flexible Configuration**: Multiple validation modes and override options
- **Complex Type Support**: Handles `List[int]`, `Dict[str, int]`, `Union`, `Optional`, and more
- **Detailed Error Messages**: Rich, colorful error messages with file location and context
- **Custom Type Mappings**: Define custom type requirements for parameters
- **Method & Function Support**: Works with both regular functions and class methods
- **Performance Optimized**: Minimal overhead with efficient type checking

## 📦 Installation

pip install python-type

## 🎯 Quick Start

```python
from python_type import validate_data

# Basic usage with type hints
@validate_data()
def greet(name: str, age: int) -> str:
    return f"Hello {name}, you are {age} years old"

# This will work
result = greet("Alice", 25)

# This will raise ValidationError
greet("Alice", "25")  # age should be int, not str
```

## 🛠️ Core Functions

### `validate_data()`

The main decorator function that provides comprehensive type validation.

**Parameters:**
- `strict: bool = True` - Validates all parameters with type hints
- `validate_return: bool = True` - Validates return type against type hints
- `custom_types: Dict[str, Any] = None` - Custom type mappings for parameters
- `**types_override` - Override specific parameter types

### `create_validator()`

Creates custom validators with predefined type mappings.

**Parameters:**
- `custom_types: Dict[str, Any]` - Dictionary with parameter type mappings
- `**kwargs` - Additional arguments passed to `validate_data()`

## 📚 Usage Examples

### Basic Type Validation

```python
@validate_data()
def calculate_area(length: float, width: float) -> float:
    return length * width

# ✅ Valid
area = calculate_area(5.0, 3.0)

# ❌ Invalid - will raise ValidationError
area = calculate_area("5", 3.0)  # length should be float
```

### Complex Type Validation

```python
from typing import List, Dict, Optional

@validate_data()
def process_users(users: List[Dict[str, str]], active_only: bool = True) -> Optional[str]:
    if not users:
        return None
    return f"Processed {len(users)} users"

# ✅ Valid
result = process_users([{"name": "Alice", "email": "alice@example.com"}])

# ❌ Invalid - wrong list content type
result = process_users([{"name": "Alice", "age": 25}])  # age should be str
```

### Parameter Override

```python
@validate_data(age=(int, str))  # Accept both int and str for age
def register_user(name: str, age: int, email: str) -> bool:
    return True

# ✅ Both valid
register_user("Alice", 25, "alice@example.com")      # age as int
register_user("Bob", "30", "bob@example.com")        # age as str
```

### Non-Strict Mode

```python
@validate_data(strict=False, user_id=int)  # Only validate user_id
def get_user_profile(user_id, include_private=False):
    return f"Profile for user {user_id}"

# ✅ Valid - only user_id is validated
profile = get_user_profile(123, "any_type_here")

# ❌ Invalid - user_id must be int
profile = get_user_profile("123", "any_type_here")
```

### Custom Type Mappings

```python
@validate_data(custom_types={'email': str, 'age': int, 'active': bool})
def create_user(email, age, active):  # No type hints needed
    return f"User created: {email}"

# ✅ Valid
create_user("user@example.com", 25, True)

# ❌ Invalid - age should be int
create_user("user@example.com", "25", True)
```

### Disable Return Validation

```python
@validate_data(validate_return=False)
def log_message(message: str) -> None:
    print(message)
    return "Actually returns string"  # No error even though hint says None
```

### Creating Custom Validators

```python
# Create a validator for API endpoints
api_validator = create_validator({
    'user_id': int,
    'data': dict,
    'api_key': str
})

@api_validator
def api_endpoint(user_id, data, api_key):
    return {"status": "success"}

# Create a validator with additional options
strict_validator = create_validator(
    {'price': float, 'quantity': int},
    strict=False,
    validate_return=False
)

@strict_validator
def calculate_total(price, quantity, discount=0):  # discount not validated
    return price * quantity * (1 - discount)
```

## 🎨 Configuration Options

### Validation Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| `strict=True` | Validates all parameters with type hints | Full type safety |
| `strict=False` | Only validates overrides and custom types | Selective validation |
| `validate_return=True` | Validates return type | Complete type checking |
| `validate_return=False` | Skip return validation | Parameter-only validation |

### Type Priority System

The validator uses a priority system for type determination:

1. **`types_override`** (Highest priority) - Direct parameter overrides
2. **`custom_types`** (Medium priority) - Custom type mappings
3. **Type hints** (Lowest priority) - Function annotations (only if `strict=True`)

```python
@validate_data(
    strict=True,                    # Enable type hints
    custom_types={'age': str},      # Override age to str
    age=int                         # Override again to int (highest priority)
)
def example(name: str, age: float):  # age hint is float, but int will be used
    pass
```

## 🔍 Error Messages

The validator provides detailed, colorful error messages with:

- **File location** and line number
- **Function/method context**
- **Parameter details** (name, position, expected vs received types)
- **Value representation** with truncation for large objects
- **Type source** (override, custom_types, or type hint)

### Example Error Output

```
======================================================================
TYPE VALIDATION ERROR
======================================================================
📁 File: /path/to/your/file.py
📍 Line: 42
🔧 Function: calculate_price()
❌ Errors found: 2
======================================================================

💥 ERROR 1:
   Parameter: 'price' (position 1)
   ✅ Expected: float (from type hint)
   ❌ Received: str
   📦 Value: str('19.99')

💥 ERROR 2:
   Parameter: 'quantity' (position 2)
   ✅ Expected: int (from override)
   ❌ Received: str
   📦 Value: str('5')
======================================================================
```

## 🏆 Advanced Features

### Class Method Support

```python
class UserService:
    @validate_data()
    def create_user(self, name: str, email: str) -> dict:
        return {"name": name, "email": email}
    
    @validate_data()
    @classmethod
    def get_user_count(cls, active_only: bool = True) -> int:
        return 42
```

### Union and Optional Types

```python
from typing import Union, Optional

@validate_data()
def process_id(user_id: Union[int, str], data: Optional[dict] = None) -> str:
    return f"Processing {user_id}"

# ✅ All valid
process_id(123)           # int id
process_id("abc")         # str id
process_id(123, None)     # explicit None
process_id(123, {})       # dict data
```

### Complex Container Types

```python
from typing import List, Dict, Tuple, Set

@validate_data()
def complex_function(
    numbers: List[int],
    mapping: Dict[str, float],
    coordinates: Tuple[int, int, int],
    tags: Set[str]
) -> bool:
    return True

# ✅ Valid
complex_function(
    [1, 2, 3],
    {"price": 19.99, "tax": 0.08},
    (10, 20, 30),
    {"python", "validation", "types"}
)
```

## ⚡ Performance Considerations

- **Minimal Overhead**: Type checking only occurs at function call time
- **Efficient Validation**: Uses Python's built-in `isinstance()` and `typing` utilities
- **Smart Caching**: Function signatures are analyzed once per function
- **Optimized Error Generation**: Error messages are only generated when validation fails

## 🤝 Best Practices

1. **Use Type Hints**: Always provide type hints for better code documentation
2. **Selective Validation**: Use `strict=False` for performance-critical code
3. **Custom Validators**: Create reusable validators for common patterns
4. **Error Handling**: Catch `ValidationError` for graceful error handling
5. **Testing**: Validate edge cases and error conditions

```python
from python_type import ValidationError

try:
    result = my_function("invalid", "arguments")
except ValidationError as e:
    logger.error(f"Type validation failed: {e}")
    # Handle error gracefully
```

## 🔧 Exception Handling

The validator raises `ValidationError` (subclass of `ValueError`) for all validation failures:

```python
from python_type import ValidationError

@validate_data()
def divide(a: int, b: int) -> float:
    return a / b

try:
    result = divide("10", 2)
except ValidationError as e:
    print(f"Validation failed: {e}")
except ZeroDivisionError:
    print("Cannot divide by zero")
```

## 🎯 Common Use Cases

### API Input Validation

```python
api_validator = create_validator({
    'user_id': int,
    'payload': dict,
    'api_key': str
})

@api_validator
def api_endpoint(user_id, payload, api_key):
    # Process API request
    return {"status": "success"}
```

### Data Processing Pipelines

```python
@validate_data()
def process_data(raw_data: List[Dict[str, Any]], 
                config: Dict[str, str]) -> List[Dict[str, Any]]:
    # Transform data
    return processed_data
```

### Configuration Validation

```python
@validate_data(strict=False, 
               port=int, 
               host=str, 
               debug=bool)
def configure_server(port, host, debug, **kwargs):
    # Configure server with validated parameters
    pass
```

## 📈 Why Use This Validator?

### Benefits

- **Runtime Safety**: Catch type errors before they cause issues
- **Better Documentation**: Type hints serve as living documentation
- **Debugging Aid**: Clear error messages help identify issues quickly
- **Flexibility**: Multiple validation modes for different use cases
- **Zero Dependencies**: Uses only Python standard library
- **Production Ready**: Minimal performance impact

### Compared to Static Type Checkers

| Feature | Static (mypy) | Runtime (this validator) |
|---------|---------------|-------------------------|
| Error Detection | Compile time | Runtime |
| Complex Types | ✅ | ✅ |
| Dynamic Validation | ❌ | ✅ |
| User Input Validation | ❌ | ✅ |
| Performance Impact | None | Minimal |
| Setup Required | Yes | No |

## 🔮 Future Enhancements

Possible future additions:
- Custom error message templates
- Validation result caching
- Async function support
- Integration with dataclasses
- Performance profiling tools

---

**Ready to get started?** Copy the validator code and start adding type safety to your Python functions today! 🚀