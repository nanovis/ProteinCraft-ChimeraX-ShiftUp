toolshed uninstall ShiftUp; devel build /home/luod/ProteinCraft/python_plugins/ProteinCraft-ShiftUp; devel install /home/luod/ProteinCraft/python_plugins/ProteinCraft-ShiftUp exit true


from chimerax.atomic import Structure
mols = session.models.list(type = Structure)
mol = mols[0]