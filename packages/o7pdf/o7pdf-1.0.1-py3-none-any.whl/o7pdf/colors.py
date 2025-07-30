"""Color constants for the O7 PDFs"""


class O7Colors:  # pylint: disable=too-few-public-methods
    """Color constants for O7"""

    N900 = "#091E42"
    N800 = "#172B4D"
    N700 = "#253858"
    N600 = "#344563"
    N500 = "#42526E"
    N400 = "#505F79"
    N300 = "#5E6C84"
    N200 = "#6B778C"
    N100 = "#7A869A"
    N90 = "#8993A4"
    N80 = "#97A0AF"
    N70 = "#A5ADBA"
    N60 = "#B3BAC5"
    N50 = "#C1C7D0"
    N40 = "#DFE1E6"
    N30 = "#EBECF0"
    N20 = "#F4F5F7"
    N10 = "#FAFBFC"
    N0 = "#FFFFFF"

    R100 = "#fd6262"
    R200 = "#fd4848"
    R300 = "#fc2f2f"
    R400 = "#fc1616"
    R500 = "#dc0303"
    R600 = "#c30303"
    R700 = "#aa0202"
    R800 = "#910202"
    R900 = "#770202"

    OR100 = "#fc967a"
    OR200 = "#fc8261"
    OR300 = "#fb6e48"
    OR400 = "#fb5a2f"
    OR500 = "#f23705"
    OR600 = "#d93104"
    OR700 = "#c02c04"
    OR800 = "#a72603"
    OR900 = "#8e2003"

    #   /* Orange O7 */
    O100 = "#fda97e"
    O200 = "#fd9865"
    O300 = "#fd874c"
    O400 = "#fd7632"
    O500 = "#f95503"
    O600 = "#e04c03"
    O700 = "#c74402"
    O800 = "#ad3b02"
    O900 = "#943302"

    OY100 = "#feb27d"
    OY200 = "#fea364"
    OY300 = "#fe944a"
    OY400 = "#fe8531"
    OY500 = "#fb6801"
    OY600 = "#e25d01"
    OY700 = "#c85301"
    OY800 = "#af4801"
    OY900 = "#953e01"

    Y100 = "#ffd180"
    Y200 = "#ffc766"
    Y300 = "#ffbe4d"
    Y400 = "#ffb533"
    Y500 = "#ffa200"
    Y600 = "#e69200"
    Y700 = "#cc8200"
    Y800 = "#b37100"
    Y900 = "#996100"

    G100 = "#28ffab"
    G200 = "#06fc9c"
    G300 = "#03e68e"
    G400 = "#03cc7e"
    G500 = "#029a5f"
    G600 = "#02814f"
    G700 = "#016840"
    G800 = "#014e30"
    G900 = "#013521"

    B100 = "#9ec9f6"
    B200 = "#86bcf4"
    B300 = "#6fb0f2"
    B400 = "#58a3ef"
    B500 = "#2989eb"
    B600 = "#157ce5"
    B700 = "#1370ce"
    B800 = "#1163b6"
    B900 = "#0f569f"

    #   /* Bleu O7 */
    BM100 = "#1b76ff"
    BM200 = "#0167ff"
    BM300 = "#005de6"
    BM400 = "#0053cd"
    BM500 = "#003e9a"
    BM600 = "#003481"
    BM700 = "#002967"
    BM800 = "#001f4e"
    BM900 = "#001534"

    BD100 = "#0047de"
    BD200 = "#003fc4"
    BD300 = "#0036ab"
    BD400 = "#002e91"
    BD500 = "#001e5e"
    BD600 = "#001645"
    BD700 = "#000e2b"
    BD800 = "#000612"
    BD900 = "#000000"


