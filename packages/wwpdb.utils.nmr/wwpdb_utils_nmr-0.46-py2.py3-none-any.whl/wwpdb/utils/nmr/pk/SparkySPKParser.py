# Generated from SparkySPKParser.g4 by ANTLR 4.13.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,150,599,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,
        7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,
        13,2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,1,
        0,1,0,1,0,1,0,1,0,4,0,46,8,0,11,0,12,0,47,1,0,1,0,1,1,1,1,5,1,54,
        8,1,10,1,12,1,57,9,1,1,1,1,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,
        1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,
        1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,99,8,2,1,
        2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,110,8,2,1,3,1,3,5,3,114,8,
        3,10,3,12,3,117,9,3,1,3,1,3,1,4,1,4,1,4,5,4,124,8,4,10,4,12,4,127,
        9,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,4,4,138,8,4,11,4,12,4,139,
        1,4,1,4,1,4,4,4,145,8,4,11,4,12,4,146,1,4,1,4,1,4,1,4,1,4,1,4,1,
        4,1,4,1,4,4,4,158,8,4,11,4,12,4,159,1,4,1,4,1,4,1,4,1,4,1,4,1,4,
        1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,
        5,4,185,8,4,10,4,12,4,188,9,4,1,4,1,4,1,4,4,4,193,8,4,11,4,12,4,
        194,1,4,1,4,1,4,4,4,200,8,4,11,4,12,4,201,1,4,1,4,1,4,1,4,1,4,1,
        4,1,4,1,4,1,4,4,4,213,8,4,11,4,12,4,214,1,4,1,4,1,4,4,4,220,8,4,
        11,4,12,4,221,1,4,1,4,1,4,4,4,227,8,4,11,4,12,4,228,1,4,1,4,1,4,
        1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,
        1,4,1,4,4,4,252,8,4,11,4,12,4,253,1,4,1,4,1,4,1,4,4,4,260,8,4,11,
        4,12,4,261,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,
        4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,
        4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,3,4,304,8,4,1,5,1,5,1,
        6,1,6,5,6,310,8,6,10,6,12,6,313,9,6,1,6,1,6,1,7,1,7,1,8,1,8,5,8,
        321,8,8,10,8,12,8,324,9,8,1,8,1,8,1,9,1,9,1,9,5,9,331,8,9,10,9,12,
        9,334,9,9,1,9,1,9,1,9,1,9,1,9,1,9,4,9,342,8,9,11,9,12,9,343,1,9,
        1,9,1,9,1,9,1,9,1,9,1,9,5,9,353,8,9,10,9,12,9,356,9,9,1,9,1,9,1,
        9,1,9,1,9,1,9,5,9,364,8,9,10,9,12,9,367,9,9,1,9,1,9,1,9,1,9,1,9,
        1,9,1,9,4,9,376,8,9,11,9,12,9,377,1,9,1,9,1,9,1,9,1,9,1,9,1,9,1,
        9,4,9,388,8,9,11,9,12,9,389,1,9,1,9,1,9,1,9,1,9,3,9,397,8,9,1,10,
        1,10,1,11,1,11,1,12,1,12,5,12,405,8,12,10,12,12,12,408,9,12,1,12,
        1,12,1,13,1,13,1,13,4,13,415,8,13,11,13,12,13,416,1,13,1,13,1,13,
        4,13,422,8,13,11,13,12,13,423,1,13,1,13,1,13,4,13,429,8,13,11,13,
        12,13,430,1,13,1,13,1,13,4,13,436,8,13,11,13,12,13,437,1,13,1,13,
        1,13,4,13,443,8,13,11,13,12,13,444,1,13,1,13,1,13,1,13,1,13,1,13,
        1,13,3,13,454,8,13,1,14,1,14,5,14,458,8,14,10,14,12,14,461,9,14,
        1,14,1,14,1,15,1,15,1,15,1,15,1,15,1,15,1,15,1,15,1,15,4,15,474,
        8,15,11,15,12,15,475,1,15,4,15,479,8,15,11,15,12,15,480,1,15,1,15,
        1,15,4,15,486,8,15,11,15,12,15,487,1,15,1,15,1,15,1,15,1,15,1,15,
        4,15,496,8,15,11,15,12,15,497,1,15,1,15,1,15,1,15,4,15,504,8,15,
        11,15,12,15,505,1,15,1,15,1,15,4,15,511,8,15,11,15,12,15,512,1,15,
        3,15,516,8,15,1,15,1,15,1,15,1,15,3,15,522,8,15,1,15,1,15,1,15,1,
        15,1,15,1,15,4,15,530,8,15,11,15,12,15,531,1,15,1,15,1,15,1,15,3,
        15,538,8,15,1,16,1,16,1,17,1,17,5,17,544,8,17,10,17,12,17,547,9,
        17,1,17,1,17,1,18,1,18,1,18,1,18,1,18,1,18,4,18,557,8,18,11,18,12,
        18,558,1,18,4,18,562,8,18,11,18,12,18,563,1,18,1,18,1,18,4,18,569,
        8,18,11,18,12,18,570,1,18,1,18,1,18,1,18,1,18,1,18,4,18,579,8,18,
        11,18,12,18,580,1,18,1,18,1,18,1,18,1,18,1,18,1,18,4,18,590,8,18,
        11,18,12,18,591,1,18,3,18,595,8,18,1,19,1,19,1,19,0,0,20,0,2,4,6,
        8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,0,7,2,0,20,20,26,
        26,1,0,74,77,1,0,94,97,1,0,94,96,1,0,128,129,1,0,142,144,1,0,146,
        147,712,0,45,1,0,0,0,2,51,1,0,0,0,4,109,1,0,0,0,6,111,1,0,0,0,8,
        303,1,0,0,0,10,305,1,0,0,0,12,307,1,0,0,0,14,316,1,0,0,0,16,318,
        1,0,0,0,18,396,1,0,0,0,20,398,1,0,0,0,22,400,1,0,0,0,24,402,1,0,
        0,0,26,453,1,0,0,0,28,455,1,0,0,0,30,537,1,0,0,0,32,539,1,0,0,0,
        34,541,1,0,0,0,36,594,1,0,0,0,38,596,1,0,0,0,40,41,5,1,0,0,41,42,
        5,2,0,0,42,43,3,2,1,0,43,44,3,6,3,0,44,46,1,0,0,0,45,40,1,0,0,0,
        46,47,1,0,0,0,47,45,1,0,0,0,47,48,1,0,0,0,48,49,1,0,0,0,49,50,5,
        0,0,1,50,1,1,0,0,0,51,55,5,3,0,0,52,54,3,4,2,0,53,52,1,0,0,0,54,
        57,1,0,0,0,55,53,1,0,0,0,55,56,1,0,0,0,56,58,1,0,0,0,57,55,1,0,0,
        0,58,59,5,10,0,0,59,3,1,0,0,0,60,110,5,28,0,0,61,62,5,11,0,0,62,
        63,5,12,0,0,63,64,5,24,0,0,64,110,5,28,0,0,65,66,5,11,0,0,66,67,
        5,13,0,0,67,68,5,24,0,0,68,110,5,28,0,0,69,70,5,11,0,0,70,71,5,14,
        0,0,71,72,5,24,0,0,72,110,5,28,0,0,73,74,5,11,0,0,74,75,5,15,0,0,
        75,76,5,24,0,0,76,110,5,28,0,0,77,78,5,11,0,0,78,79,5,16,0,0,79,
        80,5,24,0,0,80,110,5,28,0,0,81,82,5,11,0,0,82,83,5,17,0,0,83,84,
        5,24,0,0,84,110,5,28,0,0,85,86,5,11,0,0,86,87,5,18,0,0,87,88,5,24,
        0,0,88,110,5,28,0,0,89,90,5,19,0,0,90,91,5,20,0,0,91,92,5,21,0,0,
        92,93,7,0,0,0,93,110,5,28,0,0,94,95,5,19,0,0,95,96,5,20,0,0,96,98,
        5,22,0,0,97,99,5,26,0,0,98,97,1,0,0,0,98,99,1,0,0,0,99,100,1,0,0,
        0,100,110,5,28,0,0,101,102,5,19,0,0,102,103,5,20,0,0,103,104,5,23,
        0,0,104,105,5,24,0,0,105,106,5,24,0,0,106,107,5,25,0,0,107,108,5,
        25,0,0,108,110,5,28,0,0,109,60,1,0,0,0,109,61,1,0,0,0,109,65,1,0,
        0,0,109,69,1,0,0,0,109,73,1,0,0,0,109,77,1,0,0,0,109,81,1,0,0,0,
        109,85,1,0,0,0,109,89,1,0,0,0,109,94,1,0,0,0,109,101,1,0,0,0,110,
        5,1,0,0,0,111,115,5,4,0,0,112,114,3,8,4,0,113,112,1,0,0,0,114,117,
        1,0,0,0,115,113,1,0,0,0,115,116,1,0,0,0,116,118,1,0,0,0,117,115,
        1,0,0,0,118,119,5,32,0,0,119,7,1,0,0,0,120,304,5,79,0,0,121,125,
        5,33,0,0,122,124,3,10,5,0,123,122,1,0,0,0,124,127,1,0,0,0,125,123,
        1,0,0,0,125,126,1,0,0,0,126,128,1,0,0,0,127,125,1,0,0,0,128,304,
        5,79,0,0,129,130,5,34,0,0,130,131,5,77,0,0,131,304,5,79,0,0,132,
        133,5,35,0,0,133,134,5,74,0,0,134,304,5,79,0,0,135,137,5,36,0,0,
        136,138,5,75,0,0,137,136,1,0,0,0,138,139,1,0,0,0,139,137,1,0,0,0,
        139,140,1,0,0,0,140,141,1,0,0,0,141,304,5,79,0,0,142,144,5,37,0,
        0,143,145,5,74,0,0,144,143,1,0,0,0,145,146,1,0,0,0,146,144,1,0,0,
        0,146,147,1,0,0,0,147,148,1,0,0,0,148,304,5,79,0,0,149,150,5,38,
        0,0,150,151,5,74,0,0,151,304,5,79,0,0,152,153,5,39,0,0,153,154,5,
        75,0,0,154,304,5,79,0,0,155,157,5,40,0,0,156,158,5,74,0,0,157,156,
        1,0,0,0,158,159,1,0,0,0,159,157,1,0,0,0,159,160,1,0,0,0,160,161,
        1,0,0,0,161,304,5,79,0,0,162,163,5,41,0,0,163,164,5,74,0,0,164,165,
        5,75,0,0,165,304,5,79,0,0,166,167,5,42,0,0,167,168,5,73,0,0,168,
        304,5,79,0,0,169,170,5,43,0,0,170,171,5,44,0,0,171,172,5,76,0,0,
        172,304,5,79,0,0,173,174,5,43,0,0,174,175,5,45,0,0,175,176,5,76,
        0,0,176,304,5,79,0,0,177,178,5,43,0,0,178,179,5,46,0,0,179,180,5,
        76,0,0,180,304,5,79,0,0,181,182,5,43,0,0,182,186,5,47,0,0,183,185,
        5,76,0,0,184,183,1,0,0,0,185,188,1,0,0,0,186,184,1,0,0,0,186,187,
        1,0,0,0,187,189,1,0,0,0,188,186,1,0,0,0,189,304,5,79,0,0,190,192,
        5,48,0,0,191,193,5,75,0,0,192,191,1,0,0,0,193,194,1,0,0,0,194,192,
        1,0,0,0,194,195,1,0,0,0,195,196,1,0,0,0,196,304,5,79,0,0,197,199,
        5,49,0,0,198,200,5,74,0,0,199,198,1,0,0,0,200,201,1,0,0,0,201,199,
        1,0,0,0,201,202,1,0,0,0,202,203,1,0,0,0,203,304,5,79,0,0,204,205,
        5,50,0,0,205,206,5,74,0,0,206,304,5,79,0,0,207,208,5,51,0,0,208,
        209,5,74,0,0,209,304,5,79,0,0,210,212,5,52,0,0,211,213,5,75,0,0,
        212,211,1,0,0,0,213,214,1,0,0,0,214,212,1,0,0,0,214,215,1,0,0,0,
        215,216,1,0,0,0,216,304,5,79,0,0,217,219,5,53,0,0,218,220,5,75,0,
        0,219,218,1,0,0,0,220,221,1,0,0,0,221,219,1,0,0,0,221,222,1,0,0,
        0,222,223,1,0,0,0,223,304,5,79,0,0,224,226,5,54,0,0,225,227,5,75,
        0,0,226,225,1,0,0,0,227,228,1,0,0,0,228,226,1,0,0,0,228,229,1,0,
        0,0,229,230,1,0,0,0,230,304,5,79,0,0,231,232,5,55,0,0,232,233,5,
        74,0,0,233,304,5,79,0,0,234,235,5,56,0,0,235,236,5,74,0,0,236,304,
        5,79,0,0,237,238,5,57,0,0,238,239,5,74,0,0,239,304,5,79,0,0,240,
        241,5,58,0,0,241,242,5,74,0,0,242,304,5,79,0,0,243,244,5,59,0,0,
        244,245,5,74,0,0,245,304,5,79,0,0,246,247,5,60,0,0,247,248,5,75,
        0,0,248,304,5,79,0,0,249,251,5,61,0,0,250,252,5,75,0,0,251,250,1,
        0,0,0,252,253,1,0,0,0,253,251,1,0,0,0,253,254,1,0,0,0,254,255,1,
        0,0,0,255,256,5,74,0,0,256,304,5,79,0,0,257,259,5,62,0,0,258,260,
        5,75,0,0,259,258,1,0,0,0,260,261,1,0,0,0,261,259,1,0,0,0,261,262,
        1,0,0,0,262,263,1,0,0,0,263,304,5,79,0,0,264,265,5,63,0,0,265,266,
        5,75,0,0,266,304,5,79,0,0,267,268,5,64,0,0,268,269,5,75,0,0,269,
        304,5,79,0,0,270,271,5,65,0,0,271,272,5,75,0,0,272,304,5,79,0,0,
        273,274,5,66,0,0,274,275,5,75,0,0,275,304,5,79,0,0,276,277,5,67,
        0,0,277,278,5,75,0,0,278,304,5,79,0,0,279,280,5,68,0,0,280,281,5,
        75,0,0,281,304,5,79,0,0,282,283,5,69,0,0,283,284,5,75,0,0,284,304,
        5,79,0,0,285,286,5,70,0,0,286,287,5,75,0,0,287,304,5,79,0,0,288,
        289,5,71,0,0,289,290,5,75,0,0,290,304,5,79,0,0,291,292,5,72,0,0,
        292,293,5,75,0,0,293,304,5,79,0,0,294,295,3,12,6,0,295,296,5,79,
        0,0,296,304,1,0,0,0,297,298,3,16,8,0,298,299,5,79,0,0,299,304,1,
        0,0,0,300,301,3,28,14,0,301,302,5,79,0,0,302,304,1,0,0,0,303,120,
        1,0,0,0,303,121,1,0,0,0,303,129,1,0,0,0,303,132,1,0,0,0,303,135,
        1,0,0,0,303,142,1,0,0,0,303,149,1,0,0,0,303,152,1,0,0,0,303,155,
        1,0,0,0,303,162,1,0,0,0,303,166,1,0,0,0,303,169,1,0,0,0,303,173,
        1,0,0,0,303,177,1,0,0,0,303,181,1,0,0,0,303,190,1,0,0,0,303,197,
        1,0,0,0,303,204,1,0,0,0,303,207,1,0,0,0,303,210,1,0,0,0,303,217,
        1,0,0,0,303,224,1,0,0,0,303,231,1,0,0,0,303,234,1,0,0,0,303,237,
        1,0,0,0,303,240,1,0,0,0,303,243,1,0,0,0,303,246,1,0,0,0,303,249,
        1,0,0,0,303,257,1,0,0,0,303,264,1,0,0,0,303,267,1,0,0,0,303,270,
        1,0,0,0,303,273,1,0,0,0,303,276,1,0,0,0,303,279,1,0,0,0,303,282,
        1,0,0,0,303,285,1,0,0,0,303,288,1,0,0,0,303,291,1,0,0,0,303,294,
        1,0,0,0,303,297,1,0,0,0,303,300,1,0,0,0,304,9,1,0,0,0,305,306,7,
        1,0,0,306,11,1,0,0,0,307,311,5,29,0,0,308,310,3,14,7,0,309,308,1,
        0,0,0,310,313,1,0,0,0,311,309,1,0,0,0,311,312,1,0,0,0,312,314,1,
        0,0,0,313,311,1,0,0,0,314,315,5,80,0,0,315,13,1,0,0,0,316,317,5,
        81,0,0,317,15,1,0,0,0,318,322,5,30,0,0,319,321,3,18,9,0,320,319,
        1,0,0,0,321,324,1,0,0,0,322,320,1,0,0,0,322,323,1,0,0,0,323,325,
        1,0,0,0,324,322,1,0,0,0,325,326,5,84,0,0,326,17,1,0,0,0,327,397,
        5,99,0,0,328,332,5,85,0,0,329,331,3,20,10,0,330,329,1,0,0,0,331,
        334,1,0,0,0,332,330,1,0,0,0,332,333,1,0,0,0,333,335,1,0,0,0,334,
        332,1,0,0,0,335,397,5,99,0,0,336,337,5,86,0,0,337,338,5,94,0,0,338,
        397,5,99,0,0,339,341,5,87,0,0,340,342,5,94,0,0,341,340,1,0,0,0,342,
        343,1,0,0,0,343,341,1,0,0,0,343,344,1,0,0,0,344,345,1,0,0,0,345,
        397,5,99,0,0,346,347,5,88,0,0,347,348,5,94,0,0,348,397,5,99,0,0,
        349,350,5,89,0,0,350,354,5,94,0,0,351,353,5,97,0,0,352,351,1,0,0,
        0,353,356,1,0,0,0,354,352,1,0,0,0,354,355,1,0,0,0,355,357,1,0,0,
        0,356,354,1,0,0,0,357,397,5,99,0,0,358,359,5,90,0,0,359,360,5,94,
        0,0,360,397,5,99,0,0,361,365,5,91,0,0,362,364,5,97,0,0,363,362,1,
        0,0,0,364,367,1,0,0,0,365,363,1,0,0,0,365,366,1,0,0,0,366,368,1,
        0,0,0,367,365,1,0,0,0,368,397,5,99,0,0,369,370,5,92,0,0,370,371,
        5,94,0,0,371,372,3,22,11,0,372,373,5,95,0,0,373,375,5,95,0,0,374,
        376,5,97,0,0,375,374,1,0,0,0,376,377,1,0,0,0,377,375,1,0,0,0,377,
        378,1,0,0,0,378,379,1,0,0,0,379,380,5,99,0,0,380,397,1,0,0,0,381,
        382,5,93,0,0,382,383,5,94,0,0,383,384,3,22,11,0,384,385,5,95,0,0,
        385,387,5,95,0,0,386,388,5,97,0,0,387,386,1,0,0,0,388,389,1,0,0,
        0,389,387,1,0,0,0,389,390,1,0,0,0,390,391,1,0,0,0,391,392,5,99,0,
        0,392,397,1,0,0,0,393,394,3,24,12,0,394,395,5,99,0,0,395,397,1,0,
        0,0,396,327,1,0,0,0,396,328,1,0,0,0,396,336,1,0,0,0,396,339,1,0,
        0,0,396,346,1,0,0,0,396,349,1,0,0,0,396,358,1,0,0,0,396,361,1,0,
        0,0,396,369,1,0,0,0,396,381,1,0,0,0,396,393,1,0,0,0,397,19,1,0,0,
        0,398,399,7,2,0,0,399,21,1,0,0,0,400,401,7,3,0,0,401,23,1,0,0,0,
        402,406,5,83,0,0,403,405,3,26,13,0,404,403,1,0,0,0,405,408,1,0,0,
        0,406,404,1,0,0,0,406,407,1,0,0,0,407,409,1,0,0,0,408,406,1,0,0,
        0,409,410,5,100,0,0,410,25,1,0,0,0,411,454,5,112,0,0,412,414,5,101,
        0,0,413,415,5,108,0,0,414,413,1,0,0,0,415,416,1,0,0,0,416,414,1,
        0,0,0,416,417,1,0,0,0,417,418,1,0,0,0,418,454,5,112,0,0,419,421,
        5,102,0,0,420,422,5,108,0,0,421,420,1,0,0,0,422,423,1,0,0,0,423,
        421,1,0,0,0,423,424,1,0,0,0,424,425,1,0,0,0,425,454,5,112,0,0,426,
        428,5,103,0,0,427,429,5,108,0,0,428,427,1,0,0,0,429,430,1,0,0,0,
        430,428,1,0,0,0,430,431,1,0,0,0,431,432,1,0,0,0,432,454,5,112,0,
        0,433,435,5,104,0,0,434,436,5,109,0,0,435,434,1,0,0,0,436,437,1,
        0,0,0,437,435,1,0,0,0,437,438,1,0,0,0,438,439,1,0,0,0,439,454,5,
        112,0,0,440,442,5,105,0,0,441,443,5,109,0,0,442,441,1,0,0,0,443,
        444,1,0,0,0,444,442,1,0,0,0,444,445,1,0,0,0,445,446,1,0,0,0,446,
        454,5,112,0,0,447,448,5,106,0,0,448,449,5,109,0,0,449,454,5,112,
        0,0,450,451,5,107,0,0,451,452,5,108,0,0,452,454,5,112,0,0,453,411,
        1,0,0,0,453,412,1,0,0,0,453,419,1,0,0,0,453,426,1,0,0,0,453,433,
        1,0,0,0,453,440,1,0,0,0,453,447,1,0,0,0,453,450,1,0,0,0,454,27,1,
        0,0,0,455,459,5,31,0,0,456,458,3,30,15,0,457,456,1,0,0,0,458,461,
        1,0,0,0,459,457,1,0,0,0,459,460,1,0,0,0,460,462,1,0,0,0,461,459,
        1,0,0,0,462,463,5,114,0,0,463,29,1,0,0,0,464,538,5,133,0,0,465,466,
        5,115,0,0,466,467,5,116,0,0,467,538,5,133,0,0,468,469,5,115,0,0,
        469,470,5,117,0,0,470,538,5,133,0,0,471,473,5,118,0,0,472,474,5,
        128,0,0,473,472,1,0,0,0,474,475,1,0,0,0,475,473,1,0,0,0,475,476,
        1,0,0,0,476,478,1,0,0,0,477,479,5,131,0,0,478,477,1,0,0,0,479,480,
        1,0,0,0,480,478,1,0,0,0,480,481,1,0,0,0,481,482,1,0,0,0,482,538,
        5,133,0,0,483,485,5,119,0,0,484,486,5,128,0,0,485,484,1,0,0,0,486,
        487,1,0,0,0,487,485,1,0,0,0,487,488,1,0,0,0,488,489,1,0,0,0,489,
        538,5,133,0,0,490,491,5,120,0,0,491,492,5,128,0,0,492,538,5,133,
        0,0,493,495,5,121,0,0,494,496,3,32,16,0,495,494,1,0,0,0,496,497,
        1,0,0,0,497,495,1,0,0,0,497,498,1,0,0,0,498,499,1,0,0,0,499,500,
        5,133,0,0,500,538,1,0,0,0,501,503,5,122,0,0,502,504,5,129,0,0,503,
        502,1,0,0,0,504,505,1,0,0,0,505,503,1,0,0,0,505,506,1,0,0,0,506,
        507,1,0,0,0,507,538,5,133,0,0,508,510,5,123,0,0,509,511,5,129,0,
        0,510,509,1,0,0,0,511,512,1,0,0,0,512,510,1,0,0,0,512,513,1,0,0,
        0,513,515,1,0,0,0,514,516,5,131,0,0,515,514,1,0,0,0,515,516,1,0,
        0,0,516,517,1,0,0,0,517,538,5,133,0,0,518,519,5,124,0,0,519,521,
        5,130,0,0,520,522,5,131,0,0,521,520,1,0,0,0,521,522,1,0,0,0,522,
        523,1,0,0,0,523,538,5,133,0,0,524,525,5,125,0,0,525,526,5,129,0,
        0,526,538,5,133,0,0,527,529,5,126,0,0,528,530,5,127,0,0,529,528,
        1,0,0,0,530,531,1,0,0,0,531,529,1,0,0,0,531,532,1,0,0,0,532,533,
        1,0,0,0,533,538,5,133,0,0,534,535,3,34,17,0,535,536,5,133,0,0,536,
        538,1,0,0,0,537,464,1,0,0,0,537,465,1,0,0,0,537,468,1,0,0,0,537,
        471,1,0,0,0,537,483,1,0,0,0,537,490,1,0,0,0,537,493,1,0,0,0,537,
        501,1,0,0,0,537,508,1,0,0,0,537,518,1,0,0,0,537,524,1,0,0,0,537,
        527,1,0,0,0,537,534,1,0,0,0,538,31,1,0,0,0,539,540,7,4,0,0,540,33,
        1,0,0,0,541,545,5,113,0,0,542,544,3,36,18,0,543,542,1,0,0,0,544,
        547,1,0,0,0,545,543,1,0,0,0,545,546,1,0,0,0,546,548,1,0,0,0,547,
        545,1,0,0,0,548,549,5,134,0,0,549,35,1,0,0,0,550,595,5,150,0,0,551,
        552,5,135,0,0,552,553,5,136,0,0,553,595,5,150,0,0,554,556,5,137,
        0,0,555,557,5,146,0,0,556,555,1,0,0,0,557,558,1,0,0,0,558,556,1,
        0,0,0,558,559,1,0,0,0,559,561,1,0,0,0,560,562,5,148,0,0,561,560,
        1,0,0,0,562,563,1,0,0,0,563,561,1,0,0,0,563,564,1,0,0,0,564,565,
        1,0,0,0,565,595,5,150,0,0,566,568,5,138,0,0,567,569,5,146,0,0,568,
        567,1,0,0,0,569,570,1,0,0,0,570,568,1,0,0,0,570,571,1,0,0,0,571,
        572,1,0,0,0,572,595,5,150,0,0,573,574,5,139,0,0,574,575,5,146,0,
        0,575,595,5,150,0,0,576,578,5,140,0,0,577,579,3,38,19,0,578,577,
        1,0,0,0,579,580,1,0,0,0,580,578,1,0,0,0,580,581,1,0,0,0,581,582,
        1,0,0,0,582,583,5,150,0,0,583,595,1,0,0,0,584,585,5,136,0,0,585,
        586,7,5,0,0,586,595,5,150,0,0,587,589,5,141,0,0,588,590,5,145,0,
        0,589,588,1,0,0,0,590,591,1,0,0,0,591,589,1,0,0,0,591,592,1,0,0,
        0,592,593,1,0,0,0,593,595,5,150,0,0,594,550,1,0,0,0,594,551,1,0,
        0,0,594,554,1,0,0,0,594,566,1,0,0,0,594,573,1,0,0,0,594,576,1,0,
        0,0,594,584,1,0,0,0,594,587,1,0,0,0,595,37,1,0,0,0,596,597,7,6,0,
        0,597,39,1,0,0,0,52,47,55,98,109,115,125,139,146,159,186,194,201,
        214,221,228,253,261,303,311,322,332,343,354,365,377,389,396,406,
        416,423,430,437,444,453,459,475,480,487,497,505,512,515,521,531,
        537,545,558,563,570,580,591,594
    ]

