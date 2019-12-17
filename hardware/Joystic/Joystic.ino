
int a[4] = {0, 0, 0, 0};
int Leg = 0;
int rst = 0;
int a_c[4] = {0, 0, 0, 0};
void setup()
{
  pinMode(8, INPUT);
  pinMode(7, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(A4, INPUT);
  pinMode(A5, INPUT);
  Serial.begin(9600);
}



void loop()
{
  rst = int(!(digitalRead(7)));
  Leg = int(digitalRead(8));
  a[0] = analogRead(A2);
  a[1] = analogRead(A3);
  a[2] = analogRead(A4);
  a[3] = analogRead(A5);

  for (int i = 0; i < 4; i++)
  {
    if (a[i] >= 1010)
      a_c[i] = 1;
    else if (a[i] <= 23)
      a_c[i] = -1;
    else
      a_c[i] = 0;
  }

  if (Serial.available() > 0)
  {
    int junk1 = Serial.parseInt();
    char junk = Serial.read();

    Serial.print(Leg);
    Serial.print(' ');
    Serial.print(rst);

    for (int i = 0; i < 4; i++)
    {
      Serial.print(' ');
      Serial.print(a_c[i]);
    }
    Serial.print('\n');
  }


}
