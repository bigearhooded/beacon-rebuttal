"""The MatTools registry rendered as `@register_function` calls.

This is the same 98 entries the benchmark arm consumed, shown in the form a
maintainer of `pymatgen-analysis-defects` would paste into the library. We did
not fork or patch pymatgen: for the benchmark the entries were served through a
lookup tool from JSON, on the identical channel used for the `doc_RAG` arm and
for the benchmark authors' own 7,192-document corpus, so that the arms differ
only in what the retrieved block contains.

`produces` and `requires` are absent throughout. `pymatgen` adds and removes no
named state — results are attributes on returned objects — so those two slots
bind to nothing here, and `key_results` names the attributes a caller reads
instead. That substitution is the transfer boundary discussed in the response.

Generated from `semantic_A2_98.json`; every entry was written by
`deepseek-v4-flash` reading only source, signature and docstring, with no hand
editing and no sight of the benchmark's tasks or tests.
"""

from omicverse.utils import register_function

# pymatgen.analysis.defects.ccd.HarmonicDefect(omega: 'float', charge_state: 'int', ispin: 'int', vrun: 'Vasprun | None' = None, distortions: 'Sequence[float] | None' = None, structures: 'Sequence[Structure] | None' = None, energies: 'Sequence[float] | None' = None, defect_band: 'Sequence[tuple] | None' = None, relaxed_index: 'int | None' = None, relaxed_bandstructure: 'BandStructure | None' = None, wswqs: 'list[dict] | None' = None, waveder: 'Waveder | None' = None) -> None
@register_function(
    aliases=[
     "HarmonicDefect",
     "SHO defect",
     "defect phonon mode",
     "harmonic defect",
     "vibronic state"
    ],
    category="defects",
    description="Represents the vibronic state of a defect as a simple harmonic oscillator, capturing the potential energy surface, distortion coordinates, and electronic structure information for analyzing defect vibrational properties, electron-phonon coupling, and optical transitions.",
    examples=[
     "from pymatgen.analysis.defects.ccd import HarmonicDefect, get_SRH_coefficient",
     "from pymatgen.analysis.defects.ccd import HarmonicDefect"
    ],
    key_results=[
     {
      "attr": ".omega",
      "returns": "float",
      "note": "Vibronic frequency in the same units as the energy vs. Q plot (often eV)."
     },
     {
      "attr": ".charge_state",
      "returns": "int",
      "note": "Charge of the defect (e.g., 0, +1, -2)."
     },
     {
      "attr": ".relaxed_structure",
      "returns": "Structure",
      "note": "The relaxed defect structure after geometry optimization."
     },
     {
      "attr": ".defect_band_index",
      "returns": "int",
      "note": "Index of the defect band in the electronic structure (e.g., 234)."
     },
     {
      "attr": ".spin",
      "returns": "Spin",
      "note": "Spin of the defect state (Spin.up or Spin.down)."
     }
    ],
    related=[
     "get_SRH_coef",
     "get_SRH_coefficient",
     "get_dQ",
     "get_localized_states",
     "get_zfile"
    ]
)
def HarmonicDefect(...):
    ...

# pymatgen.analysis.defects.ccd.get_SRH_coef(T: 'float | npt.ArrayLike', dQ: 'float', dE: 'float', omega_i: 'float', omega_f: 'float', elph_me: 'float', volume: 'float', g: 'int' = 1, occ_tol: 'float' = 0.001) -> 'npt.ArrayLike'
@register_function(
    aliases=[
     "SRH capture rate",
     "SRH coefficient",
     "capture coefficient",
     "get_SRH_coef",
     "recombination coefficient"
    ],
    category="defects",
    description="Computes the Shockley-Read-Hall (SRH) capture coefficient for a defect transition, given temperature, phonon displacements, energies, electron-phonon matrix element, and volume; used by materials scientists to model non-radiative recombination rates in semiconductors.",
    examples=[
     "res = get_SRH_coef(T=[100, 200, 300], dQ=1.0, dE=1.0, omega_i=0.2, omega_f=0.2, elph_me=1, volume=1, g=1, )"
    ],
    key_results=[
     {
      "attr": "return value",
      "returns": "npt.ArrayLike",
      "note": "The capture coefficient(s) in cm^3 s^{-1}, one per temperature if T is an array; scalar if T is a float."
     }
    ],
    related=[
     "HarmonicDefect",
     "get_SRH_coefficient",
     "get_dQ",
     "get_localized_states",
     "get_zfile"
    ]
)
def get_SRH_coef(...):
    ...

# pymatgen.analysis.defects.ccd.get_SRH_coefficient(initial_state: 'HarmonicDefect', final_state: 'HarmonicDefect', defect_state: 'tuple[int, int, int]', T: 'float | npt.ArrayLike', dE: 'float', g: 'int' = 1, occ_tol: 'float' = 0.001, n_band_edge: 'int' = 1, use_final_state_elph: 'bool' = False) -> 'npt.ArrayLike'
@register_function(
    aliases=[
     "SRH coefficient",
     "Shockley-Read-Hall coefficient",
     "capture coefficient",
     "get_SRH_coefficient",
     "non-radiative recombination coefficient"
    ],
    category="defects",
    description="Computes the Shockley-Read-Hall (SRH) non\u2011radiative recombination coefficient for a defect transition between two charge states, used to model carrier capture rates in semiconductors.",
    examples=[
     "c_n = get_SRH_coefficient(initial_state=hd0, final_state=hd1, defect_state=(138, 1, 1), T=[100, 200, 300], dE=1.0, )",
     "get_SRH_coefficient(initial_state=hd0, final_state=hd1, defect_state=hd1.defect_band[-1], T=[100, 200, 300], dE=1.0, use_final_state_elph=True, )"
    ],
    key_results=[
     {
      "attr": "return value",
      "returns": "npt.ArrayLike",
      "note": "SRH recombination coefficient in units of cm^3 s^-1; if T is an array, the returned array has the same shape."
     }
    ],
    related=[
     "HarmonicDefect",
     "get_SRH_coef",
     "get_dQ",
     "get_localized_states",
     "get_zfile"
    ]
)
def get_SRH_coefficient(...):
    ...

# pymatgen.analysis.defects.ccd.get_dQ(ground: 'Structure', excited: 'Structure') -> 'float'
@register_function(
    aliases=[
     "CCD",
     "configuration coordinate difference",
     "dQ",
     "defect relaxation coordinate",
     "get_dQ"
    ],
    category="defects",
    description="Compute the configuration coordinate difference (dQ) between ground and excited state structures, used to quantify the lattice relaxation accompanying a defect transition, e.g., for luminescence or nonradiative recombination analysis.",
    examples=[
     "from pymatgen.analysis.defects.ccd import get_dQ; dQ = get_dQ(ground_structure, excited_structure)"
    ],
    key_results=[
     {
      "attr": "dQ",
      "returns": "float",
      "note": "Configuration coordinate difference in amu^{1/2} Å (atomic mass unit^{1/2} * Angstrom)"
     }
    ],
    related=[
     "HarmonicDefect",
     "get_SRH_coef",
     "get_SRH_coefficient",
     "get_localized_states",
     "get_zfile"
    ]
)
def get_dQ(...):
    ...

# pymatgen.analysis.defects.ccd.get_localized_states(bandstructure: 'BandStructure', procar: 'Procar', band_window: 'int' = 7) -> 'Generator[tuple[int, int, int, float], None, None]'
@register_function(
    aliases=[
     "IPR",
     "band localization analysis",
     "get_localized_states",
     "inverse participation ratio",
     "localized state finder",
     "most localized state"
    ],
    category="defects",
    description="Finds the most localized electronic state (lowest inverse participation ratio) near the Fermi level for each k-point and spin channel, helping to identify defect-localized or trap states in a band structure.",
    examples=[
     "get_localized_states(bs, procar=procar)",
     "for iband, _ikpt, _ispin, _val in get_localized_states(bs, procar=procar):",
     "for iband, _ikpt, _ispin, _val in get_localized_states(bs, procar=procar, band_window=100"
    ],
    key_results=[
     {
      "attr": "band_index",
      "returns": "int",
      "note": "Index of the band with the lowest IPR within the search window."
     },
     {
      "attr": "kpt_index",
      "returns": "int",
      "note": "Index of the k-point for which the localized state was found."
     },
     {
      "attr": "spin_index",
      "returns": "int",
      "note": "Spin channel index (0 or 1 for spin-polarized, 0 for non-spin)."
     },
     {
      "attr": "ipr_value",
      "returns": "float",
      "note": "The inverse participation ratio value; lower values indicate stronger localization."
     }
    ],
    related=[
     "HarmonicDefect",
     "get_SRH_coef",
     "get_SRH_coefficient",
     "get_dQ",
     "get_zfile"
    ]
)
def get_localized_states(...):
    ...

# pymatgen.analysis.defects.ccd.get_zfile(directory: 'Path', base_name: 'str', allow_missing: 'bool' = False) -> 'Path | None'
@register_function(
    aliases=[
     "ccd",
     "defects file finder",
     "find gzipped file",
     "get_zfile",
     "locate gz file"
    ],
    category="defects",
    description="Locate a file in a directory that may be gzipped (e.g., .gz or .GZ), useful for finding defect calculation output files where compression is common.",
    examples=[
     "path = get_zfile(Path('/scratch/defect_calc'), 'OUTCAR'); print(path)"
    ],
    key_results=[
     {
      "attr": ".name",
      "returns": "str",
      "note": "e.g., 'OUTCAR' or 'OUTCAR.gz' depending on which file was found"
     },
     {
      "attr": ".suffix",
      "returns": "str",
      "note": "e.g., '' for uncompressed, '.gz' for gzipped"
     },
     {
      "attr": ".parent",
      "returns": "Path",
      "note": "the directory containing the file, e.g., PosixPath('/some/dir')"
     }
    ],
    related=[
     "HarmonicDefect",
     "get_SRH_coef",
     "get_SRH_coefficient",
     "get_dQ",
     "get_localized_states"
    ]
)
def get_zfile(...):
    ...

# pymatgen.analysis.defects.ccd.plot_pes(hd: 'HarmonicDefect', x_shift: 'float' = 0, y_shift: 'float' = 0, width: 'float' = 1.0, ax: 'Axes' = None) -> 'None'
@register_function(
    aliases=[
     "PES plot",
     "harmonic defect potential",
     "plot_pes",
     "potential energy surface plot"
    ],
    category="defects",
    description="Plot the potential energy surface (PES) of a HarmonicDefect to visualize the energy vs. distortion along the harmonic mode, including a parabolic fit.",
    examples=[
     "plot_pes(hd0)"
    ],
    key_results=[
     {
      "attr": "hd.distortions",
      "returns": "list of floats",
      "note": "Distortion coordinate values used as x-axis data."
     },
     {
      "attr": "hd.energies",
      "returns": "list of floats",
      "note": "Raw energy values for each distortion point."
     },
     {
      "attr": "hd.relaxed_index",
      "returns": "int",
      "note": "Index of the minimum-energy geometry, used to shift energies to zero at the minimum."
     },
     {
      "attr": "hd.omega",
      "returns": "float",
      "note": "Harmonic frequency (ω) used to draw the parabolic fit."
     }
    ],
    related=[
     "HarmonicDefect",
     "get_SRH_coef",
     "get_SRH_coefficient",
     "get_dQ",
     "get_localized_states"
    ]
)
def plot_pes(...):
    ...

# pymatgen.analysis.defects.ccd.sort_positive_definite(list_in: 'list', ref1: 'object', ref2: 'object', dist: 'Callable') -> 'tuple[tuple, tuple[float]]'
@register_function(
    aliases=[
     "distance-based ordering with references",
     "positive definite sort",
     "reference-based sorting",
     "sort_positive_definite",
     "structural sorting by displacement"
    ],
    category="defects",
    description="Sort a list of objects using a positive-definite distance function and two reference points to define direction, useful when standard sorting fails because distances are always non-negative (e.g., sorting structures by displacement from a reference).",
    examples=[
     "sorted_vals, signed_dists = sort_positive_definite([5, 9, 2], ref1=0, ref2=10, dist=lambda a,b: abs(a-b))"
    ],
    key_results=[
     {
      "attr": "sorted_list",
      "returns": "tuple[object]",
      "note": "First element of the returned tuple; the list sorted in the direction from ref1 to ref2."
     },
     {
      "attr": "distances",
      "returns": "tuple[float]",
      "note": "Second element of the returned tuple; signed distances of each object from ref1 in the chosen direction."
     }
    ],
    related=[
     "HarmonicDefect",
     "get_SRH_coef",
     "get_SRH_coefficient",
     "get_dQ",
     "get_localized_states"
    ]
)
def sort_positive_definite(...):
    ...

# pymatgen.analysis.defects.core.Adsorbate(structure: 'Structure', site: 'PeriodicSite', multiplicity: 'int' = 1, oxi_state: 'float | None' = None, equivalent_sites: 'list[PeriodicSite] | None' = None, symprec: 'float' = 0.01, angle_tolerance: 'float' = 5, user_charges: 'list[int] | None' = None) -> 'None'
@register_function(
    aliases=[
     "Adsorbate",
     "adsorbate defect",
     "adsorption site",
     "surface adsorbate"
    ],
    category="defects",
    description="This class represents an adsorbate atom on a surface, treating it algorithmically as an interstitial defect but conceptually separate, enabling analysis of adsorption sites and defect properties like charge states and supercell structures.",
    examples=[
     "ads = Adsorbate(s, n_site)",
     "assert ads.name == \"N_{ads}\""
    ],
    key_results=[
     {
      "attr": ".name",
      "returns": "str",
      "note": "Returns a string like 'Ga_{ads}' for a Ga adsorbate (element symbol followed by '_ads')."
     },
     {
      "attr": ".defect_structure",
      "returns": "Structure",
      "note": "Returns a pymatgen Structure object with the defect (adsorbate) inserted at the site, used for further calculations."
     },
     {
      "attr": ".get_charge_states()",
      "returns": "list[int]",
      "note": "Returns a list of possible charge states for this adsorbate defect, computed from oxidation state or user charges."
     }
    ],
    related=[
     "Defect",
     "DefectComplex",
     "DefectType",
     "Interstitial",
     "NamedDefect"
    ]
)
def Adsorbate(...):
    ...

# pymatgen.analysis.defects.core.Defect(structure: 'Structure', site: 'PeriodicSite', multiplicity: 'int | None' = None, oxi_state: 'float | None' = None, equivalent_sites: 'list[PeriodicSite] | None' = None, symprec: 'float' = 0.01, angle_tolerance: 'float' = 5, user_charges: 'list[int] | None' = None) -> 'None'
@register_function(
    aliases=[
     "Defect",
     "defect analysis",
     "point defect",
     "pymatgen defect",
     "single point defect"
    ],
    category="defects",
    description="Represents a point defect in a crystal structure (e.g., vacancy, substitution, interstitial) and provides access to its properties such as name, charge states, and supercell structure, enabling defect modeling and analysis.",
    examples=[
     "from pymatgen.analysis.defects.core import Vacancy; vac = Vacancy(structure, site); print(vac.name)"
    ],
    key_results=[
     {
      "attr": ".name",
      "returns": "str",
      "note": "Human-readable defect name, e.g., 'v_Ga' for a Ga vacancy, 'Li_on_Mg' for substitution, 'i_O' for interstitial."
     },
     {
      "attr": ".defect_structure",
      "returns": "Structure",
      "note": "The unit-cell Structure representing the defect, including any atomic modifications."
     },
     {
      "attr": ".element_changes",
      "returns": "dict[Element, int]",
      "note": "Dictionary mapping elements to the number of atoms added (positive) or removed (negative), e.g., {Element('Ga'): -1} for a Ga vacancy."
     },
     {
      "attr": ".defect_type",
      "returns": "str",
      "note": "Type of defect, e.g., 'Vacancy', 'Substitution', 'Interstitial'."
     },
     {
      "attr": ".get_charge_states()",
      "returns": "list[int]",
      "note": "Returns a list of integer charge states for the defect, either from user_charges or automatically determined."
     }
    ],
    related=[
     "Adsorbate",
     "DefectComplex",
     "DefectType",
     "Interstitial",
     "NamedDefect"
    ]
)
def Defect(...):
    ...

# pymatgen.analysis.defects.core.DefectComplex(defects: 'list[Defect]', oxi_state: 'float | None' = None) -> 'None'
@register_function(
    aliases=[
     "DefectComplex",
     "complex defect",
     "defect aggregate",
     "defect cluster",
     "defect complex",
     "defect complex class"
    ],
    category="defects",
    description="Represents a complex of multiple point defects (e.g., a vacancy\u2013interstitial pair) as a single defect entity, allowing users to compute combined properties such as net oxidation state, defect structure, and elemental changes.",
    examples=[
     "dc = DefectComplex([sub, vac])",
     "assert dc.name == \"O_N+v_Ga\"",
     "sc_struct = dc.get_supercell_structure()",
     "dc.oxi_state == sub.oxi_state + vac.oxi_state",
     "dc.element_changes == {Element(\"Ga\"): -1, Element(\"N\"): -1, Element(\"O\"): 1}",
     "dc.defect_structure.formula == \"Ga1 N1 O1\""
    ],
    key_results=[
     {
      "attr": ".name",
      "returns": "str",
      "note": "concatenation of constituent defect names joined by '+', e.g., 'v_Ga+O_i' for a Ga vacancy plus O interstitial"
     },
     {
      "attr": ".oxi_state",
      "returns": "float",
      "note": "total oxidation state of the complex, either provided at init or automatically sum of individual defect oxidation states"
     },
     {
      "attr": ".defects",
      "returns": "list[Defect]",
      "note": "the list of Defect objects that make up this complex"
     },
     {
      "attr": ".defect_structure",
      "returns": "Structure",
      "note": "the combined defect structure after applying all constituent defect modifications to the host"
     },
     {
      "attr": ".element_changes",
      "returns": "dict[Element, int]",
      "note": "dictionary mapping each element to the net change in atom count across all constituent defects"
     }
    ],
    related=[
     "Adsorbate",
     "Defect",
     "DefectType",
     "Interstitial",
     "NamedDefect"
    ]
)
def DefectComplex(...):
    ...

