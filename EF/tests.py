import unittest
from models import Evaluation, StudentContext
from services import GradeCalculatorService

class TestGradeCalculator(unittest.TestCase):
    
    def setUp(self):
        self.calculator = GradeCalculatorService()

    def test_standard_calculation(self):
        """RF01/RF04: Cálculo normal con puntos extra."""
        evals = [Evaluation("P1", 15, 50), Evaluation("P2", 15, 50)] 
        # CORREGIDO: Usamos un ID válido (2021 + 10 + 001) en lugar de "U1"
        ctx = StudentContext("202110001", evals, True, [True, True])
        result = self.calculator.calculate_final_grade(ctx)
        self.assertEqual(result['final_grade'], 16.0) # 15 + 1 extra

    def test_fail_due_to_attendance(self):
        """RF02: Falla por inasistencia."""
        evals = [Evaluation("P1", 20, 100)]
        # CORREGIDO: Usamos un ID válido
        ctx = StudentContext("202110002", evals, False, [True])
        result = self.calculator.calculate_final_grade(ctx)
        self.assertEqual(result['final_grade'], 0.0)

    def test_grade_cap_at_20(self):
        """RNF01: Tope máximo de 20."""
        evals = [Evaluation("P1", 20, 100)]
        # CORREGIDO: Usamos un ID válido
        ctx = StudentContext("202110003", evals, True, [True])
        result = self.calculator.calculate_final_grade(ctx)
        self.assertEqual(result['final_grade'], 20.0)

    def test_valid_student_id_security(self):
        """Seguridad: Debe aceptar IDs con formato correcto (Año + Ciclo + Digitos)."""
        try:
            # 2024 + 10 + 123
            StudentContext("202410123", [], True, [])
        except ValueError:
            self.fail("StudentContext rechazó un ID válido por error.")

    def test_invalid_student_id_security(self):
        """Seguridad: Debe rechazar IDs maliciosos o con formato incorrecto."""
        bad_ids = [
            "202130123",  # Ciclo 30 no existe
            "199910123",  # Año incorrecto (según regex 20xx)
            "ABCde1234",  # Inyección de texto
            "2023101",    # Muy corto
            "2023101234"  # Muy largo
        ]
        for bad_id in bad_ids:
            with self.assertRaises(ValueError):
                StudentContext(bad_id, [], True, [])

if __name__ == '__main__':
    unittest.main()