// // DISCALAIMER : I USED AI TO WRITE THIS CODE BECAUSE I UNDERSTOOD NOTHING AND NOW IT JUST WORKS

// #include <GxEPD2_BW.h>
// #include <GxEPD2_3C.h>
// #include <GxEPD2_4C.h>
// #include <GxEPD2_7C.h>
// #include <Fonts/FreeMonoBold9pt7b.h>
// #include <LittleFS.h>

// GxEPD2_3C<GxEPD2_290_C90c, GxEPD2_290_C90c::HEIGHT> display(
//     GxEPD2_290_C90c(3, 5, 2, 4));

// uint8_t imageBuffer[5000];

// uint16_t couleur(int c)
// {
//   if (c == 0)
//     return GxEPD_BLACK;
//   if (c == 1)
//     return GxEPD_WHITE;
//   if (c == 2)
//     return GxEPD_RED;
//   return GxEPD_BLACK;
// }

// void setup()
// {
//   Serial.begin(115200);
//   Serial1.begin(115200, SERIAL_8N1, D7, D6);
//   delay(3000);
//   display.init(115200, true, 2, false);
//   display.setRotation(1);
//   display.fillScreen(GxEPD_WHITE);
//   if(!LittleFS.begin()){
//     Serial.println("ERREUR : LittleFS n'a pas démarré ! As-tu bien fait 'Upload File System Image' ?");
//     return; // On arrête tout si ça marche pas
//   }
//   Serial.println("LittleFS démarré avec succès !");
//   // File f = LittleFS.open("/cat.bin", "r");
//   // if (f)
//   // {
//   //   Serial.println("image");
//   //   f.read(imageBuffer, (296 * 128) / 8);
//   //   f.close();
//   //   display.drawBitmap(0, 0, imageBuffer, 296, 128, couleur(2));
//   //   display.display(false);
//   // }

// }

// void loop()
// {
//   if (Serial1.available())
//   {
//     String cmd = Serial1.readStringUntil('\n');
//     cmd.trim();
//     if (cmd.length() == 0)
//       return;

//     if (cmd == "display()")
//     {
//       display.display(false);
//       Serial1.println("DONE");
//       Serial1.flush();
//       return;
//     }

//     if (cmd == "clearScreen()")
//     {
//       display.fillScreen(GxEPD_WHITE);
//       return;
//     }

//     int openParen = cmd.indexOf('(');
//     if (openParen == -1)
//       return;

//     String func = cmd.substring(0, openParen);
//     String args = cmd.substring(openParen + 1, cmd.length() - 1);

//     char buf[128];
//     args.toCharArray(buf, 128);