# pymatgen.analysis.defects.core.DefectType(value, names=None, *, module=None, qualname=None, type=None, start=1)
@register_function(
    aliases=[
     "DefectType",
     "defect type enum",
     "interstitial defect",
     "other defect",
     "substitution defect",
     "vacancy defect"
    ],
    category="defects",
    description="Defines an enumeration for categorizing point defects (vacancy, substitution, interstitial, other) so they can be sorted or filtered by type.",
    examples=[
     "from pymatgen.analysis.defects.core import DefectType; print(DefectType.Vacancy.name)  # 'Vacancy'"
    ],
    key_results=[
     {
      "attr": ".name",
      "returns": "str",
      "note": "One of 'Vacancy', 'Substitution', 'Interstitial', or 'Other'."
     },
     {
      "attr": ".value",
      "returns": "int",
      "note": "Integer code: 0 (Vacancy), 1 (Substitution), 2 (Interstitial), 3 (Other)."
     },
     {
      "attr": "list(DefectType)",
      "returns": "list",
      "note": "List of all enum members: [DefectType.Vacancy, DefectType.Substitution, DefectType.Interstitial, DefectType.Other]."
     }
    ],
    related=[
     "Adsorbate",
     "Defect",
     "DefectComplex",
     "Interstitial",
     "NamedDefect"
    ]
)
def DefectType(...):
    ...

# pymatgen.analysis.defects.core.Interstitial(structure: 'Structure', site: 'PeriodicSite', multiplicity: 'int' = 1, oxi_state: 'float | None' = None, equivalent_sites: 'list[PeriodicSite] | None' = None, symprec: 'float' = 0.01, angle_tolerance: 'float' = 5, user_charges: 'list[int] | None' = None) -> 'None'
@register_function(
    aliases=[
     "Interstitial",
     "defect structure",
     "interstitial defect",
     "interstitial site",
     "point defect"
    ],
    category="defects",
    description="This class models an interstitial defect in a crystal structure, where an extra atom is inserted at a given site, and provides properties to retrieve the defect name, the resulting defect structure, and the element changes.",
    examples=[
     "inter = Interstitial(structure=defect_entries[0].defect.structure, site=PeriodicSite(\"H\", [0, 0, 0], defect_entries[0].defect.structure.lattice",
     "inter = Interstitial(s, n_site)",
     "assert inter.oxi_state == 3",
     "assert inter.get_charge_states() == [-1, 0, 1, 2, 3, 4]",
     "assert np.allclose(inter.defect_structure[0].frac_coords, inter_fpos)",
     "sc = inter.get_supercell_structure()"
    ],
    key_results=[
     {
      "attr": ".name",
      "returns": "str",
      "note": "e.g. 'O_i' for an oxygen interstitial"
     },
     {
      "attr": ".defect_structure",
      "returns": "Structure",
      "note": "the structure with the interstitial atom inserted (at index 0)"
     },
     {
      "attr": ".defect_site_index",
      "returns": "int",
      "note": "always 0 (the inserted site)"
     },
     {
      "attr": ".element_changes",
      "returns": "dict[Element, int]",
      "note": "e.g. {Element('O'): +1} for an oxygen interstitial"
     }
    ],
    related=[
     "Adsorbate",
     "Defect",
     "DefectComplex",
     "DefectType",
     "NamedDefect"
    ]
)
def Interstitial(...):
    ...

# pymatgen.analysis.defects.core.NamedDefect(name: 'str', bulk_formula: 'str', element_changes: 'dict') -> 'None'
@register_function(
    aliases=[
     "NamedDefect",
     "defect name",
     "defect placeholder",
     "defect without structure",
     "named defect",
     "simple defect"
    ],
    category="defects",
    description="Defines a defect by name, bulk formula, and elemental changes without requiring a unit cell structure, for use as a placeholder in formation energy diagram aggregation.",
    examples=[
     "de.defect = NamedDefect(name=de.defect.name, bulk_formula=bulk_formula, element_changes=None",
     "nd0 = NamedDefect.from_structures(defect_structure=defect_struct, bulk_structure=bulk_struct",
     "nd1 = NamedDefect(name=\"v_Ga\", bulk_formula=\"GaN\", element_changes={\"Ga\": -1})",
     "nd2 = NamedDefect(name=\"Mg_Ga\", bulk_formula=\"GaN\", element_changes={\"Mg\": 1, \"Ga\": -1}"
    ],
    key_results=[
     {
      "attr": ".name",
      "returns": "str",
      "note": "Defect name, e.g. 'v_Ga' for a Ga vacancy or 'v_Ga+Ga_i' for a complex."
     },
     {
      "attr": ".bulk_formula",
      "returns": "str",
      "note": "Reduced formula of the bulk structure, e.g. 'GaAs'."
     },
     {
      "attr": ".element_changes",
      "returns": "dict",
      "note": "Dictionary mapping element symbols to integer changes, e.g. {'Ga': -1} for a Ga vacancy."
     },
     {
      "attr": ".latex_name",
      "returns": "str",
      "note": "LaTeX-formatted string for display, e.g. 'Ga$_{\\rm v}$'."
     }
    ],
    related=[
     "Adsorbate",
     "Defect",
     "DefectComplex",
     "DefectType",
     "Interstitial"
    ]
)
def NamedDefect(...):
    ...

# pymatgen.analysis.defects.core.Substitution(structure: 'Structure', site: 'PeriodicSite', multiplicity: 'int | None' = None, oxi_state: 'float | None' = None, equivalent_sites: 'list[PeriodicSite] | None' = None, symprec: 'float' = 0.01, angle_tolerance: 'float' = 5, user_charges: 'list[int] | None' = None) -> 'None'
@register_function(
    aliases=[
     "Substitution",
     "defect substitution",
     "site substitution",
     "substitution defect",
     "substitutional defect"
    ],
    category="defects",
    description="Represents a substitutional defect where one atom in a crystal structure is replaced by another element, allowing computation of defect properties such as structure, multiplicity, and charge states.",
    examples=[
     "sub = Substitution(s, o_site)",
     "sub2 = Substitution(s, o_site2)",
     "assert sub.oxi_state == 1",
     "assert sub.get_charge_states() == [-1, 0, 1, 2]",
     "assert sub.get_multiplicity() == 2",
     "sc, site_ = sub.get_supercell_structure(return_site=True)"
    ],
    key_results=[
     {
      "attr": ".name",
      "returns": "str",
      "note": "Returns a string like 'As_Ga' (substituting_site_element_original_site_element) for the defect name."
     },
     {
      "attr": ".defect_structure",
      "returns": "Structure",
      "note": "Returns a copy of the pristine structure with the original atom removed and the substitution atom inserted at the same fractional coordinates."
     },
     {
      "attr": ".defect_site",
      "returns": "PeriodicSite",
      "note": "Returns the original site in the pristine structure that is being replaced (the nearest site within 0.1 Å of the substitution site)."
     },
     {
      "attr": ".defect_site_index",
      "returns": "int",
      "note": "Returns the index of the defect site in the pristine structure."
     },
     {
      "attr": ".element_changes",
      "returns": "dict[Element, int]",
      "note": "Returns a dictionary mapping elements to integer changes (e.g., {Element('Ga'): -1, Element('As'): +1}) for the substitution."
     }
    ],
    related=[
     "Adsorbate",
     "Defect",
     "DefectComplex",
     "DefectType",
     "Interstitial"
    ]
)
def Substitution(...):
    ...

# pymatgen.analysis.defects.core.Vacancy(structure: 'Structure', site: 'PeriodicSite', multiplicity: 'int | None' = None, oxi_state: 'float | None' = None, equivalent_sites: 'list[PeriodicSite] | None' = None, symprec: 'float' = 0.01, angle_tolerance: 'float' = 5, user_charges: 'list[int] | None' = None) -> 'None'
@register_function(
    aliases=[
     "Schottky defect",
     "Vacancy",
     "anion vacancy",
     "cation vacancy",
     "point defect",
     "v_{element}",
     "vacancy"
    ],
    category="defects",
    description="Represents a vacancy defect in a crystal structure, allowing a materials scientist to compute properties such as the defect name (e.g., 'v_Ga' for a gallium vacancy), the index of the removed site, the resulting structure, and the multiplicity of the defect site for concentration analysis.",
    examples=[
     "vac = Vacancy(s, s.sites[0])",
     "vac2 = Vacancy(s, s.sites[1])",
     "assert vac.oxi_state == -3",
     "assert vac.get_charge_states() == [-4, -3, -2, -1, 0, 1]",
     "assert vac.get_multiplicity() == 2",
     "assert vac.get_supercell_structure().formula == \"Ga63 N64\""
    ],
    key_results=[
     {
      "attr": ".name",
      "returns": "str",
      "note": "Returns the defect name, e.g., 'v_Ga' for a Ga vacancy."
     },
     {
      "attr": ".defect_site_index",
      "returns": "int",
      "note": "Index of the defect site in the original structure."
     },
     {
      "attr": ".element_changes",
      "returns": "dict[Element, int]",
      "note": "Returns a dictionary mapping the removed element to -1, e.g., {Element('Ga'): -1}."
     },
     {
      "attr": ".defect_structure",
      "returns": "Structure",
      "note": "The structure after removing the defect site, with proper oxidation states."
     },
     {
      "attr": ".get_multiplicity()",
      "returns": "int",
      "note": "Returns the number of symmetry‑equivalent defect sites in the bulk structure, used for concentration analysis."
     }
    ],
    related=[
     "Adsorbate",
     "Defect",
     "DefectComplex",
     "DefectType",
     "Interstitial"
    ]
)
def Vacancy(...):
    ...

# pymatgen.analysis.defects.core.center_structure(structure: 'Structure', ref_fpos: 'ArrayLike') -> 'Structure'
@register_function(
    aliases=[
     "center_structure",
     "centering function",
     "move atoms to closest image",
     "shift to reference fractional position",
     "wrap to center"
    ],
    category="defects",
    description="Shift all sites in a structure to the periodic image nearest a given reference fractional position, effectively centering the structure around that point.",
    examples=[
     "from pymatgen.analysis.defects.core import center_structure\ncentered = center_structure(structure, [0.5, 0.5, 0.5])"
    ],
    key_results=[
     {
      "attr": ".frac_coords",
      "returns": "np.ndarray",
      "note": "Fractional coordinates of all sites after the shift; each row is the fractional coordinate of a site now nearest to the reference position."
     },
     {
      "attr": ".lattice",
      "returns": "Lattice",
      "note": "The lattice of the centered structure (unchanged from the input structure)."
     }
    ],
    related=[
     "Adsorbate",
     "Defect",
     "DefectComplex",
     "DefectType",
     "Interstitial"
    ]
)
def center_structure(...):
    ...

# pymatgen.analysis.defects.core.get_element(sp_el: 'Species | Element') -> 'Element'
@register_function(
    aliases=[
     "base_element",
     "get_element",
     "pymatgen.analysis.defects.core.get_element",
     "species_to_element",
     "strip_oxidation_state"
    ],
    category="defects",
    description="Extracts the base Element from a Species (which may include oxidation state) or passes through an Element unchanged, used when you need the elemental symbol or atomic number from a potentially charged defect site.",
    examples=[
     "from pymatgen.core import Species; from pymatgen.analysis.defects.core import get_element; el = get_element(Species('Fe', 3)); print(el.symbol)  # 'Fe'"
    ],
    key_results=[
     {
      "attr": ".symbol",
      "returns": "str",
      "note": "Element symbol, e.g. 'Fe'"
     },
     {
      "attr": ".Z",
      "returns": "int",
      "note": "Atomic number, e.g. 26"
     },
     {
      "attr": ".name",
      "returns": "str",
      "note": "Full element name, e.g. 'Iron'"
     }
    ],
    related=[
     "Adsorbate",
     "Defect",
     "DefectComplex",
     "DefectType",
     "Interstitial"
    ]
)
def get_element(...):
    ...

# pymatgen.analysis.defects.core.get_plane_spacing(lattice: 'npt.NDArray') -> 'list[float]'
@register_function(
    aliases=[
     "crystallographic plane spacing",
     "get_plane_spacing",
     "interplanar spacing",
     "lattice plane distances",
     "plane spacing"
    ],
    category="defects",
    description="Computes the Cartesian spacing between periodic planes in a unit cell, used to determine interplanar distances for diffraction analysis or understanding crystallographic periodicity.",
    examples=[
     "assert np.allclose(get_plane_spacing(lattice), [2.785, 2.785, 5.239], atol=0.001)"
    ],
    related=[
     "Adsorbate",
     "Defect",
     "DefectComplex",
     "DefectType",
     "Interstitial"
    ]
)
def get_plane_spacing(...):
    ...

# pymatgen.analysis.defects.core.get_sc_fromstruct(base_struct: 'Structure', min_atoms: 'int' = 80, max_atoms: 'int' = 240, min_length: 'float' = 10.0, force_diagonal: 'bool' = False) -> 'NDArray | ArrayLike | None'
@register_function(
    aliases=[
     "cubic supercell",
     "get_sc_fromstruct",
     "optimal supercell shape",
     "supercell from structure",
     "supercell generation"
    ],
    category="defects",
    description="Generates an as-cubic-as-possible supercell from a given unit cell structure, typically used when setting up defect calculations to ensure sufficient cell size and minimal anisotropy.",
    examples=[
     "sc_mat = get_sc_fromstruct(uc)",
     "assert sc_mat.shape == (3, 3)"
    ],
    key_results=[
     {
      "attr": "returned object (pymatgen Structure)",
      "returns": "Structure",
      "note": "The generated supercell; attributes like lattice, num_sites, and methods like to() are commonly used."
     }
    ],
    related=[
     "Adsorbate",
     "Defect",
     "DefectComplex",
     "DefectType",
     "Interstitial"
    ]
)
def get_sc_fromstruct(...):
    ...

# pymatgen.analysis.defects.core.get_vacancy(structure: 'Structure', isite: 'int', **kwargs) -> 'Vacancy'
@register_function(
    aliases=[
     "defect generation",
     "get vacancy",
     "get_vacancy",
     "pymatgen vacancy",
     "site vacancy",
     "vacancy creation",
     "vacancy from structure"
    ],
    category="defects",
    description="Convenience function to quickly create a Vacancy defect object from a structure and site index, used to model missing atoms in a crystal for defect analysis.",
    examples=[
     "vac = get_vacancy(structure, 0); print(vac.name)"
    ],
    key_results=[
     {
      "attr": ".name",
      "returns": "str",
      "note": "e.g., 'v_Ga' for a Ga vacancy, derived from the element at the site"
     },
     {
      "attr": ".site",
      "returns": "Site",
      "note": "the original site object where the vacancy is created"
     },
     {
      "attr": ".charge",
      "returns": "int",
      "note": "the charge state of the vacancy (default 0 if not specified)"
     },
     {
      "attr": ".structure",
      "returns": "Structure",
      "note": "the parent structure containing the vacancy"
     }
    ],
    related=[
     "Adsorbate",
     "Defect",
     "DefectComplex",
     "DefectType",
     "Interstitial"
    ]
)
def get_vacancy(...):
    ...

# pymatgen.analysis.defects.core.perturb_sites(structure: 'Structure', distance: 'float', min_distance: 'float | None' = None, site_indices: 'list | None' = None) -> 'None'
@register_function(
    aliases=[
     "atomic jitter",
     "perturb_sites",
     "random perturbation",
     "structure perturbation",
     "symmetry breaking displacement"
    ],
    category="defects",
    description="Randomly displaces atomic positions in a structure to break symmetry, typically used to avoid symmetric local minima when relaxing defect structures or finding energy minimum configurations.",
    examples=[
     "perturb_sites(structure, distance=0.1, min_distance=0.05, site_indices=[0, 1, 2])"
    ],
    key_results=[
     {
      "attr": "structure.cart_coords (after call)",
      "returns": "np.ndarray",
      "note": "The Cartesian coordinates of all sites after perturbation; each site is displaced by a random vector of magnitude between min_distance and distance (or exactly distance if min_distance is None)."
     }
    ],
    related=[
     "Adsorbate",
     "Defect",
     "DefectComplex",
     "DefectType",
     "Interstitial"
    ]
)
def perturb_sites(...):
    ...

# pymatgen.analysis.defects.core.update_structure(structure: 'Structure', site: 'PeriodicSite', defect_type: 'DefectType') -> 'None'
@register_function(
    aliases=[
     "add defect to structure",
     "defect creation",
     "point defect insertion",
     "structure defect modification",
     "update_structure"
    ],
    category="defects",
    description="This function updates a pymatgen Structure object in\u2011place to introduce a point defect (vacancy, substitution, or interstitial) at a given PeriodicSite.",
    examples=[
     "from pymatgen.analysis.defects.core import update_structure, DefectType\nupdate_structure(structure, site, DefectType.Vacancy)  # structure is mutated in‑place"
    ],
    key_results=[
     {
      "attr": "structure (mutated in‑place)",
      "returns": "None",
      "note": "The input `structure` is modified; no value is returned. After call, the structure contains the defect: a site removed, replaced, or inserted."
     }
    ],
    related=[
     "Adsorbate",
     "Defect",
     "DefectComplex",
     "DefectType",
     "Interstitial"
    ]
)
def update_structure(...):
    ...

# pymatgen.analysis.defects.finder.DefectSiteFinder(symprec: 'float' = 0.01, angle_tolerance: 'float' = 5.0) -> 'None'
@register_function(
    aliases=[
     "DefectSiteFinder",
     "defect finder",
     "defect localization",
     "defect location finder",
     "defect position finder",
     "defect site finder"
    ],
    category="defects",
    description="Identifies the fractional coordinates of a point defect (impurity or native) in a pristine structure by comparing a relaxed defect structure to the pristine reference, without needing prior knowledge of the defect type.",
    examples=[
     "finder = DefectSiteFinder()",
     "frac_pos_guess = finder.get_native_defect_position(sc, base)",
     "fpos = finder.get_defect_fpos(sc_locked, sub.structure)",
     "fpos = finder.get_defect_fpos(sub_sc_struct, sub.structure)",
     "fpos = finder.get_defect_fpos(sc, inter.structure)",
     "fpos = finder.get_defect_fpos(inter_sc_struct, inter.structure)"
    ],
    key_results=[
     {
      "attr": ".get_defect_fpos(defect_structure, base_structure, remove_oxi=True)",
      "returns": "ArrayLike",
      "note": "Returns the defect position in fractional coordinates (array of length 3) relative to the pristine structure's lattice."
     }
    ],
    related=[
     "SiteGroup",
     "SiteVec",
     "best_match",
     "cosine_similarity",
     "get_site_groups"
    ]
)
def DefectSiteFinder(...):
    ...

