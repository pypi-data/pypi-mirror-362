# TSK Python SDK

A powerful parser and generator for TSK (TuskLang Configuration) format with full fujsen (function serialization) support.

## Installation

```bash
# Copy tsk.py to your project
cp tsk.py /path/to/your/project/

# Or install as a module
pip install -e .
```

## Basic Usage

### Parsing TSK Files

```python
from tsk import TSK, TSKParser

tsk_content = """
[storage]
id = "flex_123"
type = "image/jpeg"
tags = [ "sunset", "beach" ]

[metadata]
author = "John Doe"
created = 1719978000
"""

# Parse TSK content
data = TSKParser.parse(tsk_content)
print(data['storage']['id'])  # "flex_123"
print(data['storage']['tags'])  # ["sunset", "beach"]

# Or use TSK class
tsk = TSK.from_string(tsk_content)
print(tsk.get_value('storage', 'type'))  # "image/jpeg"
```

### Creating TSK Files

```python
from tsk import TSK

tsk = TSK()

# Set sections
tsk.set_section('config', {
    'debug': True,
    'timeout': 30,
    'endpoints': ['api1.example.com', 'api2.example.com']
})

# Set individual values
tsk.set_value('metadata', 'version', '1.0.0')
tsk.set_value('metadata', 'author', 'Jane Smith')

# Convert to string
tsk_string = tsk.to_string()
print(tsk_string)

# Save to file
tsk.to_file('config.tsk')
```

## Fujsen (Function Serialization)

Fujsen allows you to store and execute functions within TSK files - perfect for smart contracts!

### Storing Functions

```python
from tsk import TSK

tsk = TSK()

# Store a Python function using fujsen
def validate_amount(amount):
    if not isinstance(amount, (int, float)):
        return False
    if amount <= 0:
        return False
    if amount > 1000000:
        return False
    return True

tsk.set_fujsen('validation', 'amount_fujsen', validate_amount)

# Store as a lambda
tsk.set_value('helpers', 'calculate_fee_fujsen', """
lambda amount: amount * 0.025
""")

# Store JavaScript-style function (will be converted)
tsk.set_value('contract', 'process_fujsen', """
(amount, recipient) => {
  if (amount <= 0) throw new Error("Invalid amount");
  return {
    success: true,
    amount: amount,
    recipient: recipient,
    id: 'tx_' + Date.now()
  };
}
""")
```

### Executing Fujsen

```python
# Load TSK with fujsen
contract_tsk = """
[payment]
process_fujsen = \"\"\"
def process(amount, recipient):
    if amount <= 0:
        raise ValueError("Invalid amount")
    
    import time
    return {
        'id': f'tx_{int(time.time() * 1000)}',
        'amount': amount,
        'recipient': recipient,
        'fee': amount * 0.01
    }
\"\"\"

[validation]
check_email_fujsen = \"\"\"
lambda email: '@' in email and '.' in email.split('@')[1]
\"\"\"
"""

tsk = TSK.from_string(contract_tsk)

# Execute fujsen functions
payment = tsk.execute_fujsen('payment', 'process_fujsen', 100, 'alice@example.com')
print(payment)  # {'id': 'tx_...', 'amount': 100, 'recipient': '...', 'fee': 1.0}

is_valid = tsk.execute_fujsen('validation', 'check_email_fujsen', 'test@example.com')
print(is_valid)  # True
```

### Smart Contract Example

```python
defi_contract = """
[liquidity_pool]
name = "FLEX/USDT Pool"
reserve_a = 100000
reserve_b = 50000

swap_fujsen = \"\"\"
def swap(amount_in, token_in, reserve_a=100000, reserve_b=50000):
    k = reserve_a * reserve_b
    
    if token_in == 'FLEX':
        new_reserve_a = reserve_a + amount_in
        new_reserve_b = k / new_reserve_a
        amount_out = reserve_b - new_reserve_b
    else:
        new_reserve_b = reserve_b + amount_in
        new_reserve_a = k / new_reserve_b
        amount_out = reserve_a - new_reserve_a
    
    # Apply 0.3% fee
    fee = amount_out * 0.003
    return {
        'amount_out': amount_out - fee,
        'fee': fee,
        'price_impact': ((amount_out / amount_in) - 1) * 100
    }
\"\"\"

add_liquidity_fujsen = \"\"\"
lambda amount_a, amount_b, reserve_a=100000, reserve_b=50000: {
    'shares': min(amount_a / reserve_a, amount_b / reserve_b) * 100,
    'excess_a': amount_a * (1 - min(amount_a / reserve_a, amount_b / reserve_b) / (amount_a / reserve_a)) if amount_a / reserve_a > amount_b / reserve_b else 0,
    'excess_b': amount_b * (1 - min(amount_a / reserve_a, amount_b / reserve_b) / (amount_b / reserve_b)) if amount_b / reserve_b > amount_a / reserve_a else 0
}
\"\"\"
"""

pool = TSK.from_string(defi_contract)

# Execute swap
result = pool.execute_fujsen('liquidity_pool', 'swap_fujsen', 1000, 'FLEX')
print(f"Swap 1000 FLEX → {result['amount_out']:.2f} USDT")
print(f"Fee: {result['fee']:.2f} USDT")
print(f"Price Impact: {result['price_impact']:.2f}%")
```

## Data Types

TSK supports all Python data types:

