# ceblpy <img src="https://github.com/ryanndu/ceblpy/raw/main/assets/images/cebl-logo.png" align="right" width="100" height="100"/>

---

## Overview

**[ceblpy](https://github.com/ryanndu/ceblpy)** is a Python package designed for working with the Canadian Elite Basketball League (CEBL) data.

The package has functions to retrieve team and player box scores, game schedules, coach and officials information, and full play-by-play data.

---

## Installation

You can install the **[ceblpy](https://github.com/ryanndu/ceblpy)** package with:

```bash
$ pip install ceblpy
```

---

## Usage

To retrieve the CEBL schedule for a given season (e.g., 2024), use the `load_cebl_schedule()` function:

```python
from ceblpy.ceblpy import load_cebl_schedule

# Load the 2024 CEBL season schedule
schedule = load_cebl_schedule(2024)

# Preview the data
print(schedule.head())
```

---

## Contributing

Found a bug? Have an idea to make ceblpy better? We'd love to hear from you!
- **Open an issue** on our **[GitHub Issues](https://github.com/ryanndu/ceblpy/issues)** page
- **Email Me** directly at **[ryandu343@gmail.com](mailto:ryandu343@gmail.com)**

All suggestions and contributions are welcome!

---

## License

`ceblpy` was created by Ryan Du and David Awosoga. It is licensed under the terms of the MIT license.

---

## Credits

`ceblpy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).