# pymatgen.analysis.defects.finder.SiteGroup(species: ForwardRef('str'), similar_sites: ForwardRef('list[int]'), vec: ForwardRef('NDArray'))
@register_function(
    aliases=[
     "SiteGroup",
     "defect site group",
     "equivalent sites group",
     "symmetry group for sites"
    ],
    category="defects",
    description="Represents a group of symmetrically equivalent sites in a defect structure, used to store the chemical species, list of site indices that are symmetry-equivalent, and a vector (e.g., fractional coordinates or displacement) for the group.",
    examples=[
     "import numpy as np\nfrom pymatgen.analysis.defects.finder import SiteGroup\nsg = SiteGroup(species='Ga', similar_sites=[0, 2, 5], vec=np.array([0.5, 0.5, 0.5]))\nprint(sg.species, sg.similar_sites, sg.vec)"
    ],
    key_results=[
     {
      "attr": ".species",
      "returns": "str",
      "note": "Chemical species of the group, e.g. 'Ga' for gallium."
     },
     {
      "attr": ".similar_sites",
      "returns": "list[int]",
      "note": "Indices of sites that are symmetrically equivalent to this group."
     },
     {
      "attr": ".vec",
      "returns": "numpy.ndarray",
      "note": "A NumPy array representing a vector (e.g., fractional coordinates or displacement vector) associated with the site group."
     }
    ],
    related=[
     "DefectSiteFinder",
     "SiteVec",
     "best_match",
     "cosine_similarity",
     "get_site_groups"
    ]
)
def SiteGroup(...):
    ...

# pymatgen.analysis.defects.finder.SiteVec(species: ForwardRef('str'), site: ForwardRef('Structure'), vec: ForwardRef('NDArray'))
@register_function(
    aliases=[
     "SiteVec",
     "defect site tuple",
     "named tuple for defect site",
     "site representation",
     "site vector"
    ],
    category="defects",
    description="A simple named tuple that bundles a species label, a pymatgen Structure object, and a numpy array vector to represent a single site within a defect structure, used when manipulating or iterating over defect sites.",
    examples=[
     "from pymatgen.analysis.defects.finder import SiteVec\nimport numpy as np\nsv = SiteVec(species='Ga', site=some_structure, vec=np.array([0.25, 0.25, 0.25]))"
    ],
    key_results=[
     {
      "attr": ".species",
      "returns": "str",
      "note": "Element or species string, e.g. 'Ga' or 'O'"
     },
     {
      "attr": ".site",
      "returns": "Structure",
      "note": "A pymatgen Structure object representing the full structure or a copy containing this site"
     },
     {
      "attr": ".vec",
      "returns": "NDArray",
      "note": "Numpy array of fractional coordinates or vector, e.g. np.array([0.5, 0.5, 0.5])"
     }
    ],
    related=[
     "DefectSiteFinder",
     "SiteGroup",
     "best_match",
     "cosine_similarity",
     "get_site_groups"
    ]
)
def SiteVec(...):
    ...

# pymatgen.analysis.defects.finder.best_match(sv: 'SiteVec', sgs: 'list[SiteGroup]') -> 'tuple[SiteGroup, float]'
@register_function(
    aliases=[
     "best_match",
     "cosine similarity match",
     "defect site matching",
     "pristine site group assignment",
     "site vector similarity"
    ],
    category="defects",
    description="Find the best matching group of symmetrically equivalent sites in the pristine structure for a given site in the defect structure, based on cosine similarity of site vectors and matching species.",
    examples=[
     "from pymatgen.analysis.defects.finder import best_match; best_sg, sim = best_match(sv, sgs)"
    ],
    key_results=[
     {
      "attr": "best_sg.species",
      "returns": "str or Species",
      "note": "The species label of the best matching site group, e.g., 'Ga' or Element."
     },
     {
      "attr": "best_sg.vec",
      "returns": "list or numpy array",
      "note": "The vector representing the site group (e.g., fractional coordinates or symmetry vector)."
     },
     {
      "attr": "similarity (second return value)",
      "returns": "float",
      "note": "Cosine similarity between the input site vector and the best matching group's vector."
     }
    ],
    related=[
     "DefectSiteFinder",
     "SiteGroup",
     "SiteVec",
     "cosine_similarity",
     "get_site_groups"
    ]
)
def best_match(...):
    ...

# pymatgen.analysis.defects.finder.cosine_similarity(vec1: 'ArrayLike', vec2: 'ArrayLike') -> 'float'
@register_function(
    aliases=[
     "angular similarity",
     "cos_sim",
     "cosine_similarity",
     "feature vector similarity",
     "normalized dot product",
     "vector similarity"
    ],
    category="defects",
    description="Calculate the cosine similarity between two vectors, often used to compare defect feature vectors or structural fingerprints in high-throughput defect analysis.",
    examples=[
     "similarity = pymatgen.analysis.defects.finder.cosine_similarity([1, 2, 3], [4, 5, 6])"
    ],
    key_results=[
     {
      "attr": "return value",
      "returns": "float",
      "note": "Cosine similarity between -1 and 1; higher values indicate greater directional alignment."
     }
    ],
    related=[
     "DefectSiteFinder",
     "SiteGroup",
     "SiteVec",
     "best_match",
     "get_site_groups"
    ]
)
def cosine_similarity(...):
    ...

# pymatgen.analysis.defects.finder.get_site_groups(struct: 'Structure', symprec: 'float' = 0.01, angle_tolerance: 'float' = 5.0) -> 'list[SiteGroup]'
@register_function(
    aliases=[
     "SpacegroupAnalyzer site grouping",
     "get_site_groups",
     "site groups",
     "symmetry analysis",
     "symmetry equivalent sites"
    ],
    category="defects",
    description="Groups the sites in a crystal structure by symmetry equivalence, returning a list of SiteGroup namedtuples that each represent a set of symmetrically equivalent sites, commonly used in defect analysis to identify unique sites.",
    examples=[
     "from pymatgen.core import Structure\nfrom pymatgen.analysis.defects.finder import get_site_groups\n\nsites = get_site_groups(structure, symprec=0.01)\nfor sg in sites:\n    print(sg.species, sg.similar_sites[:5])"
    ],
    key_results=[
     {
      "attr": "list[SiteGroup] (returned object)",
      "returns": "list of namedtuples",
      "note": "Each SiteGroup has .species (str, e.g. 'Ga'), .similar_sites (list of int indices into the structure), and .vec (numpy array, SOAP vector for the first site in the group)"
     }
    ],
    related=[
     "DefectSiteFinder",
     "SiteGroup",
     "SiteVec",
     "best_match",
     "cosine_similarity"
    ]
)
def get_site_groups(...):
    ...

# pymatgen.analysis.defects.finder.get_site_vecs(struct: 'Structure') -> 'list[SiteVec]'
@register_function(
    aliases=[
     "SOAP vectors",
     "get_site_vecs",
     "site representation",
     "site vectors",
     "structural descriptor"
    ],
    category="defects",
    description="Computes SOAP (smooth overlap of atomic positions) vector descriptors for every site in a crystal structure, returning a list of SiteVec objects that each contain the species, the original site, and its vector; used when a materials scientist wants to obtain site-level structural fingerprints for machine learning, similarity analysis, or defect characterization.",
    examples=[
     "from pymatgen.core import Structure; from pymatgen.analysis.defects.finder import get_site_vecs; struct = Structure.from_file('POSCAR'); site_vecs = get_site_vecs(struct); print(site_vecs[0].vec)"
    ],
    key_results=[
     {
      "attr": "species",
      "returns": "str",
      "note": "e.g., 'Ga', 'O', 'Li' – the element or species string of the site"
     },
     {
      "attr": "site",
      "returns": "PeriodicSite",
      "note": "the full pymatgen Site object with coordinates, lattice, etc."
     },
     {
      "attr": "vec",
      "returns": "list[float]",
      "note": "the SOAP vector as a fixed-length list of floats, e.g., [0.12, 0.45, ...]"
     }
    ],
    related=[
     "DefectSiteFinder",
     "SiteGroup",
     "SiteVec",
     "best_match",
     "cosine_similarity"
    ]
)
def get_site_vecs(...):
    ...

# pymatgen.analysis.defects.finder.get_soap_vec(struct: 'Structure') -> 'NDArray'
@register_function(
    aliases=[
     "SOAP",
     "SOAP vector",
     "Smooth Overlap of Atomic Positions",
     "atomic environment descriptor",
     "get_soap_vec",
     "structural fingerprint"
    ],
    category="defects",
    description="Computes the Smooth Overlap of Atomic Positions (SOAP) descriptor vector for each site in a crystal structure, enabling characterization of local atomic environments for tasks such as defect identification or structure comparison.",
    examples=[
     "soap_vecs = get_soap_vec(structure)  # structure is a pymatgen Structure object"
    ],
    key_results=[
     {
      "attr": ".shape",
      "returns": "tuple",
      "note": "Shape (n_sites, n_soap_features) where n_sites is the number of atoms in the structure and n_soap_features is determined by the SOAP parameters (r_cut=5, n_max=8, l_max=6)."
     },
     {
      "attr": ".dtype",
      "returns": "numpy.dtype",
      "note": "Data type of the array elements, typically float64."
     }
    ],
    related=[
     "DefectSiteFinder",
     "SiteGroup",
     "SiteVec",
     "best_match",
     "cosine_similarity"
    ]
)
def get_soap_vec(...):
    ...

# pymatgen.analysis.defects.finder.get_weighted_average_position(lattice: 'Lattice', frac_positions: 'ArrayLike', weights: 'ArrayLike | None' = None) -> 'NDArray'
@register_function(
    aliases=[
     "center of mass in periodic system",
     "get_weighted_average_position",
     "mass center in fractional coordinates",
     "periodic centroid",
     "weighted average position",
     "weighted centroid"
    ],
    category="defects",
    description="Find the weighted center of mass of a group of atomic positions within a periodic unit cell, handling periodic boundary conditions by iteratively adjusting the average to the closest image of each site, useful for locating the centroid of a molecule or defect cluster that is smaller than the cell.",
    examples=[
     "import numpy as np; from pymatgen.core.lattice import Lattice; from pymatgen.analysis.defects.finder import get_weighted_average_position; lattice = Lattice.cubic(10); pos = [[0.1,0.2,0.3], [0.9,0.8,0.7]]; weights = [1, 2]; avg = get_weighted_average_position(lattice, pos, weights)"
    ],
    key_results=[
     {
      "attr": "return value",
      "returns": "NDArray",
      "note": "Array of shape (3,) containing fractional coordinates of the weighted average position."
     }
    ],
    related=[
     "DefectSiteFinder",
     "SiteGroup",
     "SiteVec",
     "best_match",
     "cosine_similarity"
    ]
)
def get_weighted_average_position(...):
    ...

# pymatgen.analysis.defects.generators.AntiSiteGenerator(symprec: 'float' = 0.01, angle_tolerance: 'float' = 5) -> 'None'
@register_function(
    aliases=[
     "AntiSiteGenerator",
     "anti-site defects",
     "antisite generator",
     "defect enumeration",
     "substitution generator"
    ],
    category="defects",
    description="Generates all possible anti-site substitution defects (where an atom of one element replaces another element on its site) in a given crystal structure, used to enumerate antisite defects for defect calculations.",
    examples=[
     "anti_gen = AntiSiteGenerator().get_defects(gan_struct)"
    ],
    key_results=[
     {
      "attr": ".symprec",
      "returns": "float",
      "note": "Tolerance for symmetry finding (default 0.01)."
     },
     {
      "attr": ".angle_tolerance",
      "returns": "float",
      "note": "Angle tolerance for symmetry finding (default 5)."
     },
     {
      "attr": "generate(structure)",
      "returns": "Generator[Substitution]",
      "note": "Yields Substitution defect objects; each Substitution has a .name attribute, e.g., 'Ga_As' for a gallium atom on an arsenic site."
     }
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "ChargeInterstitialGenerator",
     "DefectGenerator",
     "Interstitial",
     "InterstitialGenerator"
    ]
)
def AntiSiteGenerator(...):
    ...

# pymatgen.analysis.defects.generators.ChargeInsertionAnalyzer(chgcar: 'VolumetricData', working_ion: 'str' = 'Li', clustering_tol: 'float' = 0.5, ltol: 'float' = 0.2, stol: 'float' = 0.3, angle_tol: 'float' = 5, min_dist: 'float' = 0.9) -> 'None'
@register_function(
    aliases=[
     "ChargeInsertionAnalyzer",
     "Li insertion site finder",
     "charge density insertion analysis",
     "charge minima site detection",
     "defect candidate generation"
    ],
    category="defects",
    description="Analyzes charge density (e.g., from AECCAR or CHGCAR) to identify candidate insertion sites for a working ion (e.g., Li) by locating charge minima, then groups similar insertion sites for further filtering and analysis.",
    examples=[
     "cia = ChargeInsertionAnalyzer(chgcar)",
     "insert_groups = cia.filter_and_group(max_avg_charge=0.5)"
    ],
    key_results=[
     {
      "attr": ".labeled_sites",
      "returns": "list of tuples (fcoords, label)",
      "note": "Each tuple contains fractional coordinates (list of float) and an integer label for uniqueness grouping."
     },
     {
      "attr": ".local_minima",
      "returns": "list of array-like",
      "note": "Lists all local minima positions (fractional coordinates) without labeling."
     },
     {
      "attr": ".filter_and_group(avg_radius, max_avg_charge)",
      "returns": "list of tuples (avg_charge, site_group)",
      "note": "Filters sites by average charge density within a given radius; returns groups with their average charge value."
     }
    ],
    related=[
     "AntiSiteGenerator",
     "ChargeInterstitialGenerator",
     "DefectGenerator",
     "Interstitial",
     "InterstitialGenerator"
    ]
)
def ChargeInsertionAnalyzer(...):
    ...

# pymatgen.analysis.defects.generators.ChargeInterstitialGenerator(clustering_tol: 'float' = 0.6, ltol: 'float' = 0.2, stol: 'float' = 0.3, angle_tol: 'float' = 5, min_dist: 'float' = 1.0, avg_radius: 'float' = 0.4, max_avg_charge: 'float' = 0.9, max_insertions: 'int | None' = None) -> 'None'
@register_function(
    aliases=[
     "ChargeInterstitialGenerator",
     "Chgcar interstitial generator",
     "charge interstitial generator",
     "charge-based interstitial generator",
     "interstitial defect generator"
    ],
    category="defects",
    description="Generates interstitial defect configurations by analyzing charge density to find low-energy insertion sites, used by materials scientists to create candidate interstitials for further defect calculations.",
    examples=[
     "gen = ChargeInterstitialGenerator().get_defects(chgcar_fe3o4, {\"Ga\"})"
    ],
    key_results=[
     {
      "attr": ".generate(chgcar, insert_species, **kwargs)",
      "returns": "Generator[Interstitial, None, None]",
      "note": "Yields Interstitial objects representing candidate insertion sites, each containing structure and site information."
     },
     {
      "attr": ".get_defects(structure, insertions, multiplicities, equivalent_positions, **kwargs)",
      "returns": "Generator[Interstitial, None, None]",
      "note": "Inherited method to generate interstitials from explicit insertion sites (bypasses charge analysis)."
     }
    ],
    related=[
     "AntiSiteGenerator",
     "ChargeInsertionAnalyzer",
     "DefectGenerator",
     "Interstitial",
     "InterstitialGenerator"
    ]
)
def ChargeInterstitialGenerator(...):
    ...

# pymatgen.analysis.defects.generators.DefectGenerator()
@register_function(
    aliases=[
     "DefectGenerator",
     "defect generator",
     "point defect generator",
     "pymatgen defect generator"
    ],
    category="defects",
    description="Abstract base class for generating point defects in crystal structures, providing a common interface (generate/get_defects) that concrete subclasses implement to yield Defect objects.",
    examples=[
     "# Typical usage with a concrete subclass (e.g., VacancyGenerator):\ngen = SomeConcreteDefectGenerator(structure, symprec=0.01)\ndefects = gen.get_defects()\nfor defect in defects:\n    print(defect.name)"
    ],
    key_results=[
     {
      "attr": ".generate(*args, **kwargs)",
      "returns": "Generator[Defect, None, None]",
      "note": "Yields Defect objects one by one. Concrete subclasses override this method to produce specific defect types (e.g., vacancies, substitutions)."
     },
     {
      "attr": ".get_defects(*args, **kwargs)",
      "returns": "list[Defect]",
      "note": "Alias for generate() that collects all yielded defects into a list."
     }
    ],
    related=[
     "AntiSiteGenerator",
     "ChargeInsertionAnalyzer",
     "ChargeInterstitialGenerator",
     "Interstitial",
     "InterstitialGenerator"
    ]
)
def DefectGenerator(...):
    ...

# pymatgen.analysis.defects.generators.Interstitial(structure: 'Structure', site: 'PeriodicSite', multiplicity: 'int' = 1, oxi_state: 'float | None' = None, equivalent_sites: 'list[PeriodicSite] | None' = None, symprec: 'float' = 0.01, angle_tolerance: 'float' = 5, user_charges: 'list[int] | None' = None) -> 'None'
@register_function(
    aliases=[
     "Interstitial",
     "i_defect",
     "interstitial defect",
     "interstitial site"
    ],
    category="defects",
    description="Represents an interstitial defect in a crystal by inserting an extra atom at a specified site, enabling calculations of its name, structure, charge states, and element changes.",
    examples=[
     "inter = Interstitial(structure=defect_entries[0].defect.structure, site=PeriodicSite(\"H\", [0, 0, 0], defect_entries[0].defect.structure.lattice",
     "inter = Interstitial(s, n_site)",
     "assert inter.oxi_state == 3",
     "assert inter.get_charge_states() == [-1, 0, 1, 2, 3, 4]",
     "assert np.allclose(inter.defect_structure[0].frac_coords, inter_fpos)",
     "sc = inter.get_supercell_structure()"
    ],
    key_results=[
     {
      "attr": ".name",
      "returns": "str",
      "note": "e.g., 'Li_i' for a lithium interstitial"
     },
     {
      "attr": ".defect_structure",
      "returns": "Structure",
      "note": "A copy of the original structure with the interstitial atom inserted at index 0"
     },
     {
      "attr": ".defect_site_index",
      "returns": "int",
      "note": "Always 0 (the interstitial is always placed first in the structure)"
     },
     {
      "attr": ".element_changes",
      "returns": "dict[Element, int]",
      "note": "Mapping of element to change in count, e.g., {Element('Li'): 1} for a Li interstitial"
     }
    ],
    related=[
     "AntiSiteGenerator",
     "ChargeInsertionAnalyzer",
     "ChargeInterstitialGenerator",
     "DefectGenerator",
     "InterstitialGenerator"
    ]
)
def Interstitial(...):
    ...

