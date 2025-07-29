import pytest
import numpy as np
from nexus.io.reader.xyz_reader import XYZReader
from nexus.config.settings import Cutoff, SettingsBuilder, GeneralSettings, ClusteringSettings

def test_xyz_reader_scan(tmp_path):
    """Tests the scanning functionality of the XYZReader."""
    content = """2
Lattice="10.0 0.0 0.0 0.0 10.0 0.0 0.0 0.0 10.0"
H 0.0 0.0 0.0
O 1.0 1.0 1.0
2
Lattice="10.0 0.0 0.0 0.0 10.0 0.0 0.0 0.0 10.0"
H 2.0 2.0 2.0
O 3.0 3.0 3.0
"""
    xyz_file = tmp_path / "test.xyz"
    xyz_file.write_text(content)

    general_settings = GeneralSettings(file_location=str(xyz_file))
    clustering_settings = ClusteringSettings(node_types=["H", "O"])
    settings = SettingsBuilder().with_general(general_settings).with_clustering(clustering_settings).build()

    reader = XYZReader(settings)
    frame_indices = reader.scan()

    assert len(frame_indices) == 2
    assert frame_indices[0].num_nodes == 2

def test_xyz_reader_parse(tmp_path):
    """Tests the parsing functionality of the XYZReader."""
    content = """2
Lattice="10.0 0.0 0.0 0.0 10.0 0.0 0.0 0.0 10.0"
H 0.0 0.0 0.0
O 1.0 1.0 1.0
"""
    xyz_file = tmp_path / "test.xyz"
    xyz_file.write_text(content)

    general_settings = GeneralSettings(file_location=str(xyz_file))
    clustering_settings = ClusteringSettings(
        criterion='distance',
        node_types=["O"],
        node_masses=[15.999],
        connectivity=['O','O'],
        cutoffs=[Cutoff('O','O',3.5)]
        )
    settings = SettingsBuilder().with_general(general_settings).with_clustering(clustering_settings).build()
    
    reader = XYZReader(settings)
    frame_generator = reader.parse(0)
    frame = next(frame_generator)
    frame.initialize_nodes()

    assert frame.frame_id == 0
    assert len(frame.get_nodes()) == 2
    assert frame.get_nodes()[0].symbol == 'H'
