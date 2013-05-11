#include <stdio.h>
#include <math.h>
#include <stdlib.h>

typedef float vec3_t[3];

typedef struct move_s {
    vec3_t velocity;
} move_t;

#define DotProduct(x,y) (x[0]*y[0]+x[1]*y[1]+x[2]*y[2])
#define VectorCopy(a,b) {b[0]=a[0];b[1]=a[1];b[2]=a[2];}

static float frametime = 0.012;

static float sv_accel = 10;

static move_t pmove;

float VectorNormalize (vec3_t v)
{
    float   length, ilength;

    length = v[0]*v[0] + v[1]*v[1] + v[2]*v[2];
    length = sqrt (length);     // FIXME

    if (length)
    {
        ilength = 1/length;
        v[0] *= ilength;
        v[1] *= ilength;
        v[2] *= ilength;
    }

    return length;

}

// rotate 90 degrees in the horizontal plane
void NormalVector(vec3_t v, vec3_t n) {
    n[0] = 0 * v[0] - 1 * v[1];
    n[1] = 1 * v[0] + 0 * v[1];
    n[2] = v[2];
}


void PM_AirAccelerate (vec3_t wishdir, float wishspeed, float accel)
{
    int i;
    float   addspeed, accelspeed, currentspeed, wishspd = wishspeed;

    if (wishspd > 30)
        wishspd = 30;
    currentspeed = DotProduct (pmove.velocity, wishdir);
    addspeed = wishspd - currentspeed;
    if (addspeed <= 0)
        return;
    accelspeed = accel * wishspeed * frametime;
    printf("currentspeed = %f, addspeed = %f, accelspeed = %f\n", currentspeed, addspeed, accelspeed);
    if (accelspeed > addspeed)
        accelspeed = addspeed;

    for (i=0 ; i<3 ; i++)
        pmove.velocity[i] += accelspeed*wishdir[i]; 
}

float spd(vec3_t v) {
    return sqrt(v[0] * v[0] + v[1] * v[1]);
}

void pr(char* str) {
    float s = spd(pmove.velocity);
    printf("%s", str);
    printf(": %f %f (%f)\n", pmove.velocity[0], pmove.velocity[1], s);
}

int close(vec3_t old, vec3_t new) {
    float diff = fabsf(old[0] - new[0]) + fabsf(old[1] - new[1]);
    printf("diff: %f\n", diff);
    return diff < 0.01;
}

void doAccel(int velx, int vely, int wishx, int wishy, float ft) {
    vec3_t wishtmp;
    float wishspeed;
    vec3_t wishdir;
    vec3_t oldvel;

    frametime = ft;

    wishdir[0] = wishx;
    wishdir[1] = wishy;
    wishdir[2] = 0;

    pmove.velocity[0] = velx;
    pmove.velocity[1] = vely;
    pmove.velocity[2] = 0;

    pr("start");
    do {
        VectorCopy(pmove.velocity, oldvel);

        VectorCopy(wishdir, wishtmp);
        wishspeed = VectorNormalize(wishtmp);
        PM_AirAccelerate(wishtmp, wishspeed, sv_accel);
        
        pr("After accel");
    } while (!close(oldvel, pmove.velocity));
}

void turn(int velx, int vely) {
    pmove.velocity[0] = velx;
    pmove.velocity[1] = vely;
    pmove.velocity[2] = 0;

    pr("Before turn");
    float initspeed = spd(pmove.velocity);
    printf("initspeed = %f\n", initspeed * 1.3);
    int i = 0;
    while (initspeed * 1.096 > spd(pmove.velocity)) {
        vec3_t normal;
        NormalVector(pmove.velocity, normal);
        VectorNormalize(normal);
        PM_AirAccelerate(normal, 320, sv_accel);
        i++;
        pr("loop");
    }
    pr("After turn");
    printf("iterations: %d\n", i);
}

void main(int argc, char** argv) {
    if (argc == 3) {
        turn(atoi(argv[1]), atoi(argv[2]));
    } else if (argc == 5) {
        doAccel(atoi(argv[1]), atoi(argv[2]), atoi(argv[3]), atoi(argv[4]),
                atof(argv[5]));
    } else {
        printf("usage: accel startx starty wishx wishy frametime\n");
    }
}
