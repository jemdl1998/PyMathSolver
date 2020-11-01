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


'''
En este TextInput El usuario ingresa el codio a evaluar
error muestra el estado del codigo (cambiar a state)
firstThread es el hilo que se inicia para ejecutar clasificateLines y evitar que el programa se realentice
solve 
continua indica al programa si hay un error o no antes de proseguir
La funcion clasificateLines
clasificateLines se encarga de separar todas las lineas del codigo que ingreso el usuario e identifica
a que tipo de linea pertenece: (Antes de esto eliminar cualquier espacio en el codigo)
f(x): Es una función
x(0): Hace referencia al valor inicial de la variable independiente
y: es una variable
Example:
f(x) = x - y
x(0) = 0
y = 2
La raiz de la funcion y por lo tanto la respuesta sera 2
Despues crea un diccionario en el cual guarda cada funcion de la siguiente forma
ejemplo:
f(x) = x - 2
x(0) = 10
{f(x): {initx : 10,'function':'x-2'}}

De esta forma no importa el orden en el que el usuario a ingresado las ecuaciones o valores
iniciales. (para esto me ayudo de la variable)
'''
from kivy.uix.textinput import TextInput
from threading import Thread


class NonLinearInput(TextInput):
    def __init__(self,**kwargs):
        self.error = 'Fine'
        self.firstThread = Thread(target=self.clasificateLines,)
        self.firstThread.start()
        self.continua = True
        super(NonLinearInput,self).__init__(**kwargs)

    def clasificateLines(self,status):
        self.text = self.text.strip()
        self.lines = self.text.split('\n')
        self.functions =[]
        self.vars = []
        self.init= []
        self.fD= {}
        
        
        while True:
            for index,line in enumerate(self.lines):
                if '^' in line:
                    self.lines[index] = line.replace('^','**')
                elif '=' not in line:
                    self.lines.pop(index)
            for index,line in enumerate(self.lines):
                self.lines[index] = line.replace(' ','')

            for index,line in enumerate(self.lines):
                
                if 'f(' in line or 'F(' in line:
                    
                    self.functions.append(line)

                elif '(0)' in line:
                    
                    self.init.append(line)
                else:
                    self.vars.append(line)
            # Raise Error for the user
            if len(self.functions) != len(self.init):
                print('diferente')
                status.text = '[color=ff1b00]You still need to declare an initial value[/color]'
                break
            if self.functions==[]:
                status.text = '[color=ff1b00]You still need to declare any function[/color]'
                break
            self.eqindex = 0
            self.temp_var=''
            self.temp_list_vars=[]
            for var in self.vars:
                self.eqindex = var.index('=')
                for i in range(0,self.eqindex):
                    self.temp_var+=var[i]
                self.temp_list_vars.append(self.temp_var)
                self.temp_var = ''
            for var in self.temp_list_vars:
                if self.temp_list_vars.count(var)>1:
                    status.text = '[color=ff1b00]the variable {} were declared more than once[/color]'.format(var)
                    self.continua = False
            for function in self.functions:
                if self.functions.count(function) >1:
                    status.text = '[color=ff1b00]the function {} were declared more than once[/color]'.format(function)
                    self.continua = False
            else:
                #Make a dictionary
                self.temp_var_init = ''
                self.temp_value = ''
                self.eqindex = 0
                self.initvars ={} #For estructure the dictionary
                for i in self.init:
                    self.parentindex = i.index('(')
                    self.eqindex = i.index('=')
                    for index in range(0,self.parentindex):
                        self.temp_var_init=i[index]
                    for index in range(self.eqindex+1,len(i)):
                        self.temp_value+=i[index]
                    self.initvars[self.temp_var_init] = self.temp_value
                    self.temp_var_init=''
                    self.temp_var_init = ''
                else:
                    self.independent_vars =[]
                    for key,var in self.initvars.items():
                        self.fD['f{}'.format(key)] = {'init{}'.format(key):var,'function':None}
                        self.independent_vars.append(key)
                    self.eqindex = ''
                    for function in self.functions:
                        self.temp_var_function = ''
                        self.temp_function=''
                        self.varindexL = function.index('(')
                        self.varindexR = function.index(')')
                        self.eqindex = function.index('=')
                        for letter in range(self.eqindex+1,len(function)):
                            self.temp_function+= function[letter]
                        for letter in range(self.varindexL+1,self.varindexR):
                            self.temp_var_function += function[letter]
                        try:
                            self.fD['f{}'.format(self.temp_var_function)]['function']= self.temp_function
                            status.text = 'Fine'
                        except:
                            self.continua = False
                            status.text = '[color=ff1b00]Apparently there is a problem with your functions and initial values[/color]'
                        self.temp_var_function = ''
                        self.temp_function=''
                    print(self.fD)
                    print(self.temp_list_vars)
                    if self.continua == True:
                        ######Logica de solucion########
                        #1 Crear las lineas de importacion
                        self.imports = 'from sympy import Symbol\nfrom scipy.optimize import fsolve\nfrom math import log,exp,sin,cos,tan\n'
                        #2 funcion
                        self.function='def fun(V):\n'
                        #3 asignar valores
                        self.asignVarInit = '    '
                        for independent in self.independent_vars:
                            self.asignVarInit+=independent+','
                        self.asignVarInit+='='
                        
                        self.asignVarInit+='V\n'
                        
                        #4 declara variables
                        self.declarationVars = ''
                        for var in self.vars:
                            self.declarationVars+='    {}\n'.format(var)
                        #5 funciones y return
                        self.functions_declaration=''
                        self.returnfuncton ='    return '
                        for independent in self.independent_vars:
                            self.functions_declaration+='    f{}={}\n'.format(independent,self.fD['f{}'.format(independent)]['function'])
                            self.returnfuncton+='f{}, '.format(independent)
                        self.returnfuncton+='\n'
                        ### 6 solve this shit!
                        self.solvesol ='self.solution = fsolve(fun,['
                        for i in self.independent_vars:
                            self.solvesol+=self.fD['f{}'.format(i)]['init{}'.format(i)]+','
                        self.solvesol+= '])'


                        self.code = self.imports+self.function+self.asignVarInit+self.declarationVars+self.functions_declaration+self.returnfuncton+self.solvesol
                        #print(self.code)
                        
                        #str(self.solution)
                        
                        

                        ######Hasta aqui va la logica de solucion##########
                    else:
                        pass
                break
            break
            
            

            
    
            

    


    
    
