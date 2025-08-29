#!/usr/bin/env python3
"""
Script de prueba para verificar la interfaz del brazo robótico
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Prueba que todas las importaciones funcionen"""
    print("🔍 Probando importaciones...")
    
    try:
        from Arm import Arm
        print("✅ Arm importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando Arm: {e}")
        return False
    
    try:
        from Vector import Vector
        print("✅ Vector importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando Vector: {e}")
        return False
    
    try:
        from ImprovedGeneticSolver import ImprovedGeneticSolver
        print("✅ ImprovedGeneticSolver importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando ImprovedGeneticSolver: {e}")
        return False
    
    try:
        from window.glWidget import ArmGLWidget
        print("✅ ArmGLWidget importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando ArmGLWidget: {e}")
        return False
    
    return True

def test_arm_functionality():
    """Prueba la funcionalidad básica del brazo"""
    print("\n🤖 Probando funcionalidad del brazo...")
    
    try:
        from Arm import Arm
        
        # Crear brazo
        arm = Arm(3.0, 2.5, 2.0)
        print("✅ Brazo creado correctamente")
        
        # Probar actualización
        arm.actualizeArm(
            {'gama': 0, 'theta': 0},
            {'gama': 0, 'theta': 0},
            {'gama': 0, 'theta': 0}
        )
        print("✅ Brazo actualizado correctamente")
        
        # Obtener posición final
        final_pos = arm.getArmFinalPoint()
        print(f"✅ Posición final: ({final_pos['x']:.2f}, {final_pos['y']:.2f}, {final_pos['z']:.2f})")
        
        return True
    except Exception as e:
        print(f"❌ Error en funcionalidad del brazo: {e}")
        return False

def test_genetic_solver():
    """Prueba el solver genético"""
    print("\n🧬 Probando solver genético...")
    
    try:
        from ImprovedGeneticSolver import ImprovedGeneticSolver
        
        # Crear solver
        solver = ImprovedGeneticSolver(
            arm1Len=3.0,
            arm2Len=2.5,
            arm3Len=2.0,
            goalPoint={'x': 2.0, 'y': 1.0, 'z': 2.0}
        )
        print("✅ Solver genético creado correctamente")
        
        # Verificar si el punto es alcanzable
        is_possible = solver.is_possible_shot()
        print(f"✅ Punto objetivo alcanzable: {is_possible}")
        
        return True
    except Exception as e:
        print(f"❌ Error en solver genético: {e}")
        return False

def test_ui_file():
    """Prueba que el archivo UI existe y es válido"""
    print("\n🎨 Probando archivo UI...")
    
    ui_file = os.path.join("window", "main.ui")
    if os.path.exists(ui_file):
        print("✅ Archivo UI encontrado")
        
        # Verificar que es un archivo XML válido
        try:
            with open(ui_file, 'r') as f:
                content = f.read()
                if '<?xml' in content and 'QMainWindow' in content:
                    print("✅ Archivo UI parece ser válido")
                    return True
                else:
                    print("❌ Archivo UI no parece ser un archivo UI válido")
                    return False
        except Exception as e:
            print(f"❌ Error leyendo archivo UI: {e}")
            return False
    else:
        print("❌ Archivo UI no encontrado")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas de la interfaz del brazo robótico")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_arm_functionality,
        test_genetic_solver,
        test_ui_file
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! La interfaz está lista para usar.")
        print("\nPara ejecutar la aplicación:")
        print("  python main.py")
        return True
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
