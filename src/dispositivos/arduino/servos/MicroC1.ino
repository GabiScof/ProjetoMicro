#include <Adafruit_PWMServoDriver.h>
#include <stdio.h>
#include <ArduinoJson.h>
#include "Funcoes.h"
#include "Movimentos.h"

// Instancia o driver com o endereço padrão (0x40)
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

void setup() {
  // Inicializa a Comunicação Serial
  Serial.begin(9600);
  Serial.println("===>>> Mr.Adam foi inicializado <<<===\n");

  // Inicializa o Shield de Servos(PWM)
  pwm.begin();
  pwm.setPWMFreq(50); // Frequência de 50 Hz para servos

  // Ângulos Iniciais do Robô
  resetarRobo();

  // Inicializar Movimentos do Struct
  Danca dancas[1];            // Inicializando um array de n danças
  inicializarDancas(dancas);  // Funcao para preencher o array dancas
}

void loop() {
  // Verificação de Comandos na Serial
  if (Serial.available() > 0) {   
    String texto = Serial.readStringUntil('\n');    
    texto.trim();

    if (texto == "Resetar") {         
      resetarRobo(); // Resetar robô para Ângulos Iniciais
    }

    if (texto.startsWith("Teste")) {             // Exemplo: Teste 1 180 -> Faz o servoCabeça ir para o ângulo 180°  
      String indiceStr = texto.substring(6, 8);  // Pega o índice do Servo Motor desejado
      String anguloStr = texto.substring(8);     // Define o ângulo desejado
      int indice = indiceStr.toInt();
      int angulo = anguloStr.toInt();
      testarServo(indice, angulo);  
    }

    if (texto.startsWith("Movimento")) {         
      String dancaStr = texto.substring(10);  // Seleciona a dança do Json
      //movimentoDanca(dancaStr);
    }
    
  }

}
