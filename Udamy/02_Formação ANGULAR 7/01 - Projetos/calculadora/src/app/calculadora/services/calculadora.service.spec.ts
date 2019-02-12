import { TestBed } from '@angular/core/testing';

import { CalculadoraService } from './calculadora.service';

describe('CalculadoraService', () => {
  beforeEach(() => TestBed.configureTestingModule({
    providers: [CalculadoraService]
  }));

  it('should be created', () => {
    const service: CalculadoraService = TestBed.get(CalculadoraService);
    expect(service).toBeTruthy();
  });

  it('deve garantir que 1 + 4 = 5', () => {
    const service: CalculadoraService = TestBed.get(CalculadoraService);
    expect(service.calcular(1, 4, CalculadoraService.SOMA)).toEqual(5);
  });

  it('deve garantir que 1 - 4 = -3', () => {
    const service: CalculadoraService = TestBed.get(CalculadoraService);
    expect(service.calcular(1, 4, CalculadoraService.SUBTRACAO)).toEqual(-3);
  });

  it('deve garantir que 1 / 4 = 0.25', () => {
    const service: CalculadoraService = TestBed.get(CalculadoraService);
    expect(service.calcular(1, 4, CalculadoraService.DIVISAO)).toEqual(0.25);
  });

  it('deve garantir que 1 * 4 = 4', () => {
    const service: CalculadoraService = TestBed.get(CalculadoraService);
    expect(service.calcular(1, 4, CalculadoraService.MULTIPLICACAO)).toEqual(4);
  });

  it('deve retornar 0 para operação inválida', () => {
    const service: CalculadoraService = TestBed.get(CalculadoraService);
    expect(service.calcular(1, 4, '%')).toEqual(0);
  });
});
