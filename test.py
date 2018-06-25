import pyembroidery.ExpReader as expReader
import pyembroidery.ExpWriter as expWriter
import pyembroidery.DstReader as dstReader
import pyembroidery.DstWriter as dstWriter
import pyembroidery.PatternReader as patternPrinter
import pyembroidery.EmbPattern as EmbPattern
import pyembroidery.WriteEncoder as encode

printer = patternPrinter.PatternReader()


# Initial test code. pyembroidery can load a dst or exp file and save it to .exp format.
#added write DSTs

expReader.read("BN00883_A.EXP",printer)
#dstReader.read("sequin.dst",printer)
#dstReader.read("tree.dst",printer)

#expWriter.write(printer.pattern,"converted.exp")
#print("" , printer.count())


#invents own embpattern and totally works to write it to exp file.
# pattern = EmbPattern.EmbPattern()
#
# pattern.addStitchAbs(0,0,EmbPattern.STITCH_NEW_COLOR)
# for x in range(1,10):
#     for y in range(1,10):
#         pattern.addStitchAbs(x*150,y*150,EmbPattern.STITCH)
#     #pattern.addStitchAbs(x*150, y*150, EmbPattern.STITCH_FINAL_COLOR)
#     #pattern.addStitchAbs(x*150, y*150, EmbPattern.STITCH_NEW_COLOR)
# pattern.addStitchAbs(0,0,EmbPattern.END)
#

# In cases when the commands given are flawed in some ways, or need a lock stitch or translation etc.
# The pattern can be fed exact stitches, marking the ones with final and new for color and for location.
# If done this way, the encoder will interpolate everything else you need within the set max and min jump distances.
encoder = encode.WriteEncoder()
encoder.maxStitchLength = expWriter.maxStitchDistance
encoder.maxJumpLength = expWriter.maxJumpDistance
encoder.tie_on = True
encoder.tie_off = True
encoder.setTranslation(0,-20)

#pattern = encoder.process(pattern)
pattern = encoder.process(printer.pattern)

#writes the encoded pattern to file
#dstWriter.extendedHeader = True; #This exports rare extended headers with thread colors.
pattern.fixColorCount();
dstWriter.write(pattern,"converted.dst")

