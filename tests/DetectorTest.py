import unittest

from libpyvinyl.Detector import Detector, DetectorParameters
from libpyvinyl.BaseCalculator import BaseCalculator, CalculatorParameters


class DetectorTest(unittest.TestCase):
    """
    Test class for the Detector class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        pass

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        pass

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

    def tearDown(self):
        """ Tearing down a test. """

        for f in self.__files_to_remove:
            if os.path.isfile(f): os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d): shutil.rmtree(d)

    @unittest.expectedFailure
    def testDefaultConstruction(self):
        """ Testing the default construction of the class. """

        # Construct the object.
        calculator = Detector()

        # Test provenance.
        self.assertIsInstance(calculator, Detector)
        self.assertIsInstance(calculator, BaseCalculator)


if __name__ == '__main__':
    unittest.main()

