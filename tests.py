# FFNET TESTS
import unittest
from ffnet import *
from tools.py2f import *

# ffnet module tests #########################
class Testmlgraph(unittest.TestCase):
    def testEmpty(self):
        arch = ()
        conec = mlgraph(arch)
        self.assertEqual(conec, [])
    def testOneLayer(self):
        arch = (5,)
        conec = mlgraph(arch)
        self.assertEqual(conec, [])
    def testTwoLayers(self):
        arch = (1,1)
        conec = mlgraph(arch)
        self.assertEqual(conec, [(1,2), (0,2)])
    def testThreeLayers(self):
        arch = (2,2,1)
        conec = mlgraph(arch)
        conec0 = [(1, 3), (2, 3), (0, 3), \
                  (1, 4), (2, 4), (0, 4), \
                  (3, 5), (4, 5), (0, 5)]
        self.assertEqual(conec, conec0)
    def testNoBiases(self):
        arch = (2,2,1)
        conec = mlgraph(arch, biases = False)
        conec0 = [(1, 3), (2, 3), \
                  (1, 4), (2, 4), \
                  (3, 5), (4, 5)]
        self.assertEqual(conec, conec0)

class Testimlgraph(unittest.TestCase):
    def testEmpty(self):
        arch = ()
        self.assertRaises(TypeError, imlgraph, arch)
    def testOneLayer(self):
        arch = (5,)
        self.assertRaises(TypeError, imlgraph, arch)
    def testTwoLayers(self):
        arch = (1,1)
        self.assertRaises(TypeError, imlgraph, arch)
    def testThreeLayers(self):
        arch = (2,2,2)
        conec = imlgraph(arch)
        conec0 = [(1, 3), (2, 3), (0, 3), \
                  (1, 4), (2, 4), (0, 4), \
                  (3, 5), (4, 5), (0, 5), \
                  (1, 6), (2, 6), (0, 6), \
                  (1, 7), (2, 7), (0, 7), \
                  (6, 8), (7, 8), (0, 8)]
        self.assertEqual(conec, conec0)
    def testNoBiases(self):
        arch = (2,[(2,), (2,)],2)
        conec = imlgraph(arch, biases = False)
        conec0 = [(1, 3), (2, 3), \
                  (1, 4), (2, 4), \
                  (3, 5), (4, 5), \
                  (1, 6), (2, 6), \
                  (1, 7), (2, 7), \
                  (6, 8), (7, 8),]
        self.assertEqual(conec, conec0)


class Testtmlgraph(unittest.TestCase):
    def testEmpty(self):
        arch = ()
        conec = tmlgraph(arch)
        self.assertEqual(conec, [])
    def testOneLayer(self):
        arch = (5,)
        conec = tmlgraph(arch)
        self.assertEqual(conec, [])
    def testTwoLayers(self):
        arch = (1,1)
        conec = tmlgraph(arch)
        self.assertEqual(conec, [(0,2), (1,2)])
    def testThreeLayers(self):
        arch = (2,1,1)
        conec = tmlgraph(arch)
        conec0 = [(0, 3), (1, 3), (2, 3), \
                  (0, 4), (1, 4), (2, 4), (3, 4)]
        self.assertEqual(conec, conec0)
    def testNoBiases(self):
        arch = (2,1,1)
        conec = tmlgraph(arch, biases = False)
        conec0 = [(1, 3), (2, 3), \
                  (1, 4), (2, 4), (3, 4)]
        self.assertEqual(conec, conec0)

class Testlinear(unittest.TestCase):
    def testEqualInRanges(self):
        #self.assertRaises(ValueError, linear, 1.0, 1.0, 2.0, 3.0)
        self.assertEqual(linear(1.0, 1.0, 2.0, 3.0), (0, 2.5))
    def testEqualOutRanges(self):
        self.assertEqual(linear(2.0, 3.0, 1.0, 1.0), (0.0, 1.0))
    def testNormalCase(self):
        self.assertEqual(linear(0.0, 1.0, 0.0, 2.0), (2.0, 0.0))

