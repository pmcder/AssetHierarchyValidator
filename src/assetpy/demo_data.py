from __future__ import annotations

from .models import Asset, AssetType, Criticality, Status


def build_demo_assets() -> list[Asset]:
    """Build a Gulf Coast Petroleum Group demo hierarchy (~95 nodes).

    Structure:
        1 Enterprise → 2 Sites → 6 Facilities → 14 Systems → ~42 Equipment → ~30 Components
    """
    assets: list[Asset] = []

    # -------------------------------------------------------------------------
    # ENTERPRISE
    # -------------------------------------------------------------------------
    assets.append(Asset(
        id="ENT-001",
        name="Gulf Coast Petroleum Group",
        asset_type=AssetType.ENTERPRISE,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id=None,
        metadata={
            "founded": "1987",
            "hq_location": "Houston, TX",
            "employees": "12400",
            "annual_capacity_bpd": "320000",
        },
    ))

    # -------------------------------------------------------------------------
    # SITES
    # -------------------------------------------------------------------------
    assets.append(Asset(
        id="SITE-001",
        name="Port Arthur Refinery Complex",
        asset_type=AssetType.SITE,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="ENT-001",
        metadata={
            "location": "Port Arthur, TX",
            "capacity_bpd": "210000",
            "established": "1994",
            "site_area_acres": "1850",
        },
    ))
    assets.append(Asset(
        id="SITE-002",
        name="Beaumont Upstream Operations",
        asset_type=AssetType.SITE,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="ENT-001",
        metadata={
            "location": "Beaumont, TX",
            "capacity_bpd": "110000",
            "established": "2001",
            "site_area_acres": "920",
        },
    ))

    # -------------------------------------------------------------------------
    # FACILITIES — Port Arthur (SITE-001)
    # -------------------------------------------------------------------------
    assets.append(Asset(
        id="FAC-001",
        name="Crude Distillation Unit",
        asset_type=AssetType.FACILITY,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="SITE-001",
        metadata={
            "p_and_id": "PA-CDU-001",
            "design_capacity_bpd": "120000",
            "commissioned": "1996",
            "last_turnaround": "2022-04",
        },
    ))
    assets.append(Asset(
        id="FAC-002",
        name="Fluid Catalytic Cracker",
        asset_type=AssetType.FACILITY,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="SITE-001",
        metadata={
            "p_and_id": "PA-FCC-001",
            "design_capacity_bpd": "55000",
            "commissioned": "1999",
            "last_turnaround": "2023-10",
        },
    ))
    assets.append(Asset(
        id="FAC-003",
        name="Hydrodesulfurization Unit",
        asset_type=AssetType.FACILITY,
        status=Status.DEGRADED,
        criticality=Criticality.CRITICAL,
        parent_id="SITE-001",
        metadata={
            "p_and_id": "PA-HDS-001",
            "design_capacity_bpd": "35000",
            "commissioned": "2004",
            "last_turnaround": "2021-06",
        },
    ))
    assets.append(Asset(
        id="FAC-004",
        name="Port Arthur Utilities",
        asset_type=AssetType.FACILITY,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="SITE-001",
        metadata={
            "p_and_id": "PA-UTL-001",
            "steam_capacity_klb_hr": "850",
            "commissioned": "1994",
        },
    ))

    # FACILITIES — Beaumont (SITE-002)
    assets.append(Asset(
        id="FAC-005",
        name="Wellhead Separation Unit",
        asset_type=AssetType.FACILITY,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="SITE-002",
        metadata={
            "p_and_id": "BM-WSU-001",
            "design_capacity_bpd": "60000",
            "commissioned": "2003",
            "last_turnaround": "2023-03",
        },
    ))
    assets.append(Asset(
        id="FAC-006",
        name="Water Injection Facility",
        asset_type=AssetType.FACILITY,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="SITE-002",
        metadata={
            "p_and_id": "BM-WIF-001",
            "injection_capacity_bwpd": "95000",
            "commissioned": "2005",
        },
    ))

    # -------------------------------------------------------------------------
    # SYSTEMS
    # -------------------------------------------------------------------------

    # CDU systems
    assets.append(Asset(
        id="SYS-001",
        name="Atmospheric Distillation Column",
        asset_type=AssetType.SYSTEM,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="FAC-001",
        metadata={"tag_number": "T-1001", "design_pressure_psig": "45", "design_temp_f": "750"},
    ))
    assets.append(Asset(
        id="SYS-002",
        name="Vacuum Distillation Column",
        asset_type=AssetType.SYSTEM,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="FAC-001",
        metadata={"tag_number": "T-1002", "design_pressure_psig": "-14", "design_temp_f": "720"},
    ))
    assets.append(Asset(
        id="SYS-003",
        name="CDU Preheat Train",
        asset_type=AssetType.SYSTEM,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="FAC-001",
        metadata={"tag_number": "HX-1001-1010", "heat_duty_mmbtuh": "320"},
    ))

    # FCC systems
    assets.append(Asset(
        id="SYS-004",
        name="Reactor-Regenerator System",
        asset_type=AssetType.SYSTEM,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="FAC-002",
        metadata={"tag_number": "R-2001", "catalyst_inventory_tons": "280", "design_temp_f": "1350"},
    ))
    assets.append(Asset(
        id="SYS-005",
        name="FCC Main Fractionator",
        asset_type=AssetType.SYSTEM,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="FAC-002",
        metadata={"tag_number": "T-2001", "trays": "42", "design_pressure_psig": "20"},
    ))

    # HDS systems
    assets.append(Asset(
        id="SYS-006",
        name="HDS Reactor Train",
        asset_type=AssetType.SYSTEM,
        status=Status.DEGRADED,
        criticality=Criticality.CRITICAL,
        parent_id="FAC-003",
        metadata={"tag_number": "R-3001/3002", "h2_purity_pct": "99.2", "design_pressure_psig": "1200"},
    ))
    assets.append(Asset(
        id="SYS-007",
        name="HDS Stripper Column",
        asset_type=AssetType.SYSTEM,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="FAC-003",
        metadata={"tag_number": "T-3001", "trays": "24", "design_pressure_psig": "150"},
    ))

    # Utilities systems
    assets.append(Asset(
        id="SYS-008",
        name="Steam Generation System",
        asset_type=AssetType.SYSTEM,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="FAC-004",
        metadata={"tag_number": "B-4001/4002", "steam_pressure_psig": "600", "superheat_temp_f": "750"},
    ))
    assets.append(Asset(
        id="SYS-009",
        name="Cooling Water System",
        asset_type=AssetType.SYSTEM,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="FAC-004",
        metadata={"tag_number": "CT-4001", "flow_rate_gpm": "45000", "approach_temp_f": "10"},
    ))

    # Wellhead systems
    assets.append(Asset(
        id="SYS-010",
        name="Three-Phase Separator Train",
        asset_type=AssetType.SYSTEM,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="FAC-005",
        metadata={"tag_number": "V-5001/5002", "design_pressure_psig": "750", "design_temp_f": "200"},
    ))
    assets.append(Asset(
        id="SYS-011",
        name="Gas Compression System",
        asset_type=AssetType.SYSTEM,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="FAC-005",
        metadata={"tag_number": "K-5001/5002", "suction_pressure_psig": "50", "discharge_pressure_psig": "1000"},
    ))

    # Water injection systems
    assets.append(Asset(
        id="SYS-012",
        name="High-Pressure Injection Pumps",
        asset_type=AssetType.SYSTEM,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="FAC-006",
        metadata={"tag_number": "P-6001/6002/6003", "discharge_pressure_psig": "5000", "flow_bwpd": "95000"},
    ))
    assets.append(Asset(
        id="SYS-013",
        name="Water Treatment System",
        asset_type=AssetType.SYSTEM,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="FAC-006",
        metadata={"tag_number": "V-6010", "oxygen_scavenger": "hydrazine", "design_flow_bwpd": "100000"},
    ))
    assets.append(Asset(
        id="SYS-014",
        name="Injection Distribution Manifold",
        asset_type=AssetType.SYSTEM,
        status=Status.MAINTENANCE,
        criticality=Criticality.MEDIUM,
        parent_id="FAC-006",
        metadata={"tag_number": "MF-6001", "injection_wells": "12", "manifold_pressure_psig": "4800"},
    ))

    # -------------------------------------------------------------------------
    # EQUIPMENT
    # -------------------------------------------------------------------------

    # SYS-001: Atmospheric Distillation Column equipment
    assets.append(Asset(
        id="EQP-001",
        name="Atmospheric Column Overhead Condenser",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="SYS-001",
        metadata={"tag_number": "E-1001", "type": "Shell & Tube", "duty_mmbtuh": "65", "manufacturer": "API Heat Transfer", "install_year": "1996"},
    ))
    assets.append(Asset(
        id="EQP-002",
        name="Atmospheric Column Reflux Drum",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="SYS-001",
        metadata={"tag_number": "V-1001", "volume_bbls": "420", "manufacturer": "ASME Vessel Works", "install_year": "1996"},
    ))
    assets.append(Asset(
        id="EQP-003",
        name="Atmospheric Column Reflux Pump",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="SYS-001",
        metadata={"tag_number": "P-1001A", "type": "Centrifugal", "flow_gpm": "1800", "manufacturer": "Flowserve", "install_year": "1996"},
    ))
    assets.append(Asset(
        id="EQP-004",
        name="Atmospheric Column Reflux Pump Spare",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.MEDIUM,
        parent_id="SYS-001",
        metadata={"tag_number": "P-1001B", "type": "Centrifugal", "flow_gpm": "1800", "manufacturer": "Flowserve", "install_year": "1996"},
    ))

    # SYS-002: Vacuum Distillation Column equipment
    assets.append(Asset(
        id="EQP-005",
        name="Vacuum Column Overhead System",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="SYS-002",
        metadata={"tag_number": "EJ-1002", "type": "Steam Ejector", "stages": "3", "manufacturer": "Graham Corp", "install_year": "1997"},
    ))
    assets.append(Asset(
        id="EQP-006",
        name="Vacuum Column Transfer Line Heater",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="SYS-002",
        metadata={"tag_number": "F-1002", "type": "Fired Heater", "duty_mmbtuh": "185", "manufacturer": "Callidus Tech", "install_year": "1997"},
    ))

    # SYS-003: Preheat Train equipment
    assets.append(Asset(
        id="EQP-007",
        name="Crude/Residue Exchanger Train A",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="SYS-003",
        metadata={"tag_number": "E-1010 to E-1014", "type": "Shell & Tube", "duty_mmbtuh": "160", "manufacturer": "API Heat Transfer", "install_year": "1996"},
    ))
    assets.append(Asset(
        id="EQP-008",
        name="Crude/Residue Exchanger Train B",
        asset_type=AssetType.EQUIPMENT,
        status=Status.DEGRADED,
        criticality=Criticality.HIGH,
        parent_id="SYS-003",
        metadata={"tag_number": "E-1020 to E-1024", "type": "Shell & Tube", "duty_mmbtuh": "160", "manufacturer": "API Heat Transfer", "install_year": "1996"},
    ))
    assets.append(Asset(
        id="EQP-009",
        name="Desalter",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="SYS-003",
        metadata={"tag_number": "D-1001", "type": "Electrostatic", "capacity_bpd": "120000", "manufacturer": "Natco Group", "install_year": "1996"},
    ))

    # SYS-004: Reactor-Regenerator equipment
    assets.append(Asset(
        id="EQP-010",
        name="FCC Riser Reactor",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="SYS-004",
        metadata={"tag_number": "R-2001", "type": "Riser Reactor", "riser_height_ft": "100", "manufacturer": "UOP", "install_year": "1999"},
    ))
    assets.append(Asset(
        id="EQP-011",
        name="FCC Regenerator",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="SYS-004",
        metadata={"tag_number": "RG-2001", "type": "Fluid Bed Regenerator", "air_blower_hp": "12000", "manufacturer": "UOP", "install_year": "1999"},
    ))
    assets.append(Asset(
        id="EQP-012",
        name="Wet Gas Compressor",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="SYS-004",
        metadata={"tag_number": "K-2001", "type": "Centrifugal Compressor", "driver_hp": "15000", "manufacturer": "Elliott Group", "install_year": "1999"},
    ))

    # SYS-005: FCC Main Fractionator equipment
    assets.append(Asset(
        id="EQP-013",
        name="FCC Main Column Overhead Condenser",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="SYS-005",
        metadata={"tag_number": "E-2010", "type": "Air Cooler", "duty_mmbtuh": "45", "manufacturer": "Hudson Products", "install_year": "1999"},
    ))
    assets.append(Asset(
        id="EQP-014",
        name="FCC Slurry Pumparound Cooler",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="SYS-005",
        metadata={"tag_number": "E-2020", "type": "Shell & Tube", "duty_mmbtuh": "90", "manufacturer": "API Heat Transfer", "install_year": "1999"},
    ))

    # SYS-006: HDS Reactor Train equipment
    assets.append(Asset(
        id="EQP-015",
        name="HDS Feed/Effluent Exchanger",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="SYS-006",
        metadata={"tag_number": "E-3001", "type": "Shell & Tube", "duty_mmbtuh": "55", "manufacturer": "API Heat Transfer", "install_year": "2004"},
    ))
    assets.append(Asset(
        id="EQP-016",
        name="HDS Reactor A",
        asset_type=AssetType.EQUIPMENT,
        status=Status.DEGRADED,
        criticality=Criticality.CRITICAL,
        parent_id="SYS-006",
        metadata={"tag_number": "R-3001", "catalyst": "CoMo/Al2O3", "bed_volume_cf": "4200", "manufacturer": "Haldor Topsoe", "install_year": "2004"},
    ))
    assets.append(Asset(
        id="EQP-017",
        name="HDS Reactor B",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="SYS-006",
        metadata={"tag_number": "R-3002", "catalyst": "NiMo/Al2O3", "bed_volume_cf": "4200", "manufacturer": "Haldor Topsoe", "install_year": "2004"},
    ))
    assets.append(Asset(
        id="EQP-018",
        name="H2 Recycle Compressor",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="SYS-006",
        metadata={"tag_number": "K-3001", "type": "Reciprocating", "driver_hp": "3500", "manufacturer": "Ariel Corp", "install_year": "2004"},
    ))

    # SYS-007: HDS Stripper equipment
    assets.append(Asset(
        id="EQP-019",
        name="HDS Stripper Reboiler",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="SYS-007",
        metadata={"tag_number": "E-3010", "type": "Kettle Reboiler", "duty_mmbtuh": "28", "manufacturer": "Graham Corp", "install_year": "2004"},
    ))
    assets.append(Asset(
        id="EQP-020",
        name="HDS Product Pump",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.MEDIUM,
        parent_id="SYS-007",
        metadata={"tag_number": "P-3001A", "type": "Centrifugal", "flow_gpm": "650", "manufacturer": "Sulzer", "install_year": "2004"},
    ))

    # SYS-008: Steam Generation equipment
    assets.append(Asset(
        id="EQP-021",
        name="Waste Heat Boiler A",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="SYS-008",
        metadata={"tag_number": "B-4001", "type": "HRSG", "steam_klb_hr": "425", "manufacturer": "Babcock & Wilcox", "install_year": "1994"},
    ))
    assets.append(Asset(
        id="EQP-022",
        name="Waste Heat Boiler B",
        asset_type=AssetType.EQUIPMENT,
        status=Status.MAINTENANCE,
        criticality=Criticality.CRITICAL,
        parent_id="SYS-008",
        metadata={"tag_number": "B-4002", "type": "HRSG", "steam_klb_hr": "425", "manufacturer": "Babcock & Wilcox", "install_year": "1994"},
    ))
    assets.append(Asset(
        id="EQP-023",
        name="Boiler Feed Water Pump",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="SYS-008",
        metadata={"tag_number": "P-4001A", "type": "Multistage Centrifugal", "flow_gpm": "1200", "manufacturer": "Flowserve", "install_year": "1994"},
    ))

    # SYS-009: Cooling Water equipment
    assets.append(Asset(
        id="EQP-024",
        name="Cooling Tower A",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="SYS-009",
        metadata={"tag_number": "CT-4001A", "type": "Induced Draft", "cells": "6", "manufacturer": "SPX Cooling", "install_year": "1994"},
    ))
    assets.append(Asset(
        id="EQP-025",
        name="Cooling Water Circulation Pump",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="SYS-009",
        metadata={"tag_number": "P-4010A", "type": "Vertical Turbine", "flow_gpm": "22500", "manufacturer": "Goulds Pumps", "install_year": "1994"},
    ))

    # SYS-010: Three-Phase Separator equipment
    assets.append(Asset(
        id="EQP-026",
        name="Three-Phase Separator A",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="SYS-010",
        metadata={"tag_number": "V-5001", "diameter_ft": "12", "length_ft": "60", "manufacturer": "Oil States Industries", "install_year": "2003"},
    ))
    assets.append(Asset(
        id="EQP-027",
        name="Three-Phase Separator B",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="SYS-010",
        metadata={"tag_number": "V-5002", "diameter_ft": "12", "length_ft": "60", "manufacturer": "Oil States Industries", "install_year": "2003"},
    ))
    assets.append(Asset(
        id="EQP-028",
        name="Inlet Slug Catcher",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="SYS-010",
        metadata={"tag_number": "V-5000", "volume_bbls": "1800", "manufacturer": "Oil States Industries", "install_year": "2003"},
    ))

    # SYS-011: Gas Compression equipment
    assets.append(Asset(
        id="EQP-029",
        name="Gas Compressor K-5001",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="SYS-011",
        metadata={"tag_number": "K-5001", "type": "Reciprocating", "driver_hp": "4500", "manufacturer": "Ariel Corp", "install_year": "2003"},
    ))
    assets.append(Asset(
        id="EQP-030",
        name="Gas Compressor K-5002",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="SYS-011",
        metadata={"tag_number": "K-5002", "type": "Reciprocating", "driver_hp": "4500", "manufacturer": "Ariel Corp", "install_year": "2003"},
    ))
    assets.append(Asset(
        id="EQP-031",
        name="Gas Dehydration Unit",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="SYS-011",
        metadata={"tag_number": "V-5010", "type": "Glycol Contactor", "capacity_mmscfd": "45", "manufacturer": "Cameron", "install_year": "2003"},
    ))

    # SYS-012: High-Pressure Injection Pumps equipment
    assets.append(Asset(
        id="EQP-032",
        name="Injection Pump P-6001",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="SYS-012",
        metadata={"tag_number": "P-6001", "type": "Multistage Centrifugal", "driver_hp": "6000", "manufacturer": "Sulzer", "install_year": "2005"},
    ))
    assets.append(Asset(
        id="EQP-033",
        name="Injection Pump P-6002",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="SYS-012",
        metadata={"tag_number": "P-6002", "type": "Multistage Centrifugal", "driver_hp": "6000", "manufacturer": "Sulzer", "install_year": "2005"},
    ))
    assets.append(Asset(
        id="EQP-034",
        name="Injection Pump P-6003 (Standby)",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="SYS-012",
        metadata={"tag_number": "P-6003", "type": "Multistage Centrifugal", "driver_hp": "6000", "manufacturer": "Sulzer", "install_year": "2005"},
    ))

    # SYS-013: Water Treatment equipment
    assets.append(Asset(
        id="EQP-035",
        name="Produced Water Filter",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="SYS-013",
        metadata={"tag_number": "F-6010", "type": "Walnut Shell", "flow_bwpd": "100000", "manufacturer": "Natco Group", "install_year": "2005"},
    ))
    assets.append(Asset(
        id="EQP-036",
        name="Deoxygenation Tower",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="SYS-013",
        metadata={"tag_number": "T-6010", "type": "Vacuum Degasser", "o2_target_ppb": "10", "manufacturer": "Cameron", "install_year": "2005"},
    ))

    # SYS-014: Injection Distribution Manifold equipment
    assets.append(Asset(
        id="EQP-037",
        name="Injection Manifold Header",
        asset_type=AssetType.EQUIPMENT,
        status=Status.MAINTENANCE,
        criticality=Criticality.HIGH,
        parent_id="SYS-014",
        metadata={"tag_number": "MF-6001", "material": "Duplex SS", "design_pressure_psig": "5500", "manufacturer": "Cortec Piping", "install_year": "2005"},
    ))
    assets.append(Asset(
        id="EQP-038",
        name="Flow Control Valve Bank",
        asset_type=AssetType.EQUIPMENT,
        status=Status.MAINTENANCE,
        criticality=Criticality.MEDIUM,
        parent_id="SYS-014",
        metadata={"tag_number": "FCV-6001 to 6012", "valve_count": "12", "actuator": "Hydraulic", "manufacturer": "Emerson Fisher", "install_year": "2005"},
    ))

    # Additional equipment for SYS-001, SYS-002, SYS-004 to reach ~42
    assets.append(Asset(
        id="EQP-039",
        name="Crude Charge Pump A",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="SYS-001",
        metadata={"tag_number": "P-1010A", "type": "Centrifugal", "flow_gpm": "4200", "manufacturer": "Flowserve", "install_year": "1996"},
    ))
    assets.append(Asset(
        id="EQP-040",
        name="Atmospheric Fired Heater",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="SYS-001",
        metadata={"tag_number": "F-1001", "type": "Fired Heater", "duty_mmbtuh": "220", "manufacturer": "John Zink Hamworthy", "install_year": "1996"},
    ))
    assets.append(Asset(
        id="EQP-041",
        name="Vacuum Residue Pump",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="SYS-002",
        metadata={"tag_number": "P-1020A", "type": "Gear Pump", "flow_gpm": "850", "manufacturer": "Viking Pump", "install_year": "1997"},
    ))
    assets.append(Asset(
        id="EQP-042",
        name="FCC Air Blower",
        asset_type=AssetType.EQUIPMENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="SYS-004",
        metadata={"tag_number": "K-2010", "type": "Axial Compressor", "driver_hp": "12000", "manufacturer": "MAN Energy Solutions", "install_year": "1999"},
    ))

    # -------------------------------------------------------------------------
    # COMPONENTS
    # -------------------------------------------------------------------------

    # EQP-001: Overhead Condenser components
    assets.append(Asset(
        id="CMP-001",
        name="Overhead Condenser Tube Bundle",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="EQP-001",
        metadata={"part_number": "TB-E1001-A", "material": "Admiralty Brass", "tube_count": "850", "last_inspection": "2022-04"},
    ))
    assets.append(Asset(
        id="CMP-002",
        name="Overhead Condenser Shell",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.MEDIUM,
        parent_id="EQP-001",
        metadata={"part_number": "SH-E1001-A", "material": "CS A516-70", "design_pressure_psig": "150", "last_inspection": "2022-04"},
    ))

    # EQP-003: Reflux Pump components
    assets.append(Asset(
        id="CMP-003",
        name="Reflux Pump Mechanical Seal",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="EQP-003",
        metadata={"part_number": "MS-P1001A-01", "seal_type": "Double Cartridge", "manufacturer": "John Crane", "last_replaced": "2023-08"},
    ))
    assets.append(Asset(
        id="CMP-004",
        name="Reflux Pump Impeller",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="EQP-003",
        metadata={"part_number": "IMP-P1001A-01", "material": "316 SS", "diameter_in": "12.5", "last_replaced": "2020-06"},
    ))

    # EQP-009: Desalter components
    assets.append(Asset(
        id="CMP-005",
        name="Desalter Transformer/Rectifier",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="EQP-009",
        metadata={"part_number": "TR-D1001-01", "voltage_kv": "33", "manufacturer": "Petreco", "last_replaced": "2019-02"},
    ))
    assets.append(Asset(
        id="CMP-006",
        name="Desalter Mixing Valve",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="EQP-009",
        metadata={"part_number": "MV-D1001-01", "pressure_drop_psig": "8", "manufacturer": "Petreco", "last_replaced": "2018-10"},
    ))

    # EQP-010: FCC Riser Reactor components
    assets.append(Asset(
        id="CMP-007",
        name="Riser Termination Device",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="EQP-010",
        metadata={"part_number": "RTD-R2001-01", "type": "Vortex Separation", "manufacturer": "UOP", "last_replaced": "2019-09"},
    ))
    assets.append(Asset(
        id="CMP-008",
        name="Feed Injection Nozzles",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="EQP-010",
        metadata={"part_number": "INJ-R2001-01", "nozzle_count": "8", "material": "Alloy 625", "manufacturer": "BETE Fog Nozzle", "last_replaced": "2023-10"},
    ))

    # EQP-012: Wet Gas Compressor components
    assets.append(Asset(
        id="CMP-009",
        name="WGC Rotor Assembly",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="EQP-012",
        metadata={"part_number": "RA-K2001-01", "material": "4340 Steel", "last_balanced": "2023-10", "manufacturer": "Elliott Group"},
    ))
    assets.append(Asset(
        id="CMP-010",
        name="WGC Dry Gas Seals",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="EQP-012",
        metadata={"part_number": "DGS-K2001-01", "seal_gas": "N2", "manufacturer": "John Crane", "last_replaced": "2023-10"},
    ))

    # EQP-016: HDS Reactor A components
    assets.append(Asset(
        id="CMP-011",
        name="HDS Reactor A Catalyst Bed",
        asset_type=AssetType.COMPONENT,
        status=Status.DEGRADED,
        criticality=Criticality.CRITICAL,
        parent_id="EQP-016",
        metadata={"part_number": "CAT-R3001-01", "catalyst_type": "CoMo TK-576", "loaded_year": "2019", "activity_pct": "68", "manufacturer": "Haldor Topsoe"},
    ))
    assets.append(Asset(
        id="CMP-012",
        name="HDS Reactor A High-Flux Internals",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="EQP-016",
        metadata={"part_number": "INT-R3001-01", "type": "Quench Distributor", "material": "317L SS", "last_inspection": "2021-06", "manufacturer": "Haldor Topsoe"},
    ))

    # EQP-018: H2 Recycle Compressor components
    assets.append(Asset(
        id="CMP-013",
        name="H2 Compressor Piston Rings",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="EQP-018",
        metadata={"part_number": "PR-K3001-01", "material": "PTFE/Carbon", "set_count": "8", "last_replaced": "2024-01", "manufacturer": "Ariel Corp"},
    ))
    assets.append(Asset(
        id="CMP-014",
        name="H2 Compressor Suction Valve",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="EQP-018",
        metadata={"part_number": "SV-K3001-01", "type": "Plate Valve", "valve_count": "4", "last_replaced": "2024-01", "manufacturer": "Ariel Corp"},
    ))

    # EQP-021: Waste Heat Boiler A components
    assets.append(Asset(
        id="CMP-015",
        name="WHB-A Steam Drum",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="EQP-021",
        metadata={"part_number": "SD-B4001-01", "material": "SA-516-70", "design_pressure_psig": "700", "last_inspection": "2022-09", "manufacturer": "Babcock & Wilcox"},
    ))
    assets.append(Asset(
        id="CMP-016",
        name="WHB-A Tube Bundles",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="EQP-021",
        metadata={"part_number": "TB-B4001-01", "material": "SA-192", "tube_count": "1250", "last_replaced": "2017-04", "manufacturer": "Babcock & Wilcox"},
    ))

    # EQP-026: Three-Phase Separator A components
    assets.append(Asset(
        id="CMP-017",
        name="Separator A Mist Eliminator",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.MEDIUM,
        parent_id="EQP-026",
        metadata={"part_number": "ME-V5001-01", "type": "Mesh Pad", "material": "316 SS", "last_replaced": "2020-03", "manufacturer": "Koch-Glitsch"},
    ))
    assets.append(Asset(
        id="CMP-018",
        name="Separator A Level Controller",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="EQP-026",
        metadata={"part_number": "LC-V5001-01", "type": "Guided Wave Radar", "manufacturer": "Emerson Rosemount", "last_calibrated": "2024-09"},
    ))

    # EQP-029: Gas Compressor K-5001 components
    assets.append(Asset(
        id="CMP-019",
        name="K-5001 Connecting Rod Assembly",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="EQP-029",
        metadata={"part_number": "CR-K5001-01", "material": "4340 Forged Steel", "last_replaced": "2021-07", "manufacturer": "Ariel Corp"},
    ))
    assets.append(Asset(
        id="CMP-020",
        name="K-5001 Vibration Monitor",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="EQP-029",
        metadata={"part_number": "VM-K5001-01", "type": "Proximity Probe", "manufacturer": "Bently Nevada", "last_calibrated": "2024-06"},
    ))

    # EQP-032: Injection Pump P-6001 components
    assets.append(Asset(
        id="CMP-021",
        name="P-6001 Impeller Stack",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="EQP-032",
        metadata={"part_number": "IS-P6001-01", "stages": "9", "material": "Duplex SS", "last_replaced": "2022-11", "manufacturer": "Sulzer"},
    ))
    assets.append(Asset(
        id="CMP-022",
        name="P-6001 Mechanical Seal",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="EQP-032",
        metadata={"part_number": "MS-P6001-01", "seal_type": "Tandem Pressurized", "manufacturer": "John Crane", "last_replaced": "2023-05"},
    ))

    # EQP-035: Produced Water Filter components
    assets.append(Asset(
        id="CMP-023",
        name="Walnut Shell Filter Media",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.MEDIUM,
        parent_id="EQP-035",
        metadata={"part_number": "FM-F6010-01", "media_type": "Black Walnut 8x16 mesh", "volume_cf": "420", "last_replaced": "2023-01", "manufacturer": "Nut Shell Products"},
    ))
    assets.append(Asset(
        id="CMP-024",
        name="Water Filter Backwash Valve",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.MEDIUM,
        parent_id="EQP-035",
        metadata={"part_number": "BV-F6010-01", "type": "Pneumatic Ball Valve", "size_in": "16", "manufacturer": "Emerson Fisher", "last_replaced": "2021-08"},
    ))

    # EQP-037: Injection Manifold components
    assets.append(Asset(
        id="CMP-025",
        name="Manifold Choke Valves",
        asset_type=AssetType.COMPONENT,
        status=Status.MAINTENANCE,
        criticality=Criticality.HIGH,
        parent_id="EQP-037",
        metadata={"part_number": "CV-MF6001-01-12", "valve_count": "12", "type": "Adjustable Choke", "manufacturer": "Cameron", "last_replaced": "2022-06"},
    ))
    assets.append(Asset(
        id="CMP-026",
        name="Manifold Pressure Transmitters",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="EQP-037",
        metadata={"part_number": "PT-MF6001-01-12", "transmitter_count": "12", "manufacturer": "Emerson Rosemount", "last_calibrated": "2024-11"},
    ))

    # Additional components for EQP-006, EQP-011, EQP-023, EQP-042
    assets.append(Asset(
        id="CMP-027",
        name="Vacuum Heater Radiant Coils",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="EQP-006",
        metadata={"part_number": "RC-F1002-01", "material": "9Cr-1Mo", "tube_count": "96", "last_replaced": "2022-04", "manufacturer": "Callidus Tech"},
    ))
    assets.append(Asset(
        id="CMP-028",
        name="FCC Regenerator Cyclones",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id="EQP-011",
        metadata={"part_number": "CY-RG2001-01", "stage": "Two-Stage", "material": "Alloy 601", "last_replaced": "2019-09", "manufacturer": "UOP"},
    ))
    assets.append(Asset(
        id="CMP-029",
        name="BFW Pump Thrust Bearing",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="EQP-023",
        metadata={"part_number": "TB-P4001A-01", "type": "Tilting Pad", "manufacturer": "Kingsbury", "last_replaced": "2021-03"},
    ))
    assets.append(Asset(
        id="CMP-030",
        name="FCC Air Blower IGV Actuator",
        asset_type=AssetType.COMPONENT,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="EQP-042",
        metadata={"part_number": "IGV-K2010-01", "type": "Hydraulic Actuator", "manufacturer": "MAN Energy Solutions", "last_replaced": "2022-11"},
    ))

    return assets