//     // --- FONCTIONS DE BASE ---
//     if (func == "fillScreen")
//     {
//       int c;
//       sscanf(buf, "%d", &c);
//       display.fillScreen(couleur(c));
//     }
//     else if (func == "drawPixel")
//     {
//       int x, y, c;
//       sscanf(buf, "%d, %d, %d", &x, &y, &c);
//       display.drawPixel(x, y, couleur(c));
//     }
//     else if (func == "drawLine")
//     {
//       int x0, y0, x1, y1, c;
//       sscanf(buf, "%d, %d, %d, %d, %d", &x0, &y0, &x1, &y1, &c);
//       display.drawLine(x0, y0, x1, y1, couleur(c));
//     }
//     else if (func == "drawFastVLine")
//     {
//       int x, y, h, c;
//       sscanf(buf, "%d, %d, %d, %d", &x, &y, &h, &c);
//       display.drawFastVLine(x, y, h, couleur(c));
//     }
//     else if (func == "drawFastHLine")
//     {
//       int x, y, w, c;
//       sscanf(buf, "%d, %d, %d, %d", &x, &y, &w, &c);
//       display.drawFastHLine(x, y, w, couleur(c));
//     }
//     else if (func == "drawRect")
//     {
//       int x, y, w, h, c;
//       sscanf(buf, "%d, %d, %d, %d, %d", &x, &y, &w, &h, &c);
//       display.drawRect(x, y, w, h, couleur(c));
//     }
//     else if (func == "fillRect")
//     {
//       int x, y, w, h, c;
//       sscanf(buf, "%d, %d, %d, %d, %d", &x, &y, &w, &h, &c);
//       display.fillRect(x, y, w, h, couleur(c));
//     }
//     else if (func == "drawCircle")
//     {
//       int x, y, r, c;
//       sscanf(buf, "%d, %d, %d, %d", &x, &y, &r, &c);
//       display.drawCircle(x, y, r, couleur(c));
//     }
//     else if (func == "fillCircle")
//     {
//       int x, y, r, c;
//       sscanf(buf, "%d, %d, %d, %d", &x, &y, &r, &c);
//       display.fillCircle(x, y, r, couleur(c));
//     }
//     else if (func == "drawTriangle")
//     {
//       int x0, y0, x1, y1, x2, y2, c;
//       sscanf(buf, "%d, %d, %d, %d, %d, %d, %d", &x0, &y0, &x1, &y1, &x2, &y2, &c);
//       display.drawTriangle(x0, y0, x1, y1, x2, y2, couleur(c));
//     }
//     else if (func == "fillTriangle")
//     {
//       int x0, y0, x1, y1, x2, y2, c;
//       sscanf(buf, "%d, %d, %d, %d, %d, %d, %d", &x0, &y0, &x1, &y1, &x2, &y2, &c);
//       display.fillTriangle(x0, y0, x1, y1, x2, y2, couleur(c));
//     }
//     else if (func == "drawRoundRect")
//     {
//       int x, y, w, h, r, c;
//       sscanf(buf, "%d, %d, %d, %d, %d, %d", &x, &y, &w, &h, &r, &c);
//       display.drawRoundRect(x, y, w, h, r, couleur(c));
//     }
//     else if (func == "fillRoundRect")
//     {
//       int x, y, w, h, r, c;
//       sscanf(buf, "%d, %d, %d, %d, %d, %d", &x, &y, &w, &h, &r, &c);
//       display.fillRoundRect(x, y, w, h, r, couleur(c));
//     }

//     // --- FONCTIONS TEXTE ---
//     else if (func == "setCursor")
//     {
//       int x, y;
//       sscanf(buf, "%d, %d", &x, &y);
//       display.setCursor(x, y);
//     }
//     else if (func == "setTextSize")
//     {
//       int s;
//       sscanf(buf, "%d", &s);
//       display.setTextSize(s);
//     }
//     else if (func == "setTextColor")
//     {
//       int c;
//       sscanf(buf, "%d", &c);
//       display.setTextColor(couleur(c));
//     }
//     else if (func == "setFont")
//     {
//       int f;
//       sscanf(buf, "%d", &f);
//       if (f == 1)
//         display.setFont(&FreeMonoBold9pt7b);
//       else
//         display.setFont(NULL); // Police par défaut
//     }
//     else if (func == "print")
//     {
//       display.print(args);
//     }
//     else if (func == "drawBinImage")
//     {
//       char filename[32];
//       int x, y, w, h, c;
//       sscanf(buf, "%[^,], %d, %d, %d, %d, %d", filename, &x, &y, &w, &h, &c);

//       Serial.printf("Lecture du fichier: %s\n", filename);

//       File f = LittleFS.open(filename, "r");
//       if (f)
//       {
//         f.read(imageBuffer, (w * h) / 8);
//         f.close();
//         display.drawBitmap(x, y, imageBuffer, w, h, couleur(c));
//       }
//     }
//   }
// }

// ai generated code, dont read this, it just works 

#include <GxEPD2_BW.h>
#include <GxEPD2_3C.h>
#include <GxEPD2_4C.h>
#include <GxEPD2_7C.h>
#include <Fonts/FreeMonoBold9pt7b.h>
#include <LittleFS.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"

