import unittest
import numpy as np
import os
from unittest.mock import patch, mock_open
from tdmrsdm import TDMRSDM  # Replace with the actual module name where TDMRSDM is defined

class TestTDMRSDM(unittest.TestCase):

    def setUp(self):
        # Sample input data
        self.freq_GHz = 2.5  # GHz
        self.sst = [20,]  # degrees Celsius
        self.som = 1.5  # percentage
        self.sbd = 1.3  # g/cm^3
        self.ssm = 0.25  # g/g
    
    @patch("tdmrsdm.TDMRSDM._extract_model_constant")
    def test_initialization(self, mock_extract_constant):
        # Mock the return value for the constants extraction function
        mock_extract_constant.return_value = 1.0

        # Instantiate the TDMRSDM class
        model = TDMRSDM(
            freq_GHz=self.frequency,
            sst=self.sst,
            som=self.som,
            sbd=self.sbd,
            ssm=self.ssm
        )

        # Check attributes are initialized correctly
        self.assertEqual(model.f, self.frequency * 1.0e+9)
        np.testing.assert_array_equal(model.T, self.sst)
        self.assertEqual(model.som, self.som)
        self.assertEqual(model.rd, self.sbd)
        self.assertEqual(model.mg, self.ssm / self.sbd)
    
    @patch("tdmrsdm.TDMRSDM._extract_model_constant")
    def test_run_function(self, mock_extract_constant):
        mock_extract_constant.return_value = 1.0  # Mocked return for constants
        model = TDMRSDM(
            freq_GHz=self.frequency,
            sst=self.sst,
            som=self.som,
            sbd=self.sbd,
            ssm=self.ssm
        )
        
        result = model.run()
        self.assertIsNotNone(result, "Run method should return a result.")

    @patch("tdmrsdm.TDMRSDM._extract_model_constant")
    @patch("os.path.isdir", return_value=True)
    def test_missing_constants_folder(self, mock_isdir, mock_extract_constant):
        # Test if OSError is raised when constants directory is missing
        mock_isdir.return_value = False
        with self.assertRaises(OSError):
            TDMRSDM(
                freq_GHz=self.frequency,
                sst=self.sst,
                som=self.som,
                sbd=self.sbd,
                ssm=self.ssm
            )

if __name__ == "__main__":
    unittest.main()