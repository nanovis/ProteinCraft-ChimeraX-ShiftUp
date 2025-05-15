# vim: set expandtab shiftwidth=4 softtabstop=4:

from chimerax.core.toolshed import BundleAPI

class _ShiftUpAPI(BundleAPI):
    """API for the ShiftUp bundle."""

    api_version = 1  # Use BundleInfo and CommandInfo instances

    @staticmethod
    def register_command(bi, ci, logger):
        """Register a command with ChimeraX."""

        # bi is an instance of chimerax.core.toolshed.BundleInfo
        # ci is an instance of chimerax.core.toolshed.CommandInfo
        # logger is an instance of chimerax.core.logger.Logger

        # This method is called once for each command listed
        # in bundle_info.xml.

        from . import cmd
        if ci.name == "shiftup":
            func = cmd.enable
            desc = cmd.enable_desc
        else:
            raise ValueError(f"trying to register unknown command: {ci.name}")

        if desc.synopsis is None:
            desc.synopsis = ci.synopsis

        from chimerax.core.commands import register
        register(ci.name, desc, func)

    @staticmethod
    def initialize(session, bundle_info):
        """Initialize the bundle when it is loaded."""
        
        # Enable shift-up functionality by default
        from . import cmd
        cmd.enable(session, True)

    @staticmethod
    def finish(session, bundle_info):
        """Clean up when the bundle is unloaded."""
        
        # Restore original functionality when bundle is unloaded
        from . import cmd
        cmd.enable(session, False)

# Create the bundle_api object that ChimeraX expects
bundle_api = _ShiftUpAPI()