class Testnorms(unittest.TestCase):
    def testEmpty(self):
        inarray = [[], []]
        n = norms(inarray)
        for i in xrange(len(n)):
            self.assertEqual(n[i].tolist(), [])
    def testOneColumn(self):
        inarray = [[0.], [1.], [2.]]
        n = norms(inarray)
        bool1 = n[0].tolist() == [[0., 2.]]
        bool2 = n[1].tolist() == [[0.5, 0.]]
        bool3 = n[2].tolist() == [[2., 0.]]
        self.assert_(bool1 and bool2 and bool3)
    def testNormalCase(self):
        inarray = [[0.,0.], [0.,1.], [1.,0.], [1.,1.]]
        n = norms(inarray, lower=0.15, upper=0.85)
        self.assertEqual(n[0].tolist(), [[0., 1.], [0, 1.]])
        self.assertEqual(n[1].tolist(), [[0.7, 0.15], [0.7, 0.15]])
        self.assertAlmostEqual(n[2][0,0], 1.42857143, 8)
        self.assertAlmostEqual(n[2][0,1], -0.21428571, 8)
        
class Testnormarray(unittest.TestCase):
    def testEmpty(self):
        inarray = [[], []]
        n = normarray(inarray, [])
        for i in xrange(len(n)):
            self.assertEqual(n[i].tolist(), [])
    
    def testOneColumn(self):
        inarray = [[0.], [1.], [1.], [0.]]
        coeff = [[0.7, 0.15]]
        n = normarray(inarray, coeff)
        for i in xrange(4):
            self.assertAlmostEqual(n[i,0], coeff[0][0]*inarray[i][0] + coeff[0][1], 8)
            
class Testffconec(unittest.TestCase):
    def testEmpty(self):
        conec = []
        self.assertRaises(ValueError, ffconec, conec)

    def testWithCycles(self):
        conec = [(1, 3), (2, 3), (0, 3), (3, 1), \
                 (1, 4), (2, 4), (0, 4), (4, 2), \
                 (3, 5), (4, 5), (0, 5), (5, 1) ]
        self.assertRaises(TypeError, ffconec, conec)

    def testNoCycles(self):
        conec = [(1, 3), (2, 3), (0, 3), \
                 (1, 4), (2, 4), (0, 4), \
                 (3, 5), (4, 5), (0, 5) ]
        n = ffconec(conec)
        self.assertEqual(sorted(n[2]), [1, 2])
        self.assertEqual(sorted(n[3]), [3, 4])
        self.assertEqual(sorted(n[4]), [5])
        
class Testbconec(unittest.TestCase):
    def testNoCycles(self):
        conec = [(1, 3), (2, 3), (0, 3), \
                 (1, 4), (2, 4), (0, 4), \
                 (3, 5), (4, 5), (0, 5) ]
        inno = [1,2]
        n = bconec(conec, inno)
        self.assertEqual(n[1], [8,7])
        
class Testdconec(unittest.TestCase):
    def testNoCycles(self):
        conec = [(1, 3), (2, 3), (0, 3), \
                 (1, 4), (2, 4), (0, 4), \
                 (3, 5), (4, 5), (0, 5) ]
        inno = [1,2]
        n = dconec(conec, inno)
        self.assertEqual(n[1], [1, 4, 7, 8, 2, 5, 7, 8])
        self.assertEqual(n[2], [0, 4, 8])
        
