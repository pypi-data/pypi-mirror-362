import ast
from dataclasses import dataclass
import os
from typing import Optional


@dataclass
class LHASet:
    name: str
    info: "LHAInfo"
    grids: list["LHAGrid"]

    @staticmethod
    def from_folder(folder: str) -> "LHASet":
        """
        Load an LHASet from a folder containing the LHAInfo and LHAGrid files.
        """
        name = folder.split("/")[-1]  # Get the last part of the folder path as the name

        info = LHAInfo.from_file(folder + f"/{name}.info")
        grids = []
        for i in range(info.NumMembers):
            grid = LHAGrid.from_file(folder + f"/{name}_{i:04d}.dat")
            grids.append(grid)

        return LHASet(name=info.SetDesc, info=info, grids=grids)

    def to_folder(self, folder: str) -> None:
        """
        Save the LHASet to a folder, creating the necessary files.
        """
        name = self.name
        info = self.info
        grid = self.grids

        folder = folder.rstrip("/") + "/" + name  # Ensure no trailing slash

        # Ensure the folder exists
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Write the info file
        info.to_file(folder + f"/{name}.info")

        # Write each grid file
        for i, g in enumerate(grid):
            g.to_file(folder + f"/{name}_{i:04d}.dat")


@dataclass
class LHAGrid:
    @dataclass
    class SubGridBlock:
        x_axis: list[float]
        q_axis: list[float]
        flavor_axis: list[int]
        data: list[list[float]]  # values go q first, then x

        def validate(self) -> None:
            if len(self.flavor_axis) != len(self.data[0]):
                raise ValueError("Flavour axis length must match data row length")
            if len(self.q_axis) * len(self.x_axis) != len(self.data):
                raise ValueError(
                    f"Data rows must match q_axis {len(self.q_axis)} and x_axis {len(self.x_axis)} dimensions"
                )

        @staticmethod
        def from_string(data: str, validate=True) -> "LHAGrid.SubGridBlock":
            lines = data.strip().split("\n")
            lines = [line for line in lines if not line.startswith("#")]
            x_axis = list(map(float, lines[0].split()))
            q_axis = list(map(float, lines[1].split()))
            flavor_axis = list(map(int, lines[2].split()))
            data_rows = [list(map(float, line.split())) for line in lines[3:]]

            assert len(flavor_axis) == len(data_rows[0]), (
                "Flavour axis length must match data row length"
            )
            assert len(q_axis) * len(x_axis) == len(data_rows), (
                f"Data rows must match q_axis {len(q_axis)} and x_axis {len(x_axis)} dimensions"
            )

            grid = LHAGrid.SubGridBlock(x_axis, q_axis, flavor_axis, data_rows)
            if validate:
                grid.validate()
            return grid

        def to_string(self, validate=True) -> str:
            if validate:
                self.validate()
            ret = ""
            ret += " ".join(f"{v:.7E}" for v in self.x_axis) + " \n"
            ret += " ".join(f"{v:.7E}" for v in self.q_axis) + " \n"
            ret += " ".join(f"{v}" for v in self.flavor_axis) + " \n"
            for row in self.data:
                ret += " " + " ".join(f"{v: .7E}" for v in row) + "\n"
            return ret

    PdfType: str
    Format: str
    subgrids: list[SubGridBlock]

    def validate(self) -> None:
        if not self.subgrids:
            raise ValueError("At least one subgrid must be present")
        for subgrid in self.subgrids:
            subgrid.validate()
        # Additional validation can be added here if needed

    @staticmethod
    def from_string(data: str, validate=True) -> None:
        blocks = data.strip().split("---")
        lines = blocks[0].strip().split("\n")
        # remove lines prefixed with '#'
        lines = [line for line in lines if not line.startswith("#")]

        pdftype = lines[0].split(":")[1].strip()
        format = lines[1].split(":")[1].strip()

        subgrids = []
        for block in blocks[1:]:
            if not block.strip():
                continue
            block_data = LHAGrid.SubGridBlock.from_string(block, validate=validate)
            subgrids.append(block_data)

        grid = LHAGrid(pdftype, format, subgrids)
        if validate:
            grid.validate()
        return grid

    @staticmethod
    def from_file(filename: str, validate=True) -> "LHAGrid":
        with open(filename, "r") as f:
            data = f.read()
        return LHAGrid.from_string(data, validate=validate)

    def to_string(self, validate=True) -> str:
        if validate:
            self.validate()
        ret = ""
        ret += f"PdfType: {self.PdfType}\n"
        ret += f"Format: {self.Format}\n"
        ret += "---\n"
        for subgrid in self.subgrids:
            ret += subgrid.to_string(validate)
            ret += " ---\n"
        return ret

    def to_file(self, filename: str, validate=True) -> None:
        with open(filename, "w") as f:
            f.write(self.to_string(validate=validate))


