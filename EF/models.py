import re  # <--- Importante: Librería de Expresiones Regulares
from dataclasses import dataclass
from typing import List
from config import AppConfig

@dataclass
class Evaluation:
    """RF01: Representa una evaluación inmutable."""
    name: str
    grade: float
    weight_percent: float

    def validate(self):
        if not (AppConfig.MIN_GRADE <= self.grade <= AppConfig.MAX_FINAL_GRADE):
            raise ValueError(f"La nota de '{self.name}' debe estar entre {AppConfig.MIN_GRADE} y {AppConfig.MAX_FINAL_GRADE}.")
        if not (0 <= self.weight_percent <= AppConfig.MAX_WEIGHT_PERCENT):
            raise ValueError(f"El peso de '{self.name}' debe estar entre 0 y 100.")

    @property
    def weighted_value(self) -> float:
        return self.grade * (self.weight_percent / 100.0)

@dataclass
class StudentContext:
    """Agrupa toda la información del estudiante para el cálculo."""
    student_id: str
    evaluations: List[Evaluation]
    has_min_attendance: bool
    historical_teacher_consensus: List[bool]

    def __post_init__(self):
        """Se ejecuta automáticamente al crear el objeto."""
        self._validate_id_format()
        self._validate_evaluations_limit()  # <--- NUEVO: Llama a la validación de cantidad

    def _validate_id_format(self):
        """
        Valida el formato de seguridad del código UTEC.
        Formato: YYYY (Año) + 10/20 (Ciclo) + XXX (Aleatorio)
        Total: 9 dígitos.
        Ejemplo válido: 202310456
        """
        # Explicación del Regex:
        # ^      -> Inicio de la cadena
        # 20\d{2}-> Año: Empieza con 20 y siguen 2 dígitos (ej. 2021, 2025)
        # (10|20)-> Ciclo: Estrictamente 10 o 20
        # \d{3}  -> Aleatorio: Exactamente 3 dígitos
        # $      -> Fin de la cadena
        pattern = r"^20\d{2}(10|20)\d{3}$"
        
        if not re.match(pattern, self.student_id):
            raise ValueError(f"ID inválido '{self.student_id}'. Debe ser Año + 10/20 + 3 dígitos (Ej: 202310123).")

    def _validate_evaluations_limit(self):
        """
        Validación lógica para evitar sobrecarga de datos.
        Límite máximo de 10 evaluaciones por alumno.
        """
        if len(self.evaluations) > 10:
            raise ValueError(f"No se pueden registrar más de 10 evaluaciones (Tienes {len(self.evaluations)}).")