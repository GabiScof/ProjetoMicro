#ifndef FUNCOES_H
#define FUNCOES_H
#include <Servo.h>
#include <Arduino.h>

// Definção dos Pinos (E: Esquerdo  /  D: Direito)
extern int pinoCabeca;
extern int pinoTorso;
extern int pinoQuadril_E;
extern int pinoJoelho_E;
extern int pinoOmbro_E;
extern int pinoBraco_E;
extern int pinoAntebraco_E;
extern int pinoQuadril_D;
extern int pinoJoelho_D;
extern int pinoOmbro_D;
extern int pinoBraco_D;
extern int pinoAntebraco_D;

// Definção dos Servos
extern Servo servoCabeca;
extern Servo servoTorso;
extern Servo servoQuadril_E;
extern Servo servoJoelho_E;
extern Servo servoOmbro_E;
extern Servo servoBraco_E;
extern Servo servoAntebraco_E;
extern Servo servoQuadril_D;
extern Servo servoJoelho_D;
extern Servo servoOmbro_D;
extern Servo servoBraco_D;
extern Servo servoAntebraco_D;

// Listas
extern Servo listaServos[];
extern String nomeServos[];
extern int listaPinos[];

// Definição de Variáveis Globais
extern int ultimaDanca;
extern bool emAndamento;
extern String servoNomes[12];   
     
extern const char* input;

// Declaração das Funções
void Teste(int indice, int angulo);

void resetarRobo();

void movimentoPerna();

void movimentoBraco();

void movimentoDanca(String nomeDanca);

#endif