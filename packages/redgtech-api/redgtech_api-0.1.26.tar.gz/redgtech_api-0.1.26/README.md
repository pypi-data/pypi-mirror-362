# Redgtech API

A Python package to interact with the Redgtech API.

## Installation

You can install the package using pip:

```bash
pip install redgtech-api
```

## Usage

Here is an example of how to use the package:

import asyncio

from redgtech_api import RedgtechAPI

asyncdefmain():

    api = RedgtechAPI("your_access_token")

    data = await api.get_data()

print(data)

await api.close()

asyncio.run(main())

## API Methods

### `get_data()`

Fetches data from the Redgtech API.

#### Example

data = await api.get_data()

print(data)

### `set_switch_state(endpoint_id, state)`

Sets the state of a switch.

#### Parameters

* `endpoint_id` (str): The ID of the switch endpoint.
* `state` (bool): The desired state of the switch (True for on, False for off).

#### Example

**success = **await** api.**set_switch_state**(**"endpoint_id"**, **True**)**

**print**(**success**)

### `set_light_brightness(endpoint_id, brightness)`

Sets the brightness of a light.

#### Parameters

* `endpoint_id` (str): The ID of the light endpoint.
* `brightness` (int): The desired brightness level (0-255).

#### Example

success = await api.set_light_brightness("endpoint_id", 128)

print(success)

## License

This project is licensed under the MIT License.

## Project Structure

Ensure your project structure is correct:

redgtech-api/
├── redgtech_api/
│   ├── __init__.py
│   ├── api.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py
├── setup.py
├── README.md
├── LICENSE
├── venv/

## Package Implementation

```python
from .api import RedgtechAPI
```
