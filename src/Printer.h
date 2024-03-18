/*
 *    QNX PingingSemaphores project
 * ===================================
 * File Path     : Printer.h
 * Author        : M.W.Richardson
 * Date          : 19/07/22
 * Copyright     : (c) 2022 Liverpool Data Research Associates
 */

#ifndef PRINTER_H
#define PRINTER_H

extern void printerInit ( void );
extern void print ( const LDRA_char_pt aMsg );
extern void printerCleanup ( void );

#endif
