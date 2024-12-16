#include <Adafruit_PWMServoDriver.h>
#include <FastLED.h>
#include <Arduino.h>
#include <stdio.h>
#include "Funcoes.h"
#include "Movimentos.h"

// Definição de Variáveis
#define SERVO_MIN 150 // Pulso mínimo (em microsegundos) para 0 graus
#define SERVO_MAX 600 // Pulso máximo (em microsegundos) para 180 graus
#define TAXA 1        // Taxa da velocidade dos movimentos do robo
#define NUM_SERVOS 12 // Número de Servos no Robo
#define NUM_DANCAS 12 // Número de Dancas
#define NUM_LEDS 43   // Número de LEDS na fita
#define LED_PIN 8     // Pino PWM da Fita de LED


// Definição de Variáveis Globais
int indicePadrao = 0;
int indiceBracos = 0;
int indicePernas = 0;
String anteriorBracos = "";
String anteriorPernas = "";

// Listas
String nomeServos[] = {"Antebraco Direito", "Torso", "Quadril Esquerdo", "Joelho Esquerdo", "Ombro Esquerdo", "Braco Esquerdo", "Antebraco Esquerdo", "Quadril Direito", "Joelho Direito", "Ombro Direito", "Braco Direito", "Cabeca"};
int listaAngulosIniciais[] = {60, 87, 45, 165, 155, 140, 25, 50, 70, 15, 75, 90};   // Lista de ângulos iniciais
int listaAngulos[]         = {60, 87, 45, 165, 155, 140, 25, 50, 70, 15, 75, 90};   // Lista de ângulos a ser modificada 