class PdfColors:  # pylint: disable=too-few-public-methods
    """Color constants for PDFs"""

    @staticmethod
    def hex_to_rgb(hex_code):
        """Converts a color hex code to a dictionary with r, g, b values"""
        hex_code = hex_code.lstrip("#")
        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)
        return {"r": r, "g": g, "b": b}

    MAIN = hex_to_rgb(O7Colors.O500)
    ALT = hex_to_rgb(O7Colors.BM500)

    N900 = hex_to_rgb(O7Colors.N900)
    N800 = hex_to_rgb(O7Colors.N800)
    N700 = hex_to_rgb(O7Colors.N700)
    N600 = hex_to_rgb(O7Colors.N600)
    N500 = hex_to_rgb(O7Colors.N500)
    N400 = hex_to_rgb(O7Colors.N400)
    N300 = hex_to_rgb(O7Colors.N300)
    N200 = hex_to_rgb(O7Colors.N200)
    N100 = hex_to_rgb(O7Colors.N100)
    N90 = hex_to_rgb(O7Colors.N90)
    N80 = hex_to_rgb(O7Colors.N80)
    N70 = hex_to_rgb(O7Colors.N70)
    N60 = hex_to_rgb(O7Colors.N60)
    N50 = hex_to_rgb(O7Colors.N50)
    N40 = hex_to_rgb(O7Colors.N40)
    N30 = hex_to_rgb(O7Colors.N30)
    N20 = hex_to_rgb(O7Colors.N20)
    N10 = hex_to_rgb(O7Colors.N10)
    N0 = hex_to_rgb(O7Colors.N0)

    B100 = hex_to_rgb(O7Colors.B100)
    B200 = hex_to_rgb(O7Colors.B200)
    B300 = hex_to_rgb(O7Colors.B300)
    B400 = hex_to_rgb(O7Colors.B400)
    B500 = hex_to_rgb(O7Colors.B500)
    B600 = hex_to_rgb(O7Colors.B600)
    B700 = hex_to_rgb(O7Colors.B700)
    B800 = hex_to_rgb(O7Colors.B800)
    B900 = hex_to_rgb(O7Colors.B900)

    BM100 = hex_to_rgb(O7Colors.BM100)
    BM200 = hex_to_rgb(O7Colors.BM200)
    BM300 = hex_to_rgb(O7Colors.BM300)
    BM400 = hex_to_rgb(O7Colors.BM400)
    BM500 = hex_to_rgb(O7Colors.BM500)
    BM600 = hex_to_rgb(O7Colors.BM600)
    BM700 = hex_to_rgb(O7Colors.BM700)
    BM800 = hex_to_rgb(O7Colors.BM800)
    BM900 = hex_to_rgb(O7Colors.BM900)

    R100 = hex_to_rgb(O7Colors.R100)
    R200 = hex_to_rgb(O7Colors.R200)
    R300 = hex_to_rgb(O7Colors.R300)
    R400 = hex_to_rgb(O7Colors.R400)
    R500 = hex_to_rgb(O7Colors.R500)
    R600 = hex_to_rgb(O7Colors.R600)
    R700 = hex_to_rgb(O7Colors.R700)
    R800 = hex_to_rgb(O7Colors.R800)
    R900 = hex_to_rgb(O7Colors.R900)

    O100 = hex_to_rgb(O7Colors.O100)
    O200 = hex_to_rgb(O7Colors.O200)
    O300 = hex_to_rgb(O7Colors.O300)
    O400 = hex_to_rgb(O7Colors.O400)
    O500 = hex_to_rgb(O7Colors.O500)
    O600 = hex_to_rgb(O7Colors.O600)
    O700 = hex_to_rgb(O7Colors.O700)
    O800 = hex_to_rgb(O7Colors.O800)
    O900 = hex_to_rgb(O7Colors.O900)

    Y100 = hex_to_rgb(O7Colors.Y100)
    Y200 = hex_to_rgb(O7Colors.Y200)
    Y300 = hex_to_rgb(O7Colors.Y300)
    Y400 = hex_to_rgb(O7Colors.Y400)
    Y500 = hex_to_rgb(O7Colors.Y500)
    Y600 = hex_to_rgb(O7Colors.Y600)
    Y700 = hex_to_rgb(O7Colors.Y700)
    Y800 = hex_to_rgb(O7Colors.Y800)
    Y900 = hex_to_rgb(O7Colors.Y900)

    G100 = hex_to_rgb(O7Colors.G100)
    G200 = hex_to_rgb(O7Colors.G200)
    G300 = hex_to_rgb(O7Colors.G300)
    G400 = hex_to_rgb(O7Colors.G400)
    G500 = hex_to_rgb(O7Colors.G500)
    G600 = hex_to_rgb(O7Colors.G600)
    G700 = hex_to_rgb(O7Colors.G700)
    G800 = hex_to_rgb(O7Colors.G800)
    G900 = hex_to_rgb(O7Colors.G900)
