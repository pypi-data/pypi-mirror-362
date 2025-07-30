"""Package entry-point:  `python -m pipify` is equivalent to `pipify`."""

from .cli import main

if __name__ == "__main__":  # pragma: no cover
    main()
