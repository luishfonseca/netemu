from netemu.cli import main
import os
import sys
import shutil

if __name__ == "__main__":
    if os.geteuid() != 0:
        unshare = shutil.which("unshare")
        os.execv(
            unshare, [unshare, "-Urn", sys.executable, "-m", "netemu"] + sys.argv[1:]
        )
    main()
