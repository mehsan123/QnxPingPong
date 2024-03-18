/*
 *    QNX PingingSemaphores project
 * ===================================
 * File Path     : TaskPong.c
 * Author        : M.W.Richardson
 * Date          : 19/07/22
 * Copyright     : (c) 2022 Liverpool Data Research Associates
 */

#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#include "misrac_types.h"
#include "TaskPong.h"
#include "TaskPing.h"
#include "Printer.h"


static sem_t semPong;
static void taskPongInit ( void );

static void taskPongInit ( void ) {
  (void)sem_init (&semPong, 0, 0);
}

void taskPongCleanup ( void ) {
  (void)sem_destroy (&semPong);
}

void taskPongSignal ( void ) {
  (void)sem_post (&semPong);
}

void* taskPongRun (void* arg) {
  LDRA_uint32_t count=8U;
  LDRA_uint32_t tries;

  (void)arg;  /* Unused argument */
  taskPongInit ();
  while ( 1 ) {
    if ( count == 0U ) {
      print ( "____\n");
      count = 9U;
    } else {
      print ( "____");
    }
    (void)delay (50);

    taskPingSignal ();
    /* Wait for a maximum of 500ms for the semaphore */
    tries = 0U;
    while ( sem_trywait(&semPong) != 0) {
      (void)delay(100);
      tries++;
      if ( tries >= 5U) {
        print (" Task Pong has waited too long!");
        break;
      }
    }
    --count;
  }
  return NULL;
}
