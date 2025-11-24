from typing import Dict, Any
from models import Evaluation, StudentContext
from services import GradeCalculatorService
import re  # Importante para validar el código

class ConsoleUI:
    def run(self):
        print("=== 🎓 SISTEMA DE CÁLCULO CS3081 ===")
        try:
            # --- INICIO CAMBIO: Validación de ID al principio ---
            student_id = ""
            while True:
                student_id = input("Código del estudiante (Ej. 202310123): ").strip()
                # Validamos que sea Año(20xx) + Ciclo(10/20) + 3 dígitos
                if re.match(r"^20\d{2}(10|20)\d{3}$", student_id):
                    break
                print("❌ Error: Formato inválido. Debe ser Año + 10/20 + 3 dígitos (Ej: 202310123).")
            # --- FIN CAMBIO ---
            
            evaluations = []
            print("\n--- Registro de Evaluaciones ---")
            print("ℹ️  Instrucción: Para terminar, deje el nombre vacío y presione Enter.")
            
            while True:
                # 1. Mostrar estado actual del peso
                current_weight = sum(e.weight_percent for e in evaluations)
                print(f"\n📊 Peso Acumulado Actual: {current_weight}%")
                
                if current_weight >= 100.0:
                    print("⚠️  AVISO: Ya llegaste o superaste el 100%.")
                    print("   - Presiona ENTER sin escribir nombre para calcular.")
                    print("   - O escribe otro nombre para agregar (se generará advertencia de inconsistencia).")

                # 2. Solicitar nombre (Condición de salida)
                name = input("Nombre Evaluación: ").strip()
                
                # Si el usuario da Enter vacío, rompemos el bucle
                if not name: 
                    break
                
                try:
                    grade = float(input(f"  Nota '{name}': "))
                    weight = float(input(f"  Peso % '{name}': "))
                    evaluations.append(Evaluation(name, grade, weight))
                except ValueError:
                    print("  ❌ Error: Ingrese números válidos (ej. 15.5).")

            # 3. Resto del flujo (Asistencia y Políticas)
            att_input = input("\n¿Cumplió asistencia mínima? (S/N): ").strip().upper()
            has_attendance = (att_input == 'S')

            print("\n--- Historial Consenso Docente (ej: S,S,N) ---")
            policy_input = input("Historial (Enter si no hay datos): ").strip().upper()
            consensus = [x.strip() == 'S' for x in policy_input.split(',')] if policy_input else []

            # 4. Cálculo
            # Como ya validamos el ID arriba, aquí pasará sin problemas
            context = StudentContext(student_id, evaluations, has_attendance, consensus)
            calculator = GradeCalculatorService()
            report = calculator.calculate_final_grade(context)

            self._print_report(report)

        except Exception as e:
            # Si models.py rechaza algo que se nos pasó, aparecerá aquí
            print(f"\n❌ Error en el sistema: {e}")

    def _print_report(self, data: Dict[str, Any]):
        print("\n" + "="*40)
        print(f"📄 REPORTE FINAL: {data['student_id']}")
        print("="*40)
        
        print(f"• Evaluaciones registradas: {data.get('evaluations_count', 'N/A')}")
        print(f"• Nota Base Ponderada:  {data['base_grade']}")
        print(f"• Puntos Extra (+):     {data['extra_points']}")
        print(f"• Asistencia:           {'✅ Cumple' if data['attendance_ok'] else '❌ No cumple'}")
        print("-" * 40)
        print(f"• NOTA FINAL:           {data['final_grade']} / 20")
        print("-" * 40)
        print(f"ℹ️  Política aplicada: {data['policy_detail']}")
        
        if data['warnings']:
            print("\n⚠️  OBSERVACIONES E INCONSISTENCIAS (RF05):")
            for w in data['warnings']:
                print(f"  - {w}")
        print("="*40 + "\n")