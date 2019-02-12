n1 = float(input("Digite quantos reais possui na carteira: "))
dolar = 3.27
s = n1 / dolar
print("Com R${:.2f}, na sua carteira, vocë pode comprar ${:.2f}.".format(n1, s))