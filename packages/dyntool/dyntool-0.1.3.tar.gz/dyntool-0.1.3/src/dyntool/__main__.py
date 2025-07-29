# __main__.py

# from dyntool import main

import sys

from .server import main

sys.exit(main())  # type: ignore[call-arg]

# main()