# pymatgen.analysis.defects.generators.InterstitialGenerator(min_dist: 'float' = 0.5) -> 'None'
@register_function(
    aliases=[
     "InterstitialGenerator",
     "defect insertion",
     "interstitial defect generator",
     "point defect generator",
     "pymatgen interstitial generation"
    ],
    category="defects",
    description="Generates interstitial point defects in a crystal structure by inserting atoms at specified fractional coordinates, filtering out positions too close to existing atoms based on a minimum distance.",
    examples=[
     "gen = InterstitialGenerator().get_defects(gan_struct, insertions={\"Mg\": [[0, 0, 0]]}",
     "gen = InterstitialGenerator().get_defects(gan_struct, insertions={\"Mg\": [[0, 0, 0], bad_site]}"
    ],
    key_results=[
     {
      "attr": "min_dist",
      "returns": "float",
      "note": "Minimum allowed distance between an interstitial site and the nearest atom in the bulk structure (default 0.5 Å)."
     },
     {
      "attr": "generate(structure, insertions, multiplicities, equivalent_positions, **kwargs)",
      "returns": "Generator[Interstitial]",
      "note": "Yields Interstitial objects each containing the bulk structure, the inserted PeriodicSite, multiplicity, equivalent sites, and optional keyword arguments passed to the Interstitial constructor."
     }
    ],
    related=[
     "AntiSiteGenerator",
     "ChargeInsertionAnalyzer",
     "ChargeInterstitialGenerator",
     "DefectGenerator",
     "Interstitial"
    ]
)
def InterstitialGenerator(...):
    ...

# pymatgen.analysis.defects.generators.Substitution(structure: 'Structure', site: 'PeriodicSite', multiplicity: 'int | None' = None, oxi_state: 'float | None' = None, equivalent_sites: 'list[PeriodicSite] | None' = None, symprec: 'float' = 0.01, angle_tolerance: 'float' = 5, user_charges: 'list[int] | None' = None) -> 'None'
@register_function(
    aliases=[
     "Substitution",
     "Substitution defect",
     "antisite defect (if same lattice site, different species)",
     "pymatgen Substitution class",
     "replacement defect",
     "single-site substitution"
    ],
    category="defects",
    description="Represent a substitutional defect where one atom in a crystal structure is replaced by a different species, enabling calculation of defect properties such as charge states, multiplicity, and the resulting defect structure.",
    examples=[
     "sub = Substitution(s, o_site)",
     "sub2 = Substitution(s, o_site2)",
     "assert sub.oxi_state == 1",
     "assert sub.get_charge_states() == [-1, 0, 1, 2]",
     "assert sub.get_multiplicity() == 2",
     "sc, site_ = sub.get_supercell_structure(return_site=True)"
    ],
    key_results=[
     {
      "attr": ".name",
      "returns": "str",
      "note": "Defect name formatted as 'replacing_species_original_species', e.g., 'Mg_Ga' for Mg substituting on a Ga site."
     },
     {
      "attr": ".defect_structure",
      "returns": "Structure",
      "note": "A pymatgen Structure object with the original atom removed and the new atom inserted at the same site."
     },
     {
      "attr": ".element_changes",
      "returns": "dict[Element, int]",
      "note": "Dictionary mapping elements to their net change, e.g., {Ga: -1, Mg: +1} for Mg substitution on Ga."
     },
     {
      "attr": ".get_charge_states()",
      "returns": "list[int]",
      "note": "Returns a list of charge states for the defect, either from user_charges or determined automatically."
     }
    ],
    related=[
     "AntiSiteGenerator",
     "ChargeInsertionAnalyzer",
     "ChargeInterstitialGenerator",
     "DefectGenerator",
     "Interstitial"
    ]
)
def Substitution(...):
    ...

# pymatgen.analysis.defects.generators.SubstitutionGenerator(symprec: 'float' = 0.01, angle_tolerance: 'float' = 5) -> 'None'
@register_function(
    aliases=[
     "SubstitutionGenerator",
     "dopant generator",
     "element substitution generator",
     "substitution defect generator"
    ],
    category="defects",
    description="Generate substitutional defects (dopants, alloying) at symmetry-distinct sites in a crystal structure.",
    examples=[
     "sub_generator = SubstitutionGenerator().get_defects(gan_struct, {\"Ga\": [\"Mg\", \"Ca\"]}",
     "sub_generator = SubstitutionGenerator().get_defects(gan_struct, {\"Ga\": \"Mg\"})"
    ],
    key_results=[
     {
      "attr": ".generate",
      "returns": "Generator[Substitution, None, None]",
      "note": "Method to generate substitution defects; yields Substitution objects for each symmetry distinct site with the specified substitution."
     },
     {
      "attr": ".symprec",
      "returns": "float",
      "note": "Tolerance for symmetry finding (parameter for SpacegroupAnalyzer)."
     },
     {
      "attr": ".angle_tolerance",
      "returns": "float",
      "note": "Angle tolerance for symmetry finding (parameter for SpacegroupAnalyzer)."
     }
    ],
    related=[
     "AntiSiteGenerator",
     "ChargeInsertionAnalyzer",
     "ChargeInterstitialGenerator",
     "DefectGenerator",
     "Interstitial"
    ]
)
def SubstitutionGenerator(...):
    ...

# pymatgen.analysis.defects.generators.TopographyAnalyzer(structure: 'Structure', framework_ions: 'list[str]', cations: 'list[str]', image_tol: 'float' = 0.0001, max_cell_range: 'int' = 1, check_volume: 'bool' = True, constrained_c_frac: 'float' = 0.5, thickness: 'float' = 0.5, clustering_tol: 'float' = 0.5, min_dist: 'float' = 0.9, ltol: 'float' = 0.2, stol: 'float' = 0.3, angle_tol: 'float' = 5) -> 'None'
@register_function(
    aliases=[
     "TopographyAnalyzer",
     "Voronoi interstitial finder",
     "diffusion pathway analyzer",
     "interstitial site detector",
     "topological site analysis"
    ],
    category="defects",
    description="Perform topological analysis of a crystal structure using Voronoi tessellations to identify potential interstitial sites and analyze diffusion pathways.",
    examples=[
     "ta = TopographyAnalyzer(struct, [\"Fe\", \"O\"], [], check_volume=True)",
     "node_struct = ta.get_structure_with_nodes()",
     "ta = TopographyAnalyzer(struct, [\"O\"], [\"Fe\"], check_volume=True)"
    ],
    key_results=[
     {
      "attr": ".labeled_sites",
      "returns": "List[Site]",
      "note": "List of sites (including framework, cations, and interstitial nodes) after Voronoi construction, each with labels and fractional coordinates."
     },
     {
      "attr": ".get_structure_with_nodes()",
      "returns": "Structure",
      "note": "Returns a Structure object with the original atoms plus interstitial nodes inserted as dummy species (e.g., 'X') for visualization or further analysis."
     }
    ],
    related=[
     "AntiSiteGenerator",
     "ChargeInsertionAnalyzer",
     "ChargeInterstitialGenerator",
     "DefectGenerator",
     "Interstitial"
    ]
)
def TopographyAnalyzer(...):
    ...

# pymatgen.analysis.defects.generators.Vacancy(structure: 'Structure', site: 'PeriodicSite', multiplicity: 'int | None' = None, oxi_state: 'float | None' = None, equivalent_sites: 'list[PeriodicSite] | None' = None, symprec: 'float' = 0.01, angle_tolerance: 'float' = 5, user_charges: 'list[int] | None' = None) -> 'None'
@register_function(
    aliases=[
     "V",
     "V_defect",
     "Vacancy",
     "vacancy",
     "vacancy defect"
    ],
    category="defects",
    description="Represents a vacancy defect in a crystal structure by removing an atom from a given site, enabling computation of properties like multiplicity, oxidation state, and the resulting defect structure for downstream defect calculations.",
    examples=[
     "vac = Vacancy(s, s.sites[0])",
     "vac2 = Vacancy(s, s.sites[1])",
     "assert vac.oxi_state == -3",
     "assert vac.get_charge_states() == [-4, -3, -2, -1, 0, 1]",
     "assert vac.get_multiplicity() == 2",
     "assert vac.get_supercell_structure().formula == \"Ga63 N64\""
    ],
    key_results=[
     {
      "attr": ".name",
      "returns": "str",
      "note": "e.g. 'v_Ga' for a Ga vacancy"
     },
     {
      "attr": ".defect_structure",
      "returns": "Structure",
      "note": "bulk structure with the vacancy site removed"
     },
     {
      "attr": ".element_changes",
      "returns": "dict[Element, int]",
      "note": "e.g. {Element Ga: -1} indicating removal of one Ga atom"
     },
     {
      "attr": ".get_multiplicity",
      "returns": "int",
      "note": "number of equivalent sites in the symmetrized structure"
     }
    ],
    related=[
     "AntiSiteGenerator",
     "ChargeInsertionAnalyzer",
     "ChargeInterstitialGenerator",
     "DefectGenerator",
     "Interstitial"
    ]
)
def Vacancy(...):
    ...

# pymatgen.analysis.defects.generators.VacancyGenerator(symprec: 'float' = 0.01, angle_tolerance: 'float' = 5) -> 'None'
@register_function(
    aliases=[
     "VacancyGenerator",
     "defect generator",
     "pymatgen vacancy generation",
     "vacancy generator"
    ],
    category="defects",
    description="Generates vacancy defects (missing atoms) from a bulk crystal structure, allowing control over which species are removed and symmetry handling, for use in defect calculations.",
    examples=[
     "vg = VacancyGenerator()",
     "vac = next(vg.generate(s, rm_species=[\"O\"]))",
     "vacancy_generator = VacancyGenerator().get_defects(gan_struct)",
     "vacancy_generator = VacancyGenerator().get_defects(gan_struct, [\"Ga\"])",
     "vacancy_generator = list(VacancyGenerator().get_defects(gan_struct, rm_species=[\"Xe\"])"
    ],
    key_results=[
     {
      "attr": ".generate(structure, rm_species=None, **kwargs)",
      "returns": "Generator[Vacancy, None, None]",
      "note": "Yields Vacancy objects; each represents a missing atom at a symmetrically distinct site. The species to remove is controlled by rm_species."
     },
     {
      "attr": ".get_defects()",
      "returns": "list of Defect objects",
      "note": "Inherited from DefectGenerator; returns all defects generated so far in a list."
     }
    ],
    related=[
     "AntiSiteGenerator",
     "ChargeInsertionAnalyzer",
     "ChargeInterstitialGenerator",
     "DefectGenerator",
     "Interstitial"
    ]
)
def VacancyGenerator(...):
    ...

# pymatgen.analysis.defects.generators.VoronoiInterstitialGenerator(clustering_tol: 'float' = 0.5, min_dist: 'float' = 0.9, ltol: 'float' = 0.2, stol: 'float' = 0.3, angle_tol: 'float' = 5, **kwargs) -> 'None'
@register_function(
    aliases=[
     "Voronoi interstitial generator",
     "Voronoi interstitial site generator",
     "VoronoiInterstitialGenerator",
     "interstitial site generator"
    ],
    category="defects",
    description="Generate candidate interstitial defect sites in a crystal structure by analyzing the Voronoi tessellation of the atomic positions, clustering nodes and filtering by minimum distance to atoms.",
    examples=[
     "gen = VoronoiInterstitialGenerator().get_defects(chgcar_fe3o4.structure, {\"Li\"})"
    ],
    key_results=[
     {
      "attr": ".clustering_tol",
      "returns": "float",
      "note": "Tolerance for clustering Voronoi nodes (default 0.5)."
     },
     {
      "attr": ".min_dist",
      "returns": "float",
      "note": "Minimum distance between an interstitial site and the nearest atom (default 0.9)."
     },
     {
      "attr": ".generate",
      "returns": "Generator[Interstitial, None, None]",
      "note": "Yields Interstitial objects for each candidate site for each species in insert_species."
     }
    ],
    related=[
     "AntiSiteGenerator",
     "ChargeInsertionAnalyzer",
     "ChargeInterstitialGenerator",
     "DefectGenerator",
     "Interstitial"
    ]
)
def VoronoiInterstitialGenerator(...):
    ...

# pymatgen.analysis.defects.generators.generate_all_native_defects(host: 'Structure | Chgcar', sub_generator: 'SubstitutionGenerator | None' = None, vac_generator: 'VacancyGenerator | None' = None, int_generator: 'ChargeInterstitialGenerator | None' = None, max_insertions: 'int | None' = None) -> 'Generator[Defect, None, None]'
@register_function(
    aliases=[
     "all defects from structure",
     "defect enumeration convenience",
     "generate_all_native_defects",
     "native defect generation",
     "vacancy substitution interstitial generator"
    ],
    category="defects",
    description="Convenience function to generate all native defects (vacancies, substitutions, and interstitials) for a given host crystal structure or CHGCAR charge density file, returning a generator of Defect objects that can be iterated or collected.",
    examples=[
     "gen = generate_all_native_defects(chgcar_fe3o4)",
     "gen = generate_all_native_defects(chgcar_fe3o4.structure)"
    ],
    key_results=[
     {
      "attr": ".name",
      "returns": "str",
      "note": "String identifying the defect, e.g. 'v_Ga' for a Ga vacancy, 'Ga_sub_Al' for Al substituted by Ga, or 'i_Ga' for a Ga interstitial."
     }
    ],
    related=[
     "AntiSiteGenerator",
     "ChargeInsertionAnalyzer",
     "ChargeInterstitialGenerator",
     "DefectGenerator",
     "Interstitial"
    ]
)
def generate_all_native_defects(...):
    ...

# pymatgen.analysis.defects.generators.remove_collisions(fcoords: 'npt.NDArray', structure: 'Structure', min_dist: 'float' = 0.9) -> 'npt.NDArray'
@register_function(
    aliases=[
     "collision removal",
     "defect site filtering",
     "filter points by distance",
     "minimum distance filter",
     "remove close points",
     "remove_collisions"
    ],
    category="defects",
    description="Filters out defect sites (points) that are too close to existing atoms in a crystal structure, ensuring physically realistic defect placements.",
    examples=[
     "import numpy as np; from pymatgen.analysis.defects.generators import remove_collisions; filtered = remove_collisions(np.random.rand(20,3), structure, min_dist=0.9)"
    ],
    key_results=[
     {
      "attr": "shape",
      "returns": "tuple of ints",
      "note": "e.g., (M, 3) where M is the number of surviving points, each row is fractional coordinates"
     },
     {
      "attr": "dtype",
      "returns": "numpy dtype",
      "note": "typically float64 or float32, same as input fcoords"
     },
     {
      "attr": "ndim",
      "returns": "int",
      "note": "always 2 for a set of coordinates"
     }
    ],
    related=[
     "AntiSiteGenerator",
     "ChargeInsertionAnalyzer",
     "ChargeInterstitialGenerator",
     "DefectGenerator",
     "Interstitial"
    ]
)
def remove_collisions(...):
    ...

# pymatgen.analysis.defects.recombination.boltzmann_filling(omega_i: 'float', temperature: 'npt.ArrayLike', n_states: 'int' = 30) -> 'npt.NDArray'
@register_function(
    aliases=[
     "Bose-Einstein factor",
     "boltzmann_filling",
     "occupation number",
     "phonon occupation",
     "phonon state filling"
    ],
    category="defects",
    description="Compute the Boltzmann (Bose-Einstein) occupation factor for the lowest n_states phonon levels at a given temperature or array of temperatures, used to model thermal population of vibrational states for processes like non-radiative recombination.",
    examples=[
     "results = boltzmann_filling(0.1, 300, n_states=6)",
     "assert np.allclose(results.flatten(), ref_results, rtol=1e-3)",
     "results2 = boltzmann_filling(0.1, [100, 300], n_states=6)"
    ],
    key_results=[
     {
      "attr": ".shape",
      "returns": "tuple of ints",
      "note": "e.g., (30, 1) for n_states=30 and one temperature; (30, 5) for five temperature points."
     },
     {
      "attr": ".dtype",
      "returns": "numpy.dtype",
      "note": "Typically float64."
     },
     {
      "attr": "[i, j] indexing",
      "returns": "float",
      "note": "Filling factor for phonon state i at temperature index j."
     }
    ],
    related=[
     "get_Rad_coef",
     "get_SRH_coef",
     "get_mQn",
     "get_mn",
     "pchip_eval"
    ]
)
def boltzmann_filling(...):
    ...

# pymatgen.analysis.defects.recombination.get_Rad_coef(T: 'float | npt.ArrayLike', dQ: 'float', dE: 'float', omega_i: 'float', omega_f: 'float', omega_photon: 'float', dipole_me: 'float', volume: 'float', g: 'int' = 1, occ_tol: 'float' = 0.001) -> 'npt.ArrayLike'
@register_function(
    aliases=[
     "Radiative coefficient",
     "get_Rad_coef",
     "rad_coef",
     "radiative capture coefficient",
     "radiative recombination coefficient"
    ],
    category="defects",
    description="Compute the radiative recombination coefficient for a given defect transition, used to estimate the rate of radiative carrier capture in semiconductors.",
    examples=[
     "get_Rad_coef(T=[100, 200, 300], dQ=1.0, dE=1.0, omega_i=0.2, omega_f=0.2, omega_photon=0.6, dipole_me=1, volume=1, g=1, )"
    ],
    key_results=[
     {
      "attr": ".shape",
      "returns": "tuple",
      "note": "Shape of the returned array, matching the shape of the input T (e.g., () for scalar, (N,) for array)."
     },
     {
      "attr": ".dtype",
      "returns": "numpy.dtype",
      "note": "Data type of the returned array, typically numpy.float64 or numpy.longdouble."
     }
    ],
    related=[
     "boltzmann_filling",
     "get_SRH_coef",
     "get_mQn",
     "get_mn",
     "pchip_eval"
    ]
)
def get_Rad_coef(...):
    ...

