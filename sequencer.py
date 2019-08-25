import time

from PIL import ImageDraw, Image


from GPIO_Init import displayImage, getFont


class sequencer:
    def __init__(self):
        # self.sequenceNote = [60] * 32
        self.sequenceNote = [60,61,66,23,65,34,65,76,45,65,45,34,65,34,75,45]
        self.sequenceVelocity = [64] * 32
        self.sequenceChance = [100] * 32
        print(self.sequenceNote)

        self.sequencesLength = 16

        self.duty = 50

        # Display Use
        self.barHeight = 50
        self.bar_Y_start = 14
        self.currentOn = 0

    def scale(self, val, src, dst):
        """
        :param val: Given input value for scaling
        :param src: Initial input value's Min Max Range pass in as tuple of two (Min, Max)
        :param dst: Target output value's Min Max Range pass in as tuple of two (Min, Max)
        :return: Return mapped scaling from target's Min Max range
        """
        return (float(val - src[0]) / float(src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]

    def renderPage(self):
        page = Image.new('1', (128, 64))
        draw = ImageDraw.Draw(page)
        # draw.rectangle([(0, 0), (128, 10)], 'white')
        draw.text((0, 0), "Vel", fill='white', font=getFont())
        draw.text((20, 0), "A4#", fill='white', font=getFont())
        draw.text((50, 0), "128bp", fill='white', font=getFont())
        # draw.text((80, 0), "Cy:30", fill='white', font=getFont())

        cur = self.currentOn * 6
        draw.line((cur + 1, self.bar_Y_start - 2, cur + 2, self.bar_Y_start - 2), fill="white")

        # Line x0 y0, x1, y1
        for i in range(0, self.sequencesLength):
            curr = 7 * i
            # Each sequence
            # Top Bar
            draw.line((curr + 1, self.bar_Y_start, curr + 2, self.bar_Y_start), fill="white")
            # Bottom Bar
            draw.line((curr + 1, 63, curr + 2, 63), fill="white")
            # Center
            draw.line((curr + 1, self.bar_Y_start, curr + 1, 63), fill="white")

            l = self.scale(self.sequenceNote[i], (112, 12), (62, 15))
            draw.line((curr+1, l, curr+4, l), fill="white")

        # page.show()
        displayImage(page)


seq = sequencer()
seq.renderPage()
time.sleep(50)
