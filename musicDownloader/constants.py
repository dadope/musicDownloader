import tempfile
from pathlib import Path

from musicDownloader.util import initialSetup

_user_dir = Path.home()
_tmp = Path(tempfile.gettempdir())
_project_data_dir = _user_dir / ".musicDownloader"

TMP_DIR = _tmp / ".musicDownloader"
TEST_DIR = _tmp / ".musicDownloaderTests"

TMP_DIR.mkdir(exist_ok=True)
TEST_DIR.mkdir(exist_ok=True)

RESOURCES_DIR = _project_data_dir / "resources"
USER_DATA_DIR = _project_data_dir / "data"

if not _project_data_dir.exists():
    initialSetup.initialSetup(_user_dir, RESOURCES_DIR, USER_DATA_DIR)

url_logger = initialSetup.setup_logger("url_logger", str(USER_DATA_DIR / "url.log"),  "%(asctime)s | %(message)s")
logger =     initialSetup.setup_logger("logger",     str(USER_DATA_DIR / "logs.log"), "%(asctime)s => %(name)s:%(process)d :: (%(levelname)s) %(message)s")

url_logger.info("##### Initialising #####")