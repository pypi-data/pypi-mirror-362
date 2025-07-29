import pytest
import numpy as np
from nexus.core.node import Node
from nexus.core.frame import Frame
from nexus.core.system import System
from nexus.config.settings import Settings, SettingsBuilder, GeneralSettings

# Mock reader for testing the System class
class MockReader:
    def __init__(self, settings):
        self.settings = settings
        self.num_frames = 2
        self.frame_indices = [0, 1]

    def parse(self, frame_id):
        if frame_id < self.num_frames:
            yield Frame(frame_id=frame_id, _data={'symbol': ['H'], 'position': [np.array([0,0,0])]}, lattice=np.eye(3), nodes=[])
        else:
            raise StopIteration

    def scan(self):
        pass

    def detect(self, filepath):
        return True

def test_node_creation():
    """Tests the creation of a Node object."""
    node = Node(symbol='H', node_id=0, position=np.array([1.0, 2.0, 3.0]))
    assert node.symbol == 'H'
    assert node.node_id == 0
    np.testing.assert_array_equal(node.position, np.array([1.0, 2.0, 3.0]))

def test_frame_initialization():
    """Tests the initialization of a Frame object."""
    frame = Frame(frame_id=0, _data={}, lattice=np.eye(3), nodes=[])
    frame.initialize_nodes() # Should not raise any errors with empty data
    assert frame.frame_id == 0
    assert len(frame.nodes) == 0

def test_system_iteration():
    """Tests frame iteration in the System class."""
    general_settings = GeneralSettings(file_location="dummy.xyz", range_of_frames=(0, 1))
    settings = SettingsBuilder().with_general(general_settings).build()

    reader = MockReader(settings)
    system = System(reader, settings)
    
    frames = list(system.iter_frames())
    assert len(frames) == 2
    assert frames[0].frame_id == 0
    assert frames[1].frame_id == 1