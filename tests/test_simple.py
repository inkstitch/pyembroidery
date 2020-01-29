import os
import shutil
import pyembroidery
import test_fractals

def test_simple():

    pattern = pyembroidery.EmbPattern()

    pattern.add_thread({
        "rgb": 0x0000FF,
        "name": "Blue Test",
        "catalog": "0033",
        "brand": "PyEmbroidery Brand Thread"
    })

    pattern.add_thread({
        "rgb": 0x00FF00,
        "name": "Green",
        "catalog": "0034",
        "brand": "PyEmbroidery Brand Thread"
    })

    test_fractals.generate(pattern)

    settings = {
        "tie_on": True,
        "tie_off": True
    }
    
    temp_dir = "temp"
    if not os.path.isdir(temp_dir):
        os.mkdir(temp_dir)
    
    pyembroidery.write(pattern, temp_dir + "/generated.u01", settings)
    pyembroidery.write(pattern, temp_dir + "/generated.pec", settings)
    pyembroidery.write(pattern, temp_dir + "/generated.pes", settings)
    pyembroidery.write(pattern, temp_dir + "/generated.exp", settings)
    pyembroidery.write(pattern, temp_dir + "/generated.dst", settings)
    settings["extended header"] = True
    pyembroidery.write(pattern, temp_dir + "/generated-eh.dst", settings)
    pyembroidery.write(pattern, temp_dir + "/generated.jef", settings)
    pyembroidery.write(pattern, temp_dir + "/generated.vp3", settings)
    settings["pes version"] = 1,
    pyembroidery.write(pattern, temp_dir + "/generatedv1.pes", settings)
    settings["truncated"] = True
    pyembroidery.write(pattern, temp_dir + "/generatedv1t.pes", settings)
    settings["pes version"] = 6,
    pyembroidery.write(pattern, temp_dir + "/generatedv6t.pes", settings)

    pyembroidery.convert(temp_dir + "/generated.exp", temp_dir + "/genconvert.dst", 
        {"stable": False, "encode": False})
    
    shutil.rmtree(temp_dir)
