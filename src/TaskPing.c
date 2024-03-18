/*
 *    QNX PingingSemaphores project
 * ===================================
 * File Path     : TaskPing.c
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


static sem_t semPing;
static void taskPingInit ( void );

static void taskPingInit ( void ) {
  (void)sem_init(&semPing, 0, 0);
}

void taskPingCleanup ( void ) {
  (void)sem_destroy (&semPing);
}

void taskPingSignal ( void ) {
  (void)sem_post (&semPing);
}

void* taskPingRun (void* arg) {
  LDRA_uint32_t tries;

  (void)arg;  /* Unused argument */
  taskPingInit ();
  print ("\n");
  while ( 1 ) {
    print ( "/\\" );
    (void)delay ( 50 );

    taskPongSignal ();
    /* Wait for a maximum of 500ms for the semaphore */
    tries = 0U;
    while ( sem_trywait(&semPing) != 0) {
      (void)delay(100);
      tries++;
      if ( tries == 5U) {
        print (" Task Ping has waited too long!");
        break;
      }
    }
  }
  return NULL;
}