# pymatgen.analysis.defects.recombination.get_SRH_coef(T: 'float | npt.ArrayLike', dQ: 'float', dE: 'float', omega_i: 'float', omega_f: 'float', elph_me: 'float', volume: 'float', g: 'int' = 1, occ_tol: 'float' = 0.001) -> 'npt.ArrayLike'
@register_function(
    aliases=[
     "SRH coefficient",
     "Shockley-Read-Hall recombination coefficient",
     "capture coefficient",
     "get_SRH_coef",
     "non-radiative recombination coefficient"
    ],
    category="defects",
    description="Compute the Shockley-Read-Hall (SRH) non-radiative recombination coefficient for a defect, given phonon displacement, energies, frequencies, electron-phonon coupling, temperature(s), and cell volume.",
    examples=[
     "res = get_SRH_coef(T=[100, 200, 300], dQ=1.0, dE=1.0, omega_i=0.2, omega_f=0.2, elph_me=1, volume=1, g=1, )"
    ],
    key_results=[
     {
      "attr": "return value",
      "returns": "npt.ArrayLike",
      "note": "Capture coefficient in cm^3 s^-1, same shape as the input T (scalar or array)."
     }
    ],
    related=[
     "boltzmann_filling",
     "get_Rad_coef",
     "get_mQn",
     "get_mn",
     "pchip_eval"
    ]
)
def get_SRH_coef(...):
    ...

# pymatgen.analysis.defects.recombination.get_mQn(dQ: 'float', omega_i: 'float', omega_f: 'float', m_init: 'int', Nf: 'int', ovl: 'npt.NDArray') -> 'tuple[npt.ArrayLike, npt.ArrayLike]'
@register_function(
    aliases=[
     "defect recombination matrix elements",
     "get_mQn",
     "phonon matrix elements",
     "position operator matrix elements"
    ],
    category="defects",
    description="Compute the matrix elements of the position operator between initial and final phonon states for defect recombination calculations.",
    examples=[
     "e, matel = get_mQn(omega_i=omega_i, omega_f=omega_f, m_init=0, Nf=Nf, dQ=dQ, ovl=ovl"
    ],
    key_results=[
     {
      "attr": "energy_differences (tuple[0])",
      "returns": "numpy.ndarray",
      "note": "Array of energy differences between final and initial phonon states, computed as n_f * omega_f - m_init * omega_i."
     },
     {
      "attr": "matrix_elements (tuple[1])",
      "returns": "numpy.ndarray",
      "note": "Array of matrix element values <m_i|Q|n_f> for each final state, using harmonic oscillator factors and overlap integrals."
     }
    ],
    related=[
     "boltzmann_filling",
     "get_Rad_coef",
     "get_SRH_coef",
     "get_mn",
     "pchip_eval"
    ]
)
def get_mQn(...):
    ...

# pymatgen.analysis.defects.recombination.get_mn(dQ: 'float', omega_i: 'float', omega_f: 'float', m_init: 'int', en_final: 'float', en_pad: 'float' = 0.5) -> 'tuple[npt.ArrayLike, npt.ArrayLike]'
@register_function(
    aliases=[
     "FC factor",
     "get_mn",
     "matrix element",
     "overlap integral",
     "phonon transition matrix element",
     "position operator matrix element"
    ],
    category="defects",
    description="Computes matrix elements \u27e8m_i|n_f\u27e9 for the position operator between an initial phonon state and final phonon states within an energy window, used for calculating non-radiative capture coefficients or transition rates in defective materials.",
    examples=[
     "E, matels = get_mn(dQ=0.5, omega_i=0.01, omega_f=0.01, m_init=0, en_final=0.1, en_pad=0.05)"
    ],
    key_results=[
     {
      "attr": "E",
      "returns": "np.ndarray",
      "note": "Energies of final states (relative to bottom of final parabola) in eV, for states between en_final - en_pad and en_final + en_pad."
     },
     {
      "attr": "matels",
      "returns": "np.ndarray",
      "note": "Matrix elements ⟨m_i|n_f⟩ for each corresponding final state energy in E."
     }
    ],
    related=[
     "boltzmann_filling",
     "get_Rad_coef",
     "get_SRH_coef",
     "get_mQn",
     "pchip_eval"
    ]
)
def get_mn(...):
    ...

# pymatgen.analysis.defects.recombination.pchip_eval(x: 'npt.ArrayLike | float', x_coarse: 'npt.ArrayLike', y_coarse: 'npt.ArrayLike', pad_frac: 'float' = 0.2, n_points: 'int' = 5000) -> 'npt.ArrayLike'
@register_function(
    aliases=[
     "PCHIP interpolation",
     "coarse-to-fine interpolation",
     "defect recombination interpolation",
     "integral-preserving interpolation",
     "pchip_eval",
     "piecewise cubic Hermite interpolant evaluation"
    ],
    category="defects",
    description="Evaluates a piecewise cubic Hermite interpolant on a finer grid while preserving the integral of the coarse data, used to smoothly interpolate defect recombination energy or rate data derived from coarse sampling.",
    examples=[
     "fx = pchip_eval(xx, x_coarse=x_c, y_coarse=y_c)"
    ],
    key_results=[
     {
      "attr": "(return value)",
      "returns": "npt.ArrayLike",
      "note": "Array of interpolated values at input x. Same shape as x. Returns np.nan for any x outside the padded domain."
     }
    ],
    related=[
     "boltzmann_filling",
     "get_Rad_coef",
     "get_SRH_coef",
     "get_mQn",
     "get_mn"
    ]
)
def pchip_eval(...):
    ...

# pymatgen.analysis.defects.supercells.get_closest_sc_mat(uc_struct: 'Structure', sc_struct: 'Structure', sm: 'StructureMatcher | None' = None, debug: 'bool' = False) -> 'NDArray'
@register_function(
    aliases=[
     "SC matrix",
     "closest supercell matrix",
     "defect supercell matrix",
     "get_closest_sc_mat",
     "structure matching matrix",
     "supercell transformation"
    ],
    category="defects",
    description="Determine the supercell transformation matrix that best maps a given unit cell (host) structure to a supercell (defect) structure, used in defect calculations to recover the relationship between the pristine and defect-containing cells.",
    examples=[
     "sorted_results = get_closest_sc_mat(uc_struct, vac_sc, debug=True)",
     "res = get_closest_sc_mat(uc_struct=uc_struct, sc_struct=vac_struct, debug=False)"
    ],
    key_results=[
     {
      "attr": "sc_mat (normal return)",
      "returns": "numpy.ndarray (3x3)",
      "note": "Integer matrix such that `sc_struct = uc_struct * sc_mat` (approximately). Example: [[1,0,0],[0,2,0],[0,0,2]] for a 1x2x2 supercell."
     },
     {
      "attr": "debug list (when debug=True)",
      "returns": "list of tuples",
      "note": "Sorted list of (mean_distance, Lattice, sc_mat) for all candidate supercell matrices, with best first. Useful to inspect alternative transformations."
     }
    ],
    related=[
     "get_matched_structure_mapping",
     "get_matched_structure_mapping_old",
     "get_sc_fromstruct"
    ]
)
def get_closest_sc_mat(...):
    ...

# pymatgen.analysis.defects.supercells.get_matched_structure_mapping(uc_struct: 'Structure', sc_struct: 'Structure', sm: 'StructureMatcher | None' = None) -> 'tuple[NDArray, ArrayLike] | None'
@register_function(
    aliases=[
     "get_matched_structure_mapping",
     "structure mapping",
     "supercell mapping",
     "unit cell to supercell transformation"
    ],
    category="defects",
    description="Finds the supercell matrix and translation vector that map a supercell structure back onto its exact unit cell, used when you have a perfectly matched supercell and need to relate coordinates between the two cells.",
    examples=[
     "sc_mat2, _ = get_matched_structure_mapping(uc, sc)"
    ],
    key_results=[
     {
      "attr": "sc_m (first element of returned tuple)",
      "returns": "NDArray",
      "note": "Supercell matrix (3x3) that when applied to the unit cell lattice gives the supercell lattice."
     },
     {
      "attr": "total_t (second element of returned tuple)",
      "returns": "ArrayLike",
      "note": "Translation vector (3-element array of fractions) to apply after supercell matrix to align atomic positions between the two structures."
     }
    ],
    related=[
     "get_closest_sc_mat",
     "get_matched_structure_mapping_old",
     "get_sc_fromstruct"
    ]
)
def get_matched_structure_mapping(...):
    ...

# pymatgen.analysis.defects.supercells.get_matched_structure_mapping_old(uc_struct: 'Structure', sc_struct: 'Structure', sm: 'StructureMatcher | None' = None) -> 'tuple[NDArray, ArrayLike] | None'
@register_function(
    aliases=[
     "defect supercell mapping",
     "get_matched_structure_mapping_old",
     "structure matching",
     "supercell mapping",
     "supercell transformation",
     "unit cell to supercell mapping"
    ],
    category="defects",
    description="Finds the supercell transformation matrix and translation that maps a given unit cell structure onto a supercell structure, when the two structures exactly match (e.g., a defect supercell derived from the same primitive cell).",
    examples=[
     "from pymatgen.analysis.defects.supercells import get_matched_structure_mapping_old; result = get_matched_structure_mapping_old(uc_struct, sc_struct); if result: sc_m, total_t = result"
    ],
    key_results=[
     {
      "attr": "sc_m",
      "returns": "NDArray",
      "note": "A 3x3 supercell matrix (in lattice vector basis) such that sc_struct = uc_struct * sc_m + total_t."
     },
     {
      "attr": "total_t",
      "returns": "ArrayLike",
      "note": "A translation vector (in fractional coordinates of the supercell) applied after the matrix transformation."
     }
    ],
    related=[
     "get_closest_sc_mat",
     "get_matched_structure_mapping",
     "get_sc_fromstruct"
    ]
)
def get_matched_structure_mapping_old(...):
    ...

# pymatgen.analysis.defects.supercells.get_sc_fromstruct(base_struct: 'Structure', min_atoms: 'int' = 80, max_atoms: 'int' = 240, min_length: 'float' = 10.0, force_diagonal: 'bool' = False) -> 'NDArray | ArrayLike | None'
@register_function(
    aliases=[
     "PMG cubic supercell",
     "cubic supercell transformation",
     "find_optimal_cell_shape",
     "get_sc_fromstruct",
     "optimal supercell shape",
     "supercell generation"
    ],
    category="defects",
    description="Generate a supercell structure from a unit cell that is as close to cubic as possible, while respecting constraints on atom count and minimum lattice vector length; used when preparing supercells for defect calculations where a near-cubic shape is desired.",
    examples=[
     "sc_mat = get_sc_fromstruct(uc)",
     "assert sc_mat.shape == (3, 3)"
    ],
    key_results=[
     {
      "attr": "returned structure (pymatgen Structure)",
      "returns": "pymatgen.core.Structure",
      "note": "The supercell structure. Access .num_sites for atom count, .lattice for lattice parameters (including .matrix, .a, .b, .c, .angles), and .sites for individual sites."
     },
     {
      "attr": ".num_sites",
      "returns": "int",
      "note": "Number of atoms in the supercell – should be between min_atoms and max_atoms."
     },
     {
      "attr": ".lattice.matrix",
      "returns": "numpy.ndarray",
      "note": "3x3 matrix of the supercell lattice vectors (cubic-like shape)."
     }
    ],
    related=[
     "get_closest_sc_mat",
     "get_matched_structure_mapping",
     "get_matched_structure_mapping_old"
    ]
)
def get_sc_fromstruct(...):
    ...

# pymatgen.analysis.defects.thermo.Defect(structure: 'Structure', site: 'PeriodicSite', multiplicity: 'int | None' = None, oxi_state: 'float | None' = None, equivalent_sites: 'list[PeriodicSite] | None' = None, symprec: 'float' = 0.01, angle_tolerance: 'float' = 5, user_charges: 'list[int] | None' = None) -> 'None'
@register_function(
    aliases=[
     "Defect",
     "Defect class",
     "defect",
     "point defect",
     "pymatgen defect"
    ],
    category="defects",
    description="Represents a single point defect in a crystal structure (e.g., vacancy, substitution, interstitial). Materials scientists use this base class to store defect geometry, oxidation state, multiplicity, and charge states, and to retrieve the defect's name, relaxed structure, and element changes.",
    examples=[
     "from pymatgen.analysis.defects.generators import Vacancy\n# structure and site defined elsewhere\nvac = Vacancy(structure, site)\nprint(vac.name, vac.defect_structure)"
    ],
    key_results=[
     {
      "attr": ".name",
      "returns": "str",
      "note": "e.g., 'v_Ga' for a Ga vacancy, 'Ga_i' for a Ga interstitial, or 'Ga_As' for a substitutional defect."
     },
     {
      "attr": ".defect_structure",
      "returns": "Structure",
      "note": "The unit-cell structure with the defect applied (e.g., missing atom for vacancy)."
     },
     {
      "attr": ".element_changes",
      "returns": "dict[Element, int]",
      "note": "Dictionary describing net change in element counts, e.g., {Element('Ga'): -1} for a Ga vacancy."
     },
     {
      "attr": ".get_charge_states()",
      "returns": "list[int]",
      "note": "Returns list of allowed charge states for the defect, either from user_charges or determined automatically."
     }
    ],
    related=[
     "DefectEntry",
     "DefectSiteFinder",
     "FormationEnergyDiagram",
     "MultiFormationEnergyDiagram",
     "NamedDefect"
    ]
)
def Defect(...):
    ...

# pymatgen.analysis.defects.thermo.DefectEntry(defect: 'Defect', charge_state: 'int', sc_entry: 'ComputedStructureEntry', corrections: 'dict[str, float]' = <factory>, corrections_metadata: 'dict[str, Any]' = <factory>, sc_defect_frac_coords: 'tuple[float, float, float] | None' = None, bulk_entry: 'ComputedEntry | None' = None, entry_id: 'str | None' = None) -> None
@register_function(
    aliases=[
     "DefectEntry",
     "defect entry",
     "defect supercell entry",
     "defect thermodynamics entry"
    ],
    category="defects",
    description="Stores the results of a defect supercell calculation, including the defect object, charge state, supercell energy entry, and corrections, and provides methods to compute corrected energies and formation energies.",
    examples=[
     "fake_defect_entry = DefectEntry(defect=inter, sc_entry=defect_entries[0].sc_entry, charge_state=0"
    ],
    key_results=[
     {
      "attr": ".defect",
      "returns": "Defect",
      "note": "The defect object (e.g., Vacancy, Substitution) used to generate the supercell."
     },
     {
      "attr": ".charge_state",
      "returns": "int",
      "note": "The charge state of the defect (e.g., 0, -1, +2)."
     },
     {
      "attr": ".corrections",
      "returns": "dict[str, float]",
      "note": "A dictionary of energy corrections applied (e.g., {'freysoldt': 0.45})."
     },
     {
      "attr": ".corrected_energy",
      "returns": "float",
      "note": "Property that returns the total energy of the supercell after applying all corrections."
     },
     {
      "attr": ".get_ediff()",
      "returns": "float",
      "note": "Returns the energy difference between the defect supercell and the bulk (corrected)."
     }
    ],
    related=[
     "Defect",
     "DefectSiteFinder",
     "FormationEnergyDiagram",
     "MultiFormationEnergyDiagram",
     "NamedDefect"
    ]
)
def DefectEntry(...):
    ...

# pymatgen.analysis.defects.thermo.DefectSiteFinder(symprec: 'float' = 0.01, angle_tolerance: 'float' = 5.0) -> 'None'
@register_function(
    aliases=[
     "DefectSiteFinder",
     "defect detection",
     "defect finder",
     "defect location finder",
     "defect position finder",
     "defect site finder"
    ],
    category="defects",
    description="Finds the location (fractional coordinates) of a defect in a crystal structure by comparing a relaxed defect structure to the pristine structure, without requiring prior knowledge of the defect type or position.",
    examples=[
     "finder = DefectSiteFinder()",
     "frac_pos_guess = finder.get_native_defect_position(sc, base)",
     "fpos = finder.get_defect_fpos(sc_locked, sub.structure)",
     "fpos = finder.get_defect_fpos(sub_sc_struct, sub.structure)",
     "fpos = finder.get_defect_fpos(sc, inter.structure)",
     "fpos = finder.get_defect_fpos(inter_sc_struct, inter.structure)"
    ],
    key_results=[
     {
      "attr": "get_defect_fpos(defect_structure, base_structure, remove_oxi=True)",
      "returns": "ArrayLike (fractional coordinates)",
      "note": "Returns the fractional coordinates of the defect in the pristine structure; automatically detects whether it is an impurity or native defect and uses the appropriate method."
     },
     {
      "attr": "get_impurity_position(defect_structure, base_structure)",
      "returns": "ArrayLike (fractional coordinates)",
      "note": "Returns the weighted average position of impurity atoms (species not present in the pristine structure) in the defect structure."
     },
     {
      "attr": "get_native_defect_position(defect_structure, base_structure)",
      "returns": "ArrayLike (fractional coordinates)",
      "note": "Returns the position of a native defect (vacancy, interstitial, antisite) by averaging the most distorted sites weighted by their distortion magnitude."
     },
     {
      "attr": "get_most_distorted_sites(defect_structure, base_structure)",
      "returns": "list of tuples (site_index, distortion_magnitude)",
      "note": "Returns pairs of site index and distortion for sites in the defect structure that are most displaced relative to the pristine structure; used internally by get_native_defect_position."
     }
    ],
    related=[
     "Defect",
     "DefectEntry",
     "FormationEnergyDiagram",
     "MultiFormationEnergyDiagram",
     "NamedDefect"
    ]
)
def DefectSiteFinder(...):
    ...

