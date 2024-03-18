/*
 *    QNX PingingSemaphores project
 * ===================================
 * File Path     : TaskPing.h
 * Author        : M.W.Richardson
 * Date          : 19/07/22
 * Copyright     : (c) 2022 Liverpool Data Research Associates
 */

#ifndef TASK_PING_H
#define TASK_PING_H

extern void taskPingSignal ( void );
extern void* taskPingRun ( void* arg );
extern void taskPingCleanup ( void );

#endif
