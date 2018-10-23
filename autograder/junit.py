from junitparser import JUnitXml, FloatAttr
from pathlib import Path
import re


points_regex = re.compile(""".*display-name:.*points:(\s*[0-9]+\.?[0-9]*).*""")


def parse_xml(workdir: Path):
    xml = JUnitXml.fromfile(workdir / "TEST-junit-vintage.xml") + \
          JUnitXml.fromfile(workdir / "TEST-junit-jupiter.xml")

    for suite in xml:
        for case in suite:
            point_value = points_regex.search(case.system_out)
            if point_value:
                case.points = FloatAttr("points")
                if case.result is None:
                    case.points = float(point_value.groups()[0])
                else:
                    case.points = 0

                output = f"{case.classname}.{case.name}: {case.points} points"
            else:
                output = f"{case.classname}.{case.name}"
            print(output)

