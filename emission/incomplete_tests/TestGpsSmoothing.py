from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
# Standard imports
from future import standard_library
standard_library.install_aliases()
from builtins import *
import unittest
from datetime import datetime
import logging
import json
import numpy as np

# Our imports
from emission.core.get_database import get_section_db
import emission.analysis.intake.cleaning.cleaning_methods.jump_smoothing as cjs
import emission.analysis.intake.cleaning.cleaning_methods.speed_outlier_detection as cso
import emission.analysis.intake.cleaning.location_smoothing as ls
import emission.storage.compat.convert_moves_style_data as cmsd

class GpsSmoothingTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSmoothBoundaryOneZigZag(self):
        tp = cmsd.convert_track_point_array_to_df(
            json.load(open("emission/tests/data/smoothing_data/caltrain_one_zigzag.json")))
        boundary_smoother = cjs.SmoothBoundary(maxSpeed = 150 * 1000)
        boundary_smoother.filter(ls.add_speed(tp))
        removed_indices = np.nonzero(np.logical_not(boundary_smoother.inlier_mask_))[0].tolist()
        logging.info("removed indices = %s" % removed_indices)
        self.assertEqual(len(removed_indices), 1)
        self.assertEqual(removed_indices, [68])

    def testSmoothPosdapOneZigZag(self):
        tp = cmsd.convert_track_point_array_to_df(
            json.load(open("emission/tests/data/smoothing_data/caltrain_one_zigzag.json")))
        posdap_smoother = cjs.SmoothPosdap(maxSpeed = 150 * 1000)
        posdap_smoother.filter(ls.add_speed(tp))
        removed_indices = np.nonzero(np.logical_not(posdap_smoother.inlier_mask_))[0].tolist()
        logging.info("removed indices = %s" % removed_indices)
        self.assertEqual(len(removed_indices), 1)
        self.assertEqual(removed_indices, [68])

    def testSmoothMaxPosdapOneZigZag(self):
        tp_with_speeds = ls.add_speed(cmsd.convert_track_point_array_to_df(
            json.load(open("emission/tests/data/smoothing_data/caltrain_one_zigzag.json"))))

        cqo = cso.SimpleQuartileOutlier(quantile = 0.95, ignore_zeros = True)
        posdap_smoother = cjs.SmoothPosdap(maxSpeed = cqo.get_threshold(tp_with_speeds))
        posdap_smoother.filter(tp_with_speeds)
        removed_indices = np.nonzero(np.logical_not(posdap_smoother.inlier_mask_))[0].tolist()
        logging.info("removed indices = %s" % removed_indices)
        self.assertEqual(len(removed_indices), 1)
        self.assertEqual(removed_indices, [68])

    def testSmoothMaxBoundaryMultiZigZag(self):
        tp_with_speeds = ls.add_speed(cmsd.convert_track_point_array_to_df(
            json.load(open("emission/tests/data/smoothing_data/caltrain_multi_zigzag.json"))))

        cqo = cso.SimpleQuartileOutlier(quantile = 0.95, ignore_zeros = True)
        boundary_smoother = cjs.SmoothBoundary(maxSpeed = cqo.get_threshold(tp_with_speeds))
        boundary_smoother.filter(tp_with_speeds)
        removed_indices = np.nonzero(np.logical_not(boundary_smoother.inlier_mask_))[0].tolist()
        logging.info("removed indices = %s" % removed_indices)
        self.assertEqual(len(removed_indices), 2)
        self.assertEqual(removed_indices, [46, 58])

    def testSmoothMaxPosdapMultiZigZag(self):
        tp_with_speeds = ls.add_speed(cmsd.convert_track_point_array_to_df(
            json.load(open("emission/tests/data/smoothing_data/caltrain_multi_zigzag.json"))))

        cqo = cso.SimpleQuartileOutlier(quantile = 0.95, ignore_zeros = True)
        posdap_smoother = cjs.SmoothPosdap(maxSpeed = cqo.get_threshold(tp_with_speeds))
        posdap_smoother.filter(tp_with_speeds)
        removed_indices = np.nonzero(np.logical_not(posdap_smoother.inlier_mask_))[0].tolist()
        logging.info("removed indices = %s" % removed_indices)
        self.assertEqual(len(removed_indices), 1)
        self.assertEqual(removed_indices, [46])

    def testSmoothBoundaryWalkOneZigZag(self):
        tp_with_speeds = ls.add_speed(cmsd.convert_track_point_array_to_df(
            json.load(open("emission/tests/data/smoothing_data/walk_one_zigzag.json"))))
        boundary_smoother = cjs.SmoothBoundary(maxSpeed = 150 * 1000)
        boundary_smoother.filter(tp_with_speeds)
        removed_indices = np.nonzero(np.logical_not(boundary_smoother.inlier_mask_))[0].tolist()

        logging.info("removed indices = %s" % removed_indices)
        self.assertEqual(len(removed_indices), 0)
        self.assertEqual(removed_indices, [])

    def testSmoothMaxBoundaryWalkOneZigZag(self):
        tp_with_speeds = ls.add_speed(cmsd.convert_track_point_array_to_df(
            json.load(open("emission/tests/data/smoothing_data/walk_one_zigzag.json"))))
        cqo = cso.SimpleQuartileOutlier(quantile = 0.95, ignore_zeros = True)
        boundary_smoother = cjs.SmoothBoundary(maxSpeed = cqo.get_threshold(tp_with_speeds))
        boundary_smoother.filter(tp_with_speeds)
        removed_indices = np.nonzero(np.logical_not(boundary_smoother.inlier_mask_))[0].tolist()

        logging.info("removed indices = %s" % removed_indices)
        self.assertEqual(len(removed_indices), 1)
        self.assertEqual(removed_indices, [5])

    def testSmoothMaxPosdapWalkOneZigZag(self):
        tp_with_speeds = ls.add_speed(cmsd.convert_track_point_array_to_df(
            json.load(open("emission/tests/data/smoothing_data/walk_one_zigzag.json"))))
        cqo = cso.SimpleQuartileOutlier(quantile = 0.95, ignore_zeros = True)
        posdap_smoother = cjs.SmoothPosdap(maxSpeed = cqo.get_threshold(tp_with_speeds))
        posdap_smoother.filter(tp_with_speeds)
        removed_indices = np.nonzero(np.logical_not(posdap_smoother.inlier_mask_))[0].tolist()

        logging.info("removed indices = %s" % removed_indices)
        self.assertEqual(len(removed_indices), 0)
        self.assertEqual(removed_indices, [])

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
