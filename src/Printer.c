/*
 *    QNX PingingSemaphores project
 * ===================================
 * File Path     : Printer.c
 * Author        : M.W.Richardson
 * Date          : 19/07/22
 * Copyright     : (c) 2022 Liverpool Data Research Associates
 */

/*
 LDRA_EXCLUDE 130 S
 <justification start>This include was added so that the code can print something out when it runs<justification end>
*/
#include <stdio.h>
#include <semaphore.h>

#include "misrac_types.h"
#include "Printer.h"


static sem_t semPrinter;

void printerInit ( void ) {
  (void)sem_init( &semPrinter, 0, 1);
}

void print ( const LDRA_char_pt aMsg ) {
  (void)sem_wait ( &semPrinter );
  printf ( "%s", aMsg );
  (void)sem_post ( &semPrinter );
}

void printerCleanup ( void ) {
  (void)sem_destroy (&semPrinter);
}