class SparkySPKParser ( Parser ):

    grammarFileName = "SparkySPKParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'<sparky save file>'", "<INVALID>", "'<user>'", 
                     "'<spectrum>'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'<end user>'", "'set'", 
                     "<INVALID>", "'saveprompt'", "'saveinterval'", "'resizeViews'", 
                     "'keytimeout'", "'cachesize'", "'contourgraying'", 
                     "'default'", "'print'", "'command'", "'file'", "'options'", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'<attached data>'", "'<view>'", "'<ornament>'", 
                     "'<end spectrum>'", "<INVALID>", "'pathname'", "'dimension'", 
                     "'shift'", "'points'", "'assignMultiAxisGuess'", "'assignGuessThreshold'", 
                     "'assignRelation'", "'assignRange'", "'assignFormat'", 
                     "'listTool'", "'sortBy'", "'nameType'", "'sortAxis'", 
                     "'showFlags'", "'integrate.overlapped_sep'", "'integrate.methods'", 
                     "'integrate.allow_motion'", "'integrate.adjust_linewidths'", 
                     "'integrate.motion_range'", "'integrate.min_linewidth'", 
                     "'integrate.max_linewidth'", "'integrate.fit_baseline'", 
                     "'integrate.subtract_peaks'", "'integrate.contoured_data'", 
                     "'integrate.rectangle_data'", "'integrate.maxiterations'", 
                     "'integrate.tolerance'", "'peak.pick'", "'peak.pick-minimum-linewidth'", 
                     "'peak.pick-minimum-dropoff'", "'noise.sigma'", "'ornament.label.size'", 
                     "'ornament.line.size'", "'ornament.peak.size'", "'ornament.grid.size'", 
                     "'ornament.peakgroup.size'", "'ornament.selectsize'", 
                     "'ornament.pointersize'", "'ornament.lineendsize'", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'<end attached data>'", 
                     "<INVALID>", "<INVALID>", "'<params>'", "'<end view>'", 
                     "<INVALID>", "'precision'", "'precision_by_units'", 
                     "'viewmode'", "'show'", "'axistype'", "<INVALID>", 
                     "'contour.pos'", "'contour.neg'", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'<end params>'", "'orientation'", "'location'", "'size'", 
                     "'offset'", "'scale'", "'zoom'", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'['", "'<end ornament>'", "<INVALID>", "'peak'", "'grid'", 
                     "<INVALID>", "<INVALID>", "'id'", "<INVALID>", "'height'", 
                     "'linewidth'", "'integral'", "'fr'", "'rs'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "']'", "<INVALID>", "'label'", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'xy'" ]

    symbolicNames = [ "<INVALID>", "Sparky_save_file", "Version", "User", 
                      "Spectrum", "Integer", "Float", "Real", "Simple_name", 
                      "SPACE", "End_user", "Set", "Mode_US", "Save_prompt", 
                      "Save_interval", "Resize_views", "Key_timeout", "Cache_size", 
                      "Contour_graying", "Default", "Print", "Command", 
                      "File", "Options", "Integer_US", "Float_US", "Simple_name_US", 
                      "SPACE_US", "RETURN_US", "Attached_data", "View", 
                      "Ornament", "End_spectrum", "Name_SP", "Path_name", 
                      "Dimension", "Shift", "Points", "Assign_multi_axis_guess", 
                      "Assign_guess_threshhold", "Assign_relation", "Assign_range", 
                      "Assign_format", "List_tool", "Sort_by", "Name_type", 
                      "Sort_axis", "Show_flags", "Integrate_overlapped_sep", 
                      "Integrate_methods", "Integrate_allow_motion", "Integrate_adjust_linewidths", 
                      "Integrate_motion_range", "Integrate_min_linewidth", 
                      "Integrate_max_linewidth", "Integrate_fit_baseline", 
                      "Integrate_subtract_peaks", "Integrate_contoured_data", 
                      "Integrate_rectangle_data", "Integrate_max_iterations", 
                      "Integrate_tolerance", "Peak_pick", "Peak_pick_minimum_linewidth", 
                      "Peak_pick_minimum_dropoff", "Noise_sigma", "Ornament_labe_size", 
                      "Ornament_line_size", "Ornament_peak_size", "Ornament_grid_size", 
                      "Ornament_peak_group_size", "Ornament_select_size", 
                      "Ornament_pointer_size", "Ornament_line_end_size", 
                      "Format_ex", "Integer_SP", "Float_SP", "Simple_name_SP", 
                      "Any_name_SP", "SPACE_SP", "RETURN_SP", "End_attached_data", 
                      "Any_name_AD", "SPACE_AD", "Params", "End_view", "Name_VI", 
                      "Precision", "Precision_by_units", "View_mode", "Show", 
                      "Axis_type", "Flags_VI", "Contour_pos", "Contour_neg", 
                      "Integer_VI", "Float_VI", "Real_VI", "Simple_name_VI", 
                      "SPACE_VI", "RETURN_VI", "End_params", "Orientation", 
                      "Location", "Size", "Offset", "Scale", "Zoom", "Flags_PA", 
                      "Integer_PA", "Float_PA", "Simple_name_PA", "SPACE_PA", 
                      "RETURN_PA", "L_brakt", "End_ornament", "Type_OR", 
                      "Peak", "Grid", "Color_OR", "Flags_OR", "Id", "Pos_OR", 
                      "Height", "Line_width", "Integral", "Fr", "Rs", "Rs_ex", 
                      "Integer_OR", "Float_OR", "Real_OR", "Simple_name_OR", 
                      "SPACE_OR", "RETURN_OR", "R_brakt", "Type_LA", "Label", 
                      "Color_LA", "Flags_LA", "Mode_LA", "Pos_LA", "Xy", 
                      "Assignment_2d_ex", "Assignment_3d_ex", "Assignment_4d_ex", 
                      "Xy_pos", "Integer_LA", "Float_LA", "Simple_name_LA", 
                      "SPACE_LA", "RETURN_LA" ]

    RULE_sparky_spk = 0
    RULE_user_block = 1
    RULE_user_statement = 2
    RULE_spectrum_block = 3
    RULE_spectrum_statement = 4
    RULE_spectrum_name = 5
    RULE_attached_data = 6
    RULE_attached_data_statement = 7
    RULE_view = 8
    RULE_view_statement = 9
    RULE_view_name = 10
    RULE_view_number = 11
    RULE_params = 12
    RULE_params_statement = 13
    RULE_ornament = 14
    RULE_ornament_statement = 15
    RULE_ornament_position = 16
    RULE_label = 17
    RULE_label_statement = 18
    RULE_label_position = 19

    ruleNames =  [ "sparky_spk", "user_block", "user_statement", "spectrum_block", 
                   "spectrum_statement", "spectrum_name", "attached_data", 
                   "attached_data_statement", "view", "view_statement", 
                   "view_name", "view_number", "params", "params_statement", 
                   "ornament", "ornament_statement", "ornament_position", 
                   "label", "label_statement", "label_position" ]

    EOF = Token.EOF
    Sparky_save_file=1
    Version=2
    User=3
    Spectrum=4
    Integer=5
    Float=6
    Real=7
    Simple_name=8
    SPACE=9
    End_user=10
    Set=11
    Mode_US=12
    Save_prompt=13
    Save_interval=14
    Resize_views=15
    Key_timeout=16
    Cache_size=17
    Contour_graying=18
    Default=19
    Print=20
    Command=21
    File=22
    Options=23
    Integer_US=24
    Float_US=25
    Simple_name_US=26
    SPACE_US=27
    RETURN_US=28
    Attached_data=29
    View=30
    Ornament=31
    End_spectrum=32
    Name_SP=33
    Path_name=34
    Dimension=35
    Shift=36
    Points=37
    Assign_multi_axis_guess=38
    Assign_guess_threshhold=39
    Assign_relation=40
    Assign_range=41
    Assign_format=42
    List_tool=43
    Sort_by=44
    Name_type=45
    Sort_axis=46
    Show_flags=47
    Integrate_overlapped_sep=48
    Integrate_methods=49
    Integrate_allow_motion=50
    Integrate_adjust_linewidths=51
    Integrate_motion_range=52
    Integrate_min_linewidth=53
    Integrate_max_linewidth=54
    Integrate_fit_baseline=55
    Integrate_subtract_peaks=56
    Integrate_contoured_data=57
    Integrate_rectangle_data=58
    Integrate_max_iterations=59
    Integrate_tolerance=60
    Peak_pick=61
    Peak_pick_minimum_linewidth=62
    Peak_pick_minimum_dropoff=63
    Noise_sigma=64
    Ornament_labe_size=65
    Ornament_line_size=66
    Ornament_peak_size=67
    Ornament_grid_size=68
    Ornament_peak_group_size=69
    Ornament_select_size=70
    Ornament_pointer_size=71
    Ornament_line_end_size=72
    Format_ex=73
    Integer_SP=74
    Float_SP=75
    Simple_name_SP=76
    Any_name_SP=77
    SPACE_SP=78
    RETURN_SP=79
    End_attached_data=80
    Any_name_AD=81
    SPACE_AD=82
    Params=83
    End_view=84
    Name_VI=85
    Precision=86
    Precision_by_units=87
    View_mode=88
    Show=89
    Axis_type=90
    Flags_VI=91
    Contour_pos=92
    Contour_neg=93
    Integer_VI=94
    Float_VI=95
    Real_VI=96
    Simple_name_VI=97
    SPACE_VI=98
    RETURN_VI=99
    End_params=100
    Orientation=101
    Location=102
    Size=103
    Offset=104
    Scale=105
    Zoom=106
    Flags_PA=107
    Integer_PA=108
    Float_PA=109
    Simple_name_PA=110
    SPACE_PA=111
    RETURN_PA=112
    L_brakt=113
    End_ornament=114
    Type_OR=115
    Peak=116
    Grid=117
    Color_OR=118
    Flags_OR=119
    Id=120
    Pos_OR=121
    Height=122
    Line_width=123
    Integral=124
    Fr=125
    Rs=126
    Rs_ex=127
    Integer_OR=128
    Float_OR=129
    Real_OR=130
    Simple_name_OR=131
    SPACE_OR=132
    RETURN_OR=133
    R_brakt=134
    Type_LA=135
    Label=136
    Color_LA=137
    Flags_LA=138
    Mode_LA=139
    Pos_LA=140
    Xy=141
    Assignment_2d_ex=142
    Assignment_3d_ex=143
    Assignment_4d_ex=144
    Xy_pos=145
    Integer_LA=146
    Float_LA=147
    Simple_name_LA=148
    SPACE_LA=149
    RETURN_LA=150

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Sparky_spkContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(SparkySPKParser.EOF, 0)

        def Sparky_save_file(self, i:int=None):
            if i is None:
                return self.getTokens(SparkySPKParser.Sparky_save_file)
            else:
                return self.getToken(SparkySPKParser.Sparky_save_file, i)

        def Version(self, i:int=None):
            if i is None:
                return self.getTokens(SparkySPKParser.Version)
            else:
                return self.getToken(SparkySPKParser.Version, i)

        def user_block(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SparkySPKParser.User_blockContext)
            else:
                return self.getTypedRuleContext(SparkySPKParser.User_blockContext,i)


        def spectrum_block(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SparkySPKParser.Spectrum_blockContext)
            else:
                return self.getTypedRuleContext(SparkySPKParser.Spectrum_blockContext,i)


        def getRuleIndex(self):
            return SparkySPKParser.RULE_sparky_spk

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSparky_spk" ):
                listener.enterSparky_spk(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSparky_spk" ):
                listener.exitSparky_spk(self)




    def sparky_spk(self):

        localctx = SparkySPKParser.Sparky_spkContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_sparky_spk)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 45 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 40
                self.match(SparkySPKParser.Sparky_save_file)
                self.state = 41
                self.match(SparkySPKParser.Version)
                self.state = 42
                self.user_block()
                self.state = 43
                self.spectrum_block()
                self.state = 47 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1):
                    break

            self.state = 49
            self.match(SparkySPKParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class User_blockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def User(self):
            return self.getToken(SparkySPKParser.User, 0)

        def End_user(self):
            return self.getToken(SparkySPKParser.End_user, 0)

        def user_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SparkySPKParser.User_statementContext)
            else:
                return self.getTypedRuleContext(SparkySPKParser.User_statementContext,i)


        def getRuleIndex(self):
            return SparkySPKParser.RULE_user_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUser_block" ):
                listener.enterUser_block(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUser_block" ):
                listener.exitUser_block(self)




    def user_block(self):

        localctx = SparkySPKParser.User_blockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_user_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 51
            self.match(SparkySPKParser.User)
            self.state = 55
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 268961792) != 0):
                self.state = 52
                self.user_statement()
                self.state = 57
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 58
            self.match(SparkySPKParser.End_user)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class User_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETURN_US(self):
            return self.getToken(SparkySPKParser.RETURN_US, 0)

        def Set(self):
            return self.getToken(SparkySPKParser.Set, 0)

        def Mode_US(self):
            return self.getToken(SparkySPKParser.Mode_US, 0)

        def Integer_US(self, i:int=None):
            if i is None:
                return self.getTokens(SparkySPKParser.Integer_US)
            else:
                return self.getToken(SparkySPKParser.Integer_US, i)

        def Save_prompt(self):
            return self.getToken(SparkySPKParser.Save_prompt, 0)

        def Save_interval(self):
            return self.getToken(SparkySPKParser.Save_interval, 0)

        def Resize_views(self):
            return self.getToken(SparkySPKParser.Resize_views, 0)

        def Key_timeout(self):
            return self.getToken(SparkySPKParser.Key_timeout, 0)

        def Cache_size(self):
            return self.getToken(SparkySPKParser.Cache_size, 0)

        def Contour_graying(self):
            return self.getToken(SparkySPKParser.Contour_graying, 0)

        def Default(self):
            return self.getToken(SparkySPKParser.Default, 0)

        def Print(self, i:int=None):
            if i is None:
                return self.getTokens(SparkySPKParser.Print)
            else:
                return self.getToken(SparkySPKParser.Print, i)

        def Command(self):
            return self.getToken(SparkySPKParser.Command, 0)

        def Simple_name_US(self):
            return self.getToken(SparkySPKParser.Simple_name_US, 0)

        def File(self):
            return self.getToken(SparkySPKParser.File, 0)

        def Options(self):
            return self.getToken(SparkySPKParser.Options, 0)

        def Float_US(self, i:int=None):
            if i is None:
                return self.getTokens(SparkySPKParser.Float_US)
            else:
                return self.getToken(SparkySPKParser.Float_US, i)

        def getRuleIndex(self):
            return SparkySPKParser.RULE_user_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUser_statement" ):
                listener.enterUser_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUser_statement" ):
                listener.exitUser_statement(self)




    def user_statement(self):

        localctx = SparkySPKParser.User_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_user_statement)
        self._la = 0 # Token type
        try:
            self.state = 109
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 60
                self.match(SparkySPKParser.RETURN_US)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 61
                self.match(SparkySPKParser.Set)
                self.state = 62
                self.match(SparkySPKParser.Mode_US)
                self.state = 63
                self.match(SparkySPKParser.Integer_US)
                self.state = 64
                self.match(SparkySPKParser.RETURN_US)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 65
                self.match(SparkySPKParser.Set)
                self.state = 66
                self.match(SparkySPKParser.Save_prompt)
                self.state = 67
                self.match(SparkySPKParser.Integer_US)
                self.state = 68
                self.match(SparkySPKParser.RETURN_US)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 69
                self.match(SparkySPKParser.Set)
                self.state = 70
                self.match(SparkySPKParser.Save_interval)
                self.state = 71
                self.match(SparkySPKParser.Integer_US)
                self.state = 72
                self.match(SparkySPKParser.RETURN_US)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 73
                self.match(SparkySPKParser.Set)
                self.state = 74
                self.match(SparkySPKParser.Resize_views)
                self.state = 75
                self.match(SparkySPKParser.Integer_US)
                self.state = 76
                self.match(SparkySPKParser.RETURN_US)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 77
                self.match(SparkySPKParser.Set)
                self.state = 78
                self.match(SparkySPKParser.Key_timeout)
                self.state = 79
                self.match(SparkySPKParser.Integer_US)
                self.state = 80
                self.match(SparkySPKParser.RETURN_US)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 81
                self.match(SparkySPKParser.Set)
                self.state = 82
                self.match(SparkySPKParser.Cache_size)
                self.state = 83
                self.match(SparkySPKParser.Integer_US)
                self.state = 84
                self.match(SparkySPKParser.RETURN_US)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 85
                self.match(SparkySPKParser.Set)
                self.state = 86
                self.match(SparkySPKParser.Contour_graying)
                self.state = 87
                self.match(SparkySPKParser.Integer_US)
                self.state = 88
                self.match(SparkySPKParser.RETURN_US)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 89
                self.match(SparkySPKParser.Default)
                self.state = 90
                self.match(SparkySPKParser.Print)
                self.state = 91
                self.match(SparkySPKParser.Command)
                self.state = 92
                _la = self._input.LA(1)
                if not(_la==20 or _la==26):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 93
                self.match(SparkySPKParser.RETURN_US)
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 94
                self.match(SparkySPKParser.Default)
                self.state = 95
                self.match(SparkySPKParser.Print)
                self.state = 96
                self.match(SparkySPKParser.File)
                self.state = 98
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==26:
                    self.state = 97
                    self.match(SparkySPKParser.Simple_name_US)


                self.state = 100
                self.match(SparkySPKParser.RETURN_US)
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 101
                self.match(SparkySPKParser.Default)
                self.state = 102
                self.match(SparkySPKParser.Print)
                self.state = 103
                self.match(SparkySPKParser.Options)
                self.state = 104
                self.match(SparkySPKParser.Integer_US)
                self.state = 105
                self.match(SparkySPKParser.Integer_US)
                self.state = 106
                self.match(SparkySPKParser.Float_US)
                self.state = 107
                self.match(SparkySPKParser.Float_US)
                self.state = 108
                self.match(SparkySPKParser.RETURN_US)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Spectrum_blockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Spectrum(self):
            return self.getToken(SparkySPKParser.Spectrum, 0)

        def End_spectrum(self):
            return self.getToken(SparkySPKParser.End_spectrum, 0)

        def spectrum_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SparkySPKParser.Spectrum_statementContext)
            else:
                return self.getTypedRuleContext(SparkySPKParser.Spectrum_statementContext,i)


        def getRuleIndex(self):
            return SparkySPKParser.RULE_spectrum_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSpectrum_block" ):
                listener.enterSpectrum_block(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSpectrum_block" ):
                listener.exitSpectrum_block(self)




    def spectrum_block(self):

        localctx = SparkySPKParser.Spectrum_blockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_spectrum_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 111
            self.match(SparkySPKParser.Spectrum)
            self.state = 115
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 29)) & ~0x3f) == 0 and ((1 << (_la - 29)) & 1143492092395511) != 0):
                self.state = 112
                self.spectrum_statement()
                self.state = 117
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 118
            self.match(SparkySPKParser.End_spectrum)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Spectrum_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETURN_SP(self):
            return self.getToken(SparkySPKParser.RETURN_SP, 0)

        def Name_SP(self):
            return self.getToken(SparkySPKParser.Name_SP, 0)

        def spectrum_name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SparkySPKParser.Spectrum_nameContext)
            else:
                return self.getTypedRuleContext(SparkySPKParser.Spectrum_nameContext,i)


        def Path_name(self):
            return self.getToken(SparkySPKParser.Path_name, 0)

        def Any_name_SP(self):
            return self.getToken(SparkySPKParser.Any_name_SP, 0)

        def Dimension(self):
            return self.getToken(SparkySPKParser.Dimension, 0)

        def Integer_SP(self, i:int=None):
            if i is None:
                return self.getTokens(SparkySPKParser.Integer_SP)
            else:
                return self.getToken(SparkySPKParser.Integer_SP, i)

        def Shift(self):
            return self.getToken(SparkySPKParser.Shift, 0)

        def Float_SP(self, i:int=None):
            if i is None:
                return self.getTokens(SparkySPKParser.Float_SP)
            else:
                return self.getToken(SparkySPKParser.Float_SP, i)

        def Points(self):
            return self.getToken(SparkySPKParser.Points, 0)

        def Assign_multi_axis_guess(self):
            return self.getToken(SparkySPKParser.Assign_multi_axis_guess, 0)

        def Assign_guess_threshhold(self):
            return self.getToken(SparkySPKParser.Assign_guess_threshhold, 0)

        def Assign_relation(self):
            return self.getToken(SparkySPKParser.Assign_relation, 0)

        def Assign_range(self):
            return self.getToken(SparkySPKParser.Assign_range, 0)

        def Assign_format(self):
            return self.getToken(SparkySPKParser.Assign_format, 0)

        def Format_ex(self):
            return self.getToken(SparkySPKParser.Format_ex, 0)

        def List_tool(self):
            return self.getToken(SparkySPKParser.List_tool, 0)

        def Sort_by(self):
            return self.getToken(SparkySPKParser.Sort_by, 0)

        def Simple_name_SP(self, i:int=None):
            if i is None:
                return self.getTokens(SparkySPKParser.Simple_name_SP)
            else:
                return self.getToken(SparkySPKParser.Simple_name_SP, i)

        def Name_type(self):
            return self.getToken(SparkySPKParser.Name_type, 0)

        def Sort_axis(self):
            return self.getToken(SparkySPKParser.Sort_axis, 0)

        def Show_flags(self):
            return self.getToken(SparkySPKParser.Show_flags, 0)

        def Integrate_overlapped_sep(self):
            return self.getToken(SparkySPKParser.Integrate_overlapped_sep, 0)

        def Integrate_methods(self):
            return self.getToken(SparkySPKParser.Integrate_methods, 0)

        def Integrate_allow_motion(self):
            return self.getToken(SparkySPKParser.Integrate_allow_motion, 0)

        def Integrate_adjust_linewidths(self):
            return self.getToken(SparkySPKParser.Integrate_adjust_linewidths, 0)

        def Integrate_motion_range(self):
            return self.getToken(SparkySPKParser.Integrate_motion_range, 0)

        def Integrate_min_linewidth(self):
            return self.getToken(SparkySPKParser.Integrate_min_linewidth, 0)

        def Integrate_max_linewidth(self):
            return self.getToken(SparkySPKParser.Integrate_max_linewidth, 0)

        def Integrate_fit_baseline(self):
            return self.getToken(SparkySPKParser.Integrate_fit_baseline, 0)

        def Integrate_subtract_peaks(self):
            return self.getToken(SparkySPKParser.Integrate_subtract_peaks, 0)

        def Integrate_contoured_data(self):
            return self.getToken(SparkySPKParser.Integrate_contoured_data, 0)

        def Integrate_rectangle_data(self):
            return self.getToken(SparkySPKParser.Integrate_rectangle_data, 0)

        def Integrate_max_iterations(self):
            return self.getToken(SparkySPKParser.Integrate_max_iterations, 0)

        def Integrate_tolerance(self):
            return self.getToken(SparkySPKParser.Integrate_tolerance, 0)

        def Peak_pick(self):
            return self.getToken(SparkySPKParser.Peak_pick, 0)

        def Peak_pick_minimum_linewidth(self):
            return self.getToken(SparkySPKParser.Peak_pick_minimum_linewidth, 0)

        def Peak_pick_minimum_dropoff(self):
            return self.getToken(SparkySPKParser.Peak_pick_minimum_dropoff, 0)

        def Noise_sigma(self):
            return self.getToken(SparkySPKParser.Noise_sigma, 0)

        def Ornament_labe_size(self):
            return self.getToken(SparkySPKParser.Ornament_labe_size, 0)

        def Ornament_line_size(self):
            return self.getToken(SparkySPKParser.Ornament_line_size, 0)

        def Ornament_peak_size(self):
            return self.getToken(SparkySPKParser.Ornament_peak_size, 0)

        def Ornament_grid_size(self):
            return self.getToken(SparkySPKParser.Ornament_grid_size, 0)

        def Ornament_peak_group_size(self):
            return self.getToken(SparkySPKParser.Ornament_peak_group_size, 0)

        def Ornament_select_size(self):
            return self.getToken(SparkySPKParser.Ornament_select_size, 0)

        def Ornament_pointer_size(self):
            return self.getToken(SparkySPKParser.Ornament_pointer_size, 0)

        def Ornament_line_end_size(self):
            return self.getToken(SparkySPKParser.Ornament_line_end_size, 0)

        def attached_data(self):
            return self.getTypedRuleContext(SparkySPKParser.Attached_dataContext,0)


        def view(self):
            return self.getTypedRuleContext(SparkySPKParser.ViewContext,0)


        def ornament(self):
            return self.getTypedRuleContext(SparkySPKParser.OrnamentContext,0)


        def getRuleIndex(self):
            return SparkySPKParser.RULE_spectrum_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSpectrum_statement" ):
                listener.enterSpectrum_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSpectrum_statement" ):
                listener.exitSpectrum_statement(self)




    def spectrum_statement(self):

        localctx = SparkySPKParser.Spectrum_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_spectrum_statement)
        self._la = 0 # Token type
        try:
            self.state = 303
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 120
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 121
                self.match(SparkySPKParser.Name_SP)
                self.state = 125
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while ((((_la - 74)) & ~0x3f) == 0 and ((1 << (_la - 74)) & 15) != 0):
                    self.state = 122
                    self.spectrum_name()
                    self.state = 127
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 128
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 129
                self.match(SparkySPKParser.Path_name)
                self.state = 130
                self.match(SparkySPKParser.Any_name_SP)
                self.state = 131
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 132
                self.match(SparkySPKParser.Dimension)
                self.state = 133
                self.match(SparkySPKParser.Integer_SP)
                self.state = 134
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 135
                self.match(SparkySPKParser.Shift)
                self.state = 137 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 136
                    self.match(SparkySPKParser.Float_SP)
                    self.state = 139 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==75):
                        break

                self.state = 141
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 142
                self.match(SparkySPKParser.Points)
                self.state = 144 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 143
                    self.match(SparkySPKParser.Integer_SP)
                    self.state = 146 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==74):
                        break

                self.state = 148
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 149
                self.match(SparkySPKParser.Assign_multi_axis_guess)
                self.state = 150
                self.match(SparkySPKParser.Integer_SP)
                self.state = 151
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 152
                self.match(SparkySPKParser.Assign_guess_threshhold)
                self.state = 153
                self.match(SparkySPKParser.Float_SP)
                self.state = 154
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 155
                self.match(SparkySPKParser.Assign_relation)
                self.state = 157 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 156
                    self.match(SparkySPKParser.Integer_SP)
                    self.state = 159 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==74):
                        break

                self.state = 161
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 162
                self.match(SparkySPKParser.Assign_range)
                self.state = 163
                self.match(SparkySPKParser.Integer_SP)
                self.state = 164
                self.match(SparkySPKParser.Float_SP)
                self.state = 165
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 166
                self.match(SparkySPKParser.Assign_format)
                self.state = 167
                self.match(SparkySPKParser.Format_ex)
                self.state = 168
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 169
                self.match(SparkySPKParser.List_tool)
                self.state = 170
                self.match(SparkySPKParser.Sort_by)
                self.state = 171
                self.match(SparkySPKParser.Simple_name_SP)
                self.state = 172
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 173
                self.match(SparkySPKParser.List_tool)
                self.state = 174
                self.match(SparkySPKParser.Name_type)
                self.state = 175
                self.match(SparkySPKParser.Simple_name_SP)
                self.state = 176
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 14:
                self.enterOuterAlt(localctx, 14)
                self.state = 177
                self.match(SparkySPKParser.List_tool)
                self.state = 178
                self.match(SparkySPKParser.Sort_axis)
                self.state = 179
                self.match(SparkySPKParser.Simple_name_SP)
                self.state = 180
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 15:
                self.enterOuterAlt(localctx, 15)
                self.state = 181
                self.match(SparkySPKParser.List_tool)
                self.state = 182
                self.match(SparkySPKParser.Show_flags)
                self.state = 186
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==76:
                    self.state = 183
                    self.match(SparkySPKParser.Simple_name_SP)
                    self.state = 188
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 189
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 16:
                self.enterOuterAlt(localctx, 16)
                self.state = 190
                self.match(SparkySPKParser.Integrate_overlapped_sep)
                self.state = 192 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 191
                    self.match(SparkySPKParser.Float_SP)
                    self.state = 194 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==75):
                        break

                self.state = 196
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 17:
                self.enterOuterAlt(localctx, 17)
                self.state = 197
                self.match(SparkySPKParser.Integrate_methods)
                self.state = 199 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 198
                    self.match(SparkySPKParser.Integer_SP)
                    self.state = 201 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==74):
                        break

                self.state = 203
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 18:
                self.enterOuterAlt(localctx, 18)
                self.state = 204
                self.match(SparkySPKParser.Integrate_allow_motion)
                self.state = 205
                self.match(SparkySPKParser.Integer_SP)
                self.state = 206
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 19:
                self.enterOuterAlt(localctx, 19)
                self.state = 207
                self.match(SparkySPKParser.Integrate_adjust_linewidths)
                self.state = 208
                self.match(SparkySPKParser.Integer_SP)
                self.state = 209
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 20:
                self.enterOuterAlt(localctx, 20)
                self.state = 210
                self.match(SparkySPKParser.Integrate_motion_range)
                self.state = 212 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 211
                    self.match(SparkySPKParser.Float_SP)
                    self.state = 214 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==75):
                        break

                self.state = 216
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 21:
                self.enterOuterAlt(localctx, 21)
                self.state = 217
                self.match(SparkySPKParser.Integrate_min_linewidth)
                self.state = 219 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 218
                    self.match(SparkySPKParser.Float_SP)
                    self.state = 221 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==75):
                        break

                self.state = 223
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 22:
                self.enterOuterAlt(localctx, 22)
                self.state = 224
                self.match(SparkySPKParser.Integrate_max_linewidth)
                self.state = 226 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 225
                    self.match(SparkySPKParser.Float_SP)
                    self.state = 228 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==75):
                        break

                self.state = 230
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 23:
                self.enterOuterAlt(localctx, 23)
                self.state = 231
                self.match(SparkySPKParser.Integrate_fit_baseline)
                self.state = 232
                self.match(SparkySPKParser.Integer_SP)
                self.state = 233
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 24:
                self.enterOuterAlt(localctx, 24)
                self.state = 234
                self.match(SparkySPKParser.Integrate_subtract_peaks)
                self.state = 235
                self.match(SparkySPKParser.Integer_SP)
                self.state = 236
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 25:
                self.enterOuterAlt(localctx, 25)
                self.state = 237
                self.match(SparkySPKParser.Integrate_contoured_data)
                self.state = 238
                self.match(SparkySPKParser.Integer_SP)
                self.state = 239
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 26:
                self.enterOuterAlt(localctx, 26)
                self.state = 240
                self.match(SparkySPKParser.Integrate_rectangle_data)
                self.state = 241
                self.match(SparkySPKParser.Integer_SP)
                self.state = 242
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 27:
                self.enterOuterAlt(localctx, 27)
                self.state = 243
                self.match(SparkySPKParser.Integrate_max_iterations)
                self.state = 244
                self.match(SparkySPKParser.Integer_SP)
                self.state = 245
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 28:
                self.enterOuterAlt(localctx, 28)
                self.state = 246
                self.match(SparkySPKParser.Integrate_tolerance)
                self.state = 247
                self.match(SparkySPKParser.Float_SP)
                self.state = 248
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 29:
                self.enterOuterAlt(localctx, 29)
                self.state = 249
                self.match(SparkySPKParser.Peak_pick)
                self.state = 251 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 250
                    self.match(SparkySPKParser.Float_SP)
                    self.state = 253 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==75):
                        break

                self.state = 255
                self.match(SparkySPKParser.Integer_SP)
                self.state = 256
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 30:
                self.enterOuterAlt(localctx, 30)
                self.state = 257
                self.match(SparkySPKParser.Peak_pick_minimum_linewidth)
                self.state = 259 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 258
                    self.match(SparkySPKParser.Float_SP)
                    self.state = 261 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==75):
                        break

                self.state = 263
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 31:
                self.enterOuterAlt(localctx, 31)
                self.state = 264
                self.match(SparkySPKParser.Peak_pick_minimum_dropoff)
                self.state = 265
                self.match(SparkySPKParser.Float_SP)
                self.state = 266
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 32:
                self.enterOuterAlt(localctx, 32)
                self.state = 267
                self.match(SparkySPKParser.Noise_sigma)
                self.state = 268
                self.match(SparkySPKParser.Float_SP)
                self.state = 269
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 33:
                self.enterOuterAlt(localctx, 33)
                self.state = 270
                self.match(SparkySPKParser.Ornament_labe_size)
                self.state = 271
                self.match(SparkySPKParser.Float_SP)
                self.state = 272
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 34:
                self.enterOuterAlt(localctx, 34)
                self.state = 273
                self.match(SparkySPKParser.Ornament_line_size)
                self.state = 274
                self.match(SparkySPKParser.Float_SP)
                self.state = 275
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 35:
                self.enterOuterAlt(localctx, 35)
                self.state = 276
                self.match(SparkySPKParser.Ornament_peak_size)
                self.state = 277
                self.match(SparkySPKParser.Float_SP)
                self.state = 278
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 36:
                self.enterOuterAlt(localctx, 36)
                self.state = 279
                self.match(SparkySPKParser.Ornament_grid_size)
                self.state = 280
                self.match(SparkySPKParser.Float_SP)
                self.state = 281
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 37:
                self.enterOuterAlt(localctx, 37)
                self.state = 282
                self.match(SparkySPKParser.Ornament_peak_group_size)
                self.state = 283
                self.match(SparkySPKParser.Float_SP)
                self.state = 284
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 38:
                self.enterOuterAlt(localctx, 38)
                self.state = 285
                self.match(SparkySPKParser.Ornament_select_size)
                self.state = 286
                self.match(SparkySPKParser.Float_SP)
                self.state = 287
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 39:
                self.enterOuterAlt(localctx, 39)
                self.state = 288
                self.match(SparkySPKParser.Ornament_pointer_size)
                self.state = 289
                self.match(SparkySPKParser.Float_SP)
                self.state = 290
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 40:
                self.enterOuterAlt(localctx, 40)
                self.state = 291
                self.match(SparkySPKParser.Ornament_line_end_size)
                self.state = 292
                self.match(SparkySPKParser.Float_SP)
                self.state = 293
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 41:
                self.enterOuterAlt(localctx, 41)
                self.state = 294
                self.attached_data()
                self.state = 295
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 42:
                self.enterOuterAlt(localctx, 42)
                self.state = 297
                self.view()
                self.state = 298
                self.match(SparkySPKParser.RETURN_SP)
                pass

            elif la_ == 43:
                self.enterOuterAlt(localctx, 43)
                self.state = 300
                self.ornament()
                self.state = 301
                self.match(SparkySPKParser.RETURN_SP)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Spectrum_nameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer_SP(self):
            return self.getToken(SparkySPKParser.Integer_SP, 0)

        def Float_SP(self):
            return self.getToken(SparkySPKParser.Float_SP, 0)

        def Simple_name_SP(self):
            return self.getToken(SparkySPKParser.Simple_name_SP, 0)

        def Any_name_SP(self):
            return self.getToken(SparkySPKParser.Any_name_SP, 0)

        def getRuleIndex(self):
            return SparkySPKParser.RULE_spectrum_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSpectrum_name" ):
                listener.enterSpectrum_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSpectrum_name" ):
                listener.exitSpectrum_name(self)




    def spectrum_name(self):

        localctx = SparkySPKParser.Spectrum_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_spectrum_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 305
            _la = self._input.LA(1)
            if not(((((_la - 74)) & ~0x3f) == 0 and ((1 << (_la - 74)) & 15) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Attached_dataContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Attached_data(self):
            return self.getToken(SparkySPKParser.Attached_data, 0)

        def End_attached_data(self):
            return self.getToken(SparkySPKParser.End_attached_data, 0)

        def attached_data_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SparkySPKParser.Attached_data_statementContext)
            else:
                return self.getTypedRuleContext(SparkySPKParser.Attached_data_statementContext,i)


        def getRuleIndex(self):
            return SparkySPKParser.RULE_attached_data

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttached_data" ):
                listener.enterAttached_data(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttached_data" ):
                listener.exitAttached_data(self)




    def attached_data(self):

        localctx = SparkySPKParser.Attached_dataContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_attached_data)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 307
            self.match(SparkySPKParser.Attached_data)
            self.state = 311
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==81:
                self.state = 308
                self.attached_data_statement()
                self.state = 313
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 314
            self.match(SparkySPKParser.End_attached_data)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Attached_data_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Any_name_AD(self):
            return self.getToken(SparkySPKParser.Any_name_AD, 0)

        def getRuleIndex(self):
            return SparkySPKParser.RULE_attached_data_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttached_data_statement" ):
                listener.enterAttached_data_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttached_data_statement" ):
                listener.exitAttached_data_statement(self)




    def attached_data_statement(self):

        localctx = SparkySPKParser.Attached_data_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_attached_data_statement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 316
            self.match(SparkySPKParser.Any_name_AD)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ViewContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def View(self):
            return self.getToken(SparkySPKParser.View, 0)

        def End_view(self):
            return self.getToken(SparkySPKParser.End_view, 0)

        def view_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SparkySPKParser.View_statementContext)
            else:
                return self.getTypedRuleContext(SparkySPKParser.View_statementContext,i)


        def getRuleIndex(self):
            return SparkySPKParser.RULE_view

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterView" ):
                listener.enterView(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitView" ):
                listener.exitView(self)




    def view(self):

        localctx = SparkySPKParser.ViewContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_view)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 318
            self.match(SparkySPKParser.View)
            self.state = 322
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 83)) & ~0x3f) == 0 and ((1 << (_la - 83)) & 67581) != 0):
                self.state = 319
                self.view_statement()
                self.state = 324
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 325
            self.match(SparkySPKParser.End_view)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class View_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETURN_VI(self):
            return self.getToken(SparkySPKParser.RETURN_VI, 0)

        def Name_VI(self):
            return self.getToken(SparkySPKParser.Name_VI, 0)

        def view_name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SparkySPKParser.View_nameContext)
            else:
                return self.getTypedRuleContext(SparkySPKParser.View_nameContext,i)


        def Precision(self):
            return self.getToken(SparkySPKParser.Precision, 0)

        def Integer_VI(self, i:int=None):
            if i is None:
                return self.getTokens(SparkySPKParser.Integer_VI)
            else:
                return self.getToken(SparkySPKParser.Integer_VI, i)

        def Precision_by_units(self):
            return self.getToken(SparkySPKParser.Precision_by_units, 0)

        def View_mode(self):
            return self.getToken(SparkySPKParser.View_mode, 0)

        def Show(self):
            return self.getToken(SparkySPKParser.Show, 0)

        def Simple_name_VI(self, i:int=None):
            if i is None:
                return self.getTokens(SparkySPKParser.Simple_name_VI)
            else:
                return self.getToken(SparkySPKParser.Simple_name_VI, i)

        def Axis_type(self):
            return self.getToken(SparkySPKParser.Axis_type, 0)

        def Flags_VI(self):
            return self.getToken(SparkySPKParser.Flags_VI, 0)

        def Contour_pos(self):
            return self.getToken(SparkySPKParser.Contour_pos, 0)

        def view_number(self):
            return self.getTypedRuleContext(SparkySPKParser.View_numberContext,0)


        def Float_VI(self, i:int=None):
            if i is None:
                return self.getTokens(SparkySPKParser.Float_VI)
            else:
                return self.getToken(SparkySPKParser.Float_VI, i)

        def Contour_neg(self):
            return self.getToken(SparkySPKParser.Contour_neg, 0)

        def params(self):
            return self.getTypedRuleContext(SparkySPKParser.ParamsContext,0)


        def getRuleIndex(self):
            return SparkySPKParser.RULE_view_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterView_statement" ):
                listener.enterView_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitView_statement" ):
                listener.exitView_statement(self)




    def view_statement(self):

        localctx = SparkySPKParser.View_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_view_statement)
        self._la = 0 # Token type
        try:
            self.state = 396
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [99]:
                self.enterOuterAlt(localctx, 1)
                self.state = 327
                self.match(SparkySPKParser.RETURN_VI)
                pass
            elif token in [85]:
                self.enterOuterAlt(localctx, 2)
                self.state = 328
                self.match(SparkySPKParser.Name_VI)
                self.state = 332
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while ((((_la - 94)) & ~0x3f) == 0 and ((1 << (_la - 94)) & 15) != 0):
                    self.state = 329
                    self.view_name()
                    self.state = 334
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 335
                self.match(SparkySPKParser.RETURN_VI)
                pass
            elif token in [86]:
                self.enterOuterAlt(localctx, 3)
                self.state = 336
                self.match(SparkySPKParser.Precision)
                self.state = 337
                self.match(SparkySPKParser.Integer_VI)
                self.state = 338
                self.match(SparkySPKParser.RETURN_VI)
                pass
            elif token in [87]:
                self.enterOuterAlt(localctx, 4)
                self.state = 339
                self.match(SparkySPKParser.Precision_by_units)
                self.state = 341 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 340
                    self.match(SparkySPKParser.Integer_VI)
                    self.state = 343 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==94):
                        break

                self.state = 345
                self.match(SparkySPKParser.RETURN_VI)
                pass
            elif token in [88]:
                self.enterOuterAlt(localctx, 5)
                self.state = 346
                self.match(SparkySPKParser.View_mode)
                self.state = 347
                self.match(SparkySPKParser.Integer_VI)
                self.state = 348
                self.match(SparkySPKParser.RETURN_VI)
                pass
            elif token in [89]:
                self.enterOuterAlt(localctx, 6)
                self.state = 349
                self.match(SparkySPKParser.Show)
                self.state = 350
                self.match(SparkySPKParser.Integer_VI)
                self.state = 354
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==97:
                    self.state = 351
                    self.match(SparkySPKParser.Simple_name_VI)
                    self.state = 356
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 357
                self.match(SparkySPKParser.RETURN_VI)
                pass
            elif token in [90]:
                self.enterOuterAlt(localctx, 7)
                self.state = 358
                self.match(SparkySPKParser.Axis_type)
                self.state = 359
                self.match(SparkySPKParser.Integer_VI)
                self.state = 360
                self.match(SparkySPKParser.RETURN_VI)
                pass
            elif token in [91]:
                self.enterOuterAlt(localctx, 8)
                self.state = 361
                self.match(SparkySPKParser.Flags_VI)
                self.state = 365
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==97:
                    self.state = 362
                    self.match(SparkySPKParser.Simple_name_VI)
                    self.state = 367
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 368
                self.match(SparkySPKParser.RETURN_VI)
                pass
            elif token in [92]:
                self.enterOuterAlt(localctx, 9)
                self.state = 369
                self.match(SparkySPKParser.Contour_pos)
                self.state = 370
                self.match(SparkySPKParser.Integer_VI)
                self.state = 371
                self.view_number()
                self.state = 372
                self.match(SparkySPKParser.Float_VI)
                self.state = 373
                self.match(SparkySPKParser.Float_VI)
                self.state = 375 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 374
                    self.match(SparkySPKParser.Simple_name_VI)
                    self.state = 377 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==97):
                        break

                self.state = 379
                self.match(SparkySPKParser.RETURN_VI)
                pass
            elif token in [93]:
                self.enterOuterAlt(localctx, 10)
                self.state = 381
                self.match(SparkySPKParser.Contour_neg)
                self.state = 382
                self.match(SparkySPKParser.Integer_VI)
                self.state = 383
                self.view_number()
                self.state = 384
                self.match(SparkySPKParser.Float_VI)
                self.state = 385
                self.match(SparkySPKParser.Float_VI)
                self.state = 387 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 386
                    self.match(SparkySPKParser.Simple_name_VI)
                    self.state = 389 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==97):
                        break

                self.state = 391
                self.match(SparkySPKParser.RETURN_VI)
                pass
            elif token in [83]:
                self.enterOuterAlt(localctx, 11)
                self.state = 393
                self.params()
                self.state = 394
                self.match(SparkySPKParser.RETURN_VI)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class View_nameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer_VI(self):
            return self.getToken(SparkySPKParser.Integer_VI, 0)

        def Float_VI(self):
            return self.getToken(SparkySPKParser.Float_VI, 0)

        def Real_VI(self):
            return self.getToken(SparkySPKParser.Real_VI, 0)

        def Simple_name_VI(self):
            return self.getToken(SparkySPKParser.Simple_name_VI, 0)

        def getRuleIndex(self):
            return SparkySPKParser.RULE_view_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterView_name" ):
                listener.enterView_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitView_name" ):
                listener.exitView_name(self)




    def view_name(self):

        localctx = SparkySPKParser.View_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_view_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 398
            _la = self._input.LA(1)
            if not(((((_la - 94)) & ~0x3f) == 0 and ((1 << (_la - 94)) & 15) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class View_numberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer_VI(self):
            return self.getToken(SparkySPKParser.Integer_VI, 0)

        def Float_VI(self):
            return self.getToken(SparkySPKParser.Float_VI, 0)

        def Real_VI(self):
            return self.getToken(SparkySPKParser.Real_VI, 0)

        def getRuleIndex(self):
            return SparkySPKParser.RULE_view_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterView_number" ):
                listener.enterView_number(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitView_number" ):
                listener.exitView_number(self)




    def view_number(self):

        localctx = SparkySPKParser.View_numberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_view_number)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 400
            _la = self._input.LA(1)
            if not(((((_la - 94)) & ~0x3f) == 0 and ((1 << (_la - 94)) & 7) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Params(self):
            return self.getToken(SparkySPKParser.Params, 0)

        def End_params(self):
            return self.getToken(SparkySPKParser.End_params, 0)

        def params_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SparkySPKParser.Params_statementContext)
            else:
                return self.getTypedRuleContext(SparkySPKParser.Params_statementContext,i)


        def getRuleIndex(self):
            return SparkySPKParser.RULE_params

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParams" ):
                listener.enterParams(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParams" ):
                listener.exitParams(self)




    def params(self):

        localctx = SparkySPKParser.ParamsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_params)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 402
            self.match(SparkySPKParser.Params)
            self.state = 406
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 101)) & ~0x3f) == 0 and ((1 << (_la - 101)) & 2175) != 0):
                self.state = 403
                self.params_statement()
                self.state = 408
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 409
            self.match(SparkySPKParser.End_params)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Params_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETURN_PA(self):
            return self.getToken(SparkySPKParser.RETURN_PA, 0)

        def Orientation(self):
            return self.getToken(SparkySPKParser.Orientation, 0)

        def Integer_PA(self, i:int=None):
            if i is None:
                return self.getTokens(SparkySPKParser.Integer_PA)
            else:
                return self.getToken(SparkySPKParser.Integer_PA, i)

        def Location(self):
            return self.getToken(SparkySPKParser.Location, 0)

        def Size(self):
            return self.getToken(SparkySPKParser.Size, 0)

        def Offset(self):
            return self.getToken(SparkySPKParser.Offset, 0)

        def Float_PA(self, i:int=None):
            if i is None:
                return self.getTokens(SparkySPKParser.Float_PA)
            else:
                return self.getToken(SparkySPKParser.Float_PA, i)

        def Scale(self):
            return self.getToken(SparkySPKParser.Scale, 0)

        def Zoom(self):
            return self.getToken(SparkySPKParser.Zoom, 0)

        def Flags_PA(self):
            return self.getToken(SparkySPKParser.Flags_PA, 0)

        def getRuleIndex(self):
            return SparkySPKParser.RULE_params_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParams_statement" ):
                listener.enterParams_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParams_statement" ):
                listener.exitParams_statement(self)




    def params_statement(self):

        localctx = SparkySPKParser.Params_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_params_statement)
        self._la = 0 # Token type
        try:
            self.state = 453
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [112]:
                self.enterOuterAlt(localctx, 1)
                self.state = 411
                self.match(SparkySPKParser.RETURN_PA)
                pass
            elif token in [101]:
                self.enterOuterAlt(localctx, 2)
                self.state = 412
                self.match(SparkySPKParser.Orientation)
                self.state = 414 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 413
                    self.match(SparkySPKParser.Integer_PA)
                    self.state = 416 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==108):
                        break

                self.state = 418
                self.match(SparkySPKParser.RETURN_PA)
                pass
            elif token in [102]:
                self.enterOuterAlt(localctx, 3)
                self.state = 419
                self.match(SparkySPKParser.Location)
                self.state = 421 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 420
                    self.match(SparkySPKParser.Integer_PA)
                    self.state = 423 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==108):
                        break

                self.state = 425
                self.match(SparkySPKParser.RETURN_PA)
                pass
            elif token in [103]:
                self.enterOuterAlt(localctx, 4)
                self.state = 426
                self.match(SparkySPKParser.Size)
                self.state = 428 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 427
                    self.match(SparkySPKParser.Integer_PA)
                    self.state = 430 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==108):
                        break

                self.state = 432
                self.match(SparkySPKParser.RETURN_PA)
                pass
            elif token in [104]:
                self.enterOuterAlt(localctx, 5)
                self.state = 433
                self.match(SparkySPKParser.Offset)
                self.state = 435 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 434
                    self.match(SparkySPKParser.Float_PA)
                    self.state = 437 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==109):
                        break

                self.state = 439
                self.match(SparkySPKParser.RETURN_PA)
                pass
            elif token in [105]:
                self.enterOuterAlt(localctx, 6)
                self.state = 440
                self.match(SparkySPKParser.Scale)
                self.state = 442 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 441
                    self.match(SparkySPKParser.Float_PA)
                    self.state = 444 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==109):
                        break

                self.state = 446
                self.match(SparkySPKParser.RETURN_PA)
                pass
            elif token in [106]:
                self.enterOuterAlt(localctx, 7)
                self.state = 447
                self.match(SparkySPKParser.Zoom)
                self.state = 448
                self.match(SparkySPKParser.Float_PA)
                self.state = 449
                self.match(SparkySPKParser.RETURN_PA)
                pass
            elif token in [107]:
                self.enterOuterAlt(localctx, 8)
                self.state = 450
                self.match(SparkySPKParser.Flags_PA)
                self.state = 451
                self.match(SparkySPKParser.Integer_PA)
                self.state = 452
                self.match(SparkySPKParser.RETURN_PA)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OrnamentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Ornament(self):
            return self.getToken(SparkySPKParser.Ornament, 0)

        def End_ornament(self):
            return self.getToken(SparkySPKParser.End_ornament, 0)

        def ornament_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SparkySPKParser.Ornament_statementContext)
            else:
                return self.getTypedRuleContext(SparkySPKParser.Ornament_statementContext,i)


        def getRuleIndex(self):
            return SparkySPKParser.RULE_ornament

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrnament" ):
                listener.enterOrnament(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrnament" ):
                listener.exitOrnament(self)




    def ornament(self):

        localctx = SparkySPKParser.OrnamentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_ornament)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 455
            self.match(SparkySPKParser.Ornament)
            self.state = 459
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 113)) & ~0x3f) == 0 and ((1 << (_la - 113)) & 1064933) != 0):
                self.state = 456
                self.ornament_statement()
                self.state = 461
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 462
            self.match(SparkySPKParser.End_ornament)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Ornament_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETURN_OR(self):
            return self.getToken(SparkySPKParser.RETURN_OR, 0)

        def Type_OR(self):
            return self.getToken(SparkySPKParser.Type_OR, 0)

        def Peak(self):
            return self.getToken(SparkySPKParser.Peak, 0)

        def Grid(self):
            return self.getToken(SparkySPKParser.Grid, 0)

        def Color_OR(self):
            return self.getToken(SparkySPKParser.Color_OR, 0)

        def Integer_OR(self, i:int=None):
            if i is None:
                return self.getTokens(SparkySPKParser.Integer_OR)
            else:
                return self.getToken(SparkySPKParser.Integer_OR, i)

        def Simple_name_OR(self, i:int=None):
            if i is None:
                return self.getTokens(SparkySPKParser.Simple_name_OR)
            else:
                return self.getToken(SparkySPKParser.Simple_name_OR, i)

        def Flags_OR(self):
            return self.getToken(SparkySPKParser.Flags_OR, 0)

        def Id(self):
            return self.getToken(SparkySPKParser.Id, 0)

        def Pos_OR(self):
            return self.getToken(SparkySPKParser.Pos_OR, 0)

        def ornament_position(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SparkySPKParser.Ornament_positionContext)
            else:
                return self.getTypedRuleContext(SparkySPKParser.Ornament_positionContext,i)


        def Height(self):
            return self.getToken(SparkySPKParser.Height, 0)

        def Float_OR(self, i:int=None):
            if i is None:
                return self.getTokens(SparkySPKParser.Float_OR)
            else:
                return self.getToken(SparkySPKParser.Float_OR, i)

        def Line_width(self):
            return self.getToken(SparkySPKParser.Line_width, 0)

        def Integral(self):
            return self.getToken(SparkySPKParser.Integral, 0)

        def Real_OR(self):
            return self.getToken(SparkySPKParser.Real_OR, 0)

        def Fr(self):
            return self.getToken(SparkySPKParser.Fr, 0)

        def Rs(self):
            return self.getToken(SparkySPKParser.Rs, 0)

        def Rs_ex(self, i:int=None):
            if i is None:
                return self.getTokens(SparkySPKParser.Rs_ex)
            else:
                return self.getToken(SparkySPKParser.Rs_ex, i)

        def label(self):
            return self.getTypedRuleContext(SparkySPKParser.LabelContext,0)


        def getRuleIndex(self):
            return SparkySPKParser.RULE_ornament_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrnament_statement" ):
                listener.enterOrnament_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrnament_statement" ):
                listener.exitOrnament_statement(self)




    def ornament_statement(self):

        localctx = SparkySPKParser.Ornament_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_ornament_statement)
        self._la = 0 # Token type
        try:
            self.state = 537
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,44,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 464
                self.match(SparkySPKParser.RETURN_OR)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 465
                self.match(SparkySPKParser.Type_OR)
                self.state = 466
                self.match(SparkySPKParser.Peak)
                self.state = 467
                self.match(SparkySPKParser.RETURN_OR)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 468
                self.match(SparkySPKParser.Type_OR)
                self.state = 469
                self.match(SparkySPKParser.Grid)
                self.state = 470
                self.match(SparkySPKParser.RETURN_OR)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 471
                self.match(SparkySPKParser.Color_OR)
                self.state = 473 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 472
                    self.match(SparkySPKParser.Integer_OR)
                    self.state = 475 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==128):
                        break

                self.state = 478 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 477
                    self.match(SparkySPKParser.Simple_name_OR)
                    self.state = 480 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==131):
                        break

                self.state = 482
                self.match(SparkySPKParser.RETURN_OR)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 483
                self.match(SparkySPKParser.Flags_OR)
                self.state = 485 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 484
                    self.match(SparkySPKParser.Integer_OR)
                    self.state = 487 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==128):
                        break

                self.state = 489
                self.match(SparkySPKParser.RETURN_OR)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 490
                self.match(SparkySPKParser.Id)
                self.state = 491
                self.match(SparkySPKParser.Integer_OR)
                self.state = 492
                self.match(SparkySPKParser.RETURN_OR)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 493
                self.match(SparkySPKParser.Pos_OR)
                self.state = 495 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 494
                    self.ornament_position()
                    self.state = 497 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==128 or _la==129):
                        break

                self.state = 499
                self.match(SparkySPKParser.RETURN_OR)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 501
                self.match(SparkySPKParser.Height)
                self.state = 503 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 502
                    self.match(SparkySPKParser.Float_OR)
                    self.state = 505 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==129):
                        break

                self.state = 507
                self.match(SparkySPKParser.RETURN_OR)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 508
                self.match(SparkySPKParser.Line_width)
                self.state = 510 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 509
                    self.match(SparkySPKParser.Float_OR)
                    self.state = 512 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==129):
                        break

                self.state = 515
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==131:
                    self.state = 514
                    self.match(SparkySPKParser.Simple_name_OR)


                self.state = 517
                self.match(SparkySPKParser.RETURN_OR)
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 518
                self.match(SparkySPKParser.Integral)
                self.state = 519
                self.match(SparkySPKParser.Real_OR)
                self.state = 521
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==131:
                    self.state = 520
                    self.match(SparkySPKParser.Simple_name_OR)


                self.state = 523
                self.match(SparkySPKParser.RETURN_OR)
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 524
                self.match(SparkySPKParser.Fr)
                self.state = 525
                self.match(SparkySPKParser.Float_OR)
                self.state = 526
                self.match(SparkySPKParser.RETURN_OR)
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 527
                self.match(SparkySPKParser.Rs)
                self.state = 529 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 528
                    self.match(SparkySPKParser.Rs_ex)
                    self.state = 531 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==127):
                        break

                self.state = 533
                self.match(SparkySPKParser.RETURN_OR)
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 534
                self.label()
                self.state = 535
                self.match(SparkySPKParser.RETURN_OR)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Ornament_positionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer_OR(self):
            return self.getToken(SparkySPKParser.Integer_OR, 0)

        def Float_OR(self):
            return self.getToken(SparkySPKParser.Float_OR, 0)

        def getRuleIndex(self):
            return SparkySPKParser.RULE_ornament_position

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrnament_position" ):
                listener.enterOrnament_position(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrnament_position" ):
                listener.exitOrnament_position(self)




    def ornament_position(self):

        localctx = SparkySPKParser.Ornament_positionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_ornament_position)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 539
            _la = self._input.LA(1)
            if not(_la==128 or _la==129):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LabelContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def L_brakt(self):
            return self.getToken(SparkySPKParser.L_brakt, 0)

        def R_brakt(self):
            return self.getToken(SparkySPKParser.R_brakt, 0)

        def label_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SparkySPKParser.Label_statementContext)
            else:
                return self.getTypedRuleContext(SparkySPKParser.Label_statementContext,i)


        def getRuleIndex(self):
            return SparkySPKParser.RULE_label

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLabel" ):
                listener.enterLabel(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLabel" ):
                listener.exitLabel(self)




    def label(self):

        localctx = SparkySPKParser.LabelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_label)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 541
            self.match(SparkySPKParser.L_brakt)
            self.state = 545
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 135)) & ~0x3f) == 0 and ((1 << (_la - 135)) & 32895) != 0):
                self.state = 542
                self.label_statement()
                self.state = 547
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 548
            self.match(SparkySPKParser.R_brakt)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Label_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETURN_LA(self):
            return self.getToken(SparkySPKParser.RETURN_LA, 0)

        def Type_LA(self):
            return self.getToken(SparkySPKParser.Type_LA, 0)

        def Label(self):
            return self.getToken(SparkySPKParser.Label, 0)

        def Color_LA(self):
            return self.getToken(SparkySPKParser.Color_LA, 0)

        def Integer_LA(self, i:int=None):
            if i is None:
                return self.getTokens(SparkySPKParser.Integer_LA)
            else:
                return self.getToken(SparkySPKParser.Integer_LA, i)

        def Simple_name_LA(self, i:int=None):
            if i is None:
                return self.getTokens(SparkySPKParser.Simple_name_LA)
            else:
                return self.getToken(SparkySPKParser.Simple_name_LA, i)

        def Flags_LA(self):
            return self.getToken(SparkySPKParser.Flags_LA, 0)

        def Mode_LA(self):
            return self.getToken(SparkySPKParser.Mode_LA, 0)

        def Pos_LA(self):
            return self.getToken(SparkySPKParser.Pos_LA, 0)

        def label_position(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SparkySPKParser.Label_positionContext)
            else:
                return self.getTypedRuleContext(SparkySPKParser.Label_positionContext,i)


        def Assignment_2d_ex(self):
            return self.getToken(SparkySPKParser.Assignment_2d_ex, 0)

        def Assignment_3d_ex(self):
            return self.getToken(SparkySPKParser.Assignment_3d_ex, 0)

        def Assignment_4d_ex(self):
            return self.getToken(SparkySPKParser.Assignment_4d_ex, 0)

        def Xy(self):
            return self.getToken(SparkySPKParser.Xy, 0)

        def Xy_pos(self, i:int=None):
            if i is None:
                return self.getTokens(SparkySPKParser.Xy_pos)
            else:
                return self.getToken(SparkySPKParser.Xy_pos, i)

        def getRuleIndex(self):
            return SparkySPKParser.RULE_label_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLabel_statement" ):
                listener.enterLabel_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLabel_statement" ):
                listener.exitLabel_statement(self)




    def label_statement(self):

        localctx = SparkySPKParser.Label_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_label_statement)
        self._la = 0 # Token type
        try:
            self.state = 594
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [150]:
                self.enterOuterAlt(localctx, 1)
                self.state = 550
                self.match(SparkySPKParser.RETURN_LA)
                pass
            elif token in [135]:
                self.enterOuterAlt(localctx, 2)
                self.state = 551
                self.match(SparkySPKParser.Type_LA)
                self.state = 552
                self.match(SparkySPKParser.Label)
                self.state = 553
                self.match(SparkySPKParser.RETURN_LA)
                pass
            elif token in [137]:
                self.enterOuterAlt(localctx, 3)
                self.state = 554
                self.match(SparkySPKParser.Color_LA)
                self.state = 556 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 555
                    self.match(SparkySPKParser.Integer_LA)
                    self.state = 558 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==146):
                        break

                self.state = 561 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 560
                    self.match(SparkySPKParser.Simple_name_LA)
                    self.state = 563 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==148):
                        break

                self.state = 565
                self.match(SparkySPKParser.RETURN_LA)
                pass
            elif token in [138]:
                self.enterOuterAlt(localctx, 4)
                self.state = 566
                self.match(SparkySPKParser.Flags_LA)
                self.state = 568 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 567
                    self.match(SparkySPKParser.Integer_LA)
                    self.state = 570 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==146):
                        break

                self.state = 572
                self.match(SparkySPKParser.RETURN_LA)
                pass
            elif token in [139]:
                self.enterOuterAlt(localctx, 5)
                self.state = 573
                self.match(SparkySPKParser.Mode_LA)
                self.state = 574
                self.match(SparkySPKParser.Integer_LA)
                self.state = 575
                self.match(SparkySPKParser.RETURN_LA)
                pass
            elif token in [140]:
                self.enterOuterAlt(localctx, 6)
                self.state = 576
                self.match(SparkySPKParser.Pos_LA)
                self.state = 578 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 577
                    self.label_position()
                    self.state = 580 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==146 or _la==147):
                        break

                self.state = 582
                self.match(SparkySPKParser.RETURN_LA)
                pass
            elif token in [136]:
                self.enterOuterAlt(localctx, 7)
                self.state = 584
                self.match(SparkySPKParser.Label)
                self.state = 585
                _la = self._input.LA(1)
                if not(((((_la - 142)) & ~0x3f) == 0 and ((1 << (_la - 142)) & 7) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 586
                self.match(SparkySPKParser.RETURN_LA)
                pass
            elif token in [141]:
                self.enterOuterAlt(localctx, 8)
                self.state = 587
                self.match(SparkySPKParser.Xy)
                self.state = 589 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 588
                    self.match(SparkySPKParser.Xy_pos)
                    self.state = 591 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==145):
                        break

                self.state = 593
                self.match(SparkySPKParser.RETURN_LA)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Label_positionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer_LA(self):
            return self.getToken(SparkySPKParser.Integer_LA, 0)

        def Float_LA(self):
            return self.getToken(SparkySPKParser.Float_LA, 0)

        def getRuleIndex(self):
            return SparkySPKParser.RULE_label_position

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLabel_position" ):
                listener.enterLabel_position(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLabel_position" ):
                listener.exitLabel_position(self)




    def label_position(self):

        localctx = SparkySPKParser.Label_positionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_label_position)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 596
            _la = self._input.LA(1)
            if not(_la==146 or _la==147):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





