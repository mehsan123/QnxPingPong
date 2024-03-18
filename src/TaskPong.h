/*
 *    QNX PingingSemaphores project
 * ========================================
 * File Path     : TaskPong.h
 * Author        : M.W.Richardson
 * Date          : 19/07/22
 * Copyright     : (c) 2022 Liverpool Data Research Associates
 */

#ifndef TASK_PONG_H
#define TASK_PONG_H

extern void taskPongSignal ( void );
extern void* taskPongRun ( void* arg );
extern void taskPongCleanup ( void );

#endif
