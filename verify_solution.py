#!/usr/bin/env python3
"""
Script de verificación final para confirmar que la solución funciona
"""

import sys
import os

def verify_ui_file():
    """Verifica que el archivo UI esté correctamente formateado"""
    print("🔍 Verificando archivo UI...")
    
    ui_file = os.path.join("window", "main.ui")
    if not os.path.exists(ui_file):
        print("❌ Archivo UI no encontrado")
        return False
    
    try:
        with open(ui_file, 'r') as f:
            content = f.read()
            
        # Verificar que no hay layouts anidados incorrectamente
        if '<widget class="QHBoxLayout"' in content:
            print("❌ Error: QHBoxLayout definido como widget en lugar de layout")
            return False
        
        if '<layout class="QHBoxLayout"' in content:
            print("✅ QHBoxLayout definido correctamente como layout")
        
        # Verificar estructura básica
        if 'QMainWindow' in content and 'QOpenGLWidget' in content:
            print("✅ Estructura básica del UI correcta")
            return True
        else:
            print("❌ Estructura básica del UI incorrecta")
            return False
            
    except Exception as e:
        print(f"❌ Error leyendo archivo UI: {e}")
        return False

def verify_imports():
    """Verifica que todas las importaciones funcionen"""
    print("\n📦 Verificando importaciones...")
    
    try:
        from PyQt5 import QtWidgets, uic
        print("✅ PyQt5 importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando PyQt5: {e}")
        return False
    
    try:
        from Arm import Arm
        print("✅ Arm importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando Arm: {e}")
        return False
    
    try:
        from ImprovedGeneticSolver import ImprovedGeneticSolver
        print("✅ ImprovedGeneticSolver importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando ImprovedGeneticSolver: {e}")
        return False
    
    return True

def verify_ui_loading():
    """Verifica que el archivo UI se pueda cargar correctamente"""
    print("\n🎨 Verificando carga del archivo UI...")
    
    try:
        from PyQt5 import QtWidgets, uic
        
        # Crear aplicación temporal
        app = QtWidgets.QApplication.instance()
        if app is None:
            app = QtWidgets.QApplication(sys.argv)
        
        # Cargar UI
        ui_file = os.path.join("window", "main.ui")
        window = QtWidgets.QMainWindow()
        uic.loadUi(ui_file, window)
        
        print("✅ Archivo UI cargado correctamente")
        
        # Verificar que los widgets principales existen
        required_widgets = [
            'openGLWidget', 'targetGroup', 'angleGroup', 'infoGroup',
            'slider_theta1', 'slider_gamma1', 'slider_theta2', 'slider_gamma2',
            'slider_theta3', 'slider_gamma3', 'btn_visualize', 'btn_reset'
        ]
        
        for widget_name in required_widgets:
            if hasattr(window, widget_name):
                print(f"✅ Widget {widget_name} encontrado")
            else:
                print(f"❌ Widget {widget_name} no encontrado")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error cargando UI: {e}")
        return False

def verify_arm_functionality():
    """Verifica la funcionalidad básica del brazo"""
    print("\n🤖 Verificando funcionalidad del brazo...")
    
    try:
        from Arm import Arm
        
        # Crear brazo
        arm = Arm(3.0, 2.5, 2.0)
        
        # Probar actualización
        arm.actualizeArm(
            {'gama': 0, 'theta': 0},
            {'gama': 0, 'theta': 0},
            {'gama': 0, 'theta': 0}
        )
        
        # Obtener posición final
        final_pos = arm.getArmFinalPoint()
        
        print(f"✅ Brazo funcionando correctamente - Posición: ({final_pos['x']:.2f}, {final_pos['y']:.2f}, {final_pos['z']:.2f})")
        return True
        
    except Exception as e:
        print(f"❌ Error en funcionalidad del brazo: {e}")
        return False

def verify_genetic_solver():
    """Verifica el solver genético"""
    print("\n🧬 Verificando solver genético...")
    
    try:
        from ImprovedGeneticSolver import ImprovedGeneticSolver
        
        # Crear solver
        solver = ImprovedGeneticSolver(
            arm1Len=3.0,
            arm2Len=2.5,
            arm3Len=2.0,
            goalPoint={'x': 2.0, 'y': 1.0, 'z': 2.0}
        )
        
        # Verificar si el punto es alcanzable
        is_possible = solver.is_possible_shot()
        
        print(f"✅ Solver genético funcionando - Punto alcanzable: {is_possible}")
        return True
        
    except Exception as e:
        print(f"❌ Error en solver genético: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("🔍 Verificación Final de la Solución SpacialArm")
    print("=" * 50)
    
    tests = [
        verify_ui_file,
        verify_imports,
        verify_ui_loading,
        verify_arm_functionality,
        verify_genetic_solver
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Resultados: {passed}/{total} verificaciones pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las verificaciones pasaron!")
        print("✅ El error de layout ha sido completamente solucionado")
        print("✅ La aplicación está lista para usar")
        print("\n🚀 Para ejecutar la aplicación:")
        print("  ./run_from_terminal.sh")
        print("  o")
        print("  source .venv/bin/activate && python main.py")
        return True
    else:
        print("⚠️  Algunas verificaciones fallaron")
        print("❌ Revisa los errores arriba")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
