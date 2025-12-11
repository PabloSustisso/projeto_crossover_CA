\# Projeto de Crossover Passivo - Filtros Butterworth de 2ª Ordem



\*\*Autor:\*\* Pablo Gabriel Sustisso  

\*\*Disciplina:\*\* Circuitos de Corrente Alternada (CC44CP)  

\*\*Instituição:\*\* UTFPR - Campus Pato Branco  

\*\*Professor:\*\* Dr. Eng. Dionatan Cieslak



---



\## 1. Apresentação do Problema

Em sistemas de áudio de alta fidelidade, é necessário separar o espectro de frequências para que cada alto-falante reproduza apenas a faixa para a qual foi projetado. Enviar frequências baixas para um tweeter pode queimá-lo, enquanto enviar frequências altas para um woofer resulta em distorção e perda de energia.



O problema proposto consiste no projeto de um \*\*Crossover Passivo de Duas Vias\*\*, utilizando filtros LC (Indutor e Capacitor) para dividir o sinal de entrada entre um Woofer (frequências baixas) e um Tweeter (frequências altas).



\## 2. Objetivos e Especificações

O objetivo deste projeto é desenvolver uma ferramenta computacional para calcular, selecionar componentes comerciais e simular a resposta de frequência dos filtros.



\*\*Especificações do Projeto (Baseado na Tabela 1):\*\*

\* \*\*Tipo de Filtro:\*\* Butterworth de 2ª Ordem (resposta maximamente plana).

\* \*\*Atenuação:\*\* 12 dB/oitava.

\* \*\*Impedância da Carga ($R\_L$):\*\* $6.0 \\, \\Omega$.

\* \*\*Frequência de Corte ($f\_c$):\*\* $2.0 \\, \\text{kHz}$ ($2000 \\, \\text{Hz}$).



O projeto engloba:

1\.  \*\*Filtro Passa-Baixas (LPF):\*\* Para o Woofer.

2\.  \*\*Filtro Passa-Altas (HPF):\*\* Para o Tweeter.



\## 3. Funções de Transferência e Fórmulas



Para um filtro Butterworth de 2ª ordem, o fator de amortecimento é $\\zeta = 0.707$ ($Q = 0.707$). As fórmulas utilizadas para o cálculo dos componentes ideais são:



\*\*Cálculo dos Componentes:\*\*

$$L\_{ideal} = \\frac{R \\cdot \\sqrt{2}}{\\omega\_c}$$

$$C\_{ideal} = \\frac{1}{\\omega\_c \\cdot R \\cdot \\sqrt{2}}$$



Onde $\\omega\_c = 2 \\pi f\_c$.



\*\*Funções de Transferência (Modelagem no Código):\*\*

O código modela o circuito como divisores de tensão complexos, considerando a impedância da carga ($R\_L$).



\* \*\*LPF (Woofer):\*\* Indutor em série, Capacitor em paralelo com a Carga.

&nbsp;   $$H\_{LPF}(s) = \\frac{Z\_{paralelo}}{Z\_L + Z\_{paralelo}}$$

&nbsp;   Onde $Z\_{paralelo} = R\_L \\parallel Z\_C$.



\* \*\*HPF (Tweeter):\*\* Capacitor em série, Indutor em paralelo com a Carga.

&nbsp;   $$H\_{HPF}(s) = \\frac{Z\_{paralelo}}{Z\_C + Z\_{paralelo}}$$

&nbsp;   Onde $Z\_{paralelo} = R\_L \\parallel Z\_L$.



\## 4. Lógica do Programa

O script foi desenvolvido em \*\*Python\*\* utilizando as bibliotecas `numpy` (cálculos vetoriais) e `matplotlib` (plotagem). A lógica segue o fluxo:



1\.  \*\*Entrada de Dados:\*\* Definição de $R\_L$ e $f\_c$ conforme especificado para o aluno.

2\.  \*\*Banco de Dados:\*\* Vetores contendo os valores comerciais padrão de Indutores (Tabela 2) e Capacitores (Tabela 3).

3\.  \*\*Cálculo Ideal:\*\* Aplicação das fórmulas de Butterworth para encontrar $L$ e $C$ exatos.

4\.  \*\*Seleção Comercial:\*\* Um algoritmo de busca (`argmin`) encontra dentro dos vetores de componentes comerciais o valor que possui a menor diferença absoluta em relação ao valor ideal calculado.

5\.  \*\*Simulação:\*\* O código calcula a resposta em frequência (Magnitude em dB) para uma faixa de 10Hz a 30kHz, tanto para os componentes ideais quanto para os reais.

6\.  \*\*Visualização:\*\* Gera e salva o Gráfico de Bode comparativo.



\## 5. Como Executar o Código



\### Pré-requisitos

É necessário ter o Python instalado e as seguintes bibliotecas:

```bash

pip install numpy matplotlib