class TestFfnetSigmoid(unittest.TestCase):
    def setUp(self):
        self.conec = [(0, 3), (1, 3), (2, 3), \
                      (0, 4), (1, 4), (2, 4), (3, 4)]
        
        self.net = ffnet(self.conec); self.net([1.,1.]) #try if net works
        self.net.weights = array([1.]*7)
        
        self.tnet = ffnet(self.conec)
        self.tnet.weights = array([ 0.65527021, -1.12400619, 0.02066321, \
                                   0.13930684, -0.40153965, 0.11965115, -1.00622429 ])       
        self.input = [[0.,0.], [0.,1.], [1.,0.], [1.,1.]]
        self.target  = [[1.], [0.], [0.], [1.]]
        
    def testCall(self):
        self.assertEqual(self.net([0., 0.]), self.net.call([0., 0.]))
        self.assertAlmostEqual(self.net([0., 0.])[0], 0.8495477739862124, 8)
        
    def testDerivative(self):
        self.assertAlmostEqual(self.net.derivative([0., 0.])[0][0], 0.1529465741023702, 8)
        self.assertAlmostEqual(self.net.derivative([0., 0.])[0][1], 0.1529465741023702, 8)
        
    def testSqerror(self):
        err = self.tnet.sqerror(self.input, self.target)
        out = [ (self.tnet(self.input[i])[0] - self.target[i][0])**2 \
                for i in xrange( len(self.input) ) ]
        pyerr = 0.5 * sum(out)
        self.assertAlmostEqual(err, pyerr, 8)

    def testSqgrad(self):
        self.tnet._setnorm(self.input, self.target) # Possible bug, this shouldn't be here
        g = self.tnet.sqgrad(self.input, self.target)
        w1 = self.tnet.weights - g

        self.tnet.train_momentum(self.input, self.target, eta=1., momentum=0., maxiter=1)
        w2 = self.tnet.weights
        
        for i in xrange(len(w1)):
            self.assertAlmostEqual(w1[i], w2[i], 8)
            

    def testTrainGenetic(self):
        print "Test of genetic algorithm optimization"
        self.tnet.train_genetic(self.input, self.target, lower = -50., upper = 50., \
                                individuals = 20, generations = 1000)
        self.tnet.test(self.input, self.target)
    
    def testTrainMomentum(self): 
        print "Test of backpropagation momentum algorithm"
        self.tnet.train_momentum(self.input, self.target, maxiter=10000)
        self.tnet.test(self.input, self.target)

    def testTrainRprop(self): 
        print "Test of rprop algorithm"
        self.tnet.randomweights()
        xmi = self.tnet.train_rprop(self.input, self.target, \
                                    a=1.2, b=0.5, mimin=0.000001, mimax=50, \
                                    xmi=0.1, maxiter=10000, disp=1)
        self.tnet.test(self.input, self.target)

    def testTrainCg(self):
        print "Test of conjugate gradient algorithm"
        self.tnet.train_cg(self.input, self.target, maxiter=1000, disp=1)
        self.tnet.test(self.input, self.target)
        
    def testTrainBfgs(self):
        print "Test of BFGS algorithm"
        self.tnet.train_bfgs(self.input, self.target, maxfun = 1000)
        self.tnet.test(self.input, self.target)
        
    def testTrainTnc(self):
        print "Test of TNC algorithm"
        self.tnet.train_tnc(array(self.input), array(self.target), maxfun = 1000)
        self.tnet.test(self.input, self.target)
        
    def testTestdata(self):
        net = ffnet( mlgraph((1, 5, 1)) )
        input = [1, 2., 5]
        target = [2, 3, 5.]
        net.train_tnc(input, target, maxfun = 10)
        
class TestSaveLoadExport(unittest.TestCase):
    def setUp(self):
        conec = imlgraph( (5,5,5) )
        self.net = ffnet(conec)
        
    def tearDown(self):
        import os
        try: os.remove('tmpffnet.f')
        except: pass
        try: os.remove('tmpffnet.so')
        except: pass
        try: os.remove('tmpffnet.net')
        except: pass

    def testSaveLoad(self):
        res1 = self.net( [ 1, 2, 3, 4, 5. ] )
        savenet( self.net, 'tmpffnet.net' )
        net = loadnet( 'tmpffnet.net' )
        res2 = net( [ 1, 2, 3, 4, 5. ] )
        for i in xrange(5):
            self.assertAlmostEqual(res1[i], res2[i], 8)
        
    def testExport(self):
        resA = self.net ( [ 1, 2, 3, 4, 5. ] )
        resB = self.net.derivative( [ 1, 2, 3, 4, 5. ] )
        exportnet(self.net, 'tmpffnet.f')
        #import os; os.chdir('/tmp')
        from numpy import f2py
        f = open( 'tmpffnet.f', 'r' ); source = f.read(); f.close()
        f = open( 'fortran/ffnet.f', 'r' ); source += f.read(); f.close()
        import sys
        if sys.platform == 'win32':
            eargs = '--compiler=mingw32'
        else: eargs = ''
        f2py.compile(source, modulename = 'tmpffnet', extra_args = eargs, verbose = 0)
        import tmpffnet
        resA1 = tmpffnet.ffnet( [ 1, 2, 3, 4, 5. ] )
        resB1 = tmpffnet.dffnet( [ 1, 2, 3, 4, 5. ] )
        for i in xrange(5):
            self.assertAlmostEqual(resA[i], resA1[i], 7)
            for j in xrange(5):
                self.assertAlmostEqual(resB[i][j], resB1[i][j], 7)
        
# tools.py2f module tests #########################
class TestExport2Fortran(unittest.TestCase):  #not finished, just started
    def setUp(self):
        from numpy import array
        self.A = array([[1,2,3], [4,5,6]])
        self.B = array([[1,2,3], [4,5,6.]])
        
    def tearDown(self):
        pass
    
    def testArray(self):
        s1 = farray(self.A, 'test')      
        s2 = farray(self.B, 'test')
        
# run tests
if __name__ == '__main__':
    unittest.main()