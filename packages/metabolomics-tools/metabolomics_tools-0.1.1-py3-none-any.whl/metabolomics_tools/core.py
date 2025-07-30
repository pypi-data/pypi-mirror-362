import pandas as pd
import re
import re
from collections import defaultdict
import pubchempy as pcp

# PREPATAION OF IN SILICO LIPID MS2 SPECTRA TO INTEGRATE WITH xcms_process 
FINAL_NEEDED_COLUMNS = ['InChIKey', 'SMILES', 'CID', 'cpdName', 'formula', 'monoMass',
       'POS_mass', 'POS_intensity', 'POS_purity', 'POS_sourceId', 'NEG_mass',
       'NEG_intensity', 'NEG_purity', 'NEG_sourceId', 'predicted',
       'internalStd', 'primary', 'RT_HILIC', 'RT_RP']



DEFAULT_ISOTOPES = {
        "C": 12,
        "H": 1.0078250321,
        "N": 14.0030740052,
        "D": 2.014102,
        "O": 15.9949146221,
        "S": 31.97207069,
        "P": 30.97376151,
        "Br": 78.9183376,
        "Cl": 34.96885271,
        "F": 18.9984032,
        "Si": 27.9769265327,
        "Al": 26.9815,
        "Au": 196.9666,
        "B": 10.8110,
        "Co": 58.9332,
        "Cr": 51.9961,
        "Fe": 55.8450,
        "I": 126.9045,
        "K": 39.0983,
        "Mg": 24.3051,
        "Na": 22.9898,
        "Se": 79.91652,
        "As" :74.921595,
        "Ca": 39.96259098
        
    }



def cal_mono_mass(formulas, isotopes=None, charge=0):
    """
    Calculate the monoisotopic mass of one or more chemical formulas.

    This function parses chemical formulas, counts atoms, and calculates the
    monoisotopic mass for each formula. Optionally, custom isotopes can be
    provided, and the calculation can include an overall charge.

    Parameters
    ----------
    formulas : list of str
        List of chemical formulas as strings (e.g., ["H2O", "CO2"]).
    isotopes : dict, optional
        Dictionary of custom isotope masses, where keys are element or isotope
        labels (e.g., {"Oeighteen": 17.9991604}).
    charge : int, default=0
        The charge of the ion. A non-zero charge will adjust the final mass by
        subtracting or adding proton mass as appropriate.

    Returns
    -------
    dict
        Dictionary mapping each formula to its calculated monoisotopic mass.

    Examples
    --------
    >>> cal_mono_mass(["H2O"])
    {'H2O': 18.010564684}

    >>> cal_mono_mass(["H2O", "CO2"])
    {'H2O': 18.010564684, 'CO2': 43.98982924}

    >>> cal_mono_mass(["H2O", "CO2", "COOeighteen"], isotopes={"Oeighteen": 17.9991604})
    {'H2O': 18.010564684, 'CO2': 43.98982924, 'COOeighteen': 61.98899004}
    """
    # Define the atom counting function
    def atom_count(formulas):
        result = {}
        for formula in formulas:
            pattern = r'([A-Z][a-z]*)(\d*)'
            matches = re.findall(pattern, formula)

            atom_counts = defaultdict(int)
            for atom, count in matches:
                atom_counts[atom] += int(count) if count else 1

            result[formula] = dict(atom_counts)

        return result

    # Use atomCount function to get the atom counts
    atom_counts = atom_count(formulas)

    # Calculate the monoisotopic mass for each formula
    masses = {}
    for formula, atoms in atom_counts.items():
        masses[formula] = monomass(atoms, isotopes=isotopes, charge=charge)

    return masses



def read_file(file_path):
    """
    Read the entire contents of a file and return it as a string.

    Parameters
    ----------
    file_path : str
        Path to the file to be read.

    Returns
    -------
    str
        The full contents of the file as a single string.

    Examples
    --------
    >>> read_file("example.txt")
    'This is the content of example.txt...'
    """

    with open(file_path, "r") as file:
        content = file.read()  # Reads the entire file
    return content






def monomass(formula=None, isotopes=None, charge=0,default_isotopes = DEFAULT_ISOTOPES):
    """
    Calculate the monoisotopic mass of a chemical formula, with optional custom isotopes and charge adjustment.

    This function computes the monoisotopic mass based on an atomic composition
    dictionary. Optionally, custom isotope masses can be provided, and the
    formula mass can be adjusted for charge state (e.g., as observed in mass spectrometry).

    Parameters
    ----------
    formula : dict, optional
        A dictionary representing the atom counts in a molecular formula
        (e.g., {"H": 2, "O": 2} for hydrogen peroxide H₂O₂).
    isotopes : dict, optional
        Dictionary of custom isotopic masses to override the default ones.
        Keys are element names or isotope labels (e.g., {"Oeighteen": 17.9991604}).
    charge : int, default=0
        The charge state of the ion. If non-zero, the mass is adjusted accordingly.
        Positive charge adds protons; negative subtracts.
    default_isotopes : dict, optional
        Dictionary of default isotopic masses. Defaults to `DEFAULT_ISOTOPES`.

    Returns
    -------
    float
        The computed monoisotopic (or charged) mass of the molecular formula.

    Raises
    ------
    ValueError
        If the number of negative charges exceeds the number of hydrogens,
        making deprotonation impossible.

    Examples
    --------
    >>> monomass({"H": 2, "O": 2})
    34.005479304

    >>> monomass({"H": 2, "O": 1, "Oeighteen": 1}, isotopes={"Oeighteen": 17.9991604})
    36.009725084

    >>> monomass({"C": 6, "H": 12, "O": 6}, charge=1)
    181.0710059126534
    """
    if formula is None:
        formula = {}



    if isotopes:
        default_isotopes.update(isotopes)

    # Check if the number of negative charges exceeds the number of hydrogens
    if charge < 0 and abs(charge) > formula.get("H", 0):
        raise ValueError("The number of negative charges exceeds the number of hydrogens in the formula list")

    # Calculate the mass
    mass = sum(default_isotopes[element] * count for element, count in formula.items())

    if charge != 0:
        mass = abs((mass + charge * 1.007276466) / charge)

    return mass



