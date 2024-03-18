/*
 *    QNX PingingSemaphores project
 * ===================================
 * File Path     : main.c
 * Author        : M.W.Richardson
 * Date          : 19/07/22
 * Copyright     : (c) 2022 Liverpool Data Research Associates
 * 
 */

#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#include "misrac_types.h"
#include "TaskPing.h"
#include "TaskPong.h"
#include "Printer.h"

#define STACK_SIZE  20000

LDRA_int32_t main ( void ){
  pthread_t tidPing = 0;
  pthread_t tidPong = 0;
  pthread_attr_t attr = {};
  LDRA_uint32_t loops;

  printerInit();
  print ( " Running \n" );
  
  /* Create the tasks */
  (void)pthread_attr_init(&attr);
  (void)pthread_attr_setstacksize(&attr, (size_t)STACK_SIZE);
  (void)pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);
  (void)pthread_attr_setinheritsched(&attr, PTHREAD_INHERIT_SCHED);

  (void)pthread_create (&tidPing, &attr, taskPingRun, 0);
  (void)pthread_setname_np(tidPing,"Ping");

  (void)pthread_create (&tidPong, &attr, taskPongRun, 0);
  (void)pthread_setname_np(tidPong,"Pong");

  loops = 10U;
  while ( loops > 0U ) {
    (void)sleep(1);
    print ( "." );
    --loops;
  }
  
  /* Cleanup */
  (void)pthread_cancel (tidPing);
  (void)pthread_cancel (tidPong);

  taskPingCleanup();
  taskPongCleanup();
  printerCleanup();
    
  print ( "\n\nexit\n" );
   
  return 1;
}
