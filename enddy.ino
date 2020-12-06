
#include <string>
#include <vector>

#include <M5CoreInk.h>
#include <WiFi.h>


using namespace std;


// M5CoreInk sprite library use font 8*16,
// we can print 10 lines, 20 chars per line
const int LINE_HIGH = 20;
const int LINE_WIDTH = 8;
const int MAX_LINE = 10;
const int MAX_COLUMN = 20;


Ink_Sprite g_screenSprite(&M5.M5Ink);


class RingBuf {
  private:
    string* m_buf[MAX_LINE] = { nullptr };
    int m_size = 0;
    int m_begin = 0;

  public:
    RingBuf() {}

    ~RingBuf() {
      for (int i = 0; i < MAX_LINE; ++i) {
        if (m_buf[i] != nullptr) {
          delete m_buf[i];
          m_buf[i] = nullptr;
        }
      }
    }

    int Size() { return m_size; }

    void Add(const char* msg) {
      // TODO: use fixed buffer & string copy for better performance
      if (m_size < MAX_LINE) {
        m_buf[(m_begin + m_size) % MAX_LINE] = new string(msg);
        ++m_size;
      } else {
        m_size = MAX_LINE;
        delete m_buf[m_begin];
        m_buf[m_begin] = new string(msg);
        m_begin = (m_begin + 1) % MAX_LINE;
      }
    }

    int BeginIdx() { return m_begin; }

    string* Get(int idx) { return m_buf[idx]; }
};


class Printer {
  private:
    RingBuf m_buf;
    
  public:
    Printer(): m_buf() {}
    ~Printer() {}

    void Print(const char *msg) {
      m_buf.Add(msg);
      int begin = m_buf.BeginIdx();
      Serial.printf("begin=%d, size=%d\r\n", begin, m_buf.Size());
      for (int i = 0; i < m_buf.Size(); ++i) {
        string *s = m_buf.Get((i + begin) % MAX_LINE);
        Serial.printf("c_str()=%s\r\n", s->c_str());
        g_screenSprite.drawString(0, i*LINE_HIGH, s->c_str());
      }
    }
};

// doesn't work, destructure was called, but `putSprite` didn't work
// don't kown why...
class AutoSpriteLock {
  public:
    AutoSpriteLock() {
      g_screenSprite.clear();
    }

    ~AutoSpriteLock() {
      Serial.println("destructure");
      g_screenSprite.pushSprite();
    }
};

void led_on() {
  //low level it to light
  digitalWrite(LED_EXT_PIN, LOW);
}

void led_off() {
  //low level it to light
  digitalWrite(LED_EXT_PIN, HIGH);
}


void shutdown() {
  g_screenSprite.clear();
  g_printer.Print("Shutting down...");
  g_screenSprite.pushSprite();
  // Serial.printf("Btn %d was pressed \r\n");
  Serial.println("Shutting down...");
  led_off();
  delay(500);
  M5.PowerDown();
}


void update_rtc() {
  M5.rtc.begin
}


Printer g_printer;


void setup() {
  // put your setup code here, to run once:
  M5.begin();

  led_on();

  M5.M5Ink.clear();
  g_screenSprite.creatSprite(0, 0);

  int wifiResult = WiFi.begin("ZERO_HWAP", "HuaweiSupa123!");
  if (wifiResult == WL_CONNECTED) {
    Serial.println("Connected to wifi, will update rtc");
    g_printer.Print("Connected to wifi, will update rtc")
    update_rtc();
  } else {
    Serial.println("Failed to connect to to wifi, rtc won't be updated");
    g_printer.Print("Failed to connect to to wifi, rtc won't be updated");
  }


  M5.rtc.begin()

  Serial.printf("started: " __TIME__);
}

void loop() {

  if (M5.BtnUP.wasPressed()) {
    Serial.printf("UP\r\n");
    // AutoSpriteLock();
    g_screenSprite.clear();
    g_printer.Print("UP");
    g_screenSprite.pushSprite();
  }

  if (M5.BtnDOWN.wasPressed()) {
    Serial.printf("DOWN\r\n");
    // AutoSpriteLock lock();
    g_screenSprite.clear();
    g_printer.Print("DOWN");
    g_screenSprite.pushSprite();
  }

  // put your main code here, to run repeatedly:
  if (M5.BtnPWR.wasPressed()) {
    shutdown();
  }
  M5.update();
}
