"""Tests for all concrete quantity classes."""

from __future__ import annotations

import math

import numpy as np
import pytest

from engunits.config import SI_DEFAULTS
from engunits.quantities import (
    Acceleration,
    AmountOfSubstance,
    AngularAcceleration,
    AngularVelocity,
    Area,
    Capacitance,
    Capacity,
    Charge,
    Conductance,
    Current,
    Density,
    DynamicViscosity,
    ElectricField,
    Energy,
    Force,
    Frequency,
    HeatFlux,
    Illuminance,
    Inductance,
    KinematicViscosity,
    Length,
    LuminousIntensity,
    MagneticFlux,
    MagneticFluxDensity,
    Mass,
    MassFlowRate,
    Moment,
    MomentOfInertia,
    Momentum,
    Power,
    Pressure,
    Resistance,
    SpecificHeatCapacity,
    SurfaceTension,
    Temperature,
    ThermalConductivity,
    Velocity,
    Voltage,
    Volume,
    VolumetricFlowRate,
)
from engunits.registry import ureg
from tests.conftest import ALT_UNITS, QUANTITY_CLASSES


class TestDefaultSIUnit:
    """Each quantity type constructs with SI default when no unit is given."""

    @pytest.mark.parametrize("cls", QUANTITY_CLASSES, ids=lambda c: c.__name__)
    def test_default_si_unit(self, cls):
        q = cls(1.0)
        si_unit = SI_DEFAULTS[cls._quantity_type]
        # Verify the stored unit is the expected SI unit (pint may expand abbreviations)
        expected_unit = str(ureg.parse_expression(si_unit).units)
        assert q.units == expected_unit


class TestConversion:
    """Each quantity type converts to an alternate unit and back."""

    @pytest.mark.parametrize("cls", QUANTITY_CLASSES, ids=lambda c: c.__name__)
    def test_roundtrip_conversion(self, cls):
        original_value = 100.0
        q = cls(original_value)
        alt_unit = ALT_UNITS[cls._quantity_type]

        # Convert to alt unit
        q_alt = q(alt_unit)
        assert isinstance(q_alt, cls)

        # Convert back to SI
        si_unit = SI_DEFAULTS[cls._quantity_type]
        q_back = q_alt(str(ureg.parse_expression(si_unit).units))
        assert pytest.approx(q_back.value, rel=1e-6) == original_value


