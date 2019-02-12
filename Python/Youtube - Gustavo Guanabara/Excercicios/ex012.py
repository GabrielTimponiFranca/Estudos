n1 = float(input("Digite o preço do produto: "))
n2 = float(input("Quantos porcentos de desconto? "))
s = n1 * (1 - (n2/100))
print("O produto de R${}, com {}% de desconto, fica em R${:.2f}".format(n1, n2, s))