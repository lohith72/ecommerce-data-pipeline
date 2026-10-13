
import logging
import subprocess
import sys
from pathlib import Path


# 1. Define project paths
PROJECT_DIR = Path(__file__).resolve().parent
LOG_DIR = PROJECT_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "pipeline.log"


# 2. Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)
PYTHON = sys.executable


# 3. Define pipeline stages
scripts = [
    PROJECT_DIR / "src" / "extract.py",
    PROJECT_DIR / "src" / "transform.py",
    PROJECT_DIR / "src" / "load_to_mysql.py",
]


def run_command(command, stage_name):
    """Run a pipeline stage and stop if it fails."""
    logger.info("Starting stage: %s", stage_name)

    try:
        result = subprocess.run(
            command,
            cwd=PROJECT_DIR,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

        if result.stdout:
            print(result.stdout, end="")
            logger.info(
                "Output from %s:\n%s",
                stage_name,
                result.stdout.rstrip(),
            )

        if result.returncode != 0:
            logger.error(
                "Stage failed: %s (exit code %s)",
                stage_name,
                result.returncode,
            )
            sys.exit(result.returncode)

        logger.info("Stage completed: %s", stage_name)

    except OSError:
        logger.exception("Could not run stage: %s", stage_name)
        sys.exit(1)


def main():
    """Execute the complete data pipeline."""
    logger.info("Pipeline started")

    for script in scripts:
        if not script.exists():
            logger.error("Script not found: %s", script)
            sys.exit(1)

        run_command([PYTHON, str(script)], script.name)

    # Run automated data-quality tests
    test_file = PROJECT_DIR / "tests" / "test_data_quality.py"

    if not test_file.exists():
        logger.error("Test file not found: %s", test_file)
        sys.exit(1)

    run_command(
        [PYTHON, "-m", "pytest", str(test_file), "-v"],
        "Automated data-quality tests",
    )

    logger.info("Pipeline and all tests completed successfully!")


if __name__ == "__main__":
    main()