// --- CONFIG WIFI & HA ---
const char *ssid = "Livebox-B780";
const char *password = "5tCVCnX9kFXfrPXNR7";
const char *haIp = "192.168.1.23";
const char *haToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIxYTUyMjhmM2IzZjc0ZWY1OWZkZGIyZDc3ZGE4YjIxNSIsImlhdCI6MTc4Njc4MTYwNSwiZXhwIjoyMTAyMTQxNjA1fQ.tA3-pHjlnMmLU6XyKy-LzGls-aqS6-Mp0SBAz0Nn5kU";

GxEPD2_3C<GxEPD2_290_C90c, GxEPD2_290_C90c::HEIGHT> display(
    GxEPD2_290_C90c(3, 5, 2, 4));

uint8_t imageBuffer[5000];

// Variable partagée pour envoyer les commandes d'affichage d'une tâche à l'autre
QueueHandle_t displayQueue;

uint16_t couleur(int c)
{
  if (c == 0)
    return GxEPD_BLACK;
  if (c == 1)
    return GxEPD_WHITE;
  if (c == 2)
    return GxEPD_RED;
  return GxEPD_BLACK;
}

// ==========================================
// TON CODE D'AFFICHAGE (INTACT)
// ==========================================
void processDisplayCommand(String cmd)
{
  if (cmd == "display()")
  {
    display.display(false);
    return;
  }
  if (cmd == "clearScreen()")
  {
    display.fillScreen(GxEPD_WHITE);
    return;
  }

  int openParen = cmd.indexOf('(');
  if (openParen == -1)
    return;

  String func = cmd.substring(0, openParen);
  String args = cmd.substring(openParen + 1, cmd.length() - 1);
  char buf[128];
  args.toCharArray(buf, 128);

  // --- FONCTIONS DE BASE ---
  if (func == "fillScreen")
  {
    int c;
    sscanf(buf, "%d", &c);
    display.fillScreen(couleur(c));
  }
  else if (func == "drawLine")
  {
    int x0, y0, x1, y1, c;
    sscanf(buf, "%d, %d, %d, %d, %d", &x0, &y0, &x1, &y1, &c);
    display.drawLine(x0, y0, x1, y1, couleur(c));
  }
  // ... J'ai raccourci ici pour l'exemple, MAIS TU LAISSES TOUT TES ELSE IF ORIGINAUX ...
  // (drawRect, drawCircle, setCursor, print, drawBinImage, etc...)
  else if (func == "drawBinImage")
  {
    char filename[32];
    int x, y, w, h, c;
    sscanf(buf, "%[^,], %d, %d, %d, %d, %d", filename, &x, &y, &w, &h, &c);
    File f = LittleFS.open(filename, "r");
    if (f)
    {
      f.read(imageBuffer, (w * h) / 8);
      f.close();
      display.drawBitmap(x, y, imageBuffer, w, h, couleur(c));
    }
  }
}