```python
example = """
[types]
string = "hello world"
number = 42
float = 3.14159
boolean = true
null_value = null
array = [ 1, 2, 3 ]
dict = { "key" = "value", "nested" = { "deep" = true } }
multiline = \"\"\"
This is a
multiline string
\"\"\"
"""

tsk = TSK.from_string(example)
print(tsk.get_value('types', 'array'))  # [1, 2, 3]
print(tsk.get_value('types', 'dict'))   # {'key': 'value', 'nested': {'deep': True}}
```

## Advanced Features

### Get All Fujsen in a Section

```python
# Get all validation functions
fujsen_map = tsk.get_fujsen_map('validation')
# Returns: {'validate_amount_fujsen': <function>, 'check_email_fujsen': <function>}

# Execute all validators
test_value = 100
for name, validator in fujsen_map.items():
    try:
        result = validator(test_value)
        print(f"{name}: {result}")
    except Exception as e:
        print(f"{name}: Error - {e}")
```

### File Operations

```python
# Load from file
tsk = TSK.from_file('config.tsk')

# Modify
tsk.set_value('config', 'updated', True)

# Save back
tsk.to_file('config.tsk')

# Or use convenience functions
from tsk import load, save

tsk = load('config.tsk')
# ... make changes ...
save(tsk, 'config.tsk')
```

### JavaScript Compatibility

The Python SDK can parse and execute JavaScript-style fujsen:

```python
js_style_tsk = """
[validators]
amount_fujsen = \"\"\"
(amount) => {
  if (typeof amount !== 'number') return false;
  if (amount <= 0) return false;
  if (amount > 1000000) return false;
  return true;
}
\"\"\"
"""

tsk = TSK.from_string(js_style_tsk)
# The SDK automatically converts common JS patterns to Python
result = tsk.execute_fujsen('validators', 'amount_fujsen', 500)
print(result)  # True
```

## Error Handling

```python
try:
    # Parse invalid TSK
    data = TSKParser.parse('[invalid')
except Exception as e:
    print(f"Parse error: {e}")

try:
    # Execute non-existent fujsen
    tsk.execute_fujsen('missing', 'function')
except ValueError as e:
    print(f"Fujsen error: {e}")

try:
    # Invalid fujsen code
    tsk.set_value('bad', 'fujsen', 'not valid code')
    tsk.execute_fujsen('bad', 'fujsen')
except ValueError as e:
    print(f"Compilation error: {e}")
```

## Best Practices

1. **Use descriptive section names**: `[database]`, `[api_config]`, `[smart_contract]`
2. **Suffix fujsen fields**: `process_fujsen`, `validate_fujsen` for clarity
3. **Cache TSK instances**: Parse once, use multiple times
4. **Validate fujsen code**: Test functions before storing in production
5. **Use type hints**: For better code clarity and IDE support

## Complete Example

```python
from tsk import TSK
import time

# Create a complete application config
app_config = TSK()

# Database settings
app_config.set_section('database', {
    'host': 'localhost',
    'port': 5432,
    'name': 'flexchain',
    'pool_size': 10
})

# API configuration
app_config.set_section('api', {
    'endpoints': {
        'main': 'https://api.flexchain.io',
        'backup': 'https://backup.flexchain.io'
    },
    'timeout': 30000,
    'retry_attempts': 3
})

# Validation functions
app_config.set_value('validators', 'amount_fujsen', """
def validate(amount):
    if not isinstance(amount, (int, float)):
        return {'valid': False, 'error': 'Not a number'}
    if amount <= 0:
        return {'valid': False, 'error': 'Must be positive'}
    if amount > 1000000:
        return {'valid': False, 'error': 'Exceeds maximum'}
    return {'valid': True}
""")

# Smart contract
app_config.set_value('contract', 'transfer_fujsen', """
def transfer(from_addr, to_addr, amount):
    # Import validation from config
    validation = validate(amount)
    if not validation['valid']:
        raise ValueError(validation['error'])
    
    # Simulate transfer
    import time
    return {
        'id': f'tx_{int(time.time() * 1000)}',
        'from': from_addr,
        'to': to_addr,
        'amount': amount,
        'status': 'completed',
        'timestamp': time.time()
    }
""")

# Add helper function to contract context
def validate(amount):
    # This would normally come from validators section
    if not isinstance(amount, (int, float)) or amount <= 0:
        return {'valid': False, 'error': 'Invalid amount'}
    return {'valid': True}

# Save configuration
app_config.to_file('app_config.tsk')
print("Configuration saved!")

# Later, load and use
loaded = TSK.from_file('app_config.tsk')

# Create transfer with validation
try:
    # Note: In real usage, you'd inject the validate function
    transfer = loaded.execute_fujsen('contract', 'transfer_fujsen', 'alice', 'bob', 100)
    print("Transfer result:", transfer)
except ValueError as e:
    print("Transfer failed:", e)

# Access configuration
db_config = loaded.get_section('database')
print(f"Connecting to {db_config['host']}:{db_config['port']}")
```

## Performance Tips

1. **Fujsen Caching**: Functions are automatically cached after first compilation
2. **Batch Operations**: Use `set_section()` instead of multiple `set_value()` calls
3. **Large Files**: Parse once and keep the TSK instance in memory
4. **Complex Functions**: Pre-compile and store as Python code for best performance

## Why TSK?

- **Human-readable**: Unlike JSON, TSK is designed for humans
- **Function storage**: Fujsen enables storing executable code
- **Type-safe**: Automatic type detection and preservation
- **Comments**: Support for documentation within configs
- **Cross-language**: Works with JavaScript-style functions too
- **Blockchain-ready**: Perfect for smart contracts and dApps