"""Default units for quantity types in SI and Imperial systems."""

from __future__ import annotations

#: Mapping of quantity type name to its SI unit string.
SI_DEFAULTS: dict[str, str] = {
    # -- SI base quantities --
    "mass": "kg",
    "length": "m",
    "time": "s",
    "temperature": "K",
    "current": "A",
    "amount_of_substance": "mol",
    "luminous_intensity": "cd",
    # -- Mechanics --
    "velocity": "m/s",
    "acceleration": "m/s**2",
    "force": "N",
    "moment": "N*m",
    "energy": "J",
    "power": "W",
    "area": "m**2",
    "volume": "m**3",
    "density": "kg/m**3",
    "pressure": "Pa",
    "frequency": "Hz",
    "momentum": "kg*m/s",
    "angular_velocity": "rad/s",
    "angular_acceleration": "rad/s**2",
    "moment_of_inertia": "kg*m**2",
    "surface_tension": "N/m",
    # -- Electromagnetism --
    "voltage": "V",
    "charge": "C",
    "capacity": "A*h",
    "resistance": "ohm",
    "capacitance": "F",
    "inductance": "H",
    "magnetic_flux": "Wb",
    "magnetic_flux_density": "T",
    "conductance": "S",
    "electric_field": "V/m",
    # -- Fluid & Thermal --
    "dynamic_viscosity": "Pa*s",
    "kinematic_viscosity": "m**2/s",
    "mass_flow_rate": "kg/s",
    "volumetric_flow_rate": "m**3/s",
    "thermal_conductivity": "W/(m*K)",
    "specific_heat_capacity": "J/(kg*K)",
    "heat_flux": "W/m**2",
    # -- Optics --
    "illuminance": "lx",
}

#: Mapping of quantity type name to its Imperial/US customary unit string.
#: Electromagnetic quantities use SI universally; entries mirror SI_DEFAULTS.
IMPERIAL_DEFAULTS: dict[str, str] = {
    # -- Base quantities --
    "mass": "lb",
    "length": "ft",
    "time": "s",
    "temperature": "degF",
    "current": "A",
    "amount_of_substance": "mol",
    "luminous_intensity": "cd",
    # -- Mechanics --
    "velocity": "ft/s",
    "acceleration": "ft/s**2",
    "force": "lbf",
    "moment": "lbf*ft",
    "energy": "BTU",
    "power": "hp",
    "area": "ft**2",
    "volume": "ft**3",
    "density": "lb/ft**3",
    "pressure": "psi",
    "frequency": "Hz",
    "momentum": "lb*ft/s",
    "angular_velocity": "rpm",
    "angular_acceleration": "rad/s**2",
    "moment_of_inertia": "lb*ft**2",
    "surface_tension": "lbf/ft",
    # -- Electromagnetism (SI used universally) --
    "voltage": "V",
    "charge": "C",
    "capacity": "A*h",
    "resistance": "ohm",
    "capacitance": "F",
    "inductance": "H",
    "magnetic_flux": "Wb",
    "magnetic_flux_density": "T",
    "conductance": "S",
    "electric_field": "V/m",
    # -- Fluid & Thermal --
    "dynamic_viscosity": "lb/(ft*s)",
    "kinematic_viscosity": "ft**2/s",
    "mass_flow_rate": "lb/s",
    "volumetric_flow_rate": "ft**3/s",
    "thermal_conductivity": "BTU/(h*ft*degR)",
    "specific_heat_capacity": "BTU/(lb*degR)",
    "heat_flux": "BTU/(h*ft**2)",
    # -- Optics --
    "illuminance": "lx",
}
