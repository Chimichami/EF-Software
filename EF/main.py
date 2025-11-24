import sys
import unittest
from ui import ConsoleUI

if __name__ == '__main__':
    # Si ejecutas "python main.py test", corre los tests
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # Carga los tests del archivo tests.py
        tests = unittest.TestLoader().discover('.', pattern='tests.py')
        unittest.TextTestRunner(verbosity=2).run(tests)
    else:
        # Si ejecutas "python main.py", corre la aplicación
        app = ConsoleUI()
        app.run()