import os
from pathlib import Path
import tempfile
import warnings
from lhagrid import LHASet
import pandas as pd


def read_pdfsets_index(file: str) -> pd.DataFrame:
    """
    Read the pdfsets.index file and return a list of lines.
    """
    if not os.path.exists(file):
        raise FileNotFoundError(f"File {file} does not exist.")

    return pd.read_csv(
        file,
        sep=" ",
        header=None,
        comment="#",
        skip_blank_lines=True,
        names=["SetIndex", "Name", "NumMembers"],
    )


def write_pdfsets_index(file: str, entries: pd.DataFrame) -> None:
    """
    Write the entries to the pdfsets.index file.
    """
    if not isinstance(entries, pd.DataFrame):
        raise TypeError("Entries must be a pandas DataFrame.")

    # Ensure the DataFrame has the correct columns
    if not all(col in entries.columns for col in ["SetIndex", "Name", "NumMembers"]):
        raise ValueError(
            "DataFrame must contain 'SetIndex', 'Name', and 'NumMembers' columns."
        )

    entries.to_csv(file, sep=" ", header=False, index=False, mode="w")


def install(set: LHASet, folder=None) -> None:
    """
    Install the LHAInfo and LHAGrid to a folder.
    """
    info = set.info
    grid = set.grids
    name = set.name
    assert info.NumMembers == len(grid), (
        f"Number of members in LHAInfo ({info.NumMembers}) must match number of grids ({len(grid)})"
    )
    if folder is None:
        # try to find lhapdf installation location
        path_list = []
        try:
            import lhapdf

            path_list = lhapdf.paths()
        except ImportError:
            warnings.warn(
                "LHAPDF is not installed, using current directory as default folder"
            )
        folder = path_list[0] if not path_list else "."

    if not os.path.exists(folder):
        os.makedirs(folder)

    # check if there is a pdfsets.index file in the folder
    if not os.path.exists(folder + "/pdfsets.index"):
        # Touch the file to create it
        Path(folder + "/pdfsets.index").touch()

    df = read_pdfsets_index(folder + "/pdfsets.index")

    # check if set with that name already exists
    if not df.empty and name in df["Name"].values:
        mask = df["Name"] == name
        # assert that the mask matches only one row
        if mask.sum() != 1:
            raise ValueError(f"Name {name} is not unique in the pdfsets.index file.")
        if df[mask]["SetIndex"].values[0] != info.SetIndex:
            raise ValueError(
                f"Name {name} already exists with a different SetIndex: {df[mask]['SetIndex'].values[0]}"
            )
        else:
            # Update the existing entry
            df.loc[mask, "NumMembers"] = info.NumMembers

    if not df.empty and info.SetIndex in df["SetIndex"].values:
        mask = df["SetIndex"] == info.SetIndex
        # assert that the mask matches only one row
        if mask.sum() != 1:
            raise ValueError(
                f"SetIndex {info.SetIndex} is not unique in the pdfsets.index file."
            )
        if df[mask]["Name"].values[0] != name:
            raise ValueError(
                f"SetIndex {info.SetIndex} already exists with a different name: {df[mask]['Name'].values[0]}"
            )
        else:
            # Update the existing entry
            df.loc[mask, "NumMembers"] = info.NumMembers
    else:
        # Add a new entry to the DataFrame
        new_entry = pd.DataFrame(
            {
                "SetIndex": [info.SetIndex],
                "Name": [name],
                "NumMembers": [info.NumMembers],
            }
        )
        df = pd.concat([df, new_entry], ignore_index=True)

    write_pdfsets_index(folder + "/pdfsets.index", df)

    set.to_folder(folder)


def getPDFSet(set: LHASet):
    try:
        import lhapdf

        # Create Temporary folder, but not deleted after use
        folder = tempfile.mkdtemp(prefix="lhapdf_" + set.name)
        install(set, folder)
        # We place it in to front of the paths so that it is found first
        lhapdf.setPaths([folder] + lhapdf.paths())
        return lhapdf.getPDFSet(set.name)
    except ImportError:
        raise ImportError(
            "LHAPDF is not installed. Please install it to use this function."
        )
