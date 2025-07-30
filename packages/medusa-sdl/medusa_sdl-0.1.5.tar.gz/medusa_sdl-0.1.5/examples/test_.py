
import logging
from pathlib import Path
from medusa import Medusa, MedusaDesigner
import logging
import time

logger = logging.getLogger("test")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

# designer = MedusaDesigner()
# designer.new_design()
# exit()
# input()

# base_path = Path(r"D:\Aspuru-Guzik Lab Dropbox\Lab Manager Aspuru-Guzik\PythonScript\Han\Medusa\examples")
base_path = Path(r"C:\Users\aag\Downloads")
# layout = input("New design name\n") + ".json"
layout = "fluidic_design.json"
medusa = Medusa(
    graph_layout=base_path/layout,
    logger=logger     )

medusa.transfer_volumetric(source="ACN", 
                           target="Waste Vessel", 
                           pump_id="Pump1", 
                           volume= 0.1, transfer_type="liquid")

medusa.transfer_volumetric(source="Gas Vessel", 
                           target="Waste Vessel", 
                           pump_id="Pump1", 
                           volume= 0.5, transfer_type="gas")

medusa.heat_stir(vessel="ACN",
                 temperature=20,
                 rpm=100)

