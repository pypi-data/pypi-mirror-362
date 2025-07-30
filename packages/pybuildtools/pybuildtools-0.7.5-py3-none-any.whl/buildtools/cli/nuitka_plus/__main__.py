import json
import os
import sys


def main() -> None:
    print(f'buildtools.cli.nuitka_plus subprocess spawned. PID={os.getpid()}')
    print(f'Opening {sys.argv[1]}...')
    data: dict
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)

    args = data['args']
    print(f'Setting sys.argv = [sys.argv[0]] + {args!r}...')
    sys.argv = [sys.argv[0]] + args

    print(f"Setting os.environ['PATH'] = {data['environ']['PATH']!r}...")
    os.environ['PATH'] = data['environ']['PATH']

    print(f'Invoking nuitka.__main__.main()...')
    import nuitka.__main__ as nkmain
    nkmain.main()


if __name__ == "__main__":
    main()
