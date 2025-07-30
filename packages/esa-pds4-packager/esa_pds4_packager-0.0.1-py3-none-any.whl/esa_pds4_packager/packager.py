import os
import subprocess
import tarfile
from os import PathLike
from pathlib import Path
from tempfile import mkdtemp

import requests
from attrs import define, field

from esa_pds4_packager.config import Config, default_settings


@define
class ValidationResult:
    is_valid: bool
    stdout: str | None = field(default=None)
    stderr: str | None = field(default=None)

    def __bool__(self) -> bool:
        """
        Returns True if the validation is successful (is_valid is True).
        """
        return self.is_valid


@define
class PDS4Packager:
    config: Config = field(factory=lambda: default_settings)

    @property
    def bin_path(self) -> Path:
        """
        Returns the path to the PDS4 packager bin directory.

        This is constructed based on the workspace location and mission.
        """
        return Path(self.config.workspace_location) / "pds4-packager" / "bin"

    @property
    def etc_path(self) -> Path:
        """
        Returns the path to the PDS4 packager etc directory.

        This is constructed based on the workspace location and mission.
        """
        return Path(self.config.workspace_location) / "pds4-packager" / "etc"

    @property
    def synchronizer_path(self) -> Path:
        """
        Returns the path to the PDS4 packager config synchronizer executable.

        This is constructed based on the workspace location and mission.
        """
        path = self.bin_path / "pds4-packager-config-synchronizer"
        if os.name == "nt":
            # On Windows, use the .bat extension for the synchronizer executable
            return path.with_suffix(".bat")
        return path

    @property
    def packager_path(self) -> Path:
        """
        Returns the path to the PDS4 packager executable.

        This is constructed based on the workspace location and mission.
        """
        path = self.bin_path / "pds4-packager"
        if os.name == "nt":
            # On Windows, use the .bat extension for the packager executable
            return path.with_suffix(".bat")
        return path

    def sync(self) -> None:
        """
        Run the PDS4 packager config synchronizer.

        Args:
            workspace_path: Path to the workspace containing the extracted packager
        """
        self.config.logger.info(
            f"Running config synchronizer for mission: {self.config.mission}"
        )
        self.config.logger.debug(f"Config synchronizer path: {self.synchronizer_path}")

        result = subprocess.run(
            [str(self.synchronizer_path), "-m", self.config.mission, "-s"],
            check=False,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            self.config.logger.error(
                f"Config synchronizer failed with return code {result.returncode}",
            )
            self.config.logger.error(f"Stderr: {result.stderr}")
            self.config.logger.error(f"Stdout: {result.stdout}")
            raise RuntimeError(f"Config synchronizer failed: {result.stderr.strip()}")

        self.config.logger.info("Config synchronizer completed successfully")
        if result.stdout:
            self.config.logger.debug(f"Config synchronizer output: {result.stdout}")
        if result.stderr:
            self.config.logger.warning(f"Config synchronizer stderr: {result.stderr}")

    def download_and_setup_pds4_packager(
        self,
        force_download: bool = False,
    ) -> None:
        """
        Download and setup PDS4 packager, then run the config synchronizer.

        Uses the instance attributes for configuration: workspace_location, version, mission, temp_path.

        Args:
            force_download: Whether to force download even if packager is already set up
        """

        # Use instance attributes directly
        workspace_location = self.config.workspace_location
        version = self.config.version
        temp_path = self.config.temp_path

        if not temp_path:
            import tempfile

            temp_path = Path(tempfile.gettempdir())

        archive_file = Path(temp_path) / f"pds4-packager-{version}.tar.gz"
        workspace_path = Path(workspace_location).resolve()

        if (
            workspace_path
            / "pds4-packager"
            / "bin"
            / "pds4-packager-config-synchronizer"
        ).exists():
            if not force_download:
                self.config.logger.info(
                    "PDS4 packager already set up, skipping download."
                )
                return
            self.config.logger.info("Force download enabled, proceeding with download.")

        if not workspace_path.exists():
            self.config.logger.debug(f"Creating workspace directory: {workspace_path}")
            workspace_path.mkdir(parents=True, exist_ok=True)

        # Remove existing archive if it exists
        if archive_file.exists():
            archive_file.unlink()

        # Determine download URL based on version
        if version == "SNAPSHOT":
            url = f"https://planetary.esac.esa.int/pds4-packager/downloads/snapshots/pds4-packager-{version}.tar.gz"
        else:
            url = f"https://planetary.esac.esa.int/pds4-packager/downloads/releases/pds4-packager-{version}.tar.gz"

        # Download the archive
        self.config.logger.info(f"Downloading PDS4 packager {version} from {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(archive_file, "wb") as f:
            f.writelines(response.iter_content(chunk_size=8192))

        self.config.logger.debug(
            f"Downloaded {archive_file.stat().st_size} bytes to {archive_file}"
        )

        # Change to workspace directory
        original_cwd = os.getcwd()
        try:
            os.chdir(workspace_path)

            # Extract the archive
            self.config.logger.info(f"Extracting {archive_file} to {workspace_path}")
            with tarfile.open(archive_file, "r:gz") as tar:
                tar.extractall()

        finally:
            # Restore original working directory
            self.config.logger.debug(f"Restoring working directory to {original_cwd}")
            os.chdir(original_cwd)

    def install(self, force_download: bool = False, sync: bool = False) -> None:
        """
        Install the PDS4 packager by downloading and setting it up.

        This method is a wrapper around download_and_setup_pds4_packager with force_download set to True.
        """
        self.config.logger.info("Installing PDS4 packager...")
        self.download_and_setup_pds4_packager(force_download=force_download)
        self.config.logger.info("PDS4 packager installation complete.")
        if sync:
            self.config.logger.info("Running config synchronizer after installation.")
            self.sync()

    def ensure_installed(self) -> None:
        """
        Ensure the PDS4 packager is installed and set up.

        This method checks if the packager is already installed and runs the config synchronizer if needed.
        """
        self.config.logger.info("Ensuring PDS4 packager is installed...")
        if self.packager_path.exists():
            self.config.logger.info(
                f"PDS4 packager already exists at {self.packager_path}"
            )

        else:
            self.config.logger.info("PDS4 packager not found, installing...")
            self.install(force_download=True, sync=True)

        if not self.etc_path.glob("*.xml"):
            self.config.logger.warning(
                "No configuration files found in the etc directory. "
                "You may need to run the config synchronizer.",
            )
            self.sync()

        self.config.logger.info("PDS4 packager is ready for use.")

    def _clean_ansi(self, text: str) -> str:
        """
        Remove ANSI escape sequences from a string.

        Args:
            text: The input string potentially containing ANSI escape sequences.
        Returns:
            A cleaned string without ANSI escape sequences.
        """
        import re

        ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
        return ansi_escape.sub("", text)

    def validate_archive(
        self,
        archive: PathLike,
        output_dir: PathLike | None = None,
    ) -> ValidationResult:
        """
        Validate a PDS4 packager archive by extracting it and running the config synchronizer.

        Args:
            archive_file: Path to the PDS4 packager archive file
        """
        archive = Path(archive).resolve()

        if not self.synchronizer_path.exists():
            msg = f"PDS4 packager config synchronizer executable {self.synchronizer_path} does not exist. install the packager first."
            raise FileNotFoundError(msg)

        # ensure the output directory exists
        if output_dir is None:
            output_dir = Path(mkdtemp()).resolve()

        self.config.logger.info(f"Created temporary output directory: {output_dir}")

        packager = self.packager_path
        if not packager.exists():
            raise FileNotFoundError(
                f"PDS4 packager executable {packager} does not exist.",
            )

        if not archive.exists():
            raise FileNotFoundError(f"Archive file {archive} does not exist.")

        # Run the PDS4 packager command
        command = [str(packager), "-i", str(archive), "-o", str(output_dir), "-r"]
        self.config.logger.info(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, check=False, capture_output=True, text=True)

        if result.returncode != 0:
            self.config.logger.error(
                f"Command failed with return code {result.returncode}"
            )
            self.config.logger.error(f"Stderr: {self._clean_ansi(result.stderr)}")
            self.config.logger.error(f"Stdout: {self._clean_ansi(result.stdout)}")

        else:
            self.config.logger.info("Command executed successfully.")
            self.config.logger.debug(f"Stdout: {self._clean_ansi(result.stdout)}")
            self.config.logger.debug(f"Stderr: {self._clean_ansi(result.stderr)}")
        return ValidationResult(
            result.returncode == 0,
            stdout=self._clean_ansi(result.stdout),
            stderr=self._clean_ansi(result.stderr),
        )
