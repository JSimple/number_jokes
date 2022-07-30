import unittest
import polynomial_gardenpath as pg
from numpy.polynomial import Polynomial
import json



class PolynomialGardenpathTestCase(unittest.TestCase):
    
    def test_json(self):
        self.maxDiff = None
        joke_part_1 = {"prev_points": [], "points": [354.0, 78.0, 9220.0], "all_points": [354.0, 78.0, 9220.0], "polynomial": {"coef": [353.99999999997016, -4984.999999999991, 4709.000000000007], "str": "353.99999999997016 - 4984.999999999991\u00b7x\u00b9 + 4709.000000000007\u00b7x\u00b2"}}
        joke_part_2 = {"prev_points": [354.0, 78.0, 9220.0], "points": [5.0, 2888.0], "all_points": [354.0, 78.0, 9220.0, 5.0, 2888.0], "polynomial": {"coef": [353.9999999999838, -28800.833333333485, 45285.249999999985, -19186.66666666661, 2426.2499999999886], "str": "353.9999999999838 - 28800.833333333485\u00b7x\u00b9 + 45285.249999999985\u00b7x\u00b2 -\n19186.66666666661\u00b7x\u00b3 + 2426.2499999999886\u00b7x\u2074"}}
        joke_part_3 = {"prev_points": [354.0, 78.0, 9220.0, 5.0, 2888.0], "points": [8.0, -35.0, 900.0], "all_points": [354.0, 78.0, 9220.0, 5.0, 2888.0, 8.0, -35.0, 900.0], "polynomial": {"coef": [353.9999999946844, -122190.53333323366, 261239.89166652414, -201343.5763888106, 75443.35416664532, -14839.751388885856, 1472.7541666664572, -58.13888888888366], "str": "353.9999999946844 - 122190.53333323366\u00b7x\u00b9 + 261239.89166652414\u00b7x\u00b2 -\n201343.5763888106\u00b7x\u00b3 + 75443.35416664532\u00b7x\u2074 - 14839.751388885856\u00b7x\u2075 +\n1472.7541666664572\u00b7x\u2076 - 58.13888888888366\u00b7x\u2077"}}
        joke_part_4 = {"prev_points": [354.0, 78.0, 9220.0, 5.0, 2888.0, 8.0, -35.0, 900.0], "points": [-543.0], "all_points": [354.0, 78.0, 9220.0, 5.0, 2888.0, 8.0, -35.0, 900.0, -543.0], "polynomial": {"coef": [353.999999889496, -178515.40833203486, 407282.24612823833, -348101.16735877143, 151090.790450344, -36743.869444181946, 5071.287847184801, -371.0548611082876, 11.175570436420454], "str": "353.999999889496 - 178515.40833203486\u00b7x\u00b9 + 407282.24612823833\u00b7x\u00b2 -\n348101.16735877143\u00b7x\u00b3 + 151090.790450344\u00b7x\u2074 - 36743.869444181946\u00b7x\u2075 +\n5071.287847184801\u00b7x\u2076 - 371.0548611082876\u00b7x\u2077 + 11.175570436420454\u00b7x\u2078"}}
        pgp = pg.PolynomialGardenpath(0)
        pgp.add_joke_part_w_points([354, 78, 9220])
        self.assertEqual(json.dumps({"joke_parts":[joke_part_1]}), pgp.json())
        pgp.add_joke_part_w_points([5,2888])
        self.assertEqual(json.dumps({"joke_parts":[joke_part_1,joke_part_2]}), pgp.json())
        pgp.add_joke_part_w_points([8,-35,900])
        self.assertEqual(json.dumps({"joke_parts":[joke_part_1,joke_part_2, joke_part_3]}), pgp.json())
        pgp.add_joke_part_w_points([-543])
        self.assertEqual(json.dumps({"joke_parts":[joke_part_1,joke_part_2, joke_part_3,joke_part_4]}), pgp.json())
        
        



if __name__ == '__main__':
     unittest.main()