class TestSpecificConversions:
    """Spot-check specific well-known conversions."""

    # -- Original types --

    def test_mass_kg_to_lb(self):
        m = Mass(1, "kg")
        assert pytest.approx(m("lb").value, rel=1e-3) == 2.20462

    def test_length_m_to_ft(self):
        length = Length(1, "m")
        assert pytest.approx(length("ft").value, rel=1e-3) == 3.28084

    def test_velocity_ms_to_fts(self):
        v = Velocity(1, "m/s")
        assert pytest.approx(v("ft/s").value, rel=1e-3) == 3.28084

    def test_acceleration_ms2_to_fts2(self):
        a = Acceleration(9.80665, "m/s**2")
        assert pytest.approx(a("ft/s**2").value, rel=1e-3) == 32.174

    def test_force_n_to_lbf(self):
        f = Force(1, "N")
        assert pytest.approx(f("lbf").value, rel=1e-3) == 0.224809

    def test_power_w_to_hp(self):
        p = Power(746, "W")
        assert pytest.approx(p("hp").value, rel=1e-2) == 1.0

    def test_pressure_pa_to_psi(self):
        p = Pressure(6894.76, "Pa")
        assert pytest.approx(p("psi").value, rel=1e-3) == 1.0

    def test_temperature_k_to_degf(self):
        t = Temperature(373.15, "K")
        assert pytest.approx(t("degF").value, rel=1e-2) == 212.0

    def test_angular_velocity_rads_to_rpm(self):
        av = AngularVelocity(1, "rad/s")
        assert pytest.approx(av("rpm").value, rel=1e-3) == 60 / (2 * 3.14159265)

    def test_energy_j_to_kj(self):
        e = Energy(1000, "J")
        assert pytest.approx(e("kJ").value, rel=1e-6) == 1.0

    def test_area_m2_to_ft2(self):
        a = Area(1, "m**2")
        assert pytest.approx(a("ft**2").value, rel=1e-3) == 10.7639

    def test_volume_m3_to_l(self):
        v = Volume(1, "m**3")
        assert pytest.approx(v("L").value, rel=1e-6) == 1000.0

    def test_density_kgm3_to_lbft3(self):
        d = Density(1, "kg/m**3")
        assert pytest.approx(d("lb/ft**3").value, rel=1e-3) == 0.062428

    def test_voltage_v_to_mv(self):
        v = Voltage(1, "V")
        assert pytest.approx(v("mV").value, rel=1e-6) == 1000.0

    def test_current_a_to_ma(self):
        c = Current(1, "A")
        assert pytest.approx(c("mA").value, rel=1e-6) == 1000.0

    def test_capacity_ah_to_mah(self):
        c = Capacity(1, "A*h")
        assert pytest.approx(c("mA*h").value, rel=1e-6) == 1000.0

    def test_moment_nm_to_lbf_ft(self):
        m = Moment(1, "N*m")
        assert pytest.approx(m("lbf*ft").value, rel=1e-3) == 0.737562

    # -- New types --

    def test_amount_of_substance_mol_to_mmol(self):
        n = AmountOfSubstance(1, "mol")
        assert pytest.approx(n("mmol").value, rel=1e-6) == 1000.0

    def test_luminous_intensity_cd_to_millicandela(self):
        lum = LuminousIntensity(1, "cd")
        assert pytest.approx(lum("millicandela").value, rel=1e-6) == 1000.0

    def test_frequency_hz_to_khz(self):
        f = Frequency(1000, "Hz")
        assert pytest.approx(f("kHz").value, rel=1e-6) == 1.0

    def test_momentum_kgms_to_lbfts(self):
        p = Momentum(1, "kg*m/s")
        assert pytest.approx(p("lb*ft/s").value, rel=1e-3) == 7.23301

    def test_angular_acceleration_rads2_to_degs2(self):
        aa = AngularAcceleration(1, "rad/s**2")
        assert pytest.approx(aa("deg/s**2").value, rel=1e-3) == 57.2958

    def test_moment_of_inertia_kgm2_to_lbft2(self):
        moi = MomentOfInertia(1, "kg*m**2")
        assert pytest.approx(moi("lb*ft**2").value, rel=1e-3) == 23.7304

    def test_surface_tension_nm_to_lbfft(self):
        st = SurfaceTension(1, "N/m")
        assert pytest.approx(st("lbf/ft").value, rel=1e-3) == 0.068522

    def test_charge_c_to_mc(self):
        q = Charge(1, "C")
        assert pytest.approx(q("mC").value, rel=1e-6) == 1000.0

    def test_resistance_ohm_to_kohm(self):
        r = Resistance(1000, "ohm")
        assert pytest.approx(r("kohm").value, rel=1e-6) == 1.0

    def test_capacitance_f_to_uf(self):
        c = Capacitance(1e-6, "F")
        assert pytest.approx(c("uF").value, rel=1e-6) == 1.0

    def test_inductance_h_to_mh(self):
        ind = Inductance(1e-3, "H")
        assert pytest.approx(ind("mH").value, rel=1e-6) == 1.0

    def test_magnetic_flux_wb_to_mwb(self):
        mf = MagneticFlux(1, "Wb")
        assert pytest.approx(mf("mWb").value, rel=1e-6) == 1000.0

    def test_magnetic_flux_density_t_to_mt(self):
        mfd = MagneticFluxDensity(1, "T")
        assert pytest.approx(mfd("mT").value, rel=1e-6) == 1000.0

    def test_conductance_s_to_ms(self):
        g = Conductance(1, "S")
        assert pytest.approx(g("mS").value, rel=1e-6) == 1000.0

    def test_electric_field_vm_to_vcm(self):
        ef = ElectricField(100, "V/m")
        assert pytest.approx(ef("V/cm").value, rel=1e-6) == 1.0

    def test_dynamic_viscosity_pas_to_cp(self):
        dv = DynamicViscosity(1, "Pa*s")
        assert pytest.approx(dv("cP").value, rel=1e-6) == 1000.0

    def test_kinematic_viscosity_m2s_to_cst(self):
        kv = KinematicViscosity(1e-6, "m**2/s")
        assert pytest.approx(kv("cSt").value, rel=1e-6) == 1.0

    def test_mass_flow_rate_kgs_to_lbs(self):
        mfr = MassFlowRate(1, "kg/s")
        assert pytest.approx(mfr("lb/s").value, rel=1e-3) == 2.20462

    def test_volumetric_flow_rate_m3s_to_ls(self):
        vfr = VolumetricFlowRate(1, "m**3/s")
        assert pytest.approx(vfr("L/s").value, rel=1e-6) == 1000.0

    def test_thermal_conductivity_wmk_to_wcmk(self):
        tc = ThermalConductivity(1, "W/(m*K)")
        assert pytest.approx(tc("W/(cm*K)").value, rel=1e-6) == 0.01

    def test_specific_heat_capacity_jkgk_to_kjkgk(self):
        shc = SpecificHeatCapacity(1000, "J/(kg*K)")
        assert pytest.approx(shc("kJ/(kg*K)").value, rel=1e-6) == 1.0

    def test_heat_flux_wm2_to_kwm2(self):
        hf = HeatFlux(1000, "W/m**2")
        assert pytest.approx(hf("kW/m**2").value, rel=1e-6) == 1.0

    def test_illuminance_lx_to_klx(self):
        il = Illuminance(1000, "lx")
        assert pytest.approx(il("klx").value, rel=1e-6) == 1.0


