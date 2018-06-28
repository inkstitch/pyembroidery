import pyembroidery.EmbPattern as EmbPattern
import pyembroidery.PatternReader as PatternReader
import pyembroidery.WriteEncoder as encode

encode = encode.WriteEncoder()

def render(pattern):
    return encode.process(pattern)

def get_extension_by_filename(filename):
    import os.path
    return os.path.splitext(filename)[1][1:]


def read(filename):
    reader = PatternReader.PatternReader();
    extension = get_extension_by_filename(filename)
    extension = extension.lower()
    with open(filename, "rb") as f:
        if extension == "dst":
            import pyembroidery.DstReader
            pyembroidery.DstReader.read(f, reader)
        elif extension == "pec":
            import pyembroidery.PecReader
            pyembroidery.PecReader.read(f, reader)
        elif extension == "pes":
            import pyembroidery.PesReader
            pyembroidery.PesReader.read(f, reader)
        elif extension == "exp":
            import pyembroidery.ExpReader
            pyembroidery.ExpReader.read(f, reader)
        elif extension == "vp3":
            import pyembroidery.Vp3Reader
            pyembroidery.Vp3Reader.read(f, reader)
        elif extension == "jef":
            import pyembroidery.JefReader
            pyembroidery.JefReader.read(f, reader)
        f.close()
        return reader.pattern;


def write(pattern, file):
    extension = get_extension_by_filename(file)
    extension = extension.lower()
    with open(file, "wb") as file:
        if extension == "dst":
            import pyembroidery.DstWriter
            pyembroidery.DstWriter.write(pattern, file)
        elif extension == "pec":
            import pyembroidery.PecWriter
            pyembroidery.PecWriter.write(pattern, file)
        elif extension == "pes":
            import pyembroidery.PesWriter
            pyembroidery.PesWriter.write(pattern, file)
        elif extension == "exp":
            import pyembroidery.ExpWriter
            pyembroidery.ExpWriter.write(pattern, file)
        elif extension == "vp3":
            import pyembroidery.Vp3Writer
            pyembroidery.Vp3Writer.write(pattern, file)
        elif extension == "jef":
            import pyembroidery.JefWriter
            pyembroidery.JefWriter.write(pattern, file)
        else:
            pass
        file.close()


def convert(filename_from, filename_to):
    pattern = read(filename_from);
    if pattern == None:
        return
    # Stablize Pattern Data.
    write(pattern, filename_to)
