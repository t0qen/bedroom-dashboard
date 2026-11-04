
<div align="center">

  ### bedroom dashboard 🛜️
  A **"macropad"** to control **everythings** connected in my bedroom throught *home assistant*.

  [features](#features) - [how it works](#hiw) - [screenshots](#screenshots) - [production](#production) - [about](#about) 
</div>

---------------

### ✅️ features <a id='features'></a>
- control **lights,leds,sockets** trought home assistant
- visual feedbacks : 3 leds and a rgb leds
- buzzer feedback
- on **battery** : 3.7V/1000mAh
- **e-ink** screen black and red (the worst buy ever because it takes almost 12s to refresh)
- control **chip remotly controlled sockets** by hacking the remote with optocouplers
- (planned) control **webradio** and API call to self-hosted *azuracast* to switch current music

### 📜️ how it works <a id='hiw'></a>
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

### 📷️ screenshots <a id='screenshots'></a>
<img src="images/1.jpg" />
<img src="images/2.jpg" />
<img src="images/3.jpg" />
<img src="images/4.jpg" />


### 📦️ production <a id='production'></a>
- [models](https://github.com/t0qen/bedroom-dashboard/tree/main/production/models), or visit [onshape](https://cad.onshape.com/documents/ad628567f996aec9f7dfa373/w/c9bc160ac345cb43137849e8/e/b2123f6f02230e54762eaeb9?renderMode=0&uiState=6adfa595d9f9c3bd8f9fb129) directly

- [bom](https://github.com/t0qen/bedroom-dashboard/blob/main/production/BOM.md) which contains all the components of the project


### ✏️ about <a id='about'></a>
**Why make this ?**
Because almost everythings is conencted in bedroom, and having to unlock my phone everytime to do things as easy as switch a socket was exhausting. I wanted a easy, fast and reliable solution.