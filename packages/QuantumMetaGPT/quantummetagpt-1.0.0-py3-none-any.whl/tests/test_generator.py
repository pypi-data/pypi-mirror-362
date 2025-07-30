import pytest
import os
from unittest.mock import MagicMock
from qmetagpt.report_generator.report_builder import ReportGenerator

class TestReportGenerator:
    @pytest.fixture
    def sample_data(self):
        return {
            "title": "Test Quantum Algorithm",
            "metrics": {
                "fidelity": 0.95,
                "execution_time": 5.32,
                "success": True
            },
            "counts": {'00': 512, '11': 512},
            "circuit": MagicMock()  # Mock QuantumCircuit
        }

    def test_report_generation(self, sample_data, tmp_path):
        report_gen = ReportGenerator()
        report_path = report_gen.generate(sample_data)
        
        assert os.path.exists(report_path)
        assert report_path.endswith(".pdf")
        
        # Cleanup
        if os.path.exists(report_path):
            os.remove(report_path)