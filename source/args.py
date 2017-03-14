import argparse

import calc
import data
import log


DEBUG = None
RANGE = None
TARGET = None
FILE = None
LEEWAY_ALT = None
LEEWAY_HDG = None
ATTACK_HDG = None
BASE_DIST = None
BASE_ALT = None
TRACK_ALT = None
RELEASE_ALT = None
ABORT_ALT = None
MIN_ALT = None
AIM_DIST = None

def parse():
    global DEBUG
    global RANGE
    global TARGET
    global FILE
    global LEEWAY_ALT
    global LEEWAY_HDG
    global ATTACK_HDG
    global DECLUTTER
    global BASE_DIST
    global BASE_ALT
    global TRACK_ALT
    global RELEASE_ALT
    global ABORT_ALT
    global MIN_ALT
    global AIM_DIST

    parser = argparse.ArgumentParser(description="generate .xml files to visually render SLED attack profiles in the Tacview 3D environment", formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30))
    parser.add_argument("-v", "--version", action="version", version="0.10.0")

    parser.add_argument("range", type=str, help="the range containing the attacked target")
    parser.add_argument("target", type=str, help="the attacked target")

    optional_options = parser.add_argument_group("optional other parameters")
    optional_options.add_argument("-d", "--debug", action="store_true", help="show more exhaustive error messages")
    optional_options.add_argument("-fn", "--filename", type=str, help="name of the generated .xml file [default: \"sled\"]", metavar="str", default="sled")
    optional_options.add_argument("-la", "--leewayalt", type=_positive_int, help="available +/- leeway for the SLED's base, track, and release altitudes (in feet) [default: 200ft]", metavar="ft", default=200)
    optional_options.add_argument("-lh", "--leewayhdg", type=_angle, help="available +/- leeway for the range's attack heading at the SLED's base altitude (in degrees) [default: 10°]", metavar="°", default=10)
    optional_options.add_argument("-ah", "--attackhdg", type=_heading, help="required attack heading, overrides the range's default (in degrees)", metavar="°", default=None)
    optional_options.add_argument("-dc", "--declutter", action="store_true", help="declutter the target area by rendering the abort and minimum altitudes as planes")

    required_options = parser.add_argument_group("required SLED parametes")
    required_options.add_argument("-bd", "--basedist", type=_positive_int, help="base distance (in nautical miles)", metavar="nm", required=True)
    required_options.add_argument("-ba", "--basealt", type=_positive_float, help="base altitude (in feet MSL)", metavar="ft", required=True)
    required_options.add_argument("-ta", "--trackalt", type=_positive_float, help="track altitude (in feet MSL)", metavar="ft", required=True)
    required_options.add_argument("-ra", "--releasealt", type=_positive_float, help="release altitude (in feet MSL)", metavar="ft", required=True)
    required_options.add_argument("-aa", "--abortalt", type=_positive_float, help="abort altitude (in feet MSL)", metavar="ft", required=True)
    required_options.add_argument("-ma", "--minalt", type=_positive_float, help="minimum altitude (in feet MSL)", metavar="ft", required=True)
    required_options.add_argument("-ad", "--aimdist", type=_positive_float, help="aim-off distance (in feet)", metavar="ft", required=True)

    args = parser.parse_args()

    DEBUG = args.debug
    RANGE = args.range
    TARGET = args.target
    FILE = args.filename
    LEEWAY_ALT = args.leewayalt
    LEEWAY_HDG = args.leewayhdg
    ATTACK_HDG = args.attackhdg
    DECLUTTER = args.declutter
    BASE_DIST = args.basedist
    BASE_ALT = args.basealt
    TRACK_ALT = args.trackalt
    RELEASE_ALT = args.releasealt
    ABORT_ALT = args.abortalt
    MIN_ALT = args.minalt
    AIM_DIST = args.aimdist

def check_range():
    global RANGE

    ranges = data.load("data/ranges.yaml")

    found = False
    for item in ranges:
        if RANGE == item["name"]:
            RANGE = item
            found = True
            break

    if not found:
        log.fail("no such range \""+RANGE+"\"")
        raise Exception

def check_target():
    global TARGET

    ranges = data.load("data/ranges.yaml")

    found = False
    for item in RANGE["targets"]:
        if TARGET == item["name"]:
            TARGET = item
            found = True
            break

    if not found:
        log.fail("no such target \""+TARGET+"\" in range \""+RANGE["name"]+"\"")
        raise Exception

def convert():
    global LEEWAY_ALT
    global ATTACK_HDG
    global BASE_DIST
    global BASE_ALT
    global TRACK_ALT
    global RELEASE_ALT
    global ABORT_ALT
    global MIN_ALT
    global AIM_DIST

    LEEWAY_ALT = calc.ft_to_m(LEEWAY_ALT)
    if ATTACK_HDG is not None:
        ATTACK_HDG = calc.thdg_to_mhdg(ATTACK_HDG)
    BASE_DIST = calc.ft_to_m(BASE_DIST)
    BASE_ALT = calc.ft_to_m(BASE_ALT)
    TRACK_ALT = calc.ft_to_m(TRACK_ALT)
    RELEASE_ALT = calc.ft_to_m(RELEASE_ALT)
    ABORT_ALT = calc.ft_to_m(ABORT_ALT)
    MIN_ALT = calc.ft_to_m(MIN_ALT)
    AIM_DIST = calc.ft_to_m(AIM_DIST)

def _positive_int(value):
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("number must be positive")

    return number

def _positive_float(value):
    number = float(value)
    if number < 0:
        raise argparse.ArgumentTypeError("number must be positive")

    return number

def _heading(value):
    number = int(value)
    if number < 0 or number > 359:
        raise argparse.ArgumentTypeError("heading must be between 0° and 359°")

    return number

def _angle(value):
    number = int(value)
    if number < 0 or number > 45:
        raise argparse.ArgumentTypeError("entry leeway must be between 0° and 45°")

    return number