class TestCrossTypeArithmetic:
    """Cross-type arithmetic resolves to typed class when dimensionality is unique."""

    def test_force_div_mass(self):
        f = Force(100, "N")
        m = Mass(10, "kg")
        result = f / m
        assert isinstance(result, Acceleration)
        assert pytest.approx(result.value) == 10.0

    def test_mass_mul_velocity(self):
        m = Mass(10, "kg")
        v = Velocity(5, "m/s")
        result = m * v
        assert isinstance(result, Momentum)
        assert pytest.approx(result.value) == 50.0

    def test_power_div_velocity(self):
        p = Power(1000, "W")
        v = Velocity(10, "m/s")
        result = p / v
        assert isinstance(result, Force)
        assert pytest.approx(result.value) == 100.0


class TestFrequencyAngularVelocityConversion:
    """Tests for Frequency <-> AngularVelocity conversion (2π factor)."""

    def test_frequency_to_angular_velocity(self):
        f = Frequency(1, "Hz")
        omega = f.to_angular_velocity()
        assert isinstance(omega, AngularVelocity)
        assert pytest.approx(omega.value) == 2 * math.pi
        assert omega.units == "rad / s"

    def test_angular_velocity_to_frequency(self):
        omega = AngularVelocity(2 * math.pi, "rad/s")
        f = omega.to_frequency()
        assert isinstance(f, Frequency)
        assert pytest.approx(f.value) == 1.0
        assert f.units == "Hz"

    def test_rpm_to_frequency(self):
        omega = AngularVelocity(60, "rpm")
        f = omega.to_frequency()
        assert pytest.approx(f.value) == 1.0

    def test_rpm_to_frequency_non_unity(self):
        omega = AngularVelocity(120, "rpm")
        f = omega.to_frequency()
        assert pytest.approx(f.value) == 2.0

    def test_frequency_to_angular_velocity_khz(self):
        f = Frequency(1, "kHz")
        omega = f.to_angular_velocity()
        assert pytest.approx(omega.value) == 2000 * math.pi

    def test_roundtrip_frequency_angular_velocity(self):
        f_original = Frequency(50, "Hz")
        f_roundtrip = f_original.to_angular_velocity().to_frequency()
        assert pytest.approx(f_roundtrip.value) == 50.0

    def test_roundtrip_angular_velocity_frequency(self):
        omega_original = AngularVelocity(100, "rad/s")
        omega_roundtrip = omega_original.to_frequency().to_angular_velocity()
        assert pytest.approx(omega_roundtrip.value) == 100.0

    def test_numpy_array_frequency_to_angular_velocity(self):
        f = Frequency(np.array([1.0, 2.0, 3.0]), "Hz")
        omega = f.to_angular_velocity()
        expected = np.array([1.0, 2.0, 3.0]) * 2 * math.pi
        np.testing.assert_allclose(omega.value, expected)

    def test_numpy_array_angular_velocity_to_frequency(self):
        omega = AngularVelocity(np.array([2 * math.pi, 4 * math.pi]), "rad/s")
        f = omega.to_frequency()
        np.testing.assert_allclose(f.value, np.array([1.0, 2.0]))


