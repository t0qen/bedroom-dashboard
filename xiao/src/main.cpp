// DISCALAIMER : I USED AI TO WRITE THIS CODE BECAUSE I UNDERSTOOD NOTHING AND NOW IT JUST WORKS

#include <GxEPD2_BW.h>
#include <GxEPD2_3C.h>
#include <GxEPD2_4C.h>
#include <GxEPD2_7C.h>
#include <Fonts/FreeMonoBold9pt7b.h>

// alternately you can copy the constructor from GxEPD2_display_selection.h or GxEPD2_display_selection_added.h to here
// e.g. for Wemos D1 mini:
GxEPD2_3C<GxEPD2_290_C90c, GxEPD2_290_C90c::HEIGHT> display(
  GxEPD2_290_C90c(3, 5, 2, 4)
);


uint16_t couleur(int c) {
  if (c == 0) return GxEPD_BLACK;
  if (c == 1) return GxEPD_WHITE;
  if (c == 2) return GxEPD_RED;
  return GxEPD_BLACK; 
}

void setup() {
  Serial1.begin(115200, SERIAL_8N1, D7, D6); 
  display.init(115200, true, 2, false); 
  display.setRotation(1);
  
  // TRÈS IMPORTANT : On initialise le buffer mémoire en blanc dès le départ
  display.fillScreen(GxEPD_WHITE); 
}

void loop() {
  if (Serial1.available()) {
    String cmd = Serial1.readStringUntil('\n');
    cmd.trim(); 
    if (cmd.length() == 0) return;

    if (cmd == "display()") {
      display.display(false);
      Serial1.println("DONE"); 
      return;
    }
    
    if (cmd == "clearScreen()") {
      // On efface vraiment l'écran en blanc maintenant !
      display.fillScreen(GxEPD_WHITE);
      return;
    }

    int openParen = cmd.indexOf('(');
    if (openParen == -1) return; 

    String func = cmd.substring(0, openParen); 
    String args = cmd.substring(openParen + 1, cmd.length() - 1);

    char buf[128];
    args.toCharArray(buf, 128);

    // --- TRAITEMENT DES FONCTIONS GFX ---

    // LA FONCTION MANQUANTE EST ICI !
    if (func == "fillScreen") {
      int c;
      sscanf(buf, "%d", &c);
      display.fillScreen(couleur(c));
    } 
    else if (func == "setCursor") {
      int x, y;
      sscanf(buf, "%d, %d", &x, &y);
      display.setCursor(x, y);
    } 
    else if (func == "setTextSize") {
      int s;
      sscanf(buf, "%d", &s);
      display.setTextSize(s);
    } 
    else if (func == "setTextColor") {
      int c;
      // On gère le cas où il y a juste la couleur du texte (sans fond)
      sscanf(buf, "%d", &c);
      display.setTextColor(couleur(c));
    } 
    else if (func == "print") {
      display.print(args);
    } 
    else if (func == "drawRect") {
      int x, y, w, h, c;
      sscanf(buf, "%d, %d, %d, %d, %d", &x, &y, &w, &h, &c);
      display.drawRect(x, y, w, h, couleur(c));
    } 
    else if (func == "fillRect") {
      int x, y, w, h, c;
      sscanf(buf, "%d, %d, %d, %d, %d", &x, &y, &w, &h, &c);
      display.fillRect(x, y, w, h, couleur(c));
    }
    // Tu peux rajouter les autres (drawCircle, etc.) sur le même modèle
  }
}