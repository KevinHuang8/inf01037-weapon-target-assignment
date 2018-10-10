import unittest
import main

class Config(object):
    pass

class TestAll(unittest.TestCase):
    def test_expected_damage(self):
        test_cases = (
            (1, [1.0], [[1.0]], [0], 1.0),
            (2, [1.0, 1.0], [[0.5, 0.0], [0.0, 0.5]], [0, 1], 1.0),
            (2, [1.0, 1.0], [[0.5, 0.0], [0.0, 0.5]], [1, 0], 0.0),
            (2, [1.0, 1.0], [[0.5, 0.0], [0.0, 0.5]], [0, 0], 0.5),
            (2, [1.0, 1.0], [[0.5, 0.0], [0.0, 0.5]], [1, 1], 0.0),
        )

        for n, values, probabilities, assignment, damage in test_cases:
            instance = main.Instance(n, values, probabilities)
            config = Config()
            config.instance_file = 'data/WTA1'
            algo = main.Algorithm(config)
            algo.instance = instance
            self.assertAlmostEqual(
                algo.expected_damage(assignment),
                damage,
                0.00001
            )


if __name__ == '__main__':
    unittest.main()