class TestEnergyMomentConversion:
    """Tests for Energy <-> Moment dimensional cast."""

    def test_energy_to_moment(self):
        e = Energy(100, "J")
        m = e.to_moment()
        assert isinstance(m, Moment)
        assert pytest.approx(m.value) == 100.0

    def test_moment_to_energy(self):
        m = Moment(50, "N*m")
        e = m.to_energy()
        assert isinstance(e, Energy)
        assert pytest.approx(e.value) == 50.0

    def test_energy_kj_to_moment(self):
        e = Energy(1, "kJ")
        m = e.to_moment()
        assert pytest.approx(m.value) == 1000.0

    def test_moment_imperial_to_energy(self):
        m = Moment(100, "lbf*ft")
        e = m.to_energy()
        assert pytest.approx(e.value, rel=1e-4) == 135.5818

    def test_roundtrip_energy_moment(self):
        e_original = Energy(42, "J")
        e_roundtrip = e_original.to_moment().to_energy()
        assert pytest.approx(e_roundtrip.value) == 42.0

    def test_roundtrip_moment_energy(self):
        m_original = Moment(77, "N*m")
        m_roundtrip = m_original.to_energy().to_moment()
        assert pytest.approx(m_roundtrip.value) == 77.0


class TestChargeCapacityConversion:
    """Tests for Charge <-> Capacity dimensional cast."""

    def test_charge_to_capacity(self):
        q = Charge(3600, "C")
        cap = q.to_capacity()
        assert isinstance(cap, Capacity)
        assert pytest.approx(cap.value) == 1.0
        assert cap.units == "A * h"

    def test_capacity_to_charge(self):
        cap = Capacity(1, "A*h")
        q = cap.to_charge()
        assert isinstance(q, Charge)
        assert pytest.approx(q.value) == 3600.0
        assert q.units == "C"

    def test_capacity_mah_to_charge(self):
        cap = Capacity(1000, "mA*h")
        q = cap.to_charge()
        assert pytest.approx(q.value) == 3600.0

    def test_charge_mc_to_capacity(self):
        q = Charge(3600000, "mC")
        cap = q.to_capacity()
        assert pytest.approx(cap.value) == 1.0

    def test_roundtrip_charge_capacity(self):
        q_original = Charge(7200, "C")
        q_roundtrip = q_original.to_capacity().to_charge()
        assert pytest.approx(q_roundtrip.value) == 7200.0

    def test_roundtrip_capacity_charge(self):
        cap_original = Capacity(5, "A*h")
        cap_roundtrip = cap_original.to_charge().to_capacity()
        assert pytest.approx(cap_roundtrip.value) == 5.0
