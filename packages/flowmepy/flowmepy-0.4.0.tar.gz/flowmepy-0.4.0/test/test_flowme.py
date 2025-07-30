import os
import math
import unittest

import flowme

class TestFlowmeApi (unittest.TestCase):

    def __init__(self, method_name='runTest'):
        self.facs_path = os.path.join(os.path.dirname(__file__), 
            '../flowme/src/data/samples/FacsDiva.xml')
        self.kaluza_path = os.path.join(os.path.dirname(
            __file__), '../flowme/src/data/samples/Kaluza.analysis')
        self.fcs = flowme.fcs(self.facs_path)
        flowme.disable_optimizations()

        super().__init__(method_name)

    def test_events(self):
        events = self.fcs.events()

        # check dimensions
        self.assertEqual(events.shape, (90041, 16))

        # check values (first row for ./samples/FacsDiva.xml)
        firstrow = [0.009859, 0.984067, 1.310117, 0.845020, 1.332489, 2.175258,
                    0.691767, 1.096062, 2.385766, 1.352677, 2.829808, 3.020170,
                    1.095590, 1.555815, 1.380024, 1.615216]

        for val, tval in zip(events.values[0], firstrow):
            self.assertTrue(math.isclose(val, tval, rel_tol=1e-4))

        # check antibodies
        antibodies = [  'TIME', 'FSC-A', 'FSC-W', 'FSC-H', 'SSC-A', 'CD58', 'CD123', 'CD34',
                        'CD10', 'CD19', 'SY41', 'CD45', 'CD99', 'CD38', 'CD20',
                        'QDOT655-A']
        self.assertListEqual(list(events.columns), antibodies)

    def test_root_gate(self):
        fcs_with_intact_gate = flowme.fcs(self.facs_path, '', 'intact')
        events = fcs_with_intact_gate.events()
        gates = fcs_with_intact_gate.gate_labels()

        # check dimensions        
        self.assertEqual(events.shape, (80419, 16))
        self.assertEqual(gates.shape, (80419, 13))

    def test_gates(self):
        gates = self.fcs.gate_labels()

        # check dimensions
        self.assertEqual(gates.shape, (90041, 13))

        # check gate names
        gatenames = ['allevents', 'p1', 'p2', 'p3', 'syto+', 'singlets', 'intact', 'cd19+',
                     'pz', 'matureb-cells', 'blast', 'p4', 'erythropoiese']

        self.assertListEqual(list(gates.columns), gatenames)

        # check gating
        self.assertEqual(sum(gates["matureb-cells"]), 14756)
        self.assertEqual(sum(gates["blast"]), 357)

        # check exclusive gating
        exmb = self.fcs.label_exclusive("matureb-cells", ["blast"])
        self.assertEqual(sum(exmb), 14399) # mature B-cells without blasts


    def test_parallel_load(self):

        ff = flowme.load_fcs_from_list([self.facs_path, self.kaluza_path])

        # check if the data is the same after parallel load
        for f in ff:
            if f.filepath == self.facs_path:
                self.assertTrue(f.events.equals(self.fcs.events()))
                self.assertTrue(f.gates.equals(self.fcs.gate_labels()))


    def test_auto_gate(self):
        agates = self.fcs.auto_gate_labels()

        # check dimensions
        self.assertEqual(agates.shape, (80419, 3))

        # check gating
        self.assertEqual(sum(agates["intact"]), 64401)
        self.assertEqual(sum(agates["cd19"]), 15718)
        self.assertEqual(sum(agates["blast"]), 300)

if __name__ == '__main__':
    unittest.main()
