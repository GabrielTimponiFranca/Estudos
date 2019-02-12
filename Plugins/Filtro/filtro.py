# coding=utf-8

import numpy

# Filtro de média móvel de ordem "ord"
def filtMean(epmTag, ord):
  epmData = epmTag.copy()
  # Atribui à variável apenas a coluna dos valores
  epm_values = epmData['Value']
  # Variável auxiliar que terá a soma dos valores.
  # De 3 em 3 , se Ord=3, etc.
  epm_values_aux = epm_values.copy()
 
  # Esse laço faz a soma dos valores
  for i in range( 1, ord ):
    # Pega desde o indice 'i' até o fim do array
    # e concatena com zeros no final
    epm_values_aux += numpy.hstack( (epm_values[i:], numpy.zeros(i)) )
 
  # Calcula a média dos valores
  epm_values_aux /= ord
 
  # Esse laço apenas copia os últimos 'Ord-1' valores originais
  for i in range( 1, ord ):
    epm_values_aux[-i] = epmData['Value'][-i]
 
  # Joga os valores de volta ao objeto Numpy Array
  epmData['Value'] = epm_values_aux.copy()
  return epmData