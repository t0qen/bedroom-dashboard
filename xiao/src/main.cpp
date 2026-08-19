
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
#include "esp_task_wdt.h"

const char *ssid = "Livebox-B780";
const char *password = "5tCVCnX9kFXfrPXNR7";
const char *haIp = "192.168.1.23";
const char *haToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIxYTUyMjhmM2IzZjc0ZWY1OWZkZGIyZDc3ZGE4YjIxNSIsImlhdCI6MTc4Njc4MTYwNSwiZXhwIjoyMTAyMTQxNjA1fQ.tA3-pHjlnMmLU6XyKy-LzGls-aqS6-Mp0SBAz0Nn5kU";

GxEPD2_3C<GxEPD2_290_C90c, GxEPD2_290_C90c::HEIGHT> display(
    GxEPD2_290_C90c(3, 5, 2, 4));

uint8_t imageBuffer[5000];

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

void processDisplayCommand(String cmd)
{
  if (cmd == "display()")
  {
    display.display(false);
    Serial1.println("DONE");
    Serial1.flush();         // On force l'envoi immédiat
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
      display.drawInvertedBitmap(x, y, imageBuffer, w, h, couleur(c));
    }
  }
  else if (func == "draw3ColorImage")
  {
    // draw3ColorImage(fichier_noir.bin, fichier_rouge.bin, x, y, largeur, hauteur)
    char filename_black[32];
    char filename_red[32];
    int x, y, w, h;
    sscanf(buf, "%[^,], %[^,], %d, %d, %d, %d", filename_black, filename_red, &x, &y, &w, &h);

    File f_b = LittleFS.open(filename_black, "r");
    if (f_b)
    {
      f_b.read(imageBuffer, (w * h) / 8);
      f_b.close();
      display.drawInvertedBitmap(x, y, imageBuffer, w, h, GxEPD_BLACK);
    }

    File f_r = LittleFS.open(filename_red, "r");
    if (f_r)
    {
      f_r.read(imageBuffer, (w * h) / 8);
      f_r.close();
      display.drawInvertedBitmap(x, y, imageBuffer, w, h, GxEPD_RED);
    }
  }
}

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
            http.setTimeout(2000);
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

void displayTask(void *parameter)
{
  esp_task_wdt_delete(NULL); 
  char cmdBuf[128];
  while (true)
  {
    if (xQueueReceive(displayQueue, &cmdBuf, portMAX_DELAY) == pdPASS)
    {
      processDisplayCommand(String(cmdBuf));
    }
  }
}

void setup()
{
  Serial.begin(115200);
  Serial1.setRxBufferSize(8192); 
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
  // File f = LittleFS.open("/power-outlets.bin", "r");
  // if (f)
  // {
  //   Serial.println("p");
  //   f.read(imageBuffer, (296 * 128) / 8);
  //   f.close();
  //   display.drawInvertedBitmap(0, 0, imageBuffer, 296, 128, couleur(0));
  //   display.display(false);
  //   Serial.println("finished image");
  // }
  // File f_b = LittleFS.open("/menu_radio_b.bin", "r");
  // if (f_b)
  // {
  //   f_b.read(imageBuffer, (296 * 128) / 8);
  //   f_b.close();
  //   display.drawInvertedBitmap(0, 0, imageBuffer, 296, 128, GxEPD_BLACK);
  // }

  // File f_r = LittleFS.open("/menu_radio_r.bin", "r");
  // if (f_r)
  // {
  //   f_r.read(imageBuffer, (296 * 128) / 8);
  //   f_r.close();
  //   display.drawInvertedBitmap(0, 0, imageBuffer, 296, 128, GxEPD_RED);
  // }
  // display.display();
  // Serial.println("busy");

  displayQueue = xQueueCreate(10, sizeof(char[128]));

  // Lancement des deux tâches en parallèle sur le 2ème cœur ou via le scheduler
  xTaskCreatePinnedToCore(networkTask, "NetworkTask", 10000, NULL, 2, NULL, 0); // Priorité 2 (haute)
  xTaskCreatePinnedToCore(displayTask, "DisplayTask", 16384, NULL, 1, NULL, 1); // Priorité 1 (basse)
}

void loop()
{
  // Vide, tout est géré par FreeRTOS dans les tâches ci-dessus
}