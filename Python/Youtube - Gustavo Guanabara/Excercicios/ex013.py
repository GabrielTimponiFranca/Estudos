n1 = float(input("Quanto está recebenmdo hoje? "))
n2 = int(input("Receberá aumento de: "))
s = n1 * (1 + (n2/100))
print("Com aumento de {}% em seu salário, ele passará de R${:.2f}, para R${:.2f}".format(n2, n1, s))