#include <Adafruit_PWMServoDriver.h>
#include <Arduino.h>
#include <ArduinoJson.h>
#include <stdio.h>
#include "Funcoes.h"
#include "Movimentos.h"

// Definição de Variáveis
#define SERVO_MIN 150 // Pulso mínimo (em microsegundos) para 0 graus
#define SERVO_MAX 600 // Pulso máximo (em microsegundos) para 180 graus
#define TAXA 0.3      // Taxa da velocidade dos movimentos do robo

// Listas
String nomeServos[] = {"Cabeca", "Torso", "Quadril Esquerdo", "Joelho Esquerdo", "Ombro Esquerdo", "Braco Esquerdo", "Antebraco Esquerdo", "Quadril Direito", "Joelho Direito", "Ombro Direito", "Braco Direito", "Antebraco Direito"};
int listaAngulosIniciais[] = {90, 87, 45, 165, 155, 140, 25, 50, 70, 15, 75, 60};   // Lista de ângulos iniciais
int listaAngulos[]         = {90, 87, 45, 165, 155, 140, 25, 50, 70, 15, 75, 60};   // Lista de ângulos a ser modificada 

// Lista de ângulos mínimo e máximo
int listaMinMax[][2] = {
    {0, 180},   // Cabeça
    {0, 180},   // Torso
    {30, 65},   // Quadril Esquerdo
    {75, 165},  // Joelho Esquerdo
    {0, 160},   // Ombro Esquerdo
    {75, 140},  // Braço Esquerdo
    {5, 75},    // Antebraço Esquerdo
    {25, 60},   // Quadril Direito
    {70, 150},  // Joelho Direito
    {10, 165},  // Ombro Direito
    {75, 140},  // Braço Direito
    {10, 80}    // Antebraço Direito
};

// Função para Mover o Servo Suavemente para um Ângulo Específico
void moverServo(int numServo, int anguloDesejado, bool suave) {
  // Verificação dos ângulos
  anguloDesejado = constrain(anguloDesejado, listaMinMax[numServo][0], listaMinMax[numServo][1]);  // Limita os valores entre o Min e Max de cada servo

  // Movimento Direto para o angulo
  if (!suave) {
    int pulseMap = map(anguloDesejado, 0, 180, SERVO_MIN, SERVO_MAX);
    pwm.setPWM(numServo, 0, pulseMap);
  } 
  // Movimento Suave para o angulo com Comparacao na listaAngulos
  else {
    if (anguloDesejado > listaAngulos[numServo]) {    // Indo para um an gulo Maior que o Anterior
      for (float pulse = listaAngulos[numServo]; pulse <= anguloDesejado; pulse += TAXA) {
        int pulseMap = map(pulse, 0, 180, SERVO_MIN, SERVO_MAX);
        pwm.setPWM(numServo, 0, pulseMap);
      }
    }

    if (anguloDesejado < listaAngulos[numServo]) {    // Indo para um angulo Menor que o Anterior
      for (float pulse = listaAngulos[numServo]; pulse >= anguloDesejado; pulse -= TAXA) {
        int pulseMap = map(pulse, 0, 180, SERVO_MIN, SERVO_MAX);
        pwm.setPWM(numServo, 0, pulseMap);
      }
    }
  }
  
  listaAngulos[numServo] = anguloDesejado;
}

// Função para Testar um Único Servo pelo Índice dele
void testarServo(int indice, int angulo) {
  if (indice >= 0 && indice < 12) {             // Verifica se o índice está dentro do limite dos servos
    moverServo(indice, angulo, true);           // Faz o write no servo correspondente ao índice suavemente
    Serial.print("Servo do(a) ");
    Serial.print(nomeServos[indice]);
    Serial.print(" foi ajustado para o ângulo: ");
    Serial.print(angulo);
    Serial.println("°");
  } else {
    Serial.println("Índice inválido!");
  }
}

// Função para Resetar o Robô
void resetarRobo() {
  // Colocar o Robô nos ângulos iniciais
  for (int indice = 0; indice < sizeof(listaAngulosIniciais) / sizeof(listaAngulosIniciais[0]); indice++) {   // Percorre a lista de Angulos Iniciais
    moverServo(indice, listaAngulosIniciais[indice], false);    // Vai diretamente para os angulos
  }
  Serial.println("Robô foi resetado para os ângulos iniciais");
  delay(500);  // Pausa para estabilizar os servos
}

// Função para inicializar as danças e seus movimentos
void inicializarDancas(Danca *dancas) {
    // Primeira dança 
    strcpy(dancas[0].nome, "danca1");
    dancas[0].quantidadeServos = 6;
    dancas[0].quantidadeAngulos = 4;

    dancas[0].movimentos[0].servo = OMBRO_ESQUERDO;
    dancas[0].movimentos[0].angulos[0] = 0;
    dancas[0].movimentos[0].angulos[1] = 0; 
    dancas[0].movimentos[0].angulos[2] = 0;
    dancas[0].movimentos[0].angulos[3] = 0;

    dancas[0].movimentos[1].servo = OMBRO_DIREITO;
    dancas[0].movimentos[1].angulos[0] = 165;
    dancas[0].movimentos[1].angulos[1] = 165;
    dancas[0].movimentos[1].angulos[2] = 165;
    dancas[0].movimentos[1].angulos[3] = 165;

    dancas[0].movimentos[2].servo = BRACO_ESQUERDO;
    dancas[0].movimentos[2].angulos[0] = 75;
    dancas[0].movimentos[2].angulos[1] = 75;
    dancas[0].movimentos[2].angulos[2] = 75;
    dancas[0].movimentos[2].angulos[3] = 75;

    dancas[0].movimentos[3].servo = BRACO_DIREITO;
    dancas[0].movimentos[3].angulos[0] = 140;
    dancas[0].movimentos[3].angulos[1] = 140;
    dancas[0].movimentos[3].angulos[2] = 140;
    dancas[0].movimentos[3].angulos[3] = 140;

    dancas[0].movimentos[4].servo = ANTEBRACO_ESQUERDO;
    dancas[0].movimentos[4].angulos[0] = 40;
    dancas[0].movimentos[4].angulos[1] = 75;
    dancas[0].movimentos[4].angulos[2] = 5;
    dancas[0].movimentos[4].angulos[3] = 40;

    dancas[0].movimentos[5].servo = ANTEBRACO_DIREITO;
    dancas[0].movimentos[5].angulos[0] = 45;
    dancas[0].movimentos[5].angulos[1] = 10;
    dancas[0].movimentos[5].angulos[2] = 80;
    dancas[0].movimentos[5].angulos[3] = 45;
}
