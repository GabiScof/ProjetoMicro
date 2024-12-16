#include <Adafruit_PWMServoDriver.h>
#include <FastLED.h>
#include <stdio.h>
#include "Funcoes.h"
#include "Movimentos.h"

#define NUM_DANCAS 12 // Número de Dancas
#define NUM_LEDS 43   // Número de LEDS na fita

// Instancia o driver com o endereço padrão (0x40)
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// Cria uuma Lista de Structs do tipo Danca
Danca dancas[NUM_DANCAS];   // Inicializando um array de n danças

// Variaveis Globais
CRGB leds[NUM_LEDS];
float valorHue; 
float valorBrightness; 
bool isOn = true;  // State to check whether LEDs are on or off

void setup() {
  // Inicializa a Comunicação Serial
  Serial.begin(9600);
  Serial.println("=======>>> Mr.Adam foi inicializado <<<=======\n");

  // Inicializa o Shield de Servos(PWM)
  pwm.begin();
  pwm.setPWMFreq(50); // Frequência de 50 Hz para servos

  // Inicializa os Structs com os dados dos movimentos
  inicializarDancas(dancas);  // Funcao para preencher o array dancas

  // Exibir todas as danças na Serial
  // exibirDancas(dancas, NUM_DANCAS);   // Demora para exibir todas na serial (Pode so descomentar para ver os Structs preenchidos)

  // Ângulos Iniciais do Robô
  resetarRobo();

  // Inicialização da Fita de LEDs
  configurarLeds();
}

void loop() {
  // Verificação de Comandos na Serial
  if (Serial.available() > 0) {   
    String texto = Serial.readStringUntil('\n');    
    texto.trim();
    
    Serial.println(texto);

    if (texto == "Resetar") {         
      resetarRobo(); // Resetar robô para Ângulos Iniciais
    }

    else if (texto == "Batida") {  
      moverPadrao();    // Função para mexer a cabeca sempre no ritmo da Batida
      isOn = !isOn;     // Variavel para monitorar quando o LED está ON ou OFF
    }

    else if (texto.startsWith("Hue")) {
      texto = texto.substring(4);                // Start from the 5th character (after "hue ")
      valorHue = texto.toInt();
    }

    else if (texto.startsWith("Brightness")) {
      texto = texto.substring(11);               // Start from the 12th character (after "brightness ")
      valorBrightness = texto.toInt();
      FastLED.setBrightness(valorBrightness);
    }

    else if (texto.startsWith("Teste")) {        // Exemplo: Teste 1 180 -> Faz o servoCabeça ir para o ângulo 180°  
      String indiceStr = texto.substring(6, 8);  // Pega o índice do Servo Motor desejado
      String anguloStr = texto.substring(8);     // Define o ângulo desejado
      int indice = indiceStr.toInt();
      int angulo = anguloStr.toInt();
      testarServo(indice, angulo);  
    }

    else if (texto.startsWith("Movimento")) {       // Exemplo: Movimento leg01 arm01
      String dancaLeg = texto.substring(10, 15);
      String dancaArm = texto.substring(16, 21);  
      realizarDanca(dancas, dancaArm, true);        // Movimento do Braco
      realizarDanca(dancas, dancaLeg, false);       // Movimento da Perna
    }
    
  }

  // Restante da loop
  atualizarLeds();
}
