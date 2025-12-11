import numpy as np
import matplotlib.pyplot as plt

# --- 1. CONFIGURAÇÃO DOS PARÂMETROS DO PROJETO ---
# Dados retirados da Tabela 1 para Pablo Gabriel Sustisso
R_L = 6.0          # Impedância da carga em Ohms
fc = 2000.0        # Frequência de corte em Hz
wc = 2 * np.pi * fc # Frequência angular (rad/s)

print("--- PARÂMETROS DE PROJETO ---")
print("Aluno: Pablo Gabriel Sustisso")
print(f"Carga (R): {R_L} Ohms")
print(f"Frequência de Corte (fc): {fc} Hz")
print("-" * 30)

# --- 2. BANCO DE DADOS DE COMPONENTES COMERCIAIS ---
# Valores convertidos para unidades base (Henries e Farads)
# Tabela 2: Indutores (mH -> H) [cite: 41, 42]
indutores_comerciais = np.array([
    0.10, 0.12, 0.15, 0.18, 0.22, 0.27, 0.33, 0.39, 0.47, 0.56, 0.68, 0.82,
    1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2, 10, 12, 15
]) * 1e-3 # Convertendo de mH para Henry

# Tabela 3: Capacitores (uF -> F) [cite: 43, 44]
capacitores_comerciais = np.array([
    1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2,
    10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82, 100
]) * 1e-6 # Convertendo de uF para Farad

# --- 3. FUNÇÕES AUXILIARES ---

def encontrar_mais_proximo(valor_ideal, lista_comercial):
    """Encontra o valor mais próximo numa lista de valores comerciais."""
    idx = (np.abs(lista_comercial - valor_ideal)).argmin()
    return lista_comercial[idx]

def calculo_butterworth_2a_ordem(R, f):
    """
    Calcula L e C para filtro Butterworth de 2a ordem.
    Para Q = 0.707 (Butterworth):
    L = (R * sqrt(2)) / (2 * pi * f)
    C = 1 / (2 * pi * f * R * sqrt(2))
    """
    w = 2 * np.pi * f
    L_ideal = (R * np.sqrt(2)) / w
    C_ideal = 1 / (w * R * np.sqrt(2))
    return L_ideal, C_ideal

# --- 4. CÁLCULO E SELEÇÃO ---

# Cálculo dos valores Ideais
L_ideal, C_ideal = calculo_butterworth_2a_ordem(R_L, fc)

# Seleção dos valores Reais
L_real = encontrar_mais_proximo(L_ideal, indutores_comerciais)
C_real = encontrar_mais_proximo(C_ideal, capacitores_comerciais)

print("\n--- RESULTADOS DOS CÁLCULOS ---")
print(f"Indutor (L): Ideal = {L_ideal*1e3:.4f} mH | Real = {L_real*1e3:.2f} mH")
print(f"Capacitor (C): Ideal = {C_ideal*1e6:.4f} uF | Real = {C_real*1e6:.2f} uF")

# --- 5. SIMULAÇÃO DA RESPOSTA EM FREQUÊNCIA (BODE) ---

# Faixa de frequências para o gráfico (10Hz a 20kHz)
frequencias = np.logspace(1, 4.5, 1000) # De 10^1 a 10^4.5 Hz
w_range = 2 * np.pi * frequencias

# Função de Transferência do Filtro Passa-Baixas (LPF) de 2a Ordem (Circuito LC)
# H_lpf(s) = Z_paralelo / (Z_serie + Z_paralelo)
# Onde L está em série e C está em paralelo com a carga R.
def resposta_lpf(w, L, C, R):
    # Impedâncias
    Z_L = 1j * w * L
    Z_C = 1 / (1j * w * C)
    Z_R = R
    
    # Paralelo de C com R (Carga)
    Z_p = (Z_C * Z_R) / (Z_C + Z_R)
    
    # Divisor de tensão
    H = Z_p / (Z_L + Z_p)
    return H

# Função de Transferência do Filtro Passa-Altas (HPF) de 2a Ordem
# C em série, L em paralelo com a carga R.
def resposta_hpf(w, L, C, R):
    Z_L = 1j * w * L
    Z_C = 1 / (1j * w * C)
    Z_R = R
    
    # Paralelo de L com R (Carga)
    Z_p = (Z_L * Z_R) / (Z_L + Z_R)
    
    # Divisor de tensão
    H = Z_p / (Z_C + Z_p)
    return H

# Calculando as curvas
H_lpf_ideal = resposta_lpf(w_range, L_ideal, C_ideal, R_L)
H_lpf_real = resposta_lpf(w_range, L_real, C_real, R_L)

H_hpf_ideal = resposta_hpf(w_range, L_ideal, C_ideal, R_L)
H_hpf_real = resposta_hpf(w_range, L_real, C_real, R_L)

# Convertendo para dB
mag_lpf_ideal = 20 * np.log10(np.abs(H_lpf_ideal))
mag_lpf_real = 20 * np.log10(np.abs(H_lpf_real))
mag_hpf_ideal = 20 * np.log10(np.abs(H_hpf_ideal))
mag_hpf_real = 20 * np.log10(np.abs(H_hpf_real))

# --- 6. PLOTAGEM ---
plt.figure(figsize=(10, 6))

# Plot Woofer (LPF)
plt.semilogx(frequencias, mag_lpf_ideal, 'b--', label='LPF Ideal (Woofer)', linewidth=1.5)
plt.semilogx(frequencias, mag_lpf_real, 'b-', label='LPF Real (Woofer)', linewidth=2.5)

# Plot Tweeter (HPF)
plt.semilogx(frequencias, mag_hpf_ideal, 'r--', label='HPF Ideal (Tweeter)', linewidth=1.5)
plt.semilogx(frequencias, mag_hpf_real, 'r-', label='HPF Real (Tweeter)', linewidth=2.5)

# Linha de corte e detalhes
plt.axvline(x=fc, color='k', linestyle=':', label=f'Corte {fc/1000:.1f}kHz')
plt.axhline(y=-3, color='gray', linestyle=':', alpha=0.5)

plt.title(f'Resposta em Frequência - Crossover Butterworth 2ª Ordem\nPablo: R={R_L} Ohms, fc={fc} Hz')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Magnitude (dB)')
plt.grid(True, which="both", ls="-", alpha=0.6)
plt.legend()
plt.ylim(-40, 5) # Limita o eixo Y para melhor visualização

# Salvar e mostrar
plt.tight_layout()
plt.savefig('grafico_bode_crossover.png')
plt.show()

print("\nGráfico gerado com sucesso!")