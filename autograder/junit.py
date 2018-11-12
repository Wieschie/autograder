from junitparser import JUnitXml, FloatAttr
from pathlib import Path
import re


points_regex = re.compile(""".*display-name:.*points:(\s*[0-9]+\.?[0-9]*).*""")


def parse_xml(xmlpath: Path) -> (str, float, float):
    xml = JUnitXml.fromfile(
        str(xmlpath.absolute() / "TEST-junit-vintage.xml")
    ) + JUnitXml.fromfile(str(xmlpath.absolute() / "TEST-junit-jupiter.xml"))
    earned_points = 0
    total_points = 0
    output = ""

    for suite in xml:
        for case in suite:
            point_str = points_regex.search(case.system_out)
            point_val = float(point_str.groups()[0])
            point_out = ""
            if point_str:
                case.points = FloatAttr("points")

                total_points += point_val
                if case.result is None:
                    case.points = point_val
                    earned_points += point_val
                else:
                    case.points = 0
                point_out = f"{case.points:1g} points"

            output += f"{case.name}: {point_out}\n"
            if case.result is not None:
                output += f"{type(case.result).__name__}: {case.result.message}\n"

    return output, earned_points, total_points
