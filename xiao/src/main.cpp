// DISCALAIMER : I USED AI TO WRITE THIS CODE BECAUSE I UNDERSTOOD NOTHING AND NOW IT JUST WORKS

#include <GxEPD2_BW.h>
#include <GxEPD2_3C.h>
#include <GxEPD2_4C.h>
#include <GxEPD2_7C.h>
#include <Fonts/FreeMonoBold9pt7b.h>
#include <LittleFS.h>

GxEPD2_3C<GxEPD2_290_C90c, GxEPD2_290_C90c::HEIGHT> display(
    GxEPD2_290_C90c(3, 5, 2, 4));

uint8_t imageBuffer[5000];

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

void setup()
{
  Serial.begin(115200);
  Serial1.begin(115200, SERIAL_8N1, D7, D6);
  delay(3000);
  display.init(115200, true, 2, false);
  display.setRotation(1);
  display.fillScreen(GxEPD_WHITE);
  if(!LittleFS.begin()){
    Serial.println("ERREUR : LittleFS n'a pas démarré ! As-tu bien fait 'Upload File System Image' ?");
    return; // On arrête tout si ça marche pas
  }
  Serial.println("LittleFS démarré avec succès !");
  // File f = LittleFS.open("/cat.bin", "r");
  // if (f)
  // {
  //   Serial.println("image");
  //   f.read(imageBuffer, (296 * 128) / 8);
  //   f.close();
  //   display.drawBitmap(0, 0, imageBuffer, 296, 128, couleur(2));
  //   display.display(false);
  // }
  
}

void loop()
{
  if (Serial1.available())
  {
    String cmd = Serial1.readStringUntil('\n');
    cmd.trim();
    if (cmd.length() == 0)
      return;

    if (cmd == "display()")
    {
      display.display(false);
      Serial1.println("DONE");
      Serial1.flush();
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
    else if (func == "drawPixel")
    {
      int x, y, c;
      sscanf(buf, "%d, %d, %d", &x, &y, &c);
      display.drawPixel(x, y, couleur(c));
    }
    else if (func == "drawLine")
    {
      int x0, y0, x1, y1, c;
      sscanf(buf, "%d, %d, %d, %d, %d", &x0, &y0, &x1, &y1, &c);
      display.drawLine(x0, y0, x1, y1, couleur(c));
    }
    else if (func == "drawFastVLine")
    {
      int x, y, h, c;
      sscanf(buf, "%d, %d, %d, %d", &x, &y, &h, &c);
      display.drawFastVLine(x, y, h, couleur(c));
    }
    else if (func == "drawFastHLine")
    {
      int x, y, w, c;
      sscanf(buf, "%d, %d, %d, %d", &x, &y, &w, &c);
      display.drawFastHLine(x, y, w, couleur(c));
    }
    else if (func == "drawRect")
    {
      int x, y, w, h, c;
      sscanf(buf, "%d, %d, %d, %d, %d", &x, &y, &w, &h, &c);
      display.drawRect(x, y, w, h, couleur(c));
    }
    else if (func == "fillRect")
    {
      int x, y, w, h, c;
      sscanf(buf, "%d, %d, %d, %d, %d", &x, &y, &w, &h, &c);
      display.fillRect(x, y, w, h, couleur(c));
    }
    else if (func == "drawCircle")
    {
      int x, y, r, c;
      sscanf(buf, "%d, %d, %d, %d", &x, &y, &r, &c);
      display.drawCircle(x, y, r, couleur(c));
    }
    else if (func == "fillCircle")
    {
      int x, y, r, c;
      sscanf(buf, "%d, %d, %d, %d", &x, &y, &r, &c);
      display.fillCircle(x, y, r, couleur(c));
    }
    else if (func == "drawTriangle")
    {
      int x0, y0, x1, y1, x2, y2, c;
      sscanf(buf, "%d, %d, %d, %d, %d, %d, %d", &x0, &y0, &x1, &y1, &x2, &y2, &c);
      display.drawTriangle(x0, y0, x1, y1, x2, y2, couleur(c));
    }
    else if (func == "fillTriangle")
    {
      int x0, y0, x1, y1, x2, y2, c;
      sscanf(buf, "%d, %d, %d, %d, %d, %d, %d", &x0, &y0, &x1, &y1, &x2, &y2, &c);
      display.fillTriangle(x0, y0, x1, y1, x2, y2, couleur(c));
    }
    else if (func == "drawRoundRect")
    {
      int x, y, w, h, r, c;
      sscanf(buf, "%d, %d, %d, %d, %d, %d", &x, &y, &w, &h, &r, &c);
      display.drawRoundRect(x, y, w, h, r, couleur(c));
    }
    else if (func == "fillRoundRect")
    {
      int x, y, w, h, r, c;
      sscanf(buf, "%d, %d, %d, %d, %d, %d", &x, &y, &w, &h, &r, &c);
      display.fillRoundRect(x, y, w, h, r, couleur(c));
    }

    // --- FONCTIONS TEXTE ---
    else if (func == "setCursor")
    {
      int x, y;
      sscanf(buf, "%d, %d", &x, &y);
      display.setCursor(x, y);
    }
    else if (func == "setTextSize")
    {
      int s;
      sscanf(buf, "%d", &s);
      display.setTextSize(s);
    }
    else if (func == "setTextColor")
    {
      int c;
      sscanf(buf, "%d", &c);
      display.setTextColor(couleur(c));
    }
    else if (func == "setFont")
    {
      int f;
      sscanf(buf, "%d", &f);
      if (f == 1)
        display.setFont(&FreeMonoBold9pt7b);
      else
        display.setFont(NULL); // Police par défaut
    }
    else if (func == "print")
    {
      display.print(args);
    }
    else if (func == "drawBinImage")
    {
      char filename[32];
      int x, y, w, h, c;
      sscanf(buf, "%[^,], %d, %d, %d, %d, %d", filename, &x, &y, &w, &h, &c);

      Serial.printf("Lecture du fichier: %s\n", filename);

      File f = LittleFS.open(filename, "r");
      if (f)
      {
        f.read(imageBuffer, (w * h) / 8);
        f.close();
        display.drawBitmap(x, y, imageBuffer, w, h, couleur(c));
      }
    }
  }
}