# pymatgen.analysis.defects.thermo.FormationEnergyDiagram(defect_entries: 'list[DefectEntry]', pd_entries: 'list[ComputedEntry]', vbm: 'float', band_gap: 'float | None' = None, bulk_entry: 'ComputedStructureEntry | None' = None, inc_inf_values: 'bool' = False, bulk_stability: 'float' = 0.001) -> None
@register_function(
    aliases=[
     "FED",
     "FormationEnergyDiagram",
     "defect formation energy",
     "formation energy diagram"
    ],
    category="defects",
    description="Computes and analyzes the formation energy diagram of a point defect as a function of Fermi level and chemical potentials, enabling determination of charge state transition levels and defect concentrations.",
    examples=[
     "def_ents_w_bulk = copy.deepcopy(fed.defect_entries)",
     "FormationEnergyDiagram(defect_entries=fed.defect_entries, vbm=fed.vbm, pd_entries=fed.pd_entries, )",
     "dent.bulk_entry = fed.bulk_entry",
     "fed = FormationEnergyDiagram(defect_entries=def_ents_w_bulk, vbm=fed.vbm, pd_entries=fed.pd_entries, )",
     "assert len(fed.chempot_limits) == 3",
     "fed = FormationEnergyDiagram(defect_entries=def_ents_w_bulk, vbm=fed.vbm, bulk_entry=fed.bulk_entry, pd_entries=fed.pd_entries, )"
    ],
    key_results=[
     {
      "attr": ".get_formation_energy",
      "returns": "float",
      "note": "Returns the formation energy (in eV) for a given chemical potential and Fermi level."
     },
     {
      "attr": ".get_transitions",
      "returns": "list[tuple]",
      "note": "Returns the charge state transition levels as a list of (epsilon, charge1, charge2) tuples, where epsilon is the Fermi level in eV."
     },
     {
      "attr": ".as_dataframe",
      "returns": "pandas.DataFrame",
      "note": "Returns a DataFrame with columns such as 'charge', 'formation_energy', 'fermi_level', etc., for all computed formation energies."
     },
     {
      "attr": ".defect",
      "returns": "Defect",
      "note": "The defect object (e.g., vacancy, substitution, interstitial) associated with the diagram."
     },
     {
      "attr": ".chempot_limits",
      "returns": "dict",
      "note": "Dictionary of chemical potential limits (in eV) for each element in the defect system."
     }
    ],
    related=[
     "Defect",
     "DefectEntry",
     "DefectSiteFinder",
     "MultiFormationEnergyDiagram",
     "NamedDefect"
    ]
)
def FormationEnergyDiagram(...):
    ...

# pymatgen.analysis.defects.thermo.MultiFormationEnergyDiagram(formation_energy_diagrams: 'list[FormationEnergyDiagram]') -> None
@register_function(
    aliases=[
     "MultiFormationEnergyDiagram",
     "combined defect thermodynamics",
     "multi formation energy diagram",
     "multiple defect formation energy diagram"
    ],
    category="defects",
    description="Container for multiple formation energy diagrams, used to analyze the thermodynamics of several defect types together, e.g., to compute the equilibrium Fermi level under given conditions.",
    examples=[
     "mfed = MultiFormationEnergyDiagram(formation_energy_diagrams=[fed])",
     "ef = mfed.solve_for_fermi_level(chempots=cpots, temperature=300, dos=bulk_dos)",
     "mfed = MultiFormationEnergyDiagram.with_atomic_entries(bulk_entry=bulk_entry, defect_entries=def_ent_list, atomic_entries=atomic_entries, phase_diagram=pd, vbm=vbm, )",
     "assert len(mfed.formation_energy_diagrams) == 1"
    ],
    key_results=[
     {
      "attr": ".formation_energy_diagrams",
      "returns": "list[FormationEnergyDiagram]",
      "note": "List of individual FormationEnergyDiagram objects, one per defect type."
     },
     {
      "attr": ".band_gap",
      "returns": "float",
      "note": "Band gap of the bulk phase, taken from the first diagram."
     },
     {
      "attr": ".vbm",
      "returns": "float",
      "note": "Valence band maximum energy of the bulk phase, taken from the first diagram."
     },
     {
      "attr": ".solve_for_fermi_level",
      "returns": "float",
      "note": "Computes the equilibrium Fermi level (relative to VBM) given chemical potentials, temperature, and density of states."
     }
    ],
    related=[
     "Defect",
     "DefectEntry",
     "DefectSiteFinder",
     "FormationEnergyDiagram",
     "NamedDefect"
    ]
)
def MultiFormationEnergyDiagram(...):
    ...

# pymatgen.analysis.defects.thermo.NamedDefect(name: 'str', bulk_formula: 'str', element_changes: 'dict') -> 'None'
@register_function(
    aliases=[
     "NamedDefect",
     "defect aggregation",
     "defect name",
     "defect placeholder",
     "named defect"
    ],
    category="defects",
    description="To represent a defect solely by its name, bulk formula, and elemental changes, serving as a lightweight placeholder for defects calculated outside the framework so they can be grouped and analyzed in formation energy diagrams.",
    examples=[
     "de.defect = NamedDefect(name=de.defect.name, bulk_formula=bulk_formula, element_changes=None",
     "nd0 = NamedDefect.from_structures(defect_structure=defect_struct, bulk_structure=bulk_struct",
     "nd1 = NamedDefect(name=\"v_Ga\", bulk_formula=\"GaN\", element_changes={\"Ga\": -1})",
     "nd2 = NamedDefect(name=\"Mg_Ga\", bulk_formula=\"GaN\", element_changes={\"Mg\": 1, \"Ga\": -1}"
    ],
    key_results=[
     {
      "attr": ".name",
      "returns": "str",
      "note": "The defect name, e.g., 'v_Ga' for a Ga vacancy, or 'v_Ga+O_i' for a complex."
     },
     {
      "attr": ".bulk_formula",
      "returns": "str",
      "note": "The reduced formula of the bulk structure, e.g., 'GaAs'."
     },
     {
      "attr": ".element_changes",
      "returns": "dict",
      "note": "Dictionary of element changes, e.g., {'Ga': -1, 'As': 0} for a Ga vacancy."
     },
     {
      "attr": ".latex_name",
      "returns": "str",
      "note": "LaTeX-formatted name for display, e.g., 'v$_{\\rm Ga}$' for 'v_Ga'."
     }
    ],
    related=[
     "Defect",
     "DefectEntry",
     "DefectSiteFinder",
     "FormationEnergyDiagram",
     "MultiFormationEnergyDiagram"
    ]
)
def NamedDefect(...):
    ...

# pymatgen.analysis.defects.thermo.ensure_stable_bulk(pd: 'PhaseDiagram', entry: 'ComputedEntry', threshold: 'float' = 0.001) -> 'PhaseDiagram'
@register_function(
    aliases=[
     "convex hull forcing",
     "ensure stable bulk",
     "ensure_stable_bulk",
     "force stability on convex hull",
     "phase diagram hull modification",
     "stabilize entry"
    ],
    category="defects",
    description="Forces a given entry to be stable on the convex hull in a phase diagram by creating a new entry with an energy slightly below the hull, regardless of the original entry's stability, typically used to treat a bulk material as stable for subsequent defect calculations.",
    examples=[
     "pd2 = ensure_stable_bulk(pd, fake_bulk_ent)",
     "assert \"GaN\" in [e.composition.reduced_formula for e in pd2.stable_entries]"
    ],
    key_results=[
     {
      "attr": ".all_entries",
      "returns": "list of ComputedEntry",
      "note": "All entries in the modified phase diagram, including the new fake stable entry."
     },
     {
      "attr": ".stable_entries",
      "returns": "list of ComputedEntry",
      "note": "Entries that lie on the convex hull; the fake entry will appear here."
     },
     {
      "attr": ".get_hull_energy(composition)",
      "returns": "float",
      "note": "Energy of the convex hull at a given composition, in eV/atom."
     },
     {
      "attr": ".get_form_energy(entry)",
      "returns": "float",
      "note": "Formation energy of an entry relative to the hull (positive means unstable)."
     }
    ],
    related=[
     "Defect",
     "DefectEntry",
     "DefectSiteFinder",
     "FormationEnergyDiagram",
     "MultiFormationEnergyDiagram"
    ]
)
def ensure_stable_bulk(...):
    ...

# pymatgen.analysis.defects.thermo.fermi_dirac(energy: 'float', temperature: 'float') -> 'float'
@register_function(
    aliases=[
     "FD statistics",
     "Fermi-Dirac distribution",
     "defect equilibrium concentration factor",
     "defect occupancy probability",
     "fermi_dirac"
    ],
    category="defects",
    description="Computes the Fermi-Dirac distribution value for a given energy relative to the valence band maximum and temperature, providing the occupancy probability (up to multiplicity) for defect levels under dilute-limit thermodynamics with Fermi-Dirac statistics.",
    examples=[
     "import pymatgen.analysis.defects.thermo as dft; dft.fermi_dirac(0.5, 300)"
    ],
    key_results=[
     {
      "attr": "return value",
      "returns": "float",
      "note": "The Fermi-Dirac probability: 1/(1 + exp(energy/(k_B * T))). For energy=0.5 eV and T=300 K, typically ~4.8e-9."
     }
    ],
    related=[
     "Defect",
     "DefectEntry",
     "DefectSiteFinder",
     "FormationEnergyDiagram",
     "MultiFormationEnergyDiagram"
    ]
)
def fermi_dirac(...):
    ...

# pymatgen.analysis.defects.thermo.get_closest_sc_mat(uc_struct: 'Structure', sc_struct: 'Structure', sm: 'StructureMatcher | None' = None, debug: 'bool' = False) -> 'NDArray'
@register_function(
    aliases=[
     "defect supercell mapping",
     "find supercell transformation",
     "get_closest_sc_mat",
     "sc_mat",
     "supercell matrix"
    ],
    category="defects",
    description="Given a unit cell and a defect supercell structure, find the 3x3 supercell matrix that best maps the unit cell onto the supercell, typically to determine how the defect cell was constructed from the pristine host.",
    examples=[
     "sorted_results = get_closest_sc_mat(uc_struct, vac_sc, debug=True)",
     "res = get_closest_sc_mat(uc_struct=uc_struct, sc_struct=vac_struct, debug=False)"
    ],
    key_results=[
     {
      "attr": "return value (sc_mat)",
      "returns": "NDArray",
      "note": "3x3 integer supercell matrix such that `uc_struct * sc_mat` approximately matches `sc_struct`"
     },
     {
      "attr": "return value when debug=True",
      "returns": "list of tuples",
      "note": "Sorted list of (distance, lattice, sc_mat) for all candidate matrices, with smallest mean distance first"
     }
    ],
    related=[
     "Defect",
     "DefectEntry",
     "DefectSiteFinder",
     "FormationEnergyDiagram",
     "MultiFormationEnergyDiagram"
    ]
)
def get_closest_sc_mat(...):
    ...

# pymatgen.analysis.defects.thermo.get_freysoldt_correction(q: 'int', dielectric: 'float', defect_locpot: 'Locpot', bulk_locpot: 'Locpot', defect_frac_coords: 'ArrayLike | None' = None, lattice: 'Lattice | None' = None, energy_cutoff: 'float' = 520, mad_tol: 'float' = 0.0001, q_model: 'QModel | None' = None, step: 'float' = 0.0001) -> 'CorrectionResult'
@register_function(
    aliases=[
     "Freysoldt correction",
     "charge correction",
     "defect correction",
     "electrostatic correction",
     "finite-size correction",
     "get_freysoldt_correction"
    ],
    category="defects",
    description="Obtains the Freysoldt electrostatic finite-size correction for a charged point defect in a periodic supercell, based on the planar-averaged electrostatic potential of defect and bulk calculations.",
    examples=[
     "freysoldt_summary = get_freysoldt_correction(q=0, dielectric=14, defect_locpot=defect_locpot, bulk_locpot=bulk_locpot, defect_frac_coords=[0.5, 0.5, 0.5], )",
     "assert freysoldt_summary.correction_energy == pytest.approx(0, abs=1e-4)",
     "plot_plnr_avg(freysoldt_summary.metadata[\"plot_data\"][0])",
     "q: get_freysoldt_correction(q=q, dielectric=5, bulk_locpot=bulk_locpot, defect_locpot=defect_locpots[q], ).correction_energy"
    ],
    key_results=[
     {
      "attr": ".correction",
      "returns": "float",
      "note": "The computed electrostatic correction energy in eV."
     },
     {
      "attr": ".metadata",
      "returns": "list",
      "note": "List of plotting data (one per lattice direction) for the planar average electrostatic potential; e.g., result.metadata[0] can be passed to plot_plnr_avg()."
     }
    ],
    related=[
     "Defect",
     "DefectEntry",
     "DefectSiteFinder",
     "FormationEnergyDiagram",
     "MultiFormationEnergyDiagram"
    ]
)
def get_freysoldt_correction(...):
    ...

# pymatgen.analysis.defects.thermo.get_lower_envelope(lines: 'list[tuple[float, float]]') -> 'list[tuple[float, float]]'
@register_function(
    aliases=[
     "charge state stability envelope",
     "convex hull of lines",
     "formation energy envelope",
     "get_lower_envelope",
     "lower envelope",
     "thermodynamic envelope"
    ],
    category="defects",
    description="Computes the lower envelope of a set of linear formation energy lines (slope m, intercept b) as a function of Fermi level or chemical potential, revealing the thermodynamically most stable charge state or defect configuration at each value.",
    examples=[
     "lower_envelope = get_lower_envelope(lines)"
    ],
    key_results=[
     {
      "attr": "result[i][0]",
      "returns": "float",
      "note": "Slope (m) of the i‑th line in the lower envelope."
     },
     {
      "attr": "result[i][1]",
      "returns": "float",
      "note": "Intercept (b) of the i‑th line in the lower envelope."
     },
     {
      "attr": "len(result)",
      "returns": "int",
      "note": "Number of lines that form the lower envelope."
     }
    ],
    related=[
     "Defect",
     "DefectEntry",
     "DefectSiteFinder",
     "FormationEnergyDiagram",
     "MultiFormationEnergyDiagram"
    ]
)
def get_lower_envelope(...):
    ...

# pymatgen.analysis.defects.thermo.get_sc_locpot(uc_locpot: 'Locpot', defect_struct: 'Structure', grid_out: 'tuple', up_sample: 'int' = 2, sm: 'StructureMatcher' = None) -> 'Locpot'
@register_function(
    aliases=[
     "LOCPOT upsampling",
     "bulk locpot approximation",
     "get_sc_locpot",
     "supercell locpot from unit cell",
     "unit cell to supercell locpot"
    ],
    category="defects",
    description="Transforms a unit-cell LOCPOT into a supercell-like LOCPOT when only the defect supercell structure is available, allowing electrostatic alignment without the bulk supercell LOCPOT.",
    examples=[
     "sc_locpot = get_sc_locpot(uc_locpot, defect_struct, grid_out=(40,40,40))"
    ],
    key_results=[
     {
      "attr": ".structure",
      "returns": "Structure",
      "note": "the structure of the supercell (bulk_sc) used for the transformation"
     },
     {
      "attr": ".data",
      "returns": "dict",
      "note": "dictionary with key 'tot' and a 3D numpy array of the electrostatic potential on the supercell grid"
     },
     {
      "attr": ".dim",
      "returns": "tuple",
      "note": "dimensions (nx, ny, nz) of the supercell grid"
     },
     {
      "attr": ".ngrid",
      "returns": "tuple",
      "note": "number of grid points along each axis (same as dim)"
     }
    ],
    related=[
     "Defect",
     "DefectEntry",
     "DefectSiteFinder",
     "FormationEnergyDiagram",
     "MultiFormationEnergyDiagram"
    ]
)
def get_sc_locpot(...):
    ...

# pymatgen.analysis.defects.thermo.get_transitions(lines: 'list[tuple[float, float]]', x_min: 'float', x_max: 'float') -> 'list[tuple[float, float]]'
@register_function(
    aliases=[
     "charge state transition levels",
     "defect thermodynamic transition levels",
     "get_transitions",
     "intersection of formation energy lines",
     "stability boundaries",
     "transition points"
    ],
    category="defects",
    description="Finds the Fermi-level positions (transition points) where the most stable charge state of a defect changes, given a set of formation energy lines for different charge states.",
    examples=[
     "assert get_transitions(lower_envelope, -5, 2) == [",
     "form_en = np.array(fed.get_transitions(cp_dict, 0, 5))",
     "form_en = np.array(fed.get_transitions(point, 0, 5))",
     "trans = fed.get_transitions(fed.chempot_limits[1], x_min=-100, x_max=100)"
    ],
    key_results=[
     {
      "attr": "returned list",
      "returns": "list[tuple[float, float]]",
      "note": "Each tuple (x, y) is a point on the formation energy diagram. The first point is at x_min on the highest-slope line, the last at x_max on the lowest-slope line, and intermediate points are intersections between adjacent lines."
     }
    ],
    related=[
     "Defect",
     "DefectEntry",
     "DefectSiteFinder",
     "FormationEnergyDiagram",
     "MultiFormationEnergyDiagram"
    ]
)
def get_transitions(...):
    ...

# pymatgen.analysis.defects.thermo.get_upper_hull(points: 'ArrayLike') -> 'list[ArrayLike]'
@register_function(
    aliases=[
     "convex hull upper portion",
     "get_upper_hull",
     "upper boundary",
     "upper convex hull",
     "upper envelope",
     "upper hull"
    ],
    category="defects",
    description="Computes the upper convex hull of a set of 2D points, typically used to identify the thermodynamically stable phase boundary (e.g., lowest formation energy at each composition) in defect phase diagrams or composition\u2013energy plots.",
    examples=[
     "from pymatgen.analysis.defects.thermo import get_upper_hull\npoints = [(0,0), (1,2), (2,0), (1,1), (3,1)]\nhull = get_upper_hull(points)\nprint(hull)  # e.g. [(3, 1), (1, 2), (0, 0)]"
    ],
    key_results=[
     {
      "attr": "(returned list)",
      "returns": "list[(float, float)]",
      "note": "List of vertices (x, y) of the upper hull, ordered from rightmost (largest x) to leftmost (smallest x). Each vertex is a tuple of two floats."
     }
    ],
    related=[
     "Defect",
     "DefectEntry",
     "DefectSiteFinder",
     "FormationEnergyDiagram",
     "MultiFormationEnergyDiagram"
    ]
)
def get_upper_hull(...):
    ...

# pymatgen.analysis.defects.thermo.get_zfile(directory: 'Path', base_name: 'str', allow_missing: 'bool' = False) -> 'Path | None'
@register_function(
    aliases=[
     "defect file finder",
     "find gzipped file",
     "get_zfile",
     "locate compressed file",
     "pymatgen defect file search"
    ],
    category="defects",
    description="Locate a file that may be present in either plain or gzipped form (with .gz or .GZ extension) within a directory, returning its path or None if allowed.",
    examples=[
     "from pathlib import Path\nfrom pymatgen.analysis.defects.thermo import get_zfile\nresult = get_zfile(Path('./data'), 'defect_energies')"
    ],
    key_results=[
     {
      "attr": ".name",
      "returns": "str",
      "note": "The full file name (e.g., 'vasprun.xml.gz' or 'defect_energies.txt')"
     },
     {
      "attr": ".suffix",
      "returns": "str",
      "note": "The file extension, either '.gz' or an empty string if uncompressed"
     }
    ],
    related=[
     "Defect",
     "DefectEntry",
     "DefectSiteFinder",
     "FormationEnergyDiagram",
     "MultiFormationEnergyDiagram"
    ]
)
def get_zfile(...):
    ...