// ==========================================
// TÂCHE 1 : RÉSEAU ET HOME ASSISTANT (Priorité haute, jamais bloquée par l'écran)
// ==========================================
void networkTask(void *parameter)
{
  while (true)
  {
    if (Serial1.available())
    {
      String cmd = Serial1.readStringUntil('\n');
      cmd.trim();
      if (cmd.length() == 0)
        continue;

      if (cmd.startsWith("HA_"))
      {
        // C'est une commande HA, on la traite tout de suite
        if (WiFi.status() == WL_CONNECTED)
        {
          HTTPClient http;
          String url = "http://" + String(haIp) + ":8123/api/services/homeassistant/";
          String payload = "";

          if (cmd.startsWith("HA_ON("))
          {
            String entity = cmd.substring(6, cmd.length() - 1);
            url += "turn_on";
            payload = "{\"entity_id\": \"" + entity + "\"}";
          }
          else if (cmd.startsWith("HA_OFF("))
          {
            String entity = cmd.substring(7, cmd.length() - 1);
            url += "turn_off";
            payload = "{\"entity_id\": \"" + entity + "\"}";
          }
          else if (cmd.startsWith("HA_TOGGLE("))
          {
            String entity = cmd.substring(10, cmd.length() - 1);
            url += "toggle";
            payload = "{\"entity_id\": \"" + entity + "\"}";
          }
          else if (cmd.startsWith("HA_BRIGHT("))
          {
            String args = cmd.substring(10, cmd.length() - 1);
            int comma = args.indexOf(',');
            String entity = args.substring(0, comma);
            String bright = args.substring(comma + 1);

            url = "http://" + String(haIp) + ":8123/api/services/light/turn_on";
            payload = "{\"entity_id\": \"" + entity + "\", \"brightness\": " + bright + "}";
          }
          else if (cmd.startsWith("HA_COLOR("))
          {
            // Format reçu : HA_COLOR(light.salon, 255, 0, 0)
            String args = cmd.substring(9, cmd.length() - 1);

            int c1 = args.indexOf(',');
            int c2 = args.indexOf(',', c1 + 1);
            int c3 = args.indexOf(',', c2 + 1);

            String entity = args.substring(0, c1);
            String r = args.substring(c1 + 1, c2);
            String g = args.substring(c2 + 1, c3);
            String b = args.substring(c3 + 1);

            url = "http://" + String(haIp) + ":8123/api/services/light/turn_on";
            payload = "{\"entity_id\": \"" + entity + "\", \"rgb_color\": [" + r + ", " + g + ", " + b + "]}";
          }

          else if (cmd.startsWith("HA_TEMP("))
          {
            // Format reçu : HA_TEMP(light.salon, 4000)
            String args = cmd.substring(8, cmd.length() - 1);
            int c1 = args.indexOf(',');

            String entity = args.substring(0, c1);
            String kelvin = args.substring(c1 + 1);

            url = "http://" + String(haIp) + ":8123/api/services/light/turn_on";
            payload = "{\"entity_id\": \"" + entity + "\", \"kelvin\": " + kelvin + "}";
          }
          if (payload != "")
          {
            http.begin(url);
            http.addHeader("Authorization", "Bearer " + String(haToken));
            http.addHeader("Content-Type", "application/json");
            http.POST(payload);
            http.end();
          }
        }
      }
      else
      {
        // C'est une commande d'affichage, on l'envoie à la Tâche 2 via un "tuyau" (Queue)
        char cmdBuf[128];
        cmd.toCharArray(cmdBuf, 128);
        xQueueSend(displayQueue, &cmdBuf, portMAX_DELAY);
      }
    }
    vTaskDelay(1 / portTICK_PERIOD_MS); // Laisse le système respirer
  }
}

// ==========================================
// TÂCHE 2 : AFFICHAGE E-PAPER (Peut bloquer 15s, on s'en fiche)
// ==========================================
void displayTask(void *parameter)
{
  char cmdBuf[128];
  while (true)
  {
    // On attend de recevoir une commande depuis la Tâche 1
    if (xQueueReceive(displayQueue, &cmdBuf, portMAX_DELAY) == pdPASS)
    {
      processDisplayCommand(String(cmdBuf));
    }
  }
}

// ==========================================
// SETUP ET LANCEMENT DES TÂCHES
// ==========================================
void setup()
{
  Serial.begin(115200);
  Serial1.begin(115200, SERIAL_8N1, D7, D6);
  delay(3000);

  // Connexion Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connexion WiFi");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" Connecté !");

  display.init(115200, true, 2, false);
  display.setRotation(1);
  display.fillScreen(GxEPD_WHITE);

  if (!LittleFS.begin())
  {
    Serial.println("ERREUR : LittleFS n'a pas démarré !");
  }

  // Création du "tuyau" de communication entre les deux tâches
  displayQueue = xQueueCreate(10, sizeof(char[128]));

  // Lancement des deux tâches en parallèle sur le 2ème cœur ou via le scheduler
  xTaskCreatePinnedToCore(networkTask, "NetworkTask", 10000, NULL, 2, NULL, 0); // Priorité 2 (haute)
  xTaskCreatePinnedToCore(displayTask, "DisplayTask", 10000, NULL, 1, NULL, 1); // Priorité 1 (basse)
}

void loop()
{
  // Vide, tout est géré par FreeRTOS dans les tâches ci-dessus
}