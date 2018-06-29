class StitchBlocks:
    def __init__(self):
        self.stitchblocks = []

    def convert_from_pattern(self, pattern):
        for stitchblock in pattern.get_as_stitchblocks():
            self.stitchblocks.append(stitchblock)
