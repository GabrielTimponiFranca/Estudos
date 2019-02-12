n1 = float(input("Quantos metros de altura tem sua parede? [em cm] "))
n2 = float(input("e, quantos metros de largura tem essa parede? [em cm] "))
litros = 2
s = ((n1/100) * (n2/100)) / litros
print("Sua parede de {} por {} metros, necessita de {:.2f} litros de tinta para ser pintada".format(n1/100, n2/100, s))