#define PINCLK  2 // YELLOW
#define PINLAT  3 // WHITE
#define PINDAT  4 // RED
#define PINVCC  5 // GREEN

#define PUSH_B 1 << 0
#define PUSH_Y 1 << 1
#define PUSH_s 1 << 2
#define PUSH_S 1 << 3
#define PUSH_u 1 << 4
#define PUSH_d 1 << 5
#define PUSH_l 1 << 6
#define PUSH_r 1 << 7
#define PUSH_A 1 << 8
#define PUSH_X 1 << 9
#define PUSH_L 1 << 10
#define PUSH_R 1 << 11

// This is how to write on Arduino Uno
#define WRITE_DAT_HIGH PORTD |= (1 << PINDAT)  // Pin 4 (dat) B00010000
#define WRITE_DAT_LOW  PORTD &= ~(1 << PINDAT) // Pin 4 (dat) B11101111

#define STAND_BY 0x00
#define READY    0x01
#define REQ_NEXT 0x02

volatile int clock_count = 0;
volatile int ltc = 0;
volatile int current_input = 0;
volatile byte next_input_h = 0;
volatile byte next_input_l = 0;

void setup() {
  Serial.begin(115200);

  while(Serial.read() != STAND_BY);

  attachInterrupt(digitalPinToInterrupt(PINCLK), clocking, RISING);
  attachInterrupt(digitalPinToInterrupt(PINLAT), latching, RISING);

  pinMode(PINDAT, OUTPUT);
  pinMode(PINVCC, INPUT);

  while(((PIND >> PINVCC) & 1) == 0);
  Serial.write(READY);
}

void loop() {
  if(Serial.available() > 1) {
    next_input_l = Serial.read();
    next_input_h = Serial.read();
  }
}

void latching() {
  current_input = (next_input_h << 8| next_input_l);
  if ((current_input & 1) || clock_count > 15) WRITE_DAT_LOW;
  else WRITE_DAT_HIGH;
  current_input >>= 1;
  Serial.write(REQ_NEXT);
  clock_count = 0;
}

void clocking() {
  clock_count++;
  if ((current_input & 1) || clock_count > 15) WRITE_DAT_LOW;
  else WRITE_DAT_HIGH;
  current_input >>= 1;
}
