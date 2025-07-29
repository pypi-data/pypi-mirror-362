# activate virtualenv if exists
import os
import sys
def load():
	if sys.prefix!=sys.base_prefix: return # already using virtualenv
	vp=os.path.abspath(sys.argv[0])
	for _ in range(3):
		vp=os.path.dirname(vp)
		for vd in [ "venv", ".venv", ".env" ]:
			activate_this=f"{vp}/{vd}/bin/activate_this.py"
			if os.path.isfile(activate_this):
				with open(activate_this) as f:
					code=compile(f.read(), activate_this, 'exec')
					exec(code, dict(__file__=activate_this))
					return