// Lista de ângulos mínimo e máximo
int listaMinMax[][2] = {
    {0, 80},    // Antebraço Direito
    {0, 180},   // Torso
    {30, 65},   // Quadril Esquerdo
    {75, 165},  // Joelho Esquerdo
    {0, 160},   // Ombro Esquerdo
    {75, 140},  // Braço Esquerdo
    {5, 95},    // Antebraço Esquerdo
    {25, 60},   // Quadril Direito
    {70, 150},  // Joelho Direito
    {10, 165},  // Ombro Direito
    {75, 140},  // Braço Direito
    {0, 180}    // Cabeça
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
  if (indice >= 0 && indice < NUM_SERVOS) {     // Verifica se o índice está dentro do limite dos servos
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
  for (int indice = 0; indice < NUM_SERVOS; indice++) {   // Percorre a lista de Angulos Iniciais
    moverServo(indice, listaAngulosIniciais[indice], false);    // Vai diretamente para os angulos
  }
  Serial.println("Robô foi resetado para os ângulos iniciais");
  delay(500);  // Pausa para estabilizar os servos
}

// Função para inicializar as danças e seus movimentos
void inicializarDancas(Danca *dancas) {
    // Bracos para baixo mexendo o antebraco formato U invertido
    strcpy(dancas[0].nome, "arm01"); 
    dancas[0].quantidadeServos = 6;
    dancas[0].quantidadeAngulos = 2;

    dancas[0].movimentos[0].servo = OMBRO_ESQUERDO;
    dancas[0].movimentos[0].angulos[0] = 0;
    dancas[0].movimentos[0].angulos[1] = 0; 

    dancas[0].movimentos[1].servo = OMBRO_DIREITO;
    dancas[0].movimentos[1].angulos[0] = 165;
    dancas[0].movimentos[1].angulos[1] = 165;

    dancas[0].movimentos[2].servo = BRACO_ESQUERDO;
    dancas[0].movimentos[2].angulos[0] = 75;
    dancas[0].movimentos[2].angulos[1] = 75;

    dancas[0].movimentos[3].servo = BRACO_DIREITO;
    dancas[0].movimentos[3].angulos[0] = 140;
    dancas[0].movimentos[3].angulos[1] = 140;

    dancas[0].movimentos[4].servo = ANTEBRACO_ESQUERDO;
    dancas[0].movimentos[4].angulos[0] = 60;
    dancas[0].movimentos[4].angulos[1] = 95;

    dancas[0].movimentos[5].servo = ANTEBRACO_DIREITO;
    dancas[0].movimentos[5].angulos[0] = 0;
    dancas[0].movimentos[5].angulos[1] = 30;

    // Bracos para cima de um lado para o outro 
    strcpy(dancas[1].nome, "arm02"); 
    dancas[1].quantidadeServos = 6;
    dancas[1].quantidadeAngulos = 2;

    dancas[1].movimentos[0].servo = OMBRO_ESQUERDO;
    dancas[1].movimentos[0].angulos[0] = 155;
    dancas[1].movimentos[0].angulos[1] = 155; 

    dancas[1].movimentos[1].servo = OMBRO_DIREITO;
    dancas[1].movimentos[1].angulos[0] = 15;
    dancas[1].movimentos[1].angulos[1] = 15;

    dancas[1].movimentos[2].servo = BRACO_ESQUERDO;
    dancas[1].movimentos[2].angulos[0] = 115;
    dancas[1].movimentos[2].angulos[1] = 140;

    dancas[1].movimentos[3].servo = BRACO_DIREITO;
    dancas[1].movimentos[3].angulos[0] = 75;
    dancas[1].movimentos[3].angulos[1] = 100;

    dancas[1].movimentos[4].servo = ANTEBRACO_ESQUERDO;
    dancas[1].movimentos[4].angulos[0] = 5;
    dancas[1].movimentos[4].angulos[1] = 60;

    dancas[1].movimentos[5].servo = ANTEBRACO_DIREITO;
    dancas[1].movimentos[5].angulos[0] = 20;
    dancas[1].movimentos[5].angulos[1] = 80;

    // Movimento de levantar as pernas
    strcpy(dancas[2].nome, "leg01"); 
    dancas[2].quantidadeServos = 4;
    dancas[2].quantidadeAngulos = 2;

    dancas[2].movimentos[0].servo = QUADRIL_ESQUERDO;
    dancas[2].movimentos[0].angulos[0] = 65;
    dancas[2].movimentos[0].angulos[1] = 45; 

    dancas[2].movimentos[1].servo = QUADRIL_DIREITO;
    dancas[2].movimentos[1].angulos[0] = 50;
    dancas[2].movimentos[1].angulos[1] = 35;

    dancas[2].movimentos[2].servo = JOELHO_ESQUERDO;
    dancas[2].movimentos[2].angulos[0] = 125;
    dancas[2].movimentos[2].angulos[1] = 165;

    dancas[2].movimentos[3].servo = JOELHO_DIREITO;
    dancas[2].movimentos[3].angulos[0] = 70;
    dancas[2].movimentos[3].angulos[1] = 110;

    // Bracos e maos para cima
    strcpy(dancas[3].nome, "arm03");
    dancas[3].quantidadeServos = 6;
    dancas[3].quantidadeAngulos = 2;

    dancas[3].movimentos[0].servo = OMBRO_ESQUERDO;
    dancas[3].movimentos[0].angulos[0] = 155;
    dancas[3].movimentos[0].angulos[1] = 155; 

    dancas[3].movimentos[1].servo = OMBRO_DIREITO;
    dancas[3].movimentos[1].angulos[0] = 15;
    dancas[3].movimentos[1].angulos[1] = 15;

    dancas[3].movimentos[2].servo = BRACO_ESQUERDO;
    dancas[3].movimentos[2].angulos[0] = 120;
    dancas[3].movimentos[2].angulos[1] = 140;

    dancas[3].movimentos[3].servo = BRACO_DIREITO;
    dancas[3].movimentos[3].angulos[0] = 90;
    dancas[3].movimentos[3].angulos[1] = 75;

    dancas[3].movimentos[4].servo = ANTEBRACO_ESQUERDO;
    dancas[3].movimentos[4].angulos[0] = 25;
    dancas[3].movimentos[4].angulos[1] = 25;

    dancas[3].movimentos[5].servo = ANTEBRACO_DIREITO;
    dancas[3].movimentos[5].angulos[0] = 60;
    dancas[3].movimentos[5].angulos[1] = 60;

    // Disco Move (Bracos em diagonais opostas)
    strcpy(dancas[4].nome, "arm04");
    dancas[4].quantidadeServos = 6;
    dancas[4].quantidadeAngulos = 2;

    dancas[4].movimentos[0].servo = OMBRO_ESQUERDO;
    dancas[4].movimentos[0].angulos[0] = 155;
    dancas[4].movimentos[0].angulos[1] = 0; 

    dancas[4].movimentos[1].servo = OMBRO_DIREITO;
    dancas[4].movimentos[1].angulos[0] = 165;
    dancas[4].movimentos[1].angulos[1] = 15;

    dancas[4].movimentos[2].servo = BRACO_ESQUERDO;
    dancas[4].movimentos[2].angulos[0] = 140;
    dancas[4].movimentos[2].angulos[1] = 140;

    dancas[4].movimentos[3].servo = BRACO_DIREITO;
    dancas[4].movimentos[3].angulos[0] = 75;
    dancas[4].movimentos[3].angulos[1] = 75;

    dancas[4].movimentos[4].servo = ANTEBRACO_ESQUERDO;
    dancas[4].movimentos[4].angulos[0] = 6;
    dancas[4].movimentos[4].angulos[1] = 6;

    dancas[4].movimentos[5].servo = ANTEBRACO_DIREITO;
    dancas[4].movimentos[5].angulos[0] = 80;
    dancas[4].movimentos[5].angulos[1] = 80;

    // Bracos retos pra frente subindo e descendo
    strcpy(dancas[5].nome, "arm05");
    dancas[5].quantidadeServos = 6;
    dancas[5].quantidadeAngulos = 2;

    dancas[5].movimentos[0].servo = OMBRO_ESQUERDO;
    dancas[5].movimentos[0].angulos[0] = 100;
    dancas[5].movimentos[0].angulos[1] = 50; 

    dancas[5].movimentos[1].servo = OMBRO_DIREITO;
    dancas[5].movimentos[1].angulos[0] = 110;
    dancas[5].movimentos[1].angulos[1] = 80;

    dancas[5].movimentos[2].servo = BRACO_ESQUERDO;
    dancas[5].movimentos[2].angulos[0] = 140;
    dancas[5].movimentos[2].angulos[1] = 140;

    dancas[5].movimentos[3].servo = BRACO_DIREITO;
    dancas[5].movimentos[3].angulos[0] = 75;
    dancas[5].movimentos[3].angulos[1] = 75;

    dancas[5].movimentos[4].servo = ANTEBRACO_ESQUERDO;
    dancas[5].movimentos[4].angulos[0] = 40;
    dancas[5].movimentos[4].angulos[1] = 40;

    dancas[5].movimentos[5].servo = ANTEBRACO_DIREITO;
    dancas[5].movimentos[5].angulos[0] = 50;
    dancas[5].movimentos[5].angulos[1] = 50;

    // Bracos retos pra baixo
    strcpy(dancas[6].nome, "arm06");
    dancas[6].quantidadeServos = 6;
    dancas[6].quantidadeAngulos = 1;

    dancas[6].movimentos[0].servo = OMBRO_ESQUERDO;
    dancas[6].movimentos[0].angulos[0] = 0;

    dancas[6].movimentos[1].servo = OMBRO_DIREITO;
    dancas[6].movimentos[1].angulos[0] = 165;

    dancas[6].movimentos[2].servo = BRACO_ESQUERDO;
    dancas[6].movimentos[2].angulos[0] = 140;

    dancas[6].movimentos[3].servo = BRACO_DIREITO;
    dancas[6].movimentos[3].angulos[0] = 75;

    dancas[6].movimentos[4].servo = ANTEBRACO_ESQUERDO;
    dancas[6].movimentos[4].angulos[0] = 25;

    dancas[6].movimentos[5].servo = ANTEBRACO_DIREITO;
    dancas[6].movimentos[5].angulos[0] = 60;

    // Um Braco reto e outro pra baixo
    strcpy(dancas[7].nome, "arm07");
    dancas[7].quantidadeServos = 6;
    dancas[7].quantidadeAngulos = 2;

    dancas[7].movimentos[0].servo = OMBRO_ESQUERDO;
    dancas[7].movimentos[0].angulos[0] = 100;
    dancas[7].movimentos[0].angulos[1] = 50; 

    dancas[7].movimentos[1].servo = OMBRO_DIREITO;
    dancas[7].movimentos[1].angulos[0] = 165;
    dancas[7].movimentos[1].angulos[1] = 165;

    dancas[7].movimentos[2].servo = BRACO_ESQUERDO;
    dancas[7].movimentos[2].angulos[0] = 140;
    dancas[7].movimentos[2].angulos[1] = 140;

    dancas[7].movimentos[3].servo = BRACO_DIREITO;
    dancas[7].movimentos[3].angulos[0] = 120;
    dancas[7].movimentos[3].angulos[1] = 120;

    dancas[7].movimentos[4].servo = ANTEBRACO_ESQUERDO;
    dancas[7].movimentos[4].angulos[0] = 40;
    dancas[7].movimentos[4].angulos[1] = 40;

    dancas[7].movimentos[5].servo = ANTEBRACO_DIREITO;
    dancas[7].movimentos[5].angulos[0] = 0;
    dancas[7].movimentos[5].angulos[1] = 0;

    // Um Braco reto e outro pra cima
    strcpy(dancas[8].nome, "arm08");
    dancas[8].quantidadeServos = 6;
    dancas[8].quantidadeAngulos = 2;

    dancas[8].movimentos[0].servo = OMBRO_ESQUERDO;
    dancas[8].movimentos[0].angulos[0] = 100;
    dancas[8].movimentos[0].angulos[1] = 50; 

    dancas[8].movimentos[1].servo = OMBRO_DIREITO;
    dancas[8].movimentos[1].angulos[0] = 10;
    dancas[8].movimentos[1].angulos[1] = 10;

    dancas[8].movimentos[2].servo = BRACO_ESQUERDO;
    dancas[8].movimentos[2].angulos[0] = 140;
    dancas[8].movimentos[2].angulos[1] = 140;

    dancas[8].movimentos[3].servo = BRACO_DIREITO;
    dancas[8].movimentos[3].angulos[0] = 100;
    dancas[8].movimentos[3].angulos[1] = 100;

    dancas[8].movimentos[4].servo = ANTEBRACO_ESQUERDO;
    dancas[8].movimentos[4].angulos[0] = 40;
    dancas[8].movimentos[4].angulos[1] = 40;

    dancas[8].movimentos[5].servo = ANTEBRACO_DIREITO;
    dancas[8].movimentos[5].angulos[0] = 0;
    dancas[8].movimentos[5].angulos[1] = 0;

    // Movimento de joelhos para tras
    strcpy(dancas[9].nome, "leg02"); 
    dancas[9].quantidadeServos = 4;
    dancas[9].quantidadeAngulos = 2;

    dancas[9].movimentos[0].servo = QUADRIL_ESQUERDO;
    dancas[9].movimentos[0].angulos[0] = 45;
    dancas[9].movimentos[0].angulos[1] = 45; 

    dancas[9].movimentos[1].servo = QUADRIL_DIREITO;
    dancas[9].movimentos[1].angulos[0] = 50;
    dancas[9].movimentos[1].angulos[1] = 50;

    dancas[9].movimentos[2].servo = JOELHO_ESQUERDO;
    dancas[9].movimentos[2].angulos[0] = 100;
    dancas[9].movimentos[2].angulos[1] = 165;

    dancas[9].movimentos[3].servo = JOELHO_DIREITO;
    dancas[9].movimentos[3].angulos[0] = 70;
    dancas[9].movimentos[3].angulos[1] = 130;

    // Pernas retas
    strcpy(dancas[10].nome, "leg03"); 
    dancas[10].quantidadeServos = 4;
    dancas[10].quantidadeAngulos = 1;

    dancas[10].movimentos[0].servo = QUADRIL_ESQUERDO;
    dancas[10].movimentos[0].angulos[0] = 45;

    dancas[10].movimentos[1].servo = QUADRIL_DIREITO;
    dancas[10].movimentos[1].angulos[0] = 50;

    dancas[10].movimentos[2].servo = JOELHO_ESQUERDO;
    dancas[10].movimentos[2].angulos[0] = 165;

    dancas[10].movimentos[3].servo = JOELHO_DIREITO;
    dancas[10].movimentos[3].angulos[0] = 70;

    // Um Braco reto e outro pra cima
    strcpy(dancas[11].nome, "arm09");
    dancas[11].quantidadeServos = 6;
    dancas[11].quantidadeAngulos = 2;

    dancas[11].movimentos[0].servo = OMBRO_ESQUERDO;
    dancas[11].movimentos[0].angulos[0] = 75;
    dancas[11].movimentos[0].angulos[1] = 75; 

    dancas[11].movimentos[1].servo = OMBRO_DIREITO;
    dancas[11].movimentos[1].angulos[0] = 100;
    dancas[11].movimentos[1].angulos[1] = 100;

    dancas[11].movimentos[2].servo = BRACO_ESQUERDO;
    dancas[11].movimentos[2].angulos[0] = 140;
    dancas[11].movimentos[2].angulos[1] = 110;

    dancas[11].movimentos[3].servo = BRACO_DIREITO;
    dancas[11].movimentos[3].angulos[0] = 75;
    dancas[11].movimentos[3].angulos[1] = 105;

    dancas[11].movimentos[4].servo = ANTEBRACO_ESQUERDO;
    dancas[11].movimentos[4].angulos[0] = 95;
    dancas[11].movimentos[4].angulos[1] = 65;

    dancas[11].movimentos[5].servo = ANTEBRACO_DIREITO;
    dancas[11].movimentos[5].angulos[0] = 0;
    dancas[11].movimentos[5].angulos[1] = 30;
}

// Função para exibir dancas do Struct
void exibirDancas(Danca *dancas, int totalDancas) {
  Serial.println("============== Lista de Danças ===============");
  for (int i = 0; i < totalDancas; i++) {
    Serial.print("\nDança: ");
    Serial.println(dancas[i].nome);
    Serial.print("Quantidade de Servos: ");
    Serial.println(dancas[i].quantidadeServos);
    Serial.print("Quantidade de Angulos: ");
    Serial.println(dancas[i].quantidadeAngulos);

    for (int j = 0; j < dancas[i].quantidadeServos; j++) {
      Serial.print("  ");
      Serial.print(nomeServos[dancas[i].movimentos[j].servo]);
      Serial.print(":\t");

      Serial.print("[");
      for (int k = 0; k < dancas[i].quantidadeAngulos; k++) {
        Serial.print(dancas[i].movimentos[j].angulos[k]);
        if (k < dancas[i].quantidadeAngulos - 1) {
          Serial.print(", ");
        }
      }
      Serial.println("]");
    }
    Serial.println("\n----------------------------------------------");
  }
  Serial.println("==============================================\n");
}

// Funcão para mexer Cabeca e Torso como movimentos padroes
void moverPadrao() {
  int angulosCabeca[] = {60, 120};      
  int angulosTorso[] = {95, 79};      

    if (indicePadrao >= 2) {
      indicePadrao = 0;
    }

    moverServo(11, angulosCabeca[indicePadrao], false);  // Mover Cabeca
    moverServo(1, angulosTorso[indicePadrao], false);    // Mover Torso
    indicePadrao++;
}

// Função para fazer uma danca por Serial
void realizarDanca(Danca *dancas, String nomeDanca, bool bracos) {
  bool dancaEncontrada = false;       // Verifica se foi encontrada
  String anteriorGeral = "";
  int indiceGeral;
  
  switch (bracos) {     // Define variaveis locais correspondentes
  case true:
    indiceGeral = indiceBracos;
    anteriorGeral = anteriorBracos;
    break;

  case false:
    indiceGeral = indicePernas;
    anteriorGeral = anteriorPernas;
    break;
  }

  // Encontra a dança correspondente ao nomeDanca
  for (int i = 0; i < NUM_DANCAS; i++) {
    if (nomeDanca == dancas[i].nome) {
      dancaEncontrada = true;

      // Verificação para zerar o indice
      // Caso 1: Se o indice tiver passado o número de movimentos
      // Caso 2: Se a dança tiver mudado
      if (indiceGeral >= dancas[i].quantidadeAngulos || nomeDanca != anteriorGeral) {
        indiceGeral = 0;
        anteriorGeral = nomeDanca;
      }

      // Movimentos da dança
      for (int k = 0; k < dancas[i].quantidadeServos; k++) {
        int servo = dancas[i].movimentos[k].servo;
        int angulo = dancas[i].movimentos[k].angulos[indiceGeral];
        moverServo(servo, angulo, true);
      }
      Serial.println("Dança finalizada");
      indiceGeral++;

      // Igualação das variaveis Globais com as Variaveis Gerais
      switch (bracos) {     
      case true:
        indiceBracos = indiceGeral;
        anteriorBracos = anteriorGeral;
        break;

      case false:
        indicePernas = indiceGeral;
        anteriorPernas = anteriorGeral;
        break;
      }

      break;
    }
  }

  if (!dancaEncontrada) {
    Serial.println("Dança não encontrada");
  }
}

void configurarLeds() {
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  fill_solid(leds, NUM_LEDS, CRGB::Black);
  FastLED.setBrightness(20);
}

void atualizarLeds() {
  if (isOn) {
    for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CHSV(valorHue, 255, 255);
    }
  }
  else {
    fill_solid(leds, NUM_LEDS, CRGB::Black);
  }
  FastLED.show();
}