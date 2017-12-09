# Reactmed
## Useful commands
To copy content from client and paste it to server use netcat.
On server run netcat which receives a data from the client
```bash
netcat -l -p <PORT> > <FILE>
```
On client run netcat to send a data to the server:
```bash
netcat <HOST> <PORT>   
```
Once netcat starts, you need input data and press ENTER. Server receives data and writes content to specified file.

## Links
 1. [How to use SSH for connecting macOS Sierra to Ubuntu](https://medium.freecodecamp.org/upgrading-to-macos-sierra-will-break-your-ssh-keys-and-lock-you-out-of-your-own-servers-f413ac96139a)
 
