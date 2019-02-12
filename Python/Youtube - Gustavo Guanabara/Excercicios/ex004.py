n = input('Digite algo: ')
print(('O tipo primitivo desse valor é', type(n))
print('Só tem espaço? ', n.isspace())
print('É um número? ', n.isnumeric())
print('É alfabético? ', n.isalpha())
print('É alfanumérico? ', n.isalnum())
print('Está em maiúscula? ', n.isupper())
print('Está em minúscula? ', n.islower())
print('Está capitalizado? ', n.istitle())
if n.isnumeric():
    print('A palavra digitada, {}, é numerica'.format(n))
elif n.isalpha():
    print('A palavra digitada, {}, é uma string'.format(n))
elif n.isalnum():
    print('A palavra digitada, {}, é alpha numerica'. format(n))
elif n.isspace(): 