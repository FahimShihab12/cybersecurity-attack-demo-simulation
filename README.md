# Simulating a Cybersecurity Attack: Release of Message Contents

A small Python socket demo showing how an attacker sitting between a client and a server can read unencrypted messages (eavesdropping / man-in-the-middle).

> **For education only.** Everything runs on `127.0.0.1` (your own computer). Do not use this against systems you do not own or have permission to test.

## What this project shows

| Piece | File | Role |
|---|---|---|
| Server | `server.py` | Receives a message and replies "Message received" |
| Client | `client.py` | Sends messages typed by the user and prints the reply |
| Attacker | `attacker.py` | Sits between client and server, reads every message, forwards it unchanged |

**Attack chosen:** Release of Message Contents (a passive attack).
**Security property broken:** Confidentiality.

## How it works

Normal communication:

```
Client  ---- port 5000 ---->  Server
```

With the attacker in the middle:

```
Client ---- port 5000 ---> Attacker ---- port 5001 ---> Server
                              |
                       prints every message
```

The client still connects to port 5000, as always. The attacker takes over port 5000 and the real server is moved to port 5001, so the client never knows anything changed. The attacker forwards every message unmodified, so both sides keep working normally while the attacker reads everything.

## Requirements

- Python 3.8+ (no extra libraries; only the built-in `socket` and `sys` modules)
- Any editor/terminal (tested with VS Code)

Check your version:

```
python --version
```

## How to run

### Part A: Normal communication (no attacker)

Open two terminals in the project folder.

**Terminal 1**
```
python server.py
```

**Terminal 2**
```
python client.py
```

Type a message such as `My password is 12345` and press Enter. The server prints it and the client shows `Message received`. Type `exit` in the client to quit.

### Part B: The attack

Open three terminals. **Start them in this order.**

**Terminal 1: real server on port 5001**
```
python server.py 5001
```

**Terminal 2: attacker on port 5000**
```
python attacker.py
```

**Terminal 3: client (unchanged)**
```
python client.py
```

Type `My password is 12345` in the client. The attacker's terminal shows:

```
[ATTACKER] Intercepted CLIENT -> SERVER: My password is 12345
[ATTACKER] Intercepted SERVER -> CLIENT: Message received
```

The client sees nothing unusual.

> On macOS/Linux, use `python3` instead of `python` if needed.

## Why the attack works

1. Messages are sent as **plain text**, with no encryption.
2. The client does **not verify** that it is talking to the real server (no authentication).

## Security property affected

**Confidentiality**: unauthorized parties can read the data.

## How to prevent or reduce it

- **Encrypt traffic** with TLS/SSL (Python's `ssl` module, or HTTPS in real applications), so an eavesdropper only sees scrambled bytes.
- **Authenticate the server** with certificates, so the client can detect an impostor.
- **Use secure channels** such as a VPN, and never send sensitive data in plain text.
- **Encrypt at the application level** (for example, encrypt the message before sending it).

## Project structure

```
cyber-attack-demo/
├── server.py
├── client.py
├── attacker.py
└── README.md
```

## Troubleshooting

| Problem | Fix |
|---|---|
| `ConnectionRefusedError` | Start programs in the right order: server, then attacker, then client |
| `Address already in use` | Close old terminals or wait a few seconds, then retry |
| Attacker prints nothing | Make sure the server runs on **5001** and the client on **5000** |

## Author

Fahim Shihab Touhid, CSE, University of Liberal Arts Bangladesh (ULAB)