# pymatgen.analysis.defects.thermo.group_defect_entries(defect_entries: 'list[DefectEntry]', sm: 'StructureMatcher' = None) -> 'Generator[tuple[str, list[DefectEntry]], None, None]'
@register_function(
    aliases=[
     "defect entry grouping",
     "defect grouping",
     "group defects",
     "group_defect_entries"
    ],
    category="defects",
    description="Group defect entries by defect name and then by structure similarity, enabling deduplication and organization of defect calculations.",
    examples=[
     "for g_name, g in group_defect_entries(defect_entries=defect_entries):",
     "for g_name, g in group_defect_entries(defect_entries=named_defect_entries):"
    ],
    key_results=[
     {
      "attr": "name",
      "returns": "str",
      "note": "Defect name, e.g., 'v_Ga' for a Ga vacancy."
     },
     {
      "attr": "entries",
      "returns": "list[DefectEntry]",
      "note": "List of DefectEntry objects sharing the same name and matched structure."
     }
    ],
    related=[
     "Defect",
     "DefectEntry",
     "DefectSiteFinder",
     "FormationEnergyDiagram",
     "MultiFormationEnergyDiagram"
    ]
)
def group_defect_entries(...):
    ...

# pymatgen.analysis.defects.thermo.group_docs(docs: 'Sequence', sm: 'StructureMatcher', get_structure: 'Callable', get_hash: 'Callable | None' = None) -> 'Generator[tuple[str | None, list], None, None]'
@register_function(
    aliases=[
     "defect clustering by hash and structure",
     "defect document grouping",
     "group defective documents",
     "group_docs",
     "structure-based defect grouping"
    ],
    category="defects",
    description="Group defect documents by a simple hash (like defect name) and then by structure similarity, yielding a generator of (name or None, list of documents) pairs for further analysis.",
    examples=[
     "sgroups = group_docs([vac1, vac2, int1, vac3, vac4, int2], sm, lambda x: x.defect_structure, )",
     "sgroups = group_docs([vac1, vac2, int1, vac3, vac4, int1, int2], sm, lambda x: x.defect_structure, lambda x: x.name, )"
    ],
    key_results=[
     {
      "attr": "yielded tuple[0]",
      "returns": "str | None",
      "note": "The hash (e.g., defect name) from get_hash, or None if get_hash is not provided. If multiple structural groups exist under the same hash, it becomes 'hash:index'."
     },
     {
      "attr": "yielded tuple[1]",
      "returns": "list",
      "note": "A list of documents that share the same hash and are structurally matched by the StructureMatcher."
     }
    ],
    related=[
     "Defect",
     "DefectEntry",
     "DefectSiteFinder",
     "FormationEnergyDiagram",
     "MultiFormationEnergyDiagram"
    ]
)
def group_docs(...):
    ...

# pymatgen.analysis.defects.thermo.group_formation_energy_diagrams(feds: 'Sequence[FormationEnergyDiagram]', sm: 'StructureMatcher' = None) -> 'Generator[tuple[str | None, FormationEnergyDiagram], None, None]'
@register_function(
    aliases=[
     "combine formation energy diagrams",
     "defect formation energy grouping",
     "group FEDs",
     "group formation energy diagrams",
     "group_formation_energy_diagrams",
     "structure matching defect diagrams"
    ],
    category="defects",
    description="Groups formation energy diagrams by defect type (name and structure) so that multiple diagrams representing the same defect can be combined into one, useful for merging results from different calculations or averaging.",
    examples=[
     "for name, fed in group_formation_energy_diagrams(feds_list): print(name, len(fed.defect_entries))"
    ],
    key_results=[
     {
      "attr": ".defect",
      "returns": "Defect object (e.g., pymatgen.analysis.defects.core.Vacancy)",
      "note": "Access .name (str, e.g., 'v_Ga') and .defect_structure (Structure) for the combined defect representation."
     },
     {
      "attr": ".defect_entries",
      "returns": "List[DefectEntry]",
      "note": "All defect entries from the grouped formation energy diagrams, concatenated into a single list."
     }
    ],
    related=[
     "Defect",
     "DefectEntry",
     "DefectSiteFinder",
     "FormationEnergyDiagram",
     "MultiFormationEnergyDiagram"
    ]
)
def group_formation_energy_diagrams(...):
    ...

# pymatgen.analysis.defects.thermo.plot_formation_energy_diagrams(formation_energy_diagrams: 'FormationEnergyDiagram | list[FormationEnergyDiagram] | MultiFormationEnergyDiagram', rich_element: 'Element | None' = None, chempots: 'dict | None' = None, alignment: 'float' = 0.0, xlim: 'list | None' = None, ylim: 'list | None' = None, only_lower_envelope: 'bool' = True, show: 'bool' = True, save: 'bool | str' = False, colors: 'list | None' = None, legend_prefix: 'str | None' = None, transition_marker: 'str' = '*', transition_markersize: 'int' = 16, linestyle: 'str' = '-', linewidth: 'int' = 4, envelope_alpha: 'float' = 0.8, line_alpha: 'float' = 0.5, band_edge_color: 'str' = 'k', filterfunction: 'Callable | None' = None, legend_loc: 'str' = 'lower center', show_legend: 'bool' = True, axis: 'Axes' = None) -> 'Axes'
@register_function(
    aliases=[
     "Fermi level vs formation energy",
     "charge transition level plot",
     "defect formation energy plot",
     "formation energy diagram",
     "plot_formation_energy_diagrams",
     "thermodynamic defect diagram"
    ],
    category="defects",
    description="Plot the formation energy of defects as a function of Fermi level, used to determine charge transition levels and stable charge states of defects in a material.",
    examples=[
     "plot_formation_energy_diagrams(fed, chempots=fed.chempot_limits[0], show=False, save=False",
     "axis = plot_formation_energy_diagrams(fed, chempots=fed.chempot_limits[0], show=False, xlim=[0, 2], ylim=[0, 4], save=False, )"
    ],
    key_results=[
     {
      "attr": ".figure",
      "returns": "matplotlib.figure.Figure",
      "note": "The Figure object containing the plotted diagram, can be used to save or modify the figure."
     },
     {
      "attr": ".lines",
      "returns": "list of matplotlib.lines.Line2D",
      "note": "All line objects plotted in the diagram, including envelope and individual defect lines."
     },
     {
      "attr": ".legend_",
      "returns": "matplotlib.legend.Legend or None",
      "note": "The legend object if show_legend=True, otherwise None."
     }
    ],
    related=[
     "Defect",
     "DefectEntry",
     "DefectSiteFinder",
     "FormationEnergyDiagram",
     "MultiFormationEnergyDiagram"
    ]
)
def plot_formation_energy_diagrams(...):
    ...

# pymatgen.analysis.defects.utils.ChargeInsertionAnalyzer(chgcar: 'VolumetricData', working_ion: 'str' = 'Li', clustering_tol: 'float' = 0.5, ltol: 'float' = 0.2, stol: 'float' = 0.3, angle_tol: 'float' = 5, min_dist: 'float' = 0.9) -> 'None'
@register_function(
    aliases=[
     "ChargeInsertionAnalyzer",
     "charge density insertion",
     "charge insertion analysis",
     "defect insertion analyzer",
     "interstitial site finder"
    ],
    category="defects",
    description="Identify and analyze interstitial insertion sites in a host crystal by locating local minima in the charge density, enabling candidate structure generation for battery or ionic conductor studies.",
    examples=[
     "cia = ChargeInsertionAnalyzer(chgcar)",
     "insert_groups = cia.filter_and_group(max_avg_charge=0.5)"
    ],
    key_results=[
     {
      "attr": ".labeled_sites",
      "returns": "list[tuple[list[float], int]]",
      "note": "Each tuple contains fractional coordinates (list of 3 floats) and an integer label identifying the uniqueness group among the inserted structures (e.g., 0, 1, 2...)."
     },
     {
      "attr": ".local_minima",
      "returns": "list[list[float]]",
      "note": "List of fractional coordinates of all local charge density minima (one per candidate site), without grouping labels."
     },
     {
      "attr": ".filter_and_group(avg_radius, max_avg_charge)",
      "returns": "list[tuple[float, list[list[float]]]]",
      "note": "Returns a list of (average_charge, site_group) tuples; site_group is a list of fractional coordinates for minima whose average charge within avg_radius is below max_avg_charge."
     }
    ],
    related=[
     "CorrectionResult",
     "QModel",
     "TopographyAnalyzer",
     "VoronoiPolyhedron",
     "calculate_vol"
    ]
)
def ChargeInsertionAnalyzer(...):
    ...

# pymatgen.analysis.defects.utils.CorrectionResult(correction_energy: 'float', metadata: 'dict[Any, Any]') -> None
@register_function(
    aliases=[
     "CorrectionResult",
     "correction energy container",
     "correction result",
     "defect correction summary"
    ],
    category="defects",
    description="This is a container for the total correction energy and associated metadata from defect calculations. A materials scientist uses it to store and access the net correction applied to a supercell calculation, along with additional information for plotting or analysis.",
    examples=[
     "result = CorrectionResult(correction_energy=0.34, metadata={'method': 'FNV', 'plot_data': {}})"
    ],
    key_results=[
     {
      "attr": ".correction_energy",
      "returns": "float",
      "note": "Total correction energy in eV."
     },
     {
      "attr": ".metadata",
      "returns": "dict[Any, Any]",
      "note": "A dictionary of metadata, e.g., for plotting or intermediate analysis."
     }
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "QModel",
     "TopographyAnalyzer",
     "VoronoiPolyhedron",
     "calculate_vol"
    ]
)
def CorrectionResult(...):
    ...

# pymatgen.analysis.defects.utils.QModel(beta: 'float' = 1.0, expnorm: 'float' = 0.0, gamma: 'float' = 1.0) -> 'None'
@register_function(
    aliases=[
     "Freysoldt model",
     "QModel",
     "charge distribution model",
     "defect charge model",
     "exponential-gaussian model"
    ],
    category="defects",
    description="Models the defect charge distribution as a combination of exponential tail and Gaussian distribution, used in electrostatic correction schemes (e.g., Freysoldt method) for defect calculations in materials science.",
    examples=[
     "from pymatgen.analysis.defects.utils import QModel\nmodel = QModel(beta=2.0, expnorm=0.54, gamma=1.0)\nvalue = model.rho_rec(g2=0.5)"
    ],
    key_results=[
     {
      "attr": ".beta",
      "returns": "float",
      "note": "Gaussian decay constant in Bohr; default 1.0."
     },
     {
      "attr": ".expnorm",
      "returns": "float",
      "note": "Weight for exponential tail (0-1); default 0.0."
     },
     {
      "attr": ".gamma",
      "returns": "float",
      "note": "Exponential decay constant in Bohr; default 1.0."
     },
     {
      "attr": ".rho_rec(g2)",
      "returns": "float",
      "note": "Reciprocal space model charge density at squared reciprocal vector g2."
     },
     {
      "attr": ".rho_rec_limit0",
      "returns": "float",
      "note": "Coefficient for rho_rec expansion near g=0: rho_rec(g->0) -> 1 + rho_rec_limit0 * g^2."
     }
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "CorrectionResult",
     "TopographyAnalyzer",
     "VoronoiPolyhedron",
     "calculate_vol"
    ]
)
def QModel(...):
    ...

# pymatgen.analysis.defects.utils.TopographyAnalyzer(structure: 'Structure', framework_ions: 'list[str]', cations: 'list[str]', image_tol: 'float' = 0.0001, max_cell_range: 'int' = 1, check_volume: 'bool' = True, constrained_c_frac: 'float' = 0.5, thickness: 'float' = 0.5, clustering_tol: 'float' = 0.5, min_dist: 'float' = 0.9, ltol: 'float' = 0.2, stol: 'float' = 0.3, angle_tol: 'float' = 5) -> 'None'
@register_function(
    aliases=[
     "TopographyAnalyzer",
     "defect topology analyzer",
     "diffusion pathway analyzer",
     "interstitial site finder",
     "topography analyzer",
     "voronoi tessellation analyzer"
    ],
    category="defects",
    description="Performs topological analysis of a crystal structure using Voronoi tessellations to identify potential interstitial sites and analyze diffusion pathways, typically for defect or ion conductor studies.",
    examples=[
     "ta = TopographyAnalyzer(struct, [\"Fe\", \"O\"], [], check_volume=True)",
     "node_struct = ta.get_structure_with_nodes()",
     "ta = TopographyAnalyzer(struct, [\"O\"], [\"Fe\"], check_volume=True)"
    ],
    key_results=[
     {
      "attr": "labeled_sites",
      "returns": "list of Site",
      "note": "List of pymatgen Site objects representing the Voronoi nodes (interstitial sites) with labels (e.g., 'node_0'). These are the raw unclustered sites."
     },
     {
      "attr": "get_structure_with_nodes()",
      "returns": "Structure",
      "note": "Returns a pymatgen Structure object containing the original framework atoms plus the interstitial nodes as additional sites (typically labeled 'X' or with a placeholder species). Useful for visualization or further processing."
     }
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "CorrectionResult",
     "QModel",
     "VoronoiPolyhedron",
     "calculate_vol"
    ]
)
def TopographyAnalyzer(...):
    ...

# pymatgen.analysis.defects.utils.VoronoiPolyhedron(lattice: 'Lattice', frac_coords: 'npt.ArrayLike', polyhedron_indices: 'list | set', all_coords: 'list', name: 'str | int | None' = None) -> 'None'
@register_function(
    aliases=[
     "PBC Voronoi",
     "Voronoi point",
     "Voronoi polyhedron",
     "VoronoiPolyhedron",
     "coordination polyhedron"
    ],
    category="defects",
    description="A container to represent a Voronoi polyhedron around a point in a periodic crystal lattice, used in defect analysis to describe the local coordination environment and its geometric properties.",
    examples=[
     "vp = VoronoiPolyhedron(lattice, [0.25, 0.25, 0.25], [0, 1, 2, 3], all_coords, name='site'); print(vp.coordination, vp.volume)"
    ],
    key_results=[
     {
      "attr": ".name",
      "returns": "str or None",
      "note": "An optional identifier for the polyhedron, e.g., 'v_Ga' for a Ga vacancy site or None."
     },
     {
      "attr": ".coordination",
      "returns": "int",
      "note": "Coordination number, i.e., number of vertices in the polyhedron."
     },
     {
      "attr": ".volume",
      "returns": "float",
      "note": "Volume of the polyhedron in Å³."
     }
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "CorrectionResult",
     "QModel",
     "TopographyAnalyzer",
     "calculate_vol"
    ]
)
def VoronoiPolyhedron(...):
    ...

# pymatgen.analysis.defects.utils.calculate_vol(coords: 'npt.NDArray') -> 'float'
@register_function(
    aliases=[
     "3D convex hull",
     "calculate_vol",
     "convex hull volume",
     "point cloud volume",
     "pymatgen volume",
     "volume of points"
    ],
    category="defects",
    description="Calculate the volume of the convex hull of a set of 3D points, useful for determining the volume occupied by a defect configuration or a set of atomic coordinates.",
    examples=[
     "volume = calculate_vol(np.array([[0,0,0],[1,0,0],[0,1,0],[0,0,1]]))"
    ],
    key_results=[
     {
      "attr": "return value",
      "returns": "float",
      "note": "Volume of the convex hull in cubic units (same units as input coordinates, e.g., Å³)."
     }
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "CorrectionResult",
     "QModel",
     "TopographyAnalyzer",
     "VoronoiPolyhedron"
    ]
)
def calculate_vol(...):
    ...

# pymatgen.analysis.defects.utils.cluster_nodes(fcoords: 'npt.ArrayLike', lattice: 'Lattice', tol: 'float' = 0.2) -> 'npt.NDArray'
@register_function(
    aliases=[
     "cluster_nodes",
     "clustering defect sites",
     "defect clustering",
     "hierarchical clustering with PBC",
     "merge close points"
    ],
    category="defects",
    description="Cluster fractional coordinates that are within a distance tolerance, accounting for periodic boundary conditions, to merge points that represent the same physical site.",
    examples=[
     "clusters = cluster_nodes(frac_pos + added, gan_struct.lattice)",
     "for a, b in zip(sorted(clusters.tolist()), sorted(frac_pos)):"
    ],
    key_results=[
     {
      "attr": "return value",
      "returns": "npt.NDArray",
      "note": "An array of merged fractional coordinates. Each row is a cluster center in fractional space (e.g., [0.5, 0.5, 0.5])."
     }
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "CorrectionResult",
     "QModel",
     "TopographyAnalyzer",
     "VoronoiPolyhedron"
    ]
)
def cluster_nodes(...):
    ...

# pymatgen.analysis.defects.utils.converge(f: 'Callable', step: 'float', tol: 'float', max_h: 'float') -> 'float'
@register_function(
    aliases=[
     "converge",
     "convergence function",
     "iterative solver",
     "newton iteration",
     "root search"
    ],
    category="defects",
    description="Converges a scalar function f(h) to a tolerance by iterating h with fixed step, stopping when successive evaluations differ by less than tol, used when a simple iterative search for a parameter such as defect size or energy is needed.",
    examples=[
     "converge(lambda x: (x-5)**2, step=0.1, tol=1e-6, max_h=10)"
    ],
    key_results=[
     {
      "attr": "return_value",
      "returns": "float",
      "note": "The value of h at which the function values have stabilized within tolerance; e.g., for f(x)=(x-5)^2, step=0.1, tol=1e-6, max_h=10, the returned value is approximately 5.0."
     }
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "CorrectionResult",
     "QModel",
     "TopographyAnalyzer",
     "VoronoiPolyhedron"
    ]
)
def converge(...):
    ...

# pymatgen.analysis.defects.utils.eV_to_k(energy: 'float') -> 'float'
@register_function(
    aliases=[
     "eV to k",
     "eV_to_k",
     "energy to k-vector",
     "k from energy",
     "reciprocal vector magnitude from energy"
    ],
    category="defects",
    description="Converts an energy value in eV to the magnitude of the reciprocal wavevector (k) in units of 1/Bohr, using the free-electron relation \u0127\u00b2k\u00b2/(2m) = E. Materials scientists use it to translate between energy scales (e.g., from defect level energies, band gaps, or thermal energies) and the corresponding k-space distance, commonly needed in effective mass calculations, band structure analysis, or when ",
    examples=[
     "import pymatgen.analysis.defects.utils as dutils; print(dutils.eV_to_k(1.0))"
    ],
    key_results=[
     {
      "attr": "(return value)",
      "returns": "float",
      "note": "Reciprocal vector magnitude in units of 1/Bohr. For example, an energy of 1.0 eV returns approximately 0.511 (the exact value depends on the physical constants used)."
     }
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "CorrectionResult",
     "QModel",
     "TopographyAnalyzer",
     "VoronoiPolyhedron"
    ]
)
def eV_to_k(...):
    ...

