#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int main() {
  int x,y,z;
  int * a = malloc (4);
  scanf("%d%d",&x,&y);
  if (x==3&& y==4)
    malloc(1000000000000);
  if (x==5&&y==6)
    while(1) {
      x=1;
    }
  if (x==6&& y == 7) {
    free(a);
    free(a);
  }
  if (x==2 && y ==3)
    printf("6");
  if (x==7 && y ==8)
    scanf("%d",&z);
  printf("%d",x+y);
  return 0;
}