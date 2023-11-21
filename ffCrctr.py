import os

# read the top file you already have
with open ('top.rtf', 'r') as f:
    lines = f.readlines()

# saving atoms in a separate file (for simplicity)
with open ('atoms.temp', 'r') as f:
    for lin in lines:
        if lin.startswith('ATOM'):
            f.write(lin)

# making a temporary file with organized info
with open ('temp.str', 'w') as f:
    for lin in lines:
        lin = lin.replace('ATOM', 'MASS')
        lin = lin.replace(lin.split()[1], '')
        lin = lin.replace(lin.split()[2], '')
        lin = lin.replace(lin.split()[2], '')
        lin = lin.replace(lin.split()[2], '')
        if lin.split()[0] != 'MASS':
            lin.split()[1] = lin.split()[0]
            lin.split()[0] = 'MASS'
        lin = '   '.join(lin.split())
        
        f.write(lin + '\n')

# keeping only unique atoms
os.system("sort temp.str | uniq > mass.str")

with open ('mass.str', 'r') as f:
    lines0 = f.readlines()

# adding atom numbers and making another temporary file
with open ('temp1.str', 'w') as f:
    for i, lind in enumerate(lines0):
        linda = lind.split()[0] + '   ' + str(i+1) + '   ' + lind.split()[1] + '\n'
        f.write(linda)

with open ('temp1.str', 'r') as f:
    lines = f.readlines()

# making final file containing info you need to add to your ff file
with open ('temp2.str', 'w') as f:
    for i, lin in enumerate(lines):
        lin = lin.strip()
        a = lin.split()[2][0]
        if a == 'C':
            f.write(lin + (9 - len(lin.split()[2])) * ' ' + '12.01100 C  !\n')
           
        elif a == 'O':
            f.write(lin + (9 - len(lin.split()[2])) * ' ' + '16.00000 O  !\n')

        elif a == 'H':
            f.write(lin + (9 - len(lin.split()[2])) * ' ' + '1.00800 H  !\n')

        elif a == 'N':
            f.write(lin + (9 - len(lin.split()[2])) * ' ' + '14.0067 N  !\n')

        elif a == 'F':
            f.write(lin + (9 - len(lin.split()[2])) * ' ' + '18.99840 F  !\n')
            
    f.write('!\n')