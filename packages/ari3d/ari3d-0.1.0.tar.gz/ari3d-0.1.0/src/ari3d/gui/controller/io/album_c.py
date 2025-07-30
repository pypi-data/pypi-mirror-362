"""Controller for managing solutions for the ari3d application using Album API."""
from datetime import datetime
from pathlib import Path
from typing import Set

from album.runner.album_logging import get_active_logger

from ari3d.gui.ari3d_logging import Ari3dLogger
from ari3d.resources.default_values import DefaultValues

cur_file_path = Path(__file__).parent

SOLUTION_IDS = [
    "de.mdc:data_viewer",
    "de.mdc:particleSeg3D-predict",
    "de.mdc:feature_extraction",
]


class AlbumController:
    """Controller class for managing solutions in the ari3d application using Album API."""

    def __init__(self):
        """Initialize the AlbumController with the album API and logger."""
        self._setup_album()
        self.logger = Ari3dLogger()

    def _setup_album(self):
        from album.api import Album

        album_base_path = Path(__file__).parent.joinpath("collection")
        self.album_api = Album.Builder().base_cache_path(album_base_path).build()
        self.album_api.load_or_create_collection()

    def check_steps(self) -> Set[str]:
        """Check for updates of the solutions in the album."""
        updates = self.album_api.upgrade(dry_run=True)

        mspacman_updates = updates["mspacman"]
        mspacman_updates_list = mspacman_updates._solution_changes
        coordinate_set = {
            ":".join([x.coordinates().group(), x.coordinates().name()])
            for x in mspacman_updates_list
        }
        text = (
            "No updates available!"
            if mspacman_updates_list == []
            else (
                "Updates available for:"
                + ", ".join(coordinate_set)
                + ". Run update new steps to install them."
            )
        )

        self.logger.log.info(text)

        return coordinate_set

    def update_steps(self):
        """Update the solutions in the album."""
        coordinate_set = self.check_steps()
        self.album_api.upgrade()
        for solution in coordinate_set:
            self.reinstall_solution(solution)

    def reinstall_solution(self, solution: str):
        """Reinstall a specific solution in the album."""
        self.uninstall_solution(solution)
        self.install_solution(solution)

    def reinstall_steps(self):
        """Reinstall all solutions in the album."""
        self.uninstall_required()
        self.install_required()

    def install_solution(self, solution: str) -> bool:
        """Install a specific album solution."""
        # add catalog
        try:
            self.album_api.get_catalog_by_src(str(DefaultValues.repo_link.value))
        except LookupError:
            self.album_api.add_catalog(str(DefaultValues.repo_link.value))

        # install from catalog
        try:
            level = get_active_logger().level
            get_active_logger().setLevel("ERROR")
            if not self.album_api.is_installed(solution):
                get_active_logger().setLevel(level)
                self.logger.log.info(f"Installing {solution}")
                self.album_api.install(solution)
            self.logger.log.info(f"{solution} is ready to run!")
            get_active_logger().setLevel(level)
        except LookupError:
            self.logger.log.info(
                f"Solution {solution} not found in the catalog. Unable to run this step!"
            )
            return False

        return True

    def uninstall_solution(self, solution: str):
        """Uninstall a specific album solution."""
        # add catalog
        try:
            self.album_api.get_catalog_by_src(str(DefaultValues.repo_link.value))
        except LookupError:
            self.album_api.add_catalog(str(DefaultValues.repo_link.value))

        # install from catalog
        try:
            level = get_active_logger().level
            get_active_logger().setLevel("ERROR")
            if self.album_api.is_installed(solution):
                get_active_logger().setLevel(level)
                self.logger.log.info(f"Uninstalling {solution}")
                self.album_api.uninstall(solution)
            self.logger.log.info(f"{solution} is uninstalled!")
            get_active_logger().setLevel(level)
        except LookupError:
            self.logger.log.info(
                f"Solution {solution} not found in the catalog. Unable to uninstall this step!"
            )

    def install_from_disk(self, solution: str):
        """Install a specific solution from disk."""
        name = solution.split(":")[1]
        try:
            if not self.album_api.is_installed(solution):
                self.logger.log.info(f"Installing {solution}")
                self.album_api.install(
                    str(cur_file_path.joinpath("..", "..", "..", "solutions", name))
                )
            self.logger.log.info(f"{solution} is ready to run")
        except LookupError:
            self.album_api.install(
                str(cur_file_path.joinpath("..", "..", "..", "solutions", name))
            )

    def run(self, solution, argv=None):
        """Run a specific solution in the album."""
        self.album_api.run(solution, argv=argv)

    def install_required(self):
        """Install all required solutions for the interactive workflow."""
        # loop to install all solutions necessary for this interactive workflow
        for solution_id in SOLUTION_IDS:
            success = self.install_solution(solution_id)
            if not success:
                self.logger.log.error(
                    f"Solution {solution_id} could not be installed. Please check the logs for details."
                )
                raise RuntimeError("Installation failed for one or more solutions.")

    def try_install_required(self):
        """Try to install all required solutions for the interactive workflow."""
        # loop to install all solutions necessary for this interactive workflow
        for solution_id in SOLUTION_IDS:
            try:
                self.install_solution(solution_id)
            except RuntimeError:
                self.logger.log.warning(
                    f"Solution {solution_id} could not be installed. You will not be able to run this step!"
                )

    @staticmethod
    def write_install_txt(project_files_path: Path):
        """Write a file indicating that the installation of solutions is done."""
        # create results file for snakemake
        output_file = project_files_path.joinpath("installation_done.txt")
        with open(output_file, "w") as f:
            f.write("Installation of solutions done.\n")
            f.write(f"Date: {str(datetime.now().strftime('%Y%m%d_%H%M%S'))}")

    def uninstall_required(self):
        """Uninstall all required solutions for the interactive workflow."""
        # loop to install all solutions necessary for this interactive workflow
        for solution_id in SOLUTION_IDS:
            try:
                self.uninstall_solution(solution_id)
            except Exception as e:
                print(f"Failed to uninstall {solution_id}: {e}")
