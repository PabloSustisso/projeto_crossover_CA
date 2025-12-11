# Projeto de Crossover Passivo - Filtros Butterworth de 2ª Ordem

**Autor:** Pablo Gabriel Sustisso  
**Disciplina:** Circuitos de Corrente Alternada (CC44CP)  
**Instituição:** UTFPR - Campus Pato Branco  
**Professor:** Dr. Eng. Dionatan Cieslak

---

## 1. Apresentação do Problema
Em sistemas de áudio de alta fidelidade, é necessário separar o espectro de frequências para que cada alto-falante reproduza apenas a faixa para a qual foi projetado. Enviar frequências baixas para um tweeter pode queimá-lo, enquanto enviar frequências altas para um woofer resulta em distorção e perda de energia.

O problema proposto consiste no projeto de um **Crossover Passivo de Duas Vias**, utilizando filtros LC (Indutor e Capacitor) para dividir o sinal de entrada entre um Woofer (frequências baixas) e um Tweeter (frequências altas).

## 2. Objetivos e Especificações
O objetivo deste projeto é desenvolver uma ferramenta computacional para calcular, selecionar componentes comerciais e simular a resposta de frequência dos filtros.

**Especificações do Projeto (Baseado na Tabela 1):**
* **Tipo de Filtro:** Butterworth de 2ª Ordem (resposta maximamente plana).
* **Atenuação:** 12 dB/oitava.
* **Impedância da Carga ($R_L$):** $6.0 \, \Omega$.
* **Frequência de Corte ($f_c$):** $2.0 \, \text{kHz}$ ($2000 \, \text{Hz}$).

O projeto engloba:
1.  **Filtro Passa-Baixas (LPF):** Para o Woofer.
2.  **Filtro Passa-Altas (HPF):** Para o Tweeter.

## 3. Funções de Transferência e Fórmulas

Para um filtro Butterworth de 2ª ordem, o fator de amortecimento é $\zeta = 0.707$ ($Q = 0.707$). As fórmulas utilizadas para o cálculo dos componentes ideais são:

**Cálculo dos Componentes:**
$$L_{ideal} = \frac{R \cdot \sqrt{2}}{\omega_c}$$
$$C_{ideal} = \frac{1}{\omega_c \cdot R \cdot \sqrt{2}}$$

Onde $\omega_c = 2 \pi f_c$.

**Funções de Transferência (Modelagem no Código):**
O código modela o circuito como divisores de tensão complexos, considerando a impedância da carga ($R_L$).

* **LPF (Woofer):** Indutor em série, Capacitor em paralelo com a Carga.
    $$H_{LPF}(s) = \frac{Z_{paralelo}}{Z_L + Z_{paralelo}}$$
    Onde $Z_{paralelo} = R_L \parallel Z_C$.

* **HPF (Tweeter):** Capacitor em série, Indutor em paralelo com a Carga.
    $$H_{HPF}(s) = \frac{Z_{paralelo}}{Z_C + Z_{paralelo}}$$
    Onde $Z_{paralelo} = R_L \parallel Z_L$.

## 4. Lógica do Programa
O script foi desenvolvido em **Python** utilizando as bibliotecas `numpy` (cálculos vetoriais) e `matplotlib` (plotagem). A lógica segue o fluxo:

1.  **Entrada de Dados:** Definição de $R_L$ e $f_c$ conforme especificado para o aluno.
2.  **Banco de Dados:** Vetores contendo os valores comerciais padrão de Indutores (Tabela 2) e Capacitores (Tabela 3).
3.  **Cálculo Ideal:** Aplicação das fórmulas de Butterworth para encontrar $L$ e $C$ exatos.
4.  **Seleção Comercial:** Um algoritmo de busca (`argmin`) encontra dentro dos vetores de componentes comerciais o valor que possui a menor diferença absoluta em relação ao valor ideal calculado.
5.  **Simulação:** O código calcula a resposta em frequência (Magnitude em dB) para uma faixa de 10Hz a 30kHz, tanto para os componentes ideais quanto para os reais.
6.  **Visualização:** Gera e salva o Gráfico de Bode comparativo.

## 5. Como Executar o Código

### Pré-requisitos
É necessário ter o Python instalado e as seguintes bibliotecas:
```bash
pip install numpy matplotlib
```

## 6. Análise dos Resultados
Com base na impedância de 6 Ohms e frequência de corte de 2000 Hz, o software obteve os seguintes resultados:
### Indutor(L)
1. **Valor Ideal Calculado**: $0.6752 \ \text{mH}$
2. **Valor Comercial Selecionado**: $0.68 \ \text{mH}$
3. **Erro Aproximado**: $+0.7\$%
### Capacitor(C)
1. **Valor Ideal Calculado**: $9.378 \ \mu\text{F}$
2. **Valor Comercial Selecionado**: $10.0 \ \mu\text{F}$
3. **Erro Aproximado**: $+6.6\$%

## 7. Análise Crítica
A discretização dos componentes introduz alterações no comportamento do filtro:
1. Indutor: A diferença entre $0.675 \text{mH}$ (ideal) e $0.68 \text{mH}$ (real) é ínfima (< 1%). O impacto desta escolha é desprezível.
2. Capacitor: A diferença entre $9.37 \mu\text{F}$ (ideal) e $10 \mu\text{F}$ (real) é mais perceptível (~6.6%).
2.1 Impacto Prático: Como o capacitor real é maior que o ideal, e a frequência de corte é inversamente proporcional a $\sqrt{LC}$, a frequência de corte real do filtro deslocou-se ligeiramente para baixo (menor que 2000 Hz).
2.2 Audibilidade: Em um ambiente de áudio real, um desvio de 6% na frequência de corte (caindo para aproximadamente 1.9 kHz) dificilmente seria audível para o ouvido humano destreinado, mantendo a integridade do sistema. A transição continua suave, sem picos de ressonância perigosos, pois os valores estão próximos o suficiente para manter o fator de qualidade ($Q$) próximo de 0.707.


