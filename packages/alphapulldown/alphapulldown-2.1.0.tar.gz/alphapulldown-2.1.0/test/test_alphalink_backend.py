#!/usr/bin/env python3
"""Test for AlphaLink backend integration.

This test reproduces the issue where AlphaLink backend fails because
the setup method returns a different structure than AlphaFold backend.
"""

import unittest
import tempfile
import os
import pickle
import gzip
import numpy as np
from unittest.mock import patch, MagicMock
import sys

# Add the parent directory to the path so we can import alphapulldown
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from alphapulldown.folding_backend.alphalink_backend import AlphaLinkBackend
from alphapulldown.objects import MultimericObject, MonomericObject
from alphapulldown.scripts.run_structure_prediction import predict_structure


class TestAlphaLinkBackend(unittest.TestCase):
    """Test cases for AlphaLink backend integration."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create mock feature files
        self.feature_dir = os.path.join(self.temp_dir, "features")
        os.makedirs(self.feature_dir, exist_ok=True)
        
        # Create mock pickle files
        self.protein_a_pkl = os.path.join(self.feature_dir, "proteinA.pkl")
        self.protein_b_pkl = os.path.join(self.feature_dir, "proteinB.pkl")
        
        # Create mock feature data
        mock_feature_data = {
            'aatype': np.random.randint(0, 21, (1, 50)),
            'msa_feat': np.random.randn(1, 50, 49),
            'target_feat': np.random.randn(1, 50, 22),
            'msa_mask': np.ones((1, 50)),
            'target_feat_mask': np.ones((1, 50)),
        }
        
        with open(self.protein_a_pkl, 'wb') as f:
            pickle.dump(mock_feature_data, f)
        
        with open(self.protein_b_pkl, 'wb') as f:
            pickle.dump(mock_feature_data, f)
        
        # Create mock crosslinks file
        self.crosslinks_file = os.path.join(self.temp_dir, "crosslinks.pkl.gz")
        crosslinks_data = {
            'proteinA': {'proteinB': [(1, 50, 0.2), (30, 80, 0.2)]}
        }
        with gzip.open(self.crosslinks_file, 'wb') as f:
            pickle.dump(crosslinks_data, f)
        
        # Create mock AlphaLink weights file
        self.alphalink_weights = os.path.join(self.temp_dir, "AlphaLink-Multimer_SDA_v3.pt")
        with open(self.alphalink_weights, 'w') as f:
            f.write("mock weights file")

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_alphalink_backend_setup_structure(self):
        """Test that AlphaLink backend setup returns the expected structure."""
        # Test the setup method directly
        result = AlphaLinkBackend.setup(
            model_dir=self.alphalink_weights,
            model_name="multimer_af2_crop"
        )
        
        # Check that it returns the expected keys
        expected_keys = {"param_path", "configs"}
        self.assertEqual(set(result.keys()), expected_keys)
        
        # Check that param_path points to our mock file
        self.assertEqual(result["param_path"], self.alphalink_weights)
        
        # Check that configs is not None
        self.assertIsNotNone(result["configs"])

    @patch('alphapulldown.folding_backend.backend.change_backend')
    @patch('alphapulldown.folding_backend.backend.setup')
    @patch('alphapulldown.folding_backend.backend.predict')
    @patch('alphapulldown.folding_backend.backend.postprocess')
    def test_predict_structure_with_alphalink(self, mock_postprocess, mock_predict, mock_setup, mock_change_backend):
        """Test that predict_structure works with AlphaLink backend."""
        
        # Mock the backend setup to return AlphaLink-style structure
        mock_setup.return_value = {
            "param_path": self.alphalink_weights,
            "configs": {"mock": "config"}
        }
        
        # Mock the predict method to return a generator
        def mock_predict_generator(**kwargs):
            yield {
                'object': MagicMock(),
                'prediction_results': "mock_results",
                'output_dir': self.temp_dir
            }
        
        mock_predict.return_value = mock_predict_generator()
        
        # Create mock objects to model
        mock_object = MagicMock()
        objects_to_model = [
            {
                'object': mock_object,
                'output_dir': self.temp_dir
            }
        ]
        
        # Test parameters
        model_flags = {
            "model_dir": self.alphalink_weights,
            "crosslinks": self.crosslinks_file,
            "num_cycle": 3,
            "num_predictions_per_model": 1
        }
        
        postprocess_flags = {
            "compress_pickles": False,
            "remove_pickles": False,
            "remove_keys_from_pickles": True,
            "use_gpu_relax": True,
            "models_to_relax": "None",
            "features_directory": [self.feature_dir],
            "convert_to_modelcif": True
        }
        
        # This should not raise a KeyError about 'model_runners'
        try:
            predict_structure(
                objects_to_model=objects_to_model,
                model_flags=model_flags,
                postprocess_flags=postprocess_flags,
                fold_backend="alphalink"
            )
        except KeyError as e:
            if "model_runners" in str(e):
                self.fail("AlphaLink backend should not require 'model_runners' key")
            else:
                raise

    def test_alphalink_backend_integration_issue(self):
        """Test that reproduces the original issue."""
        
        # This test reproduces the exact issue from the user's error
        # The problem is in run_structure_prediction.py line 197 where it tries to access
        # model_runners_and_configs["model_runners"] but AlphaLink backend doesn't return this key
        
        with patch('alphapulldown.folding_backend.backend.change_backend'):
            with patch('alphapulldown.folding_backend.backend.setup') as mock_setup:
                # Mock AlphaLink backend setup return value
                mock_setup.return_value = {
                    "param_path": self.alphalink_weights,
                    "configs": {"mock": "config"}
                }
                
                with patch('alphapulldown.folding_backend.backend.predict') as mock_predict:
                    # Mock predict to return generator
                    def mock_predict_generator(**kwargs):
                        yield {
                            'object': MagicMock(),
                            'prediction_results': "mock_results", 
                            'output_dir': self.temp_dir
                        }
                    mock_predict.return_value = mock_predict_generator()
                    
                    with patch('alphapulldown.folding_backend.backend.postprocess'):
                        # This should work without KeyError
                        objects_to_model = [{'object': MagicMock(), 'output_dir': self.temp_dir}]
                        model_flags = {"model_dir": self.alphalink_weights, "crosslinks": self.crosslinks_file}
                        postprocess_flags = {}
                        
                        try:
                            predict_structure(
                                objects_to_model=objects_to_model,
                                model_flags=model_flags,
                                postprocess_flags=postprocess_flags,
                                fold_backend="alphalink"
                            )
                        except KeyError as e:
                            if "model_runners" in str(e):
                                self.fail("AlphaLink backend integration is broken - missing 'model_runners' key")
                            else:
                                raise


if __name__ == '__main__':
    unittest.main() 