from typing import List, Dict, Any
from config import AppConfig
from models import StudentContext

class ExtraPointsPolicy:
    """RF03: Lógica para otorgar puntos extra."""
    @staticmethod
    def is_applicable(consensus_history: List[bool], has_attendance: bool) -> bool:
        # Si no hay asistencia, no hay puntos extra
        if not has_attendance:
            return False
        # Si la lista de consenso está vacía o hay algún 'False', no aplica (según regla estricta)
        if not consensus_history:
            return False 
        return all(consensus_history)

class GradeCalculatorService:
    """RF04, RNF03: Servicio de cálculo determinista (Stateless)."""
    
    def calculate_final_grade(self, context: StudentContext) -> Dict[str, Any]:
        # 1. Validación
        for evaluation in context.evaluations:
            evaluation.validate()

        # 2. Cálculo Base
        total_weighted_grade = sum(e.weighted_value for e in context.evaluations)
        total_weight = sum(e.weight_percent for e in context.evaluations)
        
        warnings = []
        if total_weight == 0 and context.evaluations:
             warnings.append("El peso total es 0%.")
        elif total_weight != 100.0:
            warnings.append(f"El peso total es {total_weight}%.")
            if total_weight > 100.0:
                total_weighted_grade = (total_weighted_grade / total_weight) * 100.0
                warnings.append("Nota normalizada por exceso de peso.")

        base_grade = total_weighted_grade

        # 3. Reglas de Negocio
        final_grade = base_grade
        points_added = 0.0
        policy_message = "N/A"

        if not context.has_min_attendance:
            final_grade = 0.0
            policy_message = "Reprobado por inasistencia (RF02)."
        else:
            # Llama a la otra clase definida arriba
            if ExtraPointsPolicy.is_applicable(context.historical_teacher_consensus, context.has_min_attendance):
                potential_grade = base_grade + AppConfig.EXTRA_POINTS_VALUE
                final_grade = min(potential_grade, AppConfig.MAX_FINAL_GRADE)
                points_added = final_grade - base_grade
                policy_message = "Puntos extra aplicados."
            else:
                policy_message = "No aplica puntos extra."

        return {
            "student_id": context.student_id,
            "base_grade": round(base_grade, 2),
            "final_grade": round(final_grade, 2),
            "extra_points": round(points_added, 2),
            "attendance_ok": context.has_min_attendance,
            "warnings": warnings,
            "policy_detail": policy_message
        }