# pymatgen.analysis.defects.utils.generate_reciprocal_vectors_squared(a1: 'npt.ArrayLike', a2: 'npt.ArrayLike', a3: 'npt.ArrayLike', encut: 'float') -> 'Generator[float, None, None]'
@register_function(
    aliases=[
     "energy cutoff",
     "g-vectors squared",
     "generate_reciprocal_vectors_squared",
     "plane wave cutoff",
     "reciprocal space truncation",
     "reciprocal vectors squared"
    ],
    category="defects",
    description="Generate squared magnitudes of reciprocal lattice vectors within a specified energy cutoff, used for determining plane-wave basis set truncation in defect calculations.",
    examples=[
     "import numpy as np; from pymatgen.analysis.defects.utils import generate_reciprocal_vectors_squared; a1 = np.array([1,0,0]); a2 = np.array([0,1,0]); a3 = np.array([0,0,1]); list(generate_reciprocal_vectors_squared(a1, a2, a3, 20.0))[:5]"
    ],
    key_results=[
     {
      "attr": "generator yields",
      "returns": "float",
      "note": "Squared reciprocal vector magnitude (1/Bohr)^2, e.g., 0.0, 1.0, 2.0, ... for each allowed g-vector whose squared norm is less than gcut^2 = 2*encut (in atomic units)."
     }
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "CorrectionResult",
     "QModel",
     "TopographyAnalyzer",
     "VoronoiPolyhedron"
    ]
)
def generate_reciprocal_vectors_squared(...):
    ...

# pymatgen.analysis.defects.utils.generic_group_labels(list_in: 'Sequence', comp: 'Callable' = <built-in function eq>) -> 'list[int]'
@register_function(
    aliases=[
     "comparator-based grouping",
     "equivalence grouping",
     "generic_group_labels",
     "group labels",
     "unsortable objects labeling"
    ],
    category="defects",
    description="Assigns group labels to elements of a sequence based on a user-supplied comparator, enabling grouping of unsortable objects into equivalence classes.",
    examples=[
     "generic_group_labels([1, 2, 1, 3], comp=lambda x, y: x == y)  # returns [0, 1, 0, 2]"
    ],
    key_results=[
     {
      "attr": "return value",
      "returns": "list[int]",
      "note": "Each integer is a group label; objects that compare equal (via `comp`) share the same label. Labels start at 0 and increment for each new equivalent group."
     }
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "CorrectionResult",
     "QModel",
     "TopographyAnalyzer",
     "VoronoiPolyhedron"
    ]
)
def generic_group_labels(...):
    ...

# pymatgen.analysis.defects.utils.genrecip(a1: 'npt.ArrayLike', a2: 'npt.ArrayLike', a3: 'npt.ArrayLike', encut: 'float') -> 'Generator[npt.ArrayLike, None, None]'
@register_function(
    aliases=[
     "G-vectors",
     "energy cutoff generation",
     "genrecip",
     "plane-wave basis vectors",
     "reciprocal lattice vectors",
     "reciprocal space mesh"
    ],
    category="defects",
    description="Generate reciprocal lattice vectors (G-vectors) with kinetic energy below a specified cutoff, for use in plane-wave basis set construction or sampling reciprocal space in DFT calculations.",
    examples=[
     "import numpy as np\nfrom pymatgen.analysis.defects.utils import genrecip\na1 = np.array([1.0, 0.0, 0.0])\na2 = np.array([0.0, 1.0, 0.0])\na3 = np.array([0.0, 0.0, 1.0])\nvectors = list(genrecip(a1, a2, a3, encut=100.0))"
    ],
    key_results=[
     {
      "attr": "yielded item",
      "returns": "npt.ArrayLike (shape (3,), dtype float)",
      "note": "Each yielded vector is a three-component reciprocal lattice vector in units of 1/Bohr, satisfying |G|^2 < (eV_to_k(encut))^2."
     }
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "CorrectionResult",
     "QModel",
     "TopographyAnalyzer",
     "VoronoiPolyhedron"
    ]
)
def genrecip(...):
    ...

# pymatgen.analysis.defects.utils.get_avg_chg(chgcar: 'VolumetricData', fcoord: 'npt.ArrayLike', radius: 'float' = 0.4) -> 'float'
@register_function(
    aliases=[
     "average charge",
     "charge density sphere",
     "get_avg_chg",
     "sphere integration",
     "volumetric data analysis"
    ],
    category="defects",
    description="Computes the average charge density within a sphere of a given radius centered at a specified fractional coordinate in a volumetric charge density (e.g., from a DFT calculation), used to evaluate local charge around defects or integration of charge in a region.",
    examples=[
     "avg_chg_sphere = get_avg_chg(chgcar, fpos)"
    ],
    key_results=[
     {
      "attr": "return_value",
      "returns": "float",
      "note": "The average charge (or charge density, depending on units of chgcar) within the sphere, computed as total charge in sphere divided by sphere volume."
     }
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "CorrectionResult",
     "QModel",
     "TopographyAnalyzer",
     "VoronoiPolyhedron"
    ]
)
def get_avg_chg(...):
    ...

# pymatgen.analysis.defects.utils.get_ipr_in_window(bandstructure: 'BandStructure', procar: 'Procar', band_window: 'int' = 5) -> 'dict[Spin, npt.NDArray]'
@register_function(
    aliases=[
     "IPR",
     "defect localization IPR",
     "get_ipr_in_window",
     "inverse participation ratio"
    ],
    category="defects",
    description="Computes the inverse participation ratio (IPR) for bands within a specified window around the Fermi level, used to identify localized (defect) states in a VASP band structure.",
    examples=[
     "ipr_dict = get_ipr_in_window(bandstructure, procar, band_window=5)\nprint(ipr_dict[(0,0)].shape)  # (num_bands, 2)"
    ],
    key_results=[
     {
      "attr": "result[(kpoint_index, spin_index)]",
      "returns": "numpy.ndarray",
      "note": "2D array of shape (num_bands_in_window, 2): first column = band indices (relative to full band structure), second column = IPR values."
     },
     {
      "attr": "result.keys()",
      "returns": "dict_keys of tuples (int, int)",
      "note": "Each key is (k‑point index, spin index) where spin index is 0 for up, 1 for down."
     },
     {
      "attr": "result.values()",
      "returns": "dict_values of numpy.ndarray",
      "note": "Each value is the IPR array for that (k‑point, spin) combination."
     },
     {
      "attr": "array[:, 0]",
      "returns": "numpy.ndarray",
      "note": "Band indices within the window (integers)."
     },
     {
      "attr": "array[:, 1]",
      "returns": "numpy.ndarray",
      "note": "Inverse participation ratios (float) for each band in the window."
     }
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "CorrectionResult",
     "QModel",
     "TopographyAnalyzer",
     "VoronoiPolyhedron"
    ]
)
def get_ipr_in_window(...):
    ...

# pymatgen.analysis.defects.utils.get_labeled_inserted_structure(sites: 'npt.NDArray', host_structure: 'Structure', working_ion: 'str', min_dist: 'float', clustering_tol: 'float', sm: 'StructureMatcher') -> 'list[tuple[list[float], int]]'
@register_function(
    aliases=[
     "defect site labeling",
     "get_labeled_inserted_structure",
     "interstitial site grouping",
     "labeled insertion sites",
     "structure matching for interstitials"
    ],
    category="defects",
    description="Group candidate interstitial sites by symmetry after removing collisions with the host and clustering, returning fractional coordinates and integer labels for each unique site.",
    examples=[
     "result = get_labeled_inserted_structure(sites, host_structure, \"Li\", min_dist=0.5, clustering_tol=0.25, sm=StructureMatcher())\nfor fcoords, label in result:\n    print(f\"Site {fcoords} -> label {label}\")"
    ],
    key_results=[
     {
      "attr": "return value (list of tuples)",
      "returns": "list[tuple[list[float], int]]",
      "note": "Each tuple contains fractional coordinates (list of 3 floats) and an integer label indicating the symmetry-equivalent group. For example, [([0.5, 0.5, 0.5], 0), ([0.25, 0.25, 0.25], 1)]."
     },
     {
      "attr": "tuple[0] (fcoords)",
      "returns": "list[float]",
      "note": "Fractional coordinates of the candidate site after collision removal and clustering."
     },
     {
      "attr": "tuple[1] (label)",
      "returns": "int",
      "note": "Integer label assigned by structure matching; sites with the same label are symmetrically equivalent."
     }
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "CorrectionResult",
     "QModel",
     "TopographyAnalyzer",
     "VoronoiPolyhedron"
    ]
)
def get_labeled_inserted_structure(...):
    ...

# pymatgen.analysis.defects.utils.get_local_extrema(chgcar: 'VolumetricData', find_min: 'bool' = True) -> 'npt.NDArray'
@register_function(
    aliases=[
     "charge density peaks",
     "get_local_extrema",
     "local extrema",
     "maxima search",
     "minima search",
     "peak detection",
     "topological analysis"
    ],
    category="defects",
    description="Finds all fractional coordinates of local minima (or maxima, if specified) in a volumetric charge density, useful for identifying potential defect sites or interstitial positions in a crystal.",
    examples=[
     "loc_min = get_local_extrema(chgcar, frac_pos)",
     "for a, b in zip(sorted(loc_min.tolist()), sorted(frac_pos)):"
    ],
    key_results=[
     {
      "attr": "returned value",
      "returns": "numpy.ndarray",
      "note": "Array of shape (N, 3) with fractional coordinates (each row is [x, y, z]) of local extrema in the original unit cell."
     }
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "CorrectionResult",
     "QModel",
     "TopographyAnalyzer",
     "VoronoiPolyhedron"
    ]
)
def get_local_extrema(...):
    ...

# pymatgen.analysis.defects.utils.get_localized_states(bandstructure: 'BandStructure', procar: 'Procar', band_window: 'int' = 7) -> 'Generator[tuple[int, int, int, float], None, None]'
@register_function(
    aliases=[
     "IPR analysis",
     "band localization",
     "defect states",
     "get_localized_states",
     "inverse participation ratio",
     "localized states"
    ],
    category="defects",
    description="Identifies the most localized electronic states near the Fermi level by computing the inverse participation ratio (IPR) from a PROCAR file, useful for finding defect states or surface states in a band structure.",
    examples=[
     "get_localized_states(bs, procar=procar)",
     "for iband, _ikpt, _ispin, _val in get_localized_states(bs, procar=procar):",
     "for iband, _ikpt, _ispin, _val in get_localized_states(bs, procar=procar, band_window=100"
    ],
    key_results=[
     {
      "attr": "band",
      "returns": "int",
      "note": "Band index of the most localized state."
     },
     {
      "attr": "kpt",
      "returns": "int",
      "note": "K-point index."
     },
     {
      "attr": "spin",
      "returns": "int",
      "note": "Spin channel index."
     },
     {
      "attr": "ipr",
      "returns": "float",
      "note": "Inverse participation ratio value (lower means more localized)."
     }
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "CorrectionResult",
     "QModel",
     "TopographyAnalyzer",
     "VoronoiPolyhedron"
    ]
)
def get_localized_states(...):
    ...

# pymatgen.analysis.defects.utils.get_plane_spacing(lattice: 'npt.NDArray') -> 'list[float]'
@register_function(
    aliases=[
     "crystal plane spacing",
     "get_plane_spacing",
     "interplanar spacing",
     "lattice plane spacing",
     "plane spacing"
    ],
    category="defects",
    description="Computes the Cartesian spacing between periodic planes of a unit cell, returning for each lattice vector the spacing of planes generated by the other two vectors. Useful for understanding the distance between crystal planes or checking consistency of lattice vectors.",
    examples=[
     "assert np.allclose(get_plane_spacing(lattice), [2.785, 2.785, 5.239], atol=0.001)"
    ],
    key_results=[
     {
      "attr": "returned list",
      "returns": "list[float]",
      "note": "The k-th element is the spacing (in Angstroms, assuming input lattice vectors are in Cartesian coordinates) of the set of planes that are generated by all lattice vectors except the k-th one. For example, for a 3D lattice, result[0] is the spacing between planes parallel to vectors 1 and 2."
     }
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "CorrectionResult",
     "QModel",
     "TopographyAnalyzer",
     "VoronoiPolyhedron"
    ]
)
def get_plane_spacing(...):
    ...

# pymatgen.analysis.defects.utils.get_symmetry_labeled_structures() -> 'None'
@register_function(
    aliases=[
     "get_labeled_inserted_structure",
     "get_symmetry_labeled_structures"
    ],
    category="defects",
    description="This deprecated function was an alias for `get_labeled_inserted_structure`; it returns `None` and issues a deprecation warning, so do not use it.",
    examples=[
     "import pymatgen.analysis.defects.utils as utils\nutils.get_symmetry_labeled_structures()  # Deprecated; prints warning, returns None"
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "CorrectionResult",
     "QModel",
     "TopographyAnalyzer",
     "VoronoiPolyhedron"
    ]
)
def get_symmetry_labeled_structures(...):
    ...

# pymatgen.analysis.defects.utils.get_zfile(directory: 'Path', base_name: 'str', allow_missing: 'bool' = False) -> 'Path | None'
@register_function(
    aliases=[
     "file resolution",
     "find gzipped file",
     "get zipped file",
     "get_zfile",
     "locate compressed file"
    ],
    category="defects",
    description="Locates a file in a directory, automatically matching plain or gzipped (.gz/.GZ) versions, typically used to read defect calculation outputs that may be compressed.",
    examples=[
     "result = get_zfile(Path('./calc_dir'), 'OUTCAR'); if result: print(result.name)"
    ],
    key_results=[
     {
      "attr": ".name",
      "returns": "str",
      "note": "Filename including extension, e.g., 'OUTCAR.gz' or 'OUTCAR'."
     },
     {
      "attr": ".suffix",
      "returns": "str",
      "note": "File extension, e.g., '.gz' or empty string."
     },
     {
      "attr": ".parent",
      "returns": "Path",
      "note": "Parent directory of the found file."
     }
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "CorrectionResult",
     "QModel",
     "TopographyAnalyzer",
     "VoronoiPolyhedron"
    ]
)
def get_zfile(...):
    ...

# pymatgen.analysis.defects.utils.group_docs(docs: 'Sequence', sm: 'StructureMatcher', get_structure: 'Callable', get_hash: 'Callable | None' = None) -> 'Generator[tuple[str | None, list], None, None]'
@register_function(
    aliases=[
     "defect grouping by structure",
     "group_docs",
     "hash-and-structure grouping",
     "structure-based grouping"
    ],
    category="defects",
    description="Group defect documents (or generic objects) first by a hash key (e.g., defect name) and then by structural similarity using StructureMatcher, yielding generator of (hash_key, list_of_structurally_matched_docs) tuples.",
    examples=[
     "sgroups = group_docs([vac1, vac2, int1, vac3, vac4, int2], sm, lambda x: x.defect_structure, )",
     "sgroups = group_docs([vac1, vac2, int1, vac3, vac4, int1, int2], sm, lambda x: x.defect_structure, lambda x: x.name, )"
    ],
    key_results=[
     {
      "attr": "yielded tuple",
      "returns": "(str | None, list)",
      "note": "First element is the hash key (e.g., defect name) or None if no get_hash provided; second is a list of documents sharing that hash and being structurally equivalent according to the StructureMatcher."
     }
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "CorrectionResult",
     "QModel",
     "TopographyAnalyzer",
     "VoronoiPolyhedron"
    ]
)
def group_docs(...):
    ...

# pymatgen.analysis.defects.utils.remove_collisions(fcoords: 'npt.NDArray', structure: 'Structure', min_dist: 'float' = 0.9) -> 'npt.NDArray'
@register_function(
    aliases=[
     "clean candidate sites",
     "collision removal",
     "filter points by distance",
     "minimum distance filter",
     "remove close points",
     "remove_collisions"
    ],
    category="defects",
    description="Filters a set of candidate fractional coordinates (e.g., for interstitial sites or defect positions) by removing those that lie within a minimum distance of any atom in a given structure, ensuring the remaining points are sufficiently far from existing atoms.",
    examples=[
     "import numpy as np\nfrom pymatgen.core import Structure, Lattice\nfrom pymatgen.analysis.defects.utils import remove_collisions\n\n# Example: create a simple cubic structure with one atom\nlattice = Lattice.cubic(3.0)\nstructure = Structure(lattice, [\"Si\"], [[0.0, 0.0, 0.0]])\ncandidates = np.array([[0.1, "
    ],
    key_results=[
     {
      "attr": "return value",
      "returns": "numpy.ndarray",
      "note": "A 2D array of shape (N, 3) of fractional coordinates that are at least min_dist away from all atoms in the structure."
     }
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "CorrectionResult",
     "QModel",
     "TopographyAnalyzer",
     "VoronoiPolyhedron"
    ]
)
def remove_collisions(...):
    ...

# pymatgen.analysis.defects.utils.sort_positive_definite(list_in: 'list', ref1: 'object', ref2: 'object', dist: 'Callable') -> 'tuple[tuple, tuple[float]]'
@register_function(
    aliases=[
     "direction-aware sort",
     "positive definite sort",
     "signed distance sort",
     "sort along line",
     "sort_positive_definite"
    ],
    category="defects",
    description="Sort a list of objects (e.g., structures) that can only be compared via a positive-definite distance metric, by using two reference points to define a direction along which the objects lie, returning the sorted list and signed distances.",
    examples=[
     "sorted_structs, distances = sort_positive_definite(structures, ref_struct1, ref_struct2, dist=StructureMatcher().get_distance)"
    ],
    key_results=[
     {
      "attr": "return value[0]",
      "returns": "tuple of objects",
      "note": "The sorted list of input objects in the order determined by the signed distance from ref1."
     },
     {
      "attr": "return value[1]",
      "returns": "tuple of floats",
      "note": "The signed distances of each object from ref1, positive in the direction from ref1 to ref2."
     }
    ],
    related=[
     "ChargeInsertionAnalyzer",
     "CorrectionResult",
     "QModel",
     "TopographyAnalyzer",
     "VoronoiPolyhedron"
    ]
)
def sort_positive_definite(...):
    ...
