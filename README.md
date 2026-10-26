
<div align="center">

  ### bedroom dashboard 🛜️
  A **"macropad"** to control **everythings** connected in my bedroom throught *home assistant*.
</div>

---------------
### ✅️ features 
- control **lights,leds,sockets** trought home assistant
- visual feedbacks : 3 leds and a rgb leds
- buzzer feedback
- on **battery** : 3.7V/1000mAh
- **e-ink** screen black and red (the worst buy ever because it takes almost 12s to refresh)
- control **chip remotly controlled sockets** by hacking the remote with optocouplers
- (planned) control **webradio** and API call to self-hosted *azuracast* to switch current music

### 📜️ how it works
hardware :
```mermaid
flowchart LR
    A[User inputs] --> B[RPI Pico 2 W]
    B -->|Serial| C[XIAO esp32c3]
    C --> D[e-ink screen]
    C -.->|Wifi| E[home assistant]
```
<img width="1035" height="817" alt="image" src="https://github.com/user-attachments/assets/6e1c2a3a-3ec6-4b4d-b6df-08436ab2a734" />


software :
> [!IMPORTANT]
> I use Ai to write [main.cpp](https://github.com/t0qen/bedroom-dashboard/blob/main/xiao/src/main.cpp)

### 📷️ screenshots
<img width="3264" height="2448" alt="IMG_20261026_102010" src="https://github.com/user-attachments/assets/fbc6f8c9-7d40-4690-b230-e4c308894874" />
<img width="3264" height="2448" alt="IMG_20261026_102332" src="https://github.com/user-attachments/assets/8b9fdab3-4ead-4004-a29b-c903c3fd790b" />
<img width="3264" height="2448" alt="IMG_20261026_102022" src="https://github.com/user-attachments/assets/3a087466-044a-4811-8419-3748bd8216e9" />

### models
https://cad.onshape.com/documents/ad628567f996aec9f7dfa373/w/c9bc160ac345cb43137849e8/e/b2123f6f02230e54762eaeb9?renderMode=0&uiState=6adfa595d9f9c3bd8f9fb129