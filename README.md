<div align="center">
<img align="left" img src="assets/robo.png" width="120"  height="120" alt="Robô dançando" />

# Projeto de Microcontroladores: Robô dançante

<span style="text-decoration:none color:black;">[Gabriela Scofield](https://github.com/GabiScof)</span>, <span style="text-decoration:none; color:black;">[Aurora Richaud](https://github.com/aurorarichaud
)</span>, <span style="text-decoration:none; color:black;">[Bruno Pinto](https://github.com/brunobpinto)</span> e <span style="text-decoration:none; color:black;">[Gabriel Valente](https://github.com/gvalente02)</span>

</div>

<br>
<br>

<div>
    <h2 style="font-family: Arial, sans-serif; color: #333; border-bottom: 2px solid #007BFF; padding-bottom: 5px; margin-bottom: 15px;">
        Breve descrição
    </h2>

  <p style="text-align: left;">
    Elaboração de um robô que copia os movimentos de dança do usuário. 
  </p>
</div>

<br>
<br>

<div>
    <h2 style="font-family: Arial, sans-serif; color: #333; border-bottom: 2px solid #007BFF; padding-bottom: 5px; margin-bottom: 15px;">
        Pilares do Projeto
    </h2>

  <p style="text-align: left;">
    O projeto foi elaborado com base em três grandes pilares, cada um responsável por uma parte fundamental no funcionamento do robô:
  </p>
  <table style="width: 100%; border-collapse: collapse; font-family: Arial, sans-serif;">
      <tr>
          <th style="background-color: #007BFF; color: white; padding: 10px; text-align: left;">Pilar</th>
          <th style="background-color: #f1f1f1; padding: 10px; text-align: left;">Descrição</th>
      </tr>
      <tr>
          <td style="padding: 10px; font-weight: bold;">💻 Software</td>
          <td style="padding: 10px;">Programação da detecção das poses realizadas pelo usuário em <code>Python</code>.</td>
      </tr>
      <tr>
          <td style="padding: 10px; font-weight: bold;">⚙️ Hardware</td>
          <td style="padding: 10px;">Envio do comando para girar o servo motor pelo programa no <code>Arduino</code> a partir da pose enviada pelo <code>Python</code>.</td>
      </tr>
      <tr>
          <td style="padding: 10px; font-weight: bold;">🛠️ Prototipagem</td>
          <td style="padding: 10px;">Impressão 3D das peças para montar o robô, com servos e peças.</td>
      </tr>
  </table>

</div>
<br>
<br>
<div>
   <h2 style="font-family: Arial, sans-serif; color: #333; border-bottom: 2px solid #007BFF; padding-bottom: 5px; margin-bottom: 15px;">
        Pré-Requisitos
    </h2>
<p>
      
Antes de começar, certifique-se de que você tem o seguinte configurado:

### Softwares necessários:
- **Python 3.8 ou superior**
- **Arduino IDE**

### Hardware necessário:
- Placa Arduino (ou compatível).
- Servo motor.
- Cabo USB para Arduino.
- Peças impressas em 3D.


</p>

</div>
<br>
<br>
<div>
   <h2 style="font-family: Arial, sans-serif; color: #333; border-bottom: 2px solid #007BFF; padding-bottom: 5px; margin-bottom: 15px;">
        Configurações iniciais
    </h2>

<p>

  ### Bibliotecas e dependências:
- Para instalar as dependências do Python, execute:
  <br>
  ```bash
  pip install -r requirements.txt

### Configurações no Arduino:

Antes de executar o projeto, certifique-se de configurar corretamente a porta serial do Arduino. A porta serial varia dependendo do sistema operacional e da conexão com o Arduino.

1. Abra o arquivo principal do código Python `main.py`
2. Localize o seguinte trecho de código:
    ```python
    try:
        arduino = serial.Serial("COM5", baudrate=9600) #Alterar porta de acordo com dispositivo
3. Substitua `'COM5'` pela porta serial do seu Arduino:




