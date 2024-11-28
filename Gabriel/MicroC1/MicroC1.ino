#include <Servo.h>
#include <stdio.h>
#include <ArduinoJson.h>
#include "Funcoes.h"

// Definção dos Pinos (E: Esquerdo  /  D: Direito)
int pinoCabeca        = 0;
int pinoTorso         = 0;
int pinoQuadril_E     = 8;
int pinoJoelho_E      = 0;
int pinoOmbro_E       = 0;
int pinoBraco_E       = 0;
int pinoAntebraco_E   = 0;
int pinoQuadril_D     = 0;
int pinoJoelho_D      = 0;
int pinoOmbro_D       = 0;
int pinoBraco_D       = 0;
int pinoAntebraco_D   = 0;

// Definção dos Servos
Servo servoCabeca;        // 0°(Esquerda), 90°(Meio), 180°(Direita)
Servo servoTorso;         // 0°(Esquerda), 90°(Meio), 180°(Direita)
Servo servoQuadril_E;     // Esquerda:  0°(Para trás), 45°(Perpendicular), 90°(Para frente)
Servo servoJoelho_E;      // Esquerda:  180°(Vertical) até 90°(Dobrado)
Servo servoOmbro_E;       // Esquerda:  0°(Para baixo), 90°(Para frente), 180°(Para cima)
Servo servoBraco_E;       // Esquerda:  0°(Para trás), 45°(Perpendicular), 90°(Para frente)
Servo servoAntebraco_E;   // Esquerda:  0°(Para trás), 45°(Perpendicular), 90°(Para frente)
Servo servoQuadril_D;     // Direita:   90°(Para trás), 45°(Perpendicular), 0°(Para frente)
Servo servoJoelho_D;      // Direita:   0°(Vertical) até 90°(Dobrado)
Servo servoOmbro_D;       // Direita:   180°(Para baixo), 90°(Para frente), 0°(Para cima)
Servo servoBraco_D;       // Direita:   90°(Para trás), 45°(Perpendicular), 0°(Para frente)
Servo servoAntebraco_D;   // Direita:   90°(Para trás), 45°(Perpendicular), 0°(Para frente)

// Listas
Servo listaServos[] = {servoCabeca, servoTorso, servoQuadril_E, servoJoelho_E, servoOmbro_E, servoBraco_E, servoAntebraco_E, servoQuadril_D, servoJoelho_D, servoOmbro_D, servoBraco_D, servoAntebraco_D};
String nomeServos[] = {"Cabeca", "Torso", "Quadril Esquerdo", "Joelho Esquerdo", "Ombro Esquerdo", "Braco Esquerdo", "Antebraco Esquerdo", "Quadril Direito", "Joelho Direito", "Ombro Direito", "Braco Direito", "Antebraco Direito"};
int listaPinos[] = {pinoCabeca, pinoTorso, pinoQuadril_E, pinoJoelho_E, pinoOmbro_E, pinoBraco_E, pinoAntebraco_E, pinoQuadril_D, pinoJoelho_D, pinoOmbro_D, pinoBraco_D, pinoAntebraco_D};

// Criar Json como input para o programa. O input poderia ser atraves da Serial ou outro metodo.
const char* input = "[{\"nome\":\"danca_1\",\"movimentos\":{\"Cabeca\":[90,45,30],\"Ombro Esquerdo\":[180,135,90],\"Quadril Direito\":[45,60,75]}},{\"nome\":\"danca_2\",\"movimentos\":{\"Cabeca\":[0,15,30],\"Ombro Esquerdo\":[90,120,150],\"Quadril Direito\":[0,45,90],\"Torso\":[0,180,90]}}]";

// Definição de Variáveis Globais
int ultimaDanca = 0;
bool emAndamento = false;  
String servoNomes[12];   


void setup() {
  // Inicializa a Comunicação Serial
  Serial.begin(9600);

  // Laço para ligar todos os servos
  for (int i = 0; i < sizeof(listaServos) / sizeof(listaServos[0]); i++) {
    listaServos[i].attach(listaPinos[i]);
    Serial.println("Servo do(a) " + nomeServos[i] + " conectado ao pino " + String(listaPinos[i]));
  }

  // Ângulos Iniciais do Robô
  resetarRobo();
  
}


void loop() {
  // Verificação de Comandos na Serial
  if (Serial.available() > 0) {   
    String texto = Serial.readStringUntil('\n');    
    texto.trim();

    if (texto.startsWith("Teste")) {          // Exemplo: Teste 1 180 -> Faz o servoCabeça ir para o ângulo 180°  
      String indiceStr = texto.substring(6);  // Pega o índice do Servo Motor desejado
      String anguloStr = texto.substring(8);  // Define o ângulo desejado
      int indice = indiceStr.toInt();
      int angulo = anguloStr.toInt();
      Teste(indice, angulo);  
    }

    if (texto.startsWith("Movimento")) {         
      String dancaStr = texto.substring(10);  // Seleciona a dança do Json
      movimentoDanca(dancaStr);
    }

    if (texto == "Perna") {
      movimentoPerna();
    }

    if (texto == "Braco") {
      movimentoBraco();
    }

    if (texto == "Parar") {
      ultimaDanca = 0;
      resetarRobo();
      Serial.println("Robô foi parado e resetado para a Posição Inicial");
    }

  }

  // Lógica do Loop das Danças
  if (emAndamento == false) {  // Ou seja, se o robo não esta dancando

    if (ultimaDanca == 1) {    // A Ultima Danca definida pela Serial é sempre a proxima a ser feita. Caso continue a mesma, vira um loop
      emAndamento = true;
      //movimentoDanca1();
    }

    if (ultimaDanca == 2) {    
      emAndamento = true;
      //movimentoDanca2();
    }
  }

}
