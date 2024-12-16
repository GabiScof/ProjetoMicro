#ifndef FUNCOES_H
#define FUNCOES_H
#include <Adafruit_PWMServoDriver.h>
#include <FastLED.h>
#include <Arduino.h>
#include "Movimentos.h"

// ==========================================>>>   SERVOS    <<<==========================================
//    INDEX   NAME                  ANGLES
//    11      Cabeca                Padrão:    0°   (Esquerda),     90°   (Meio),         180°  (Direita)
//    1       Torso                 Padrão:    0°   (Esquerda),     90°   (Meio),         180°  (Direita)
//    2       Quadril Esquerdo      Esquerda:  30°  (Para trás),    45°   (Reto),         65°   (Para frente)
//    3       Joelho Esquerdo       Esquerda:  165° (Vertical) até  75°   (Dobrado)
//    4       Ombro Esquerdo        Esquerda:  0°   (Para baixo),   75°   (Para frente),  160°  (Para cima)
//    5       Braco Esquerdo        Esquerda:  75°  (Reto),         140°  (Dobrado)
//    6       Antebraco Esquerdo    Esquerda:  5°   (Reto),         95°   (Dobrado)
//    7       Quadril Direito       Direita:   60°  (Para trás),    50°   (Reto),         25°   (Para frente)
//    8       Joelho Direito        Direita:   70°  (Vertical) até  150°  (Dobrado)
//    9       Ombro Direito         Direita:   165° (Para baixo),   100°  (Para frente),  10°    (Para cima)
//    10      Braco Direito         Direita:   140° (Reto),         75°   (Dobrado)
//    0       Antebraco Direito     Direita:   80°  (Reto),         0°    (Dobrado)


// ============================>>>   DANCAS    <<<============================
//    NAME          DESCRIPTION
//    arm01         Bracos para baixo mexendo o antebraco formato U invertido   
//    arm02         Bracos para cima de um lado para o outro 
//    arm03         Bracos e maos para cima
//    arm04         Disco Move (Bracos em diagonais opostas)
//    arm05         Bracos retos pra frente subindo e descendo
//    arm06         Bracos retos pra baixo
//    arm07         Um Braco reto e outro pra baixo
//    arm08         Um Braco reto e outro pra cima
//    arm09         Funk Surprise
//    leg01         Movimento de levantar as pernas 
//    leg02         Movimento de joelhos para tras
//    leg03         Pernas retas



// Declaração das Variáveis
extern Adafruit_PWMServoDriver pwm;
extern CRGB leds[];
extern bool isOn;
extern float valorHue; 

// Declaração das Funções
void moverServo(int numServo, int anguloDesejado, bool suave = true);

void testarServo(int indice, int angulo);

void resetarRobo();

void inicializarDancas(Danca *dancas);

void exibirDancas(Danca *dancas, int totalDancas);

void moverPadrao();

void realizarDanca(Danca *dancas, String nomeDanca, bool bracos);

void configurarLeds();

void atualizarLeds();

#endif