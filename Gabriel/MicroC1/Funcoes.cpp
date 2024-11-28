#include "Funcoes.h"
#include <Arduino.h>
#include <ArduinoJson.h>
#include <Servo.h>
#include <stdio.h>

// Implementação da função
void Teste(int indice, int angulo) {
  if (indice >= 0 && indice < 7) { // Verifica se o índice está dentro do limite dos servos
    listaServos[indice].write(angulo); // Faz o write no servo correspondente ao índice
    Serial.print("Servo do(a) ");
    Serial.print(nomeServos[indice]);
    Serial.print(" foi ajustado para o ângulo: ");
    Serial.print(angulo);
    Serial.println("°");
  } else {
    Serial.println("Índice inválido!");
  }
}


void resetarRobo() {
  // Ângulos Iniciais do Robô
  servoCabeca.write(0);          // Ajusta e trava ângulo em 0°         
  servoTorso.write(70);          // Ajusta e trava ângulo em 70°          
  servoQuadril_E.write(60);      // Ajusta e trava ângulo em 60°      
  servoJoelho_E.write(180);      // Ajusta e trava ângulo em 180°       
  servoOmbro_E.write(80);        // Ajusta e trava ângulo em 80°        
  servoBraco_E.write(90);        // Ajusta e trava ângulo em 90°        
  servoAntebraco_E.write(80);    // Ajusta e trava ângulo em 80°    
  servoQuadril_D.write(30);      // Ajusta e trava ângulo em 30°      
  servoJoelho_D.write(0);        // Ajusta e trava ângulo em 0°       
  servoOmbro_D.write(100);       // Ajusta e trava ângulo em 100°        
  servoBraco_D.write(0);         // Ajusta e trava ângulo em 0°        
  servoAntebraco_D.write(10);    // Ajusta e trava ângulo em 10°    

  delay(500);  // Pausa para estabilizar os servos
}


void movimentoPerna() {

  int angulosTorso[]    = {0, 140, 70};       // Ângulos para o servoTorso
  int angulosQuadril[]  = {0, 90, 60};        // Ângulos para o servoQuadril
  int angulosJoelho[]   = {90, 180};          // Ângulos para o servoJoelho

  int delaysTorso[]     = {1000,1000,1000};   // Delays para o servoTorso
  int delaysQuadril[]   = {1000,100,1000};    // Delays para o servoTorso
  int delaysJoelho[]    = {1000,1000};        // Delays para o servoTorso

  Serial.println("Movimento da Perna em andamento");

  // Movendo o servoTorso
  for (int i = 0; i < 3; i++) {
    servoTorso.write(angulosTorso[i]);
    delay(delaysTorso[i]);
  }

  // Movendo o servoQuadril e o servoJoelho
  for (int i = 0; i < 3; i++) {
    servoQuadril_E.write(angulosQuadril[i]);
    delay(delaysQuadril[i]);

    if (i < 2) {
      servoJoelho_E.write(angulosJoelho[i]);
      delay(delaysJoelho[i]);
    } 
  }
  Serial.println("Movimento da Perna foi executado com sucesso");
}


void movimentoBraco() {

  int angulosOmbro[]     = {40, 80};              // Ângulos para o servoOmbro
  int angulosBraco[]     = {45, 90, 45, 90};      // Ângulos para o servoBraco
  int angulosAntebraco[] = {45, 90, 45, 90};      // Ângulos para o servoAntebraco

  int delaysOmbro[]      = {1000, 1000};          // Delays para o servoOmbro
  int delaysBraco[]      = {100, 100, 100, 100};  // Delays para o servoBraco
  int delaysAntebraco[]  = {500, 500, 500, 500};  // Delays para o servoAntebraco

  Serial.println("Movimento do Braço em andamento");

  // Movendo o servoOmbro
  for (int i = 0; i < 2; i++) {
    servoOmbro_E.write(angulosOmbro[i]);
    delay(delaysOmbro[i]);
  }

  // Movendo o servoBraco e servoAntebraco
  for (int i = 0; i < 4; i++) {
    servoBraco_E.write(angulosBraco[i]);
    delay(delaysBraco[i]);

    servoAntebraco_E.write(angulosAntebraco[i]);
    delay(delaysAntebraco[i]);
  }
  Serial.println("Movimento do Braço foi executado com sucesso");
}

void movimentoDanca(String nomeDanca) {
  // Criar um JsonDocument
  JsonDocument Movimentos;

  // Verificar Erro de Deserialização
  DeserializationError error = deserializeJson(Movimentos, input);
  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.c_str());
    return;
  }

  // Serializar e Imprimir o JsonDocument na Serial
  //serializeJsonPretty(Movimentos, Serial);    // Trava a Serial

  // Acessar o array de danças
  JsonArray dancas = Movimentos.as<JsonArray>();


  // Procurar por "danca_1" no array
  for (JsonObject danca : dancas) {
    String jsonNomeDanca = danca["nome"];
    if (jsonNomeDanca == nomeDanca) {
      // Obter os movimentos de danca_1
      JsonObject movimentos = danca["movimentos"];
      Serial.println();
      Serial.print(F("Movimentos da "));
      Serial.print(nomeDanca);
      Serial.println(":");
      // JsonArray de todos os Movimentos da Danca
      JsonDocument movimentosServos;

      int tamanho = 0;

      // Iterar dinamicamente sobre os pares chave-valor dentro de movimentos
      for (JsonPair servo : movimentos) {
        String servoNome = servo.key().c_str();                   // Nome do servo
        JsonArray servoValores = servo.value().as<JsonArray>();   // Valores do servo

        // Armazenar os movimentos do servo na lista
        movimentosServos.add(servoValores);
        servoNomes[tamanho] = servoNome;
        tamanho++;
      }

      serializeJsonPretty(movimentosServos, Serial);

      // 1º movimento de todos os servos, depois para o 2º, e assim por diante
      int numMovimentos = movimentosServos[0].size();  // Número de movimentos (assumindo que todos os servos têm o mesmo número de movimentos)
      Serial.println();
      Serial.print("Numero de Movimentos: ");
      Serial.println(numMovimentos);

      for (int i = 0; i < numMovimentos; i++) {
        // Para cada movimento (i), mova todos os servos para o ângulo correspondente
        for (int j = 0; j < movimentosServos.size(); j++) {
          int angulo = movimentosServos[j][i];  // Pega o i-ésimo ângulo do j-ésimo servo

          // Encontrar o índice do servo na listaServos
          int servoIndex = -1;
          for (int k = 0; k < 12; k++) {
            if (servoNomes[j].equals(nomeServos[k])) {
              servoIndex = k;
              break;
            }
          }

          // Mover o servo correspondente
          if (servoIndex != -1) {
            listaServos[servoIndex].write(angulo);  // Escrever o ângulo no servo correspondente
            Serial.print(F("Movendo "));
            Serial.print(nomeServos[servoIndex]);
            Serial.print(F(" para o ângulo: "));
            Serial.println(angulo);
          }
        }
        Serial.println();
        delay(500);  // Aguardar um pouco antes de mover para o próximo movimento de todos os servos
      }


      break; // Parar o loop após encontrar a dança
    }
  }
}