@dataclass
class LHAInfo:
    SetDesc: str
    SetIndex: int
    Authors: str
    Format: str
    DataVersion: str
    NumMembers: int
    Particle: int
    Flavors: list[int]
    OrderQCD: int
    FlavorScheme: str
    NumFlavors: int
    XMin: float
    XMax: float
    QMin: float
    QMax: float
    MZ: float
    MUp: float
    MDown: float
    MStrange: float
    MCharm: float
    MBottom: float
    MTop: float
    AlphaS_Type: str
    Reference: Optional[str] = None
    ErrorType: Optional[str] = None
    ForcePositive: Optional[int] = None
    AlphaS_MZ: Optional[float] = None
    AlphaS_OrderQCD: Optional[int] = None
    AlphaS_Qs: Optional[list[float]] = None
    AlphaS_Vals: Optional[list[float]] = None
    AlphaS_Lambda3: Optional[float] = None
    AlphaS_Lambda4: Optional[float] = None
    AlphaS_Lambda5: Optional[float] = None

    def validate(self) -> None:
        if not self.SetDesc:
            raise ValueError("SetDesc must not be empty")
        if not self.Authors:
            raise ValueError("Authors must not be empty")
        if self.NumMembers < 1:
            raise ValueError("NumMembers must be at least 1")
        if len(self.Flavors) == 0:
            raise ValueError("Flavors list must not be empty")
        if self.OrderQCD < 0:
            raise ValueError("OrderQCD must be a non-negative integer")
        if self.NumFlavors < 1:
            raise ValueError("NumFlavors must be at least 1")
        if self.XMin >= self.XMax:
            raise ValueError("XMin must be less than XMax")
        if self.QMin >= self.QMax:
            raise ValueError("QMin must be less than QMax")
        # Additional validation can be added here if needed

    @staticmethod
    def from_file(filename: str, validate=True) -> "LHAInfo":
        with open(filename, "r") as f:
            data = f.read()
        return LHAInfo.from_string(data, validate=validate)

    def to_string(self, validate=True) -> str:
        if validate:
            self.validate()
        ret = ""
        ret += f"SetDesc: {self.SetDesc}\n"
        ret += f"SetIndex: {self.SetIndex}\n"
        ret += f"Authors: {self.Authors}\n"
        ret += f"Reference: {self.Reference}\n"
        ret += f"Format: {self.Format}\n"
        ret += f"DataVersion: {self.DataVersion}\n"
        ret += f"NumMembers: {self.NumMembers}\n"
        ret += f"Particle: {self.Particle}\n"
        ret += f"Flavors: {self.Flavors}\n"
        ret += f"OrderQCD: {self.OrderQCD}\n"
        if self.ForcePositive is not None:
            ret += f"ForcePositive: {self.ForcePositive}\n"
        ret += f"FlavorScheme: {self.FlavorScheme}\n"
        ret += f"NumFlavors: {self.NumFlavors}\n"
        if self.ErrorType is not None:
            ret += f"ErrorType: {self.ErrorType}\n"
        ret += f"XMin: {self.XMin:.7e}\n"
        ret += f"XMax: {self.XMax:.7e}\n"
        ret += f"QMin: {self.QMin:.7e}\n"
        ret += f"QMax: {self.QMax:.7e}\n"
        ret += f"MZ: {self.MZ:.7e}\n"
        ret += f"MUp: {'0' if self.MUp == 0.0 else f'{self.MUp:.7e}'}\n"
        ret += f"MDown: {'0' if self.MDown == 0.0 else f'{self.MDown:.7e}'}\n"
        ret += f"MStrange: {'0' if self.MStrange == 0.0 else f'{self.MStrange:.7e}'}\n"
        ret += f"MCharm: {self.MCharm:.7e}\n"
        ret += f"MBottom: {self.MBottom:.7e}\n"
        ret += f"MTop: {self.MTop:.7e}\n"
        if self.AlphaS_MZ is not None:
            ret += f"AlphaS_MZ: {self.AlphaS_MZ:.7f}\n"
        if self.AlphaS_OrderQCD is not None:
            ret += f"AlphaS_OrderQCD: {self.AlphaS_OrderQCD}\n"
        if self.AlphaS_Type is not None:
            ret += f"AlphaS_Type: {self.AlphaS_Type}\n"
        if self.AlphaS_Qs is not None:
            ret += f"AlphaS_Qs: [{', '.join([f'{v:.7e}' for v in self.AlphaS_Qs])}]\n"
        if self.AlphaS_Vals is not None:
            ret += (
                f"AlphaS_Vals: [{', '.join([f'{v:.7e}' for v in self.AlphaS_Vals])}]\n"
            )
        if self.AlphaS_Lambda3 is not None:
            ret += f"AlphaS_Lambda3: {self.AlphaS_Lambda3}\n"
        if self.AlphaS_Lambda4 is not None:
            ret += f"AlphaS_Lambda4: {self.AlphaS_Lambda4}\n"
        if self.AlphaS_Lambda5 is not None:
            ret += f"AlphaS_Lambda5: {self.AlphaS_Lambda5}\n"
        return ret

    def to_file(self, filename: str, validate=True) -> None:
        with open(filename, "w") as f:
            f.write(self.to_string(validate=validate))

    @staticmethod
    def from_string(data: str, validate=True) -> "LHAInfo":
        lines = data.strip().split("\n")
        info = {}
        for line in lines:
            if not line.strip() or line.startswith("#"):
                continue
            key, value = line.split(":", 1)
            info[key.strip()] = value.strip()

        # Use explicit cases in the info dict access
        info = LHAInfo(
            SetDesc=info["SetDesc"],
            SetIndex=int(info["SetIndex"]),
            Authors=info["Authors"],
            Reference=info["Reference"],
            Format=info["Format"],
            DataVersion=info["DataVersion"],
            NumMembers=int(info["NumMembers"]),
            Particle=int(info["Particle"]),
            Flavors=ast.literal_eval(info["Flavors"]),
            OrderQCD=int(info["OrderQCD"]),
            FlavorScheme=info["FlavorScheme"],
            NumFlavors=int(info["NumFlavors"]),
            ErrorType=info["ErrorType"],
            XMin=float(info["XMin"]),
            XMax=float(info["XMax"]),
            QMin=float(info["QMin"]),
            QMax=float(info["QMax"]),
            MZ=float(info["MZ"]),
            MUp=float(info["MUp"]),
            MDown=float(info["MDown"]),
            MStrange=float(info["MStrange"]),
            MCharm=float(info["MCharm"]),
            MBottom=float(info["MBottom"]),
            MTop=float(info["MTop"]),
            AlphaS_MZ=float(info.get("AlphaS_MZ", 0.0)),
            AlphaS_OrderQCD=int(info.get("AlphaS_OrderQCD", 0)),
            AlphaS_Type=info.get("AlphaS_Type", ""),
            AlphaS_Qs=ast.literal_eval(info.get("AlphaS_Qs", "")),
            AlphaS_Vals=ast.literal_eval(info.get("AlphaS_Vals", "")),
            AlphaS_Lambda4=float(info.get("AlphaS_Lambda4", 0.0)),
            AlphaS_Lambda5=float(info.get("AlphaS_Lambda5", 0.0)),
        )
        if validate:
            info.validate()
        return info
