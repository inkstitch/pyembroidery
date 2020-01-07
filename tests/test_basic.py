import pyembroidery

def test_read_generic():
    pattern = pyembroidery.read("tests/formats/pes/Hopea.pes")
    pattern = pyembroidery.read("tests/formats/pec/Hopea.pec")
    pattern = pyembroidery.read("tests/formats/exp/Hopea.exp")
    pattern = pyembroidery.read("tests/formats/dst/Hopea.DST")
    pattern = pyembroidery.read("tests/formats/jef/Hopea.jef")
    pattern = pyembroidery.read("tests/formats/vp3/Hopea.vp3")

def test_read_pes():
    pattern = pyembroidery.read_pes("tests/formats/pes/Hopea.pes")

def test_read_pec():
    pattern = pyembroidery.read_pes("tests/formats/pec/Hopea.pec")

def test_read_exp():
    pattern = pyembroidery.read_exp("tests/formats/exp/Hopea.exp")

def test_read_dst():
    pattern = pyembroidery.read_dst("tests/formats/dst/Hopea.DST")

def test_read_jef():
    pattern = pyembroidery.read_jef("tests/formats/jef/Hopea.jef")

def test_read_vp3():
    pattern = pyembroidery.read_vp3("tests/formats/vp3/Hopea.vp3")
