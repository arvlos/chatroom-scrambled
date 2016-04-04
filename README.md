This is a chat program created as a part of a HW assignment. 




All the system messages are broadcast from the clientside to simplify the encryption / decryption routine

TODO:
Change the AES encryption from ECB to CBC or any other more secure one;
Add an initial handshake that doesn't assume the presence of a preshared key;
Reintroduce broadcasting of the system messages while still dealing with encryption;
Move the "User entered the chatroom" message from the client to the server;