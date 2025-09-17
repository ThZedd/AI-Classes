#Exercícios 1, 2 e 3
num_est = input("Número de Estudante: \n")

nome = input("Nome: \n")

curso = input("Curso: \n")

def get_grades():
    grades = []
    input_grades = float(input("Introduza notas (-1 para sair):\n"))
    while not input_grades == -1:
        grades.append(float(input_grades)) 
        input_grades = float(input())
    return grades

     
def calc_avg(grades):
    print(f"Olá {nome} [{num_est}] \nBem vindo ao curso de {curso}")

    print(f"Media: {sum(grades)/ len(grades) if len(grades) else 0}  {grades}")
    
calc_avg(get_grades())