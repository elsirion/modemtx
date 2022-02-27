import argparse
from subprocess import Popen, PIPE
from requests import post

API = "https://blockstream.info/testnet/api/tx"
CHARSET = b"0123456789ABCDEF"

def send_tx(tx: str, baud: str):
    modem = Popen(['minimodem', str(baud), '--tx'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    stdinBytes = bytes("{}\n".format(tx), "UTF-8")
    modem.communicate(input=stdinBytes)
    modem.kill()

def listen_tx(baud: str):
    modem = Popen(['minimodem', str(baud), '--rx'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    while True:
        tx = modem.stdout.readline()
        filteredTx = "".join([chr(c) for c in tx if c in CHARSET])
        print("received filtered transaction: {}".format(filteredTx))
        result = post(API, data=filteredTx)
        print("response: {}".format(result.text))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sender and transmit Bitcoin transactions via audio channels')
    parser.add_argument('baudRate', metavar='baud', type=str,
                        help='transmission speed')

    # Send or receive?
    group = parser.add_mutually_exclusive_group()
    group.required = True
    group.add_argument('--send', metavar='transaction', type=str,
                        help='send transaction')
    group.add_argument('--receive', action='store_true',
                        help='receive transactions and submit to blockchain')

    args = parser.parse_args()
    if args.send:
        print("Sending tx …")
        send_tx(args.send, args.baudRate)
    if args.receive:
        print("Listening for transactions …")
        listen_tx(args.baudRate)
