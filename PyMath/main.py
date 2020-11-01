#    This file is part of PyMathSolver.

#    PyMathSolver is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    PyMathSolver is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Foobar.  If not, see <https://www.gnu.org/licenses/>.


from kivy.config import Config
Config.set('graphics', 'resizable', False)


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen,SlideTransition,NoTransition
from kivy.uix.boxlayout import BoxLayout

from kivy.core.window import Window

from UIpy.homeScreen import homeScreen
from UIpy.nonLinearScreen import nonLinearScreen
from UIpy.resultScreen import resultScreen
from modules.solve import Solver

from threading import Thread


#Para poder acceder a los labels de la pantalla de resultados
result_screen = resultScreen(name = 'Results')

class mainApp(App):
    #La resolucion inicial es para evitar la deformacion de los iconos por ahora,
    #Solver() es la clase que resuelve el codigo
    #sm es el Screen Manager
    #Solo result_screen se encuentra instanciado para poder acceder a sus Ids
    def build(self,**kwargs):
        self.window = Window
        self.window.size = (600, 450) # 
        self.solver = Solver()
        self.title = 'PyMath'
        self.sm = ScreenManager()
        self.sm.add_widget(homeScreen(name= 'home'))
        self.sm.add_widget(nonLinearScreen(name = 'nonLinear' ))
        self.sm.add_widget(result_screen)
        
        return self.sm
        
    def nonLinearWindow(self):
        self.window.size = (900,600)
        self.sm.transition = SlideTransition(direction = 'up',duration = .4)
        self.sm.current = 'nonLinear'
    
    def backButton(self):
        self.window.size = (600,450)
        self.sm.transition = SlideTransition(direction = 'down',duration = .4)
        self.sm.current = 'home'

    def solveButton(self,code):
        #Resuelve el codio y lo guarda en las diferentes variables dependiendo del modo
        result_screen.ids.lbl_solution.text = '[color=ff1b00]{}[/color]'.format(str(self.solver.solve(code)))
        print(code)
    #El boton de solucion se espera que ejecute esta funcion para todos los modos.
    def start_solve_thread(self,code):
        thread = Thread(target=self.solveButton,args=(code,))
        thread.start()
    


if __name__ == "__main__":
    mainApp().run()