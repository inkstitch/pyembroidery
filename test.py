import pyembroidery.ExpReader as expReader
import pyembroidery.ExpWriter as expWriter
import pyembroidery.DstReader as dstReader
import pyembroidery.DstWriter as dstWriter
import pyembroidery.PecWriter as pecWriter
import pyembroidery.PesWriter as pesWriter
import pyembroidery.JefWriter as jefWriter
import pyembroidery.PatternReader as pattern_reader
import pyembroidery.EmbPattern as EmbPattern
import pyembroidery.WriteEncoder as encode
import math

reader0 = pattern_reader.PatternReader()
reader1 = pattern_reader.PatternReader()
reader2 = pattern_reader.PatternReader()
reader3 = pattern_reader.PatternReader()

# In cases when the commands given are flawed in some ways, or need a lock stitch or translation etc.
# The pattern can be fed exact stitches, marking the ones with final and new for color and for location.
# If done this way, the encoder will interpolate everything else you need within the set max and min jump distances.
encoder = encode.WriteEncoder()
encoder.max_stitch_length = dstWriter.MAX_STITCH_DISTANCE
encoder.max_jump_length = dstWriter.MAX_JUMP_DISTANCE  # this is smallest value, so it'll work for all.
encoder.tie_on = True
encoder.tie_off = True
encoder.set_translation(0, -20)

# Initial test code. pyembroidery

expReader.read("BN00883_A.EXP", reader0)
dstReader.read("tree.dst", reader1)

dstWriter.write(reader0.pattern, "bn-convert.dst")
expWriter.write(reader1.pattern, "tree-covnert.exp")

dstReader.read("sequin.dst", reader2)
pesWriter.write(reader2.pattern, "sequin-convert.pes")

# GENERATES A FRACTAL
pattern = EmbPattern.EmbPattern()
pattern.add_stitch_absolute(0, 0, EmbPattern.STITCH_NEW_COLOR)

def evaluate_lsystem(symbol, rules, depth):
    if depth <= 0 or symbol not in rules:
        symbol()
    else:
        for produced_symbol in rules[symbol]:
            evaluate_lsystem(produced_symbol, rules, depth - 1)


class Turtle:
    angle = 0
    x = 0
    y = 0

    def forward(self, distance):
        self.x += distance * math.cos(self.angle)
        self.y += distance * math.sin(self.angle)
        pattern.add_stitch_absolute(self.x, self.y, EmbPattern.STITCH)
        end = [self.x, self.y]

    def turn(self, angle):
        self.angle += angle


turtle = Turtle()
amount = math.pi / 3;
a = lambda: turtle.forward(20)
b = lambda: turtle.forward(20)
l = lambda: turtle.turn(amount)
r = lambda: turtle.turn(-amount)
initial = lambda: None
rules = {
    initial: [a],
    a: [a, l, b, l, l, b, r, a, r, r, a, a, r, b, l],
    b: [r, a, l, b, b, l, l, b, l, a, r, r, a, r, b]
}
evaluate_lsystem(initial, rules, 5)
pattern.add_stitch_absolute(0, 0, EmbPattern.END)
# GENERATION END

pattern = encoder.process(pattern)  # invokes the encoder, to convert this to standard forms.

pecWriter.write(pattern, "generated.pec")
pesWriter.write(pattern, "generated.pes")
expWriter.write(pattern, "generated.exp")
dstWriter.write(pattern, "generated.dst")
dstWriter.extended_header = True
dstWriter.write(pattern, "generated-eh.dst")
jefWriter.write(pattern, "generated.jef")
