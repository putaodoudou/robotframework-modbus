*** Settings ***
Library  ModbusLibrary

*** Variables ***
${TEST MACHINE}                         127.0.0.1
${SERVER 1}                             ${TEST MACHINE}
${SERVER 2}                             ${TEST MACHINE}
${SERVER 1 NAME}                        'Server_1'
${SERVER 2 NAME}                        'Server_2'
${CLIENT 1}                             ${TEST MACHINE}
${CLIENT 2}                             ${TEST MACHINE}
${CLIENT 1 NAME}                        'Client_1'
${CLIENT 2 NAME}                        'Client_2'

*** Test Cases ***
Request single coil
    Start Modbus Server  ${SERVER 1}  ${SERVER 1 NAME}
    Start Modbus Client  ${CLIENT 1}  ${CLIENT 1 NAME}
    Connect Modbus Client  ${SERVER 1}  ${CLIENT 1 NAME}
    Server And Client Send And Receive Single Coil

*** Keywords ***
Server And Client Send And Receive Single Coil
    Server Sends Single Coil Request  0xFF00
    ${message}=  Client Receives Single Coil Request
    Should be equal  ${message}  0xFF00
    Client Sends Single Coil Response  0x0000
    ${message}=  Server Receives Single Coil Response
    Should be equal  ${message}  0x0000