def get_pubchem_cid_from_smiles(smiles:str) -> str:
    """
    Retrieve the PubChem Compound ID (CID) for a given SMILES string.

    This function uses the PubChemPy library to query the PubChem database
    and return the CID corresponding to the input SMILES (Simplified Molecular Input Line Entry System) string.

    Parameters
    ----------
    smiles : str
        A valid SMILES string representing a chemical compound.

    Returns
    -------
    str or None
        The PubChem Compound ID (CID) as a string if found; otherwise, returns None.

    Examples
    --------
    >>> get_pubchem_cid_from_smiles("C1=CC=CC=C1")  # Benzene
    '241'

    Notes
    -----
    This function requires the `pubchempy` package and an active internet connection.
    """
    try:
        compound = pcp.get_compounds(smiles, 'smiles')[0]
        return compound.cid
    except:
        return None



def parse_spectrum_data(file_path) -> pd.DataFrame:
    """
    Parse a Mass Spectrum (MSP) file into a pandas DataFrame.

    This function reads an MSP file (commonly used for spectral libraries),
    parses metadata and peak lists, and returns a structured DataFrame.
    Each block in the MSP file corresponds to one compound or spectrum.

    Parameters
    ----------
    file_path : str
        Path to the MSP file to be parsed.

    Returns
    -------
    pd.DataFrame
        A DataFrame where each row corresponds to a spectrum entry.
        Metadata fields are columns, and the "Num Peaks" column contains
        a list of (m/z, intensity) tuples representing the peaks.

    Examples
    --------
    >>> df = parse_spectrum_data("example.msp")
    >>> df.columns
    Index(['Name', 'PrecursorMZ', 'Num Peaks', ...], dtype='object')
    >>> df["Num Peaks"][0]
    [(100.1, 50.0), (101.2, 42.3), ...]

    Notes
    -----
    - Lines starting with a number are treated as m/z-intensity peaks.
    - Key-value metadata lines are split at the first occurrence of ": ".
    - Peaks are stored in the "Num Peaks" column as a list of tuples.
    """
    data = read_file(file_path)
    entries = []
    blocks = data.strip().split("\n\n")  # Split different compounds
    
    for block in blocks:
        entry = {}
        lines = block.split("\n")
        peaks = []
        
        for line in lines:
            if re.match(r"^\d", line):  # Peaks (numeric start)
                mz, intensity = line.split()
                peaks.append((float(mz), float(intensity)))
            else:
                key_value = line.split(": ", 1)
                if len(key_value) == 2:
                    key, value = key_value
                    entry[key.strip()] = value.strip()
        
        entry["Num Peaks"] = peaks  # Add peaks as a list of tuples
        entries.append(entry)
    
    return entries



def get_mz_per_spectra(ms2_fragments):
    """
    Extract and join the m/z values from MS2 fragment peaks.

    Given a list of MS2 fragment peaks as (m/z, intensity) tuples,
    this function returns a semicolon-separated string of m/z values.

    Parameters
    ----------
    ms2_fragments : list of tuple
        A list where each element is a tuple (m/z, intensity), typically
        extracted from parsed MS/MS data.

    Returns
    -------
    str
        A semicolon-separated string of m/z values (e.g., "100.1;101.2;150.3").

    Examples
    --------
    >>> get_mz_per_spectra([(100.1, 200.0), (101.2, 150.0)])
    '100.1;101.2'
    """
    return  ';'.join([str(x[0]) for x in ms2_fragments])



def get_intensity_per_spectra(ms2_fragments):
    """
    Extract and join the intensity values from MS2 fragment peaks.

    This function takes a list of (m/z, intensity) tuples representing MS2 fragment peaks,
    and returns a semicolon-separated string of intensities for a single compound/spectrum.

    Parameters
    ----------
    ms2_fragments : list of tuple
        A list where each element is a tuple (m/z, intensity), typically
        parsed from MS/MS data for one compound.

    Returns
    -------
    str
        A semicolon-separated string of intensity values (e.g., "200.0;150.0;80.5").

    Examples
    --------
    >>> get_intensity_per_spectra([(100.1, 200.0), (101.2, 150.0)])
    '200.0;150.0'
    """
    return  ';'.join([str(x[1]) for x in ms2_fragments])


