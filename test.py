import pyembroidery.ExpReader as expReader
import pyembroidery.ExpWriter as expWriter
import pyembroidery.DstReader as dstReader
import pyembroidery.DstWriter as dstWriter
import pyembroidery.PecWriter as pecWriter
import pyembroidery.PesWriter as pesWriter
import pyembroidery.PatternReader as pattern_reader
import pyembroidery.EmbPattern as EmbPattern
import pyembroidery.WriteEncoder as encode

reader0 = pattern_reader.PatternReader()
reader1 = pattern_reader.PatternReader()
reader2 = pattern_reader.PatternReader()
reader3 = pattern_reader.PatternReader()


# In cases when the commands given are flawed in some ways, or need a lock stitch or translation etc.
# The pattern can be fed exact stitches, marking the ones with final and new for color and for location.
# If done this way, the encoder will interpolate everything else you need within the set max and min jump distances.
encoder = encode.WriteEncoder()
encoder.max_stitch_length = dstWriter.MAX_STITCH_DISTANCE
encoder.max_jump_length = dstWriter.MAX_JUMP_DISTANCE #this is smallest value, so it'll work for all.
encoder.tie_on = True
encoder.tie_off = True
encoder.set_translation(0,-20)


# Initial test code. pyembroidery

expReader.read("BN00883_A.EXP",reader0)
dstReader.read("tree.dst",reader1)

dstWriter.write(reader0.pattern,"bn-convert.dst")
expWriter.write(reader1.pattern,"tree-covnert.exp")

dstReader.read("sequin.dst",reader2)
pesWriter.write(reader2.pattern,"sequin-convert.pes")


#invents own embpattern
pattern = EmbPattern.EmbPattern()
pattern.add_stitch_absolute(0,0,EmbPattern.STITCH_NEW_COLOR)
for x in range(1,10):
    for y in range(1,10):
        pattern.add_stitch_absolute(x*150,y*150,EmbPattern.STITCH)
    pattern.add_stitch_absolute(x*150, y*150, EmbPattern.STITCH_FINAL_COLOR)
    pattern.add_stitch_absolute(x*150, y*150, EmbPattern.STITCH_NEW_COLOR)
pattern.add_stitch_absolute(0,0,EmbPattern.END)

pattern = encoder.process(pattern) #invokes the encoder, to convert this to standard forms.

pecWriter.write(pattern,"generated.pec")
pesWriter.write(pattern,"generated.pes")
expWriter.write(pattern,"generated.exp")
dstWriter.write(pattern,"generated.dst")
dstWriter.extended_header = True
dstWriter.write(pattern,"generated-eh.dst")


