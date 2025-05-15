from chimerax.core.commands import CmdDesc, register, NoArg

def hello(session):
    """Print hello world message"""
    session.logger.info("Hello from ShiftUp plugin!")

hello_desc = CmdDesc(
    synopsis='Print hello world message'
) 