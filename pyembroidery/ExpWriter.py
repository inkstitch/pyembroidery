import pyembroidery.EmbPattern as EmbPattern

MAX_JUMP_DISTANCE = 127
MAX_STITCH_DISTANCE = 127

def write(pattern, file):
    with open(file, "wb") as f:
        stitches = pattern.stitches
        jumping = False
        xx = 0
        yy = 0
        for stitch in stitches:
            x = stitch[0]
            y = stitch[1]
            data = stitch[2]
            dx = x - xx
            dy = y - yy
            if data is EmbPattern.STITCH:
                if jumping:
                    f.write(b'\x00\x00')
                    jumping = False
                delta_x = round(dx) & 0xFF
                delta_y = -round(dy) & 0xFF
                f.write(bytes([delta_x, delta_y]))
            elif data is EmbPattern.JUMP:
                jumping = True
                delta_x = round(dx) & 0xFF
                delta_y = -round(dy) & 0xFF
                f.write(b'\x80\x04')
                f.write(bytes([delta_x, delta_y]))
            elif data is EmbPattern.COLOR_CHANGE:
                if jumping:
                    f.write(b'\x00\x00')
                    jumping = False
                f.write(b'\x80\x01\x00\x00')
            elif data is EmbPattern.STOP:
                if jumping:
                    f.write(b'\x00\x00')
                    jumping = False
                f.write(b'\x80\x01\x00\x00')
            elif data is EmbPattern.END:
                pass
            if jumping:
                f.write(b'\x00\x00')
                jumping = False
            xx = x
            yy = y
