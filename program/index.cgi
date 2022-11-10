#!/Users/soichiro/python/workspace/milk-formula-temperature-simulator/.venv/bin/python3

import cgitb
import main
from wsgiref.handlers import CGIHandler

CGIHandler().run(main)

