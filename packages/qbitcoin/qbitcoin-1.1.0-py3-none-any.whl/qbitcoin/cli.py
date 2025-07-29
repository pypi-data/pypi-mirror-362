#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import os
from binascii import hexlify, a2b_base64
from collections import namedtuple
from decimal import Decimal
from typing import List

import click
import grpc
import simplejson as json
from google.protobuf.json_format import MessageToDict
from pyqrllib.pyqrllib import hstr2bin, bin2hstr
from qbitcoin.crypto.falcon import FalconSignature

from qbitcoin.core import config
from qbitcoin.core.Wallet import Wallet, WalletDecryptionError
from qbitcoin.core.misc.helper import parse_hexblob, parse_qaddress
from qbitcoin.core.MultiSigAddressState import MultiSigAddressState
from qbitcoin.core.txs.MessageTransaction import MessageTransaction
from qbitcoin.core.txs.SlaveTransaction import SlaveTransaction
from qbitcoin.core.txs.TokenTransaction import TokenTransaction
from qbitcoin.core.txs.Transaction import Transaction
from qbitcoin.core.txs.TransferTokenTransaction import TransferTokenTransaction
from qbitcoin.core.txs.TransferTransaction import TransferTransaction
from qbitcoin.core.txs.multisig.MultiSigCreate import MultiSigCreate
from qbitcoin.core.txs.multisig.MultiSigSpend import MultiSigSpend
from qbitcoin.generated import qbit_pb2_grpc, qbit_pb2

ENV_QRL_WALLET_DIR = 'ENV_QRL_WALLET_DIR'

OutputMessage = namedtuple('OutputMessage', 'error address_items balance_items')
BalanceItem = namedtuple('BalanceItem', 'address balance')

CONNECTION_TIMEOUT = 5


class CLIContext(object):
    def __init__(self, verbose, host, port_public, wallet_dir, output_json):
        self.verbose = verbose
        self.host = host
        self.port_public = port_public

        self.wallet_dir = os.path.abspath(wallet_dir)
        self.wallet_path = os.path.join(self.wallet_dir, 'wallet.json')
        self.output_json = output_json

    def get_stub_public_api(self):
        node_public_address = '{}:{}'.format(self.host, self.port_public)
        channel = grpc.insecure_channel(node_public_address)
        return qbit_pb2_grpc.PublicAPIStub(channel)


def _print_error(ctx, error_descr, wallets=None):
    # FIXME: Dead function
    if ctx.obj.output_json:
        if wallets is None:
            wallets = []
        msg = {'error': error_descr, 'wallets': wallets}
        click.echo(json.dumps(msg))
    else:
        print("ERROR: {}".format(error_descr))


def _serialize_output(ctx, addresses: List[OutputMessage], source_description) -> dict:
    if len(addresses) == 0:
        msg = {'error': 'No wallet found at {}'.format(source_description), 'wallets': []}
        return msg

    msg = {'error': None, 'wallets': []}

    for pos, item in enumerate(addresses):
        try:
            balance_unquarked = Decimal(_public_get_address_balance(ctx, item.qaddress)) / config.dev.quark_per_qbitcoin
            balance = '{:5.8f}'.format(balance_unquarked)
        except Exception as e:
            msg['error'] = str(e)
            balance = '?'

        msg['wallets'].append({
            'number': pos,
            'address': item.qaddress,
            'balance': balance,
            'signature_type': 'FALCON'
        })
    return msg


def _public_get_address_balance(ctx, address):
    stub = ctx.obj.get_stub_public_api()
    get_balance_req = qbit_pb2.GetBalanceReq(address=parse_qaddress(address))
    get_balance_resp = stub.GetBalance(get_balance_req, timeout=CONNECTION_TIMEOUT)
    return get_balance_resp.balance


def get_item_from_wallet(wallet, wallet_idx):
    if 0 <= wallet_idx < len(wallet.address_items):
        return wallet.address_items[wallet_idx]

    click.echo('Wallet index not found {}'.format(wallet_idx), color='yellow')
    return None


def _print_addresses(ctx, addresses: List[OutputMessage], source_description):
    def _normal(wallet):
        return "{:<8}{:<83}{:<13}".format(wallet['number'], wallet['address'], wallet['balance'])

    def _verbose(wallet):
        return "{:<8}{:<83}{:<13}{}".format(
            wallet['number'], wallet['address'], wallet['balance'], wallet['signature_type']
        )

    output = _serialize_output(ctx, addresses, source_description)
    if ctx.obj.output_json:
        output["location"] = source_description
        click.echo(json.dumps(output))
    else:
        if output['error'] and output['wallets'] == []:
            click.echo(output['error'])
        else:
            click.echo("Wallet at          : {}".format(source_description))
            if ctx.obj.verbose:
                header = "{:<8}{:<83}{:<13}{:<8}".format('Number', 'Address', 'Balance', 'Signature')
                divider = ('-' * 112)
            else:
                header = "{:<8}{:<83}{:<13}".format('Number', 'Address', 'Balance')
                divider = ('-' * 101)
            click.echo(header)
            click.echo(divider)

            for wallet in output['wallets']:
                if ctx.obj.verbose:
                    click.echo(_verbose(wallet))
                else:
                    click.echo(_normal(wallet))


def _public_get_address_balance(ctx, address):
    stub = ctx.obj.get_stub_public_api()
    get_address_state_req = qbit_pb2.GetAddressStateReq(address=parse_qaddress(address))
    get_optimized_address_state_resp = stub.GetOptimizedAddressState(get_address_state_req, timeout=CONNECTION_TIMEOUT)
    return get_optimized_address_state_resp.state.balance


def _select_wallet(ctx, address_or_index):
    try:
        wallet = Wallet(wallet_path=ctx.obj.wallet_path)
        if len(wallet.address_items) == 0:
            click.echo('This command requires a local wallet')
            return None, None

        if wallet.encrypted:
            secret = click.prompt('The wallet is encrypted. Enter password', hide_input=True)
            wallet.decrypt(secret)

        # Handle empty input case
        if not address_or_index:
            # Return first wallet address by default if no address is provided
            if len(wallet.address_items) > 0:
                falcon = wallet.get_falcon_by_index(0)
                return wallet.address_items[0].qaddress, falcon
            return None, None

        if address_or_index.isdigit():
            address_or_index = int(address_or_index)
            addr_item = get_item_from_wallet(wallet, address_or_index)
            if addr_item:
                # Return Falcon-512 keypair
                falcon = wallet.get_falcon_by_index(address_or_index)
                return addr_item.qaddress, falcon

        elif address_or_index.startswith('Q'):
            for i, addr_item in enumerate(wallet.address_items):
                if address_or_index == addr_item.qaddress:
                    falcon = wallet.get_falcon_by_index(i)
                    return addr_item.qaddress, falcon
            click.echo('Source address not found in your wallet', color='yellow')
            quit(1)

        # If not a valid wallet address or index, treat as external address
        return parse_qaddress(address_or_index), None
    except Exception as e:
        click.echo("Error selecting wallet")
        click.echo(str(e))
        quit(1)


def _qbitcoin_to_quark(x: Decimal, base=Decimal(config.dev.quark_per_qbitcoin)) -> int:
    return int(Decimal(x * base).to_integral_value())


def _parse_dsts_amounts(addresses: str, amounts: str, token_decimals: int = 0, check_multi_sig_address=False):
    """
    'Qaddr1 Qaddr2...' -> [\\xcx3\\xc2, \\xc2d\\xc3]
    '10 10' -> [10e9, 10e9] (in quark)
    :param addresses:
    :param amounts:
    :return:
    """
    addresses_split = [parse_qaddress(addr, check_multi_sig_address) for addr in addresses.split(' ')]

    if token_decimals != 0:
        multiplier = Decimal(10 ** int(token_decimals))
        quark_amounts = [_qbitcoin_to_quark(Decimal(amount), base=multiplier) for amount in amounts.split(' ')]
    else:
        quark_amounts = [_qbitcoin_to_quark(Decimal(amount)) for amount in amounts.split(' ')]

    if len(addresses_split) != len(quark_amounts):
        raise Exception("dsts and amounts should be the same length")

    return addresses_split, quark_amounts


########################
########################
########################
########################

@click.version_option(version=config.dev.version, prog_name='QRL Command Line Interface')
@click.group()
@click.option('--verbose', '-v', default=False, is_flag=True, help='verbose output whenever possible')
@click.option('--host', default='127.0.0.1', help='remote host address             [127.0.0.1]')
@click.option('--port_pub', default=19009, help='remote port number (public api) [19009]')
@click.option('--wallet_dir', default='.', help='local wallet dir', envvar=ENV_QRL_WALLET_DIR)
@click.option('--json', default=False, is_flag=True, help='output in json')
@click.pass_context
def qrl(ctx, verbose, host, port_pub, wallet_dir, json):
    """
    QRL Command Line Interface
    """
    ctx.obj = CLIContext(verbose=verbose,
                         host=host,
                         port_public=port_pub,
                         wallet_dir=wallet_dir,
                         output_json=json)


@qrl.command(name='wallet_ls')
@click.pass_context
def wallet_ls(ctx):
    """
    Lists available wallets
    """
    wallet = Wallet(wallet_path=ctx.obj.wallet_path)
    _print_addresses(ctx, wallet.address_items, ctx.obj.wallet_dir)


@qrl.command(name='wallet_gen')
@click.pass_context
@click.option('--encrypt', default=False, is_flag=True, help='Encrypts important fields with AES')
def wallet_gen(ctx, encrypt):
    """
    Generates a new wallet with one Falcon-512 address
    """
    wallet = Wallet(wallet_path=ctx.obj.wallet_path)
    if len(wallet.address_items) > 0:
        click.echo("Wallet already exists")
        return

    wallet.add_new_address()

    _print_addresses(ctx, wallet.address_items, ctx.obj.wallet_path)

    if encrypt:
        secret = click.prompt('Enter password to encrypt wallet with', hide_input=True, confirmation_prompt=True)
        wallet.encrypt(secret)

    wallet.save()


@qrl.command(name='wallet_add')
@click.pass_context
def wallet_add(ctx):
    """
    Adds a Falcon-512 address to an existing wallet
    """
    secret = None
    wallet = Wallet(wallet_path=ctx.obj.wallet_path)
    wallet_was_encrypted = wallet.encrypted
    if wallet.encrypted:
        secret = click.prompt('The wallet is encrypted. Enter password', hide_input=True)
        wallet.decrypt(secret)

    wallet.add_new_address()

    _print_addresses(ctx, wallet.address_items, config.user.wallet_dir)

    if wallet_was_encrypted:
        wallet.encrypt(secret)

    wallet.save()


@qrl.command(name='balance')
@click.argument('address', required=True)
@click.pass_context
def balance(ctx, address):
    """
    Get the balance of a QRL address
    """
    try:
        # Validate the address format
        try:
            _ = parse_qaddress(address)
        except Exception:
            click.echo(f"Invalid QRL address format: {address}")
            return

        # Get balance from node
        balance_quark = _public_get_address_balance(ctx, address)
        
        # Convert from quark to Qbitcoin
        balance_qbitcoin = Decimal(balance_quark) / config.dev.quark_per_qbitcoin
        
        # Display the balance
        click.echo(f"Address: {address}")
        click.echo(f"Balance: {balance_qbitcoin} Qbitcoin ({balance_quark} quark)")
        
    except Exception as e:
        click.echo(f"Error retrieving balance: {e}")


@qrl.command(name='wallet_secret')
@click.option('--wallet-idx', default=1, prompt=True)
@click.pass_context
def wallet_secret(ctx, wallet_idx):
    """
    Provides the mnemonic/seed of the given address index
    """
    wallet = Wallet(wallet_path=ctx.obj.wallet_path)
    if wallet.encrypted:
        secret = click.prompt('The wallet is encrypted. Enter password', hide_input=True)
        wallet.decrypt(secret)

    address_item = get_item_from_wallet(wallet, wallet_idx)
    if address_item:
        click.echo('Wallet Address  : {}'.format(address_item.qaddress))
        click.echo('Mnemonic        : {}'.format(address_item.mnemonic))
        click.echo('Seed            : {}'.format(address_item.seed))


@qrl.command(name='wallet_rm')
@click.option('--wallet-idx', type=int, prompt=True, help='index of address in wallet')
@click.option('--skip-confirmation', default=False, is_flag=True, prompt=False, help='skip the confirmation prompt')
@click.pass_context
def wallet_rm(ctx, wallet_idx, skip_confirmation):
    """
    Removes an address from the wallet using the given address index.

    Warning! Use with caution. Removing an address from the wallet
    will result in loss of access to the address and is not
    reversible unless you have address recovery information.
    Use the wallet_secret command for obtaining the recovery Mnemonic/Hexseed and
    the wallet_recover command for restoring an address.
    """
    wallet = Wallet(wallet_path=ctx.obj.wallet_path)

    address_item = get_item_from_wallet(wallet, wallet_idx)

    if address_item:
        if not skip_confirmation:
            click.echo(
                'You are about to remove address [{0}]: {1} from the wallet.'.format(wallet_idx, address_item.qaddress))
            click.echo(
                'Warning! By continuing, you risk complete loss of access to this address if you do not have a '
                'recovery Mnemonic/Hexseed.')
            click.confirm('Do you want to continue?', abort=True)
        wallet.remove(address_item.qaddress)

        _print_addresses(ctx, wallet.address_items, config.user.wallet_dir)


@qrl.command(name='wallet_encrypt')
@click.pass_context
def wallet_encrypt(ctx):
    wallet = Wallet(wallet_path=ctx.obj.wallet_path)
    click.echo('Encrypting wallet at {}'.format(wallet.wallet_path))

    secret = click.prompt('Enter password', hide_input=True, confirmation_prompt=True)
    wallet.encrypt(secret)
    wallet.save()


@qrl.command(name='wallet_decrypt')
@click.pass_context
def wallet_decrypt(ctx):
    wallet = Wallet(wallet_path=ctx.obj.wallet_path)
    click.echo('Decrypting wallet at {}'.format(wallet.wallet_path))

    secret = click.prompt('Enter password', hide_input=True)

    try:
        wallet.decrypt(secret)
    except WalletDecryptionError as e:
        click.echo(str(e))
        quit(1)
    except Exception as e:
        click.echo(str(e))
        quit(1)

    try:
        wallet.save()
    except Exception as e:
        click.echo(str(e))
        quit(1)


@qrl.command(name='tx_inspect')
@click.option('--txblob', type=str, default='', prompt=True, help='transaction blob')
@click.pass_context
def tx_inspect(ctx, txblob):
    """
    Inspected a transaction blob
    """
    tx = None
    try:
        txbin = parse_hexblob(txblob)
        pbdata = qbit_pb2.Transaction()
        pbdata.ParseFromString(txbin)
        tx = Transaction.from_pbdata(pbdata)
    except Exception as e:
        click.echo("tx blob is not valid")
        quit(1)

    tmp_json = tx.to_json()
    # FIXME: binary fields are represented in base64. Improve output
    print(tmp_json)


@qrl.command(name='tx_push')
@click.option('--txblob', type=str, default='', help='transaction blob (unsigned)')
@click.pass_context
def tx_push(ctx, txblob):
    """
    Sends a signed transaction blob to a node
    """
    tx = None
    try:
        txbin = parse_hexblob(txblob)
        pbdata = qbit_pb2.Transaction()
        pbdata.ParseFromString(txbin)
        tx = Transaction.from_pbdata(pbdata)
    except Exception as e:
        click.echo("tx blob is not valid")
        quit(1)

    tmp_json = tx.to_json()
    # FIXME: binary fields are represented in base64. Improve output
    print(tmp_json)
    if len(tx.signature) == 0:
        click.echo('Signature missing')
        quit(1)

    stub = ctx.obj.get_stub_public_api()
    pushTransactionReq = qbit_pb2.PushTransactionReq(transaction_signed=tx.pbdata)
    pushTransactionResp = stub.PushTransaction(pushTransactionReq, timeout=CONNECTION_TIMEOUT)
    print(pushTransactionResp.error_code)


@qrl.command(name='tx_message')
@click.option('--src', type=str, default='', prompt=True, help='signer QRL address')
@click.option('--master', type=str, default='', prompt=True, help='master QRL address')
@click.option('--addr_to', type=str, default='', prompt=True, help='QRL Address receiving this message (optional)')
@click.option('--message', type=str, prompt=True, help='Message (max 80 bytes)')
@click.option('--fee', type=Decimal, default=0.0, prompt=True, help='fee in Qbitcoin')
@click.pass_context
def tx_message(ctx, src, master, addr_to, message, fee):
    """
    Message Transaction
    """
    try:
        _, src_falcon = _select_wallet(ctx, src)
        if not src_falcon:
            click.echo("A local wallet is required to sign the transaction")
            quit(1)

        address_src_pk = src_falcon['public_key_bytes']

        message = message.encode()
        if addr_to:
            addr_to = parse_qaddress(addr_to, False)
        else:
            addr_to = None

        master_addr = None
        if master:
            master_addr = parse_qaddress(master)
        fee_quark = _qbitcoin_to_quark(fee)
    except Exception as e:
        click.echo("Error validating arguments: {}".format(e))
        quit(1)

    try:
        stub = ctx.obj.get_stub_public_api()
        tx = MessageTransaction.create(message_hash=message,
                                       addr_to=addr_to,
                                       fee=fee_quark,
                                       xmss_pk=address_src_pk,
                                       master_addr=master_addr)
        # Sign with Falcon-512
        tx_data = tx.get_data_bytes()
        signature = FalconSignature.sign_message(tx_data, src_falcon['private_key_bytes'])
        tx._data.signature = signature

        push_transaction_req = qbit_pb2.PushTransactionReq(transaction_signed=tx.pbdata)
        push_transaction_resp = stub.PushTransaction(push_transaction_req, timeout=CONNECTION_TIMEOUT)

        print(push_transaction_resp)
    except Exception as e:
        print("Error {}".format(str(e)))


@qrl.command(name='tx_multi_sig_create')
@click.option('--src', type=str, default='', prompt=True, help='source QRL address')
@click.option('--master', type=str, default='', prompt=True, help='master QRL address')
@click.option('--threshold', default=0, prompt=True, help='Threshold')
@click.option('--fee', type=Decimal, default=0.0, prompt=True, help='fee in Qbitcoin')
@click.option('--signature_index', default=1, prompt=True, help='Signature Index for Falcon-512')
@click.pass_context
def tx_multi_sig_create(ctx, src, master, threshold, fee, signature_index):
    """
    Creates Multi Sig Create Transaction, that results into the formation of new multi_sig_address if accepted.
    """
    signatories = []
    weights = []
    while True:
        address = click.prompt('Address of Signatory ', default='')
        if address == '':
            break
        weight = int(click.prompt('Weight '))
        signatories.append(parse_qaddress(address))
        weights.append(weight)

    try:
        _, src_falcon = _select_wallet(ctx, src)
        if not src_falcon:
            click.echo("A local wallet is required to sign the transaction")
            quit(1)

        address_src_pk = src_falcon['public_key_bytes']

         

        master_addr = None
        if master:
            master_addr = parse_qaddress(master)
        # FIXME: This could be problematic. Check
        fee_quark = _qbitcoin_to_quark(fee)

    except KeyboardInterrupt:
        click.echo("Terminated by user")
        quit(1)
    except Exception as e:
        click.echo("Error validating arguments: {}".format(e))
        quit(1)

    try:
        stub = ctx.obj.get_stub_public_api()
        tx = MultiSigCreate.create(signatories=signatories,
                                   weights=weights,
                                   threshold=threshold,
                                   fee=fee_quark,
                                   xmss_pk=address_src_pk,
                                   master_addr=master_addr)

        # Sign with Falcon-512
        tx_data = tx.get_data_bytes()
        signature = FalconSignature.sign_message(tx_data, src_falcon['private_key_bytes'])
        tx._data.signature = signature
        tx._data.nonce = signature_index

        push_transaction_req = qbit_pb2.PushTransactionReq(transaction_signed=tx.pbdata)
        push_transaction_resp = stub.PushTransaction(push_transaction_req, timeout=CONNECTION_TIMEOUT)

        print(push_transaction_resp.error_code)
        print('Multi sig Address Q{}'.format(bin2hstr(MultiSigAddressState.generate_multi_sig_address(tx.txhash))))
    except Exception as e:
        print("Error {}".format(str(e)))


@qrl.command(name='tx_multi_sig_spend')
@click.option('--src', type=str, default='', prompt=True, help='signer QRL address')
@click.option('--master', type=str, default='', help='master QRL address')
@click.option('--multi_sig_address', type=str, default='', prompt=True, help='signer Multi Sig Address')
@click.option('--dsts', type=str, prompt=True, help='List of destination addresses')
@click.option('--amounts', type=str, prompt=True, help='List of amounts to transfer (Qbitcoin)')
@click.option('--expiry_block_number', type=int, prompt=True, help='Expiry Blocknumber')
@click.option('--fee', type=Decimal, default=0.0, prompt=True, help='fee in Qbitcoin')
@click.option('--signature_index', default=1, help='Signature Index for Falcon-512')
@click.pass_context
def tx_multi_sig_spend(ctx, src, master, multi_sig_address, dsts, amounts, expiry_block_number, fee, signature_index):
    """
    Transfer coins from src to dsts
    """
    address_src_pk = None
    master_addr = None

    addresses_dst = []
    quark_amounts = []
    fee_quark = []

    signing_object = None

    try:
        # Retrieve signing object
        selected_wallet = _select_wallet(ctx, src)
        if selected_wallet is None or len(selected_wallet) != 2:
            click.echo("A wallet was not found")
            quit(1)

        _, src_falcon = selected_wallet

        if not src_falcon:
            click.echo("A local wallet is required to sign the transaction")
            quit(1)

        address_src_pk = src_falcon['public_key_bytes']

        

        signing_object = src_falcon

        # Get and validate other inputs
        if master:
            master_addr = parse_qaddress(master)

        addresses_dst, quark_amounts = _parse_dsts_amounts(dsts, amounts, check_multi_sig_address=True)
        fee_quark = _qbitcoin_to_quark(fee)
    except Exception as e:
        click.echo("Error validating arguments: {}".format(e))
        quit(1)
    multi_sig_address = bytes(hstr2bin(multi_sig_address[1:]))
    try:
        # MultiSigSpend transaction
        tx = MultiSigSpend.create(multi_sig_address=multi_sig_address,
                                  addrs_to=addresses_dst,
                                  amounts=quark_amounts,
                                  expiry_block_number=expiry_block_number,
                                  fee=fee_quark,
                                  xmss_pk=address_src_pk,
                                  master_addr=master_addr)

        # Sign transaction
        tx.sign(signing_object)

        if not tx.validate():
            print("It was not possible to validate the signature")
            quit(1)

        print("\nTransaction Blob (signed): \n")
        txblob = tx.pbdata.SerializeToString()
        txblobhex = hexlify(txblob).decode()
        print(txblobhex)

        # Push transaction
        print()
        print("Sending to a QRL Node...")
        stub = ctx.obj.get_stub_public_api()
        push_transaction_req = qbit_pb2.PushTransactionReq(transaction_signed=tx.pbdata)
        push_transaction_resp = stub.PushTransaction(push_transaction_req, timeout=CONNECTION_TIMEOUT)

        # Print result
        print(push_transaction_resp)
    except Exception as e:
        print("Error {}".format(str(e)))


def base64tohex(data):
    return hexlify(a2b_base64(data))


def tx_unbase64(tx_json_str):
    tx_json = json.loads(tx_json_str)
    tx_json["publicKey"] = base64tohex(tx_json["publicKey"])
    tx_json["signature"] = base64tohex(tx_json["signature"])
    tx_json["transactionHash"] = base64tohex(tx_json["transactionHash"])
    tx_json["transfer"]["addrsTo"] = [base64tohex(v) for v in tx_json["transfer"]["addrsTo"]]
    return json.dumps(tx_json, indent=True, sort_keys=True)


@qrl.command(name='tx_transfer')
@click.option('--src', type=str, default='', prompt=True, help='signer qbitcoin  address')
@click.option('--master', type=str, default='', help='master QRL address')
@click.option('--dsts', type=str, prompt=True, help='List of destination addresses')
@click.option('--amounts', type=str, prompt=True, help='List of amounts to transfer (Qbit)')
@click.option('--message_data', type=str, prompt=True, help='Message (Optional)')
@click.option('--fee', type=Decimal, default=0.0, prompt=True, help='fee in qbit ')
@click.pass_context
def tx_transfer(ctx, src, master, dsts, amounts, message_data, fee):
    """
    Transfer coins from src to dsts
    """
    address_src_pk = None
    master_addr = None

    addresses_dst = []
    quark_amounts = []
    fee_quark = 0

    signing_object = None
    message_data = message_data.encode()

    try:
        # Retrieve signing object
        src_addr, src_falcon = _select_wallet(ctx, src)
        if src_addr is None or src_falcon is None:
            click.echo("A valid wallet is required to sign the transaction")
            quit(1)

        address_src_pk = src_falcon['public_key_bytes']
        signing_object = src_falcon

        # Get and validate other inputs
        if master:
            master_addr = parse_qaddress(master)
        addresses_dst, quark_amounts = _parse_dsts_amounts(dsts, amounts, check_multi_sig_address=True)
        fee_quark = _qbitcoin_to_quark(fee)
    except Exception as e:
        click.echo("Error validating arguments: {}".format(e))
        quit(1)

    try:
        # Create transaction
        tx = TransferTransaction.create(addrs_to=addresses_dst,
                                        amounts=quark_amounts,
                                        message_data=message_data,
                                        fee=fee_quark,
                                        xmss_pk=address_src_pk,
                                        master_addr=master_addr)

        # Sign transaction with Falcon-512
        tx_data = tx.get_data_bytes()
        signature = FalconSignature.sign_message(tx_data, signing_object['private_key_bytes'])
        tx._data.signature = signature

        # Print result
        txjson = tx_unbase64(tx.to_json())
        print(txjson)

        if not tx.validate():
            print("It was not possible to validate the signature")
            quit(1)

        print("\nTransaction Blob (signed): \n")
        txblob = tx.pbdata.SerializeToString()
        txblobhex = hexlify(txblob).decode()
        print(txblobhex)

        # Push transaction
        print("Sending to a QRL Node...")
        stub = ctx.obj.get_stub_public_api()
        push_transaction_req = qbit_pb2.PushTransactionReq(transaction_signed=tx.pbdata)
        push_transaction_resp = stub.PushTransaction(push_transaction_req, timeout=CONNECTION_TIMEOUT)

        # Print result
        print(push_transaction_resp)
    except Exception as e:
        print("Error {}".format(str(e)))


@qrl.command(name='tx_token')
@click.option('--src', type=str, default='', prompt=True, help='source QRL address')
@click.option('--master', type=str, default='', prompt=True, help='master QRL address')
@click.option('--symbol', default='', prompt=True, help='Symbol Name')
@click.option('--name', default='', prompt=True, help='Token Name')
@click.option('--owner', default='', prompt=True, help='Owner QRL address')
@click.option('--decimals', default=0, prompt=True, help='decimals')
@click.option('--fee', type=Decimal, default=0.0, prompt=True, help='fee in Qbitcoin')
@click.pass_context
def tx_token(ctx, src, master, symbol, name, owner, decimals, fee):
    """
    Create Token Transaction, that results into the formation of new token if accepted.
    """

    initial_balances = []

    if decimals > 19:
        click.echo("The number of decimal cannot exceed 19 under any possible configuration")
        quit(1)

    while True:
        address = click.prompt('Address ', default='')
        if address == '':
            break
        amount = int(click.prompt('Amount ')) * (10 ** int(decimals))
        initial_balances.append(qbit_pb2.AddressAmount(address=parse_qaddress(address),
                                                      amount=amount))

    try:
        src_addr, src_falcon = _select_wallet(ctx, src)
        if src_addr is None or src_falcon is None:
            click.echo("A valid wallet is required to sign the transaction")
            quit(1)

        address_src_pk = src_falcon['public_key_bytes']

        address_owner = parse_qaddress(owner)
        master_addr = None
        if master:
            master_addr = parse_qaddress(master)
        # FIXME: This could be problematic. Check
        fee_quark = _qbitcoin_to_quark(fee)

        if len(name) > config.dev.max_token_name_length:
            raise Exception("Token name must be quarkter than {} chars".format(config.dev.max_token_name_length))
        if len(symbol) > config.dev.max_token_symbol_length:
            raise Exception("Token symbol must be quarkter than {} chars".format(config.dev.max_token_symbol_length))

    except KeyboardInterrupt:
        click.echo("Terminated by user")
        quit(1)
    except Exception as e:
        click.echo("Error validating arguments: {}".format(e))
        quit(1)

    try:
        stub = ctx.obj.get_stub_public_api()
        tx = TokenTransaction.create(symbol=symbol.encode(),
                                     name=name.encode(),
                                     owner=address_owner,
                                     decimals=decimals,
                                     initial_balances=initial_balances,
                                     fee=fee_quark,
                                     xmss_pk=address_src_pk,
                                     master_addr=master_addr)

        # Sign with Falcon-512
        tx_data = tx.get_data_bytes()
        signature = FalconSignature.sign_message(tx_data, src_falcon['private_key_bytes'])
        tx._data.signature = signature

        push_transaction_req = qbit_pb2.PushTransactionReq(transaction_signed=tx.pbdata)
        push_transaction_resp = stub.PushTransaction(push_transaction_req, timeout=CONNECTION_TIMEOUT)

        print(push_transaction_resp.error_code)
    except Exception as e:
        print("Error {}".format(str(e)))


@qrl.command(name='tx_transfertoken')
@click.option('--src', type=str, default='', prompt=True, help='source QRL address')
@click.option('--master', type=str, default='', prompt=True, help='master QRL address')
@click.option('--token_txhash', default='', prompt=True, help='Token Txhash')
@click.option('--dsts', type=str, prompt=True, help='List of destination addresses')
@click.option('--amounts', type=str, prompt=True, help='List of amounts to transfer (Qbitcoin)')
@click.option('--decimals', default=0, prompt=True, help='decimals')
@click.option('--fee', type=Decimal, default=0.0, prompt=True, help='fee in Qbitcoin')
@click.pass_context
def tx_transfertoken(ctx, src, master, token_txhash, dsts, amounts, decimals, fee):
    """
    Create Transfer Token Transaction, which moves tokens from src to dst.
    """

    if decimals > 19:
        click.echo("The number of decimal cannot exceed 19 under any configuration")
        quit(1)

    try:
        addresses_dst, quark_amounts = _parse_dsts_amounts(dsts, amounts, token_decimals=decimals)
        bin_token_txhash = parse_hexblob(token_txhash)
        master_addr = None
        if master:
            master_addr = parse_qaddress(master)
        # FIXME: This could be problematic. Check
        fee_quark = _qbitcoin_to_quark(fee)

        _, src_falcon = _select_wallet(ctx, src)
        if not src_falcon:
            click.echo("A local wallet is required to sign the transaction")
            quit(1)

        address_src_pk = src_falcon['public_key_bytes']

    except KeyboardInterrupt:
        click.echo("Terminated by user")
        quit(1)
    except Exception as e:
        click.echo("Error validating arguments: {}".format(e))
        quit(1)

    try:
        stub = ctx.obj.get_stub_public_api()
        tx = TransferTokenTransaction.create(token_txhash=bin_token_txhash,
                                             addrs_to=addresses_dst,
                                             amounts=quark_amounts,
                                             fee=fee_quark,
                                             xmss_pk=address_src_pk,
                                             master_addr=master_addr)
        # Sign with Falcon-512
        tx_data = tx.get_data_bytes()
        signature = FalconSignature.sign_message(tx_data, src_falcon['private_key_bytes'])
        tx._data.signature = signature

        push_transaction_req = qbit_pb2.PushTransactionReq(transaction_signed=tx.pbdata)
        push_transaction_resp = stub.PushTransaction(push_transaction_req, timeout=CONNECTION_TIMEOUT)

        print(push_transaction_resp.error_code)
    except Exception as e:
        print("Error {}".format(str(e)))


@qrl.command(name='slave_tx_generate')
@click.option('--src', type=str, default='', prompt=True, help='source address or index')
@click.option('--master', type=str, default='', prompt=True, help='master QRL address')
@click.option('--number_of_slaves', default=0, type=int, prompt=True, help='Number of slaves addresses')
@click.option('--access_type', default=0, type=int, prompt=True, help='0 - All Permission, 1 - Only Mining Permission')
@click.option('--fee', type=Decimal, default=0.0, prompt=True, help='fee (Qbitcoin)')
@click.option('--pk', default=0, prompt=False, help='public key (when local wallet is missing)')
@click.option('--signature_index', default=1, prompt=False, help='Signature Index for Falcon-512')
@click.pass_context
def slave_tx_generate(ctx, src, master, number_of_slaves, access_type, fee, pk, signature_index):
    """
    Generates Slave Transaction for the wallet
    """
    try:
        _, src_falcon = _select_wallet(ctx, src)

        
        if src_falcon:
            address_src_pk = src_falcon['public_key_bytes']
        else:
            address_src_pk = pk.encode()

        master_addr = None
        if master:
            master_addr = parse_qaddress(master)
        fee_quark = _qbitcoin_to_quark(fee)
    except Exception as e:
        click.echo("Error validating arguments: {}".format(e))
        quit(1)

    slave_xmss = []
    slave_pks = []
    access_types = []
    slave_xmss_seed = []
    if number_of_slaves > 100:
        click.echo("Error: Max Limit for the number of slaves is 100")
        quit(1)

    for i in range(number_of_slaves):
        print("Generating Slave #" + str(i + 1))
        private_key_bytes, public_key_bytes = FalconSignature.generate_keypair()
        slave_pks.append(public_key_bytes)
        access_types.append(access_type)
        # Store key pairs for later use
        from qbitcoin.tools.wallet_creator import WalletCreator
        slave_address = WalletCreator.generate_address(public_key_bytes)
        slave_xmss.append({
            'private_key_bytes': private_key_bytes,
            'public_key_bytes': public_key_bytes,
            'address': slave_address
        })
        print("Successfully Generated Slave %s/%s" % (str(i + 1), number_of_slaves))

    try:
        tx = SlaveTransaction.create(slave_pks=slave_pks,
                                     access_types=access_types,
                                     fee=fee_quark,
                                     xmss_pk=address_src_pk,
                                     master_addr=master_addr)
        
        # Sign with Falcon-512
        if src_falcon:
            tx_data = tx.get_data_bytes()
            signature = FalconSignature.sign_message(tx_data, src_falcon['private_key_bytes'])
            tx._data.signature = signature
           
            
        # Save slave information to JSON file
        slave_info = []
        for slave in slave_xmss:
            slave_info.append({
                'address': slave['address'],
                'pk': bin2hstr(slave['public_key_bytes']),
                'sk': bin2hstr(slave['private_key_bytes'])
            })
        
        with open('slaves.json', 'w') as f:
            address = src_falcon['address'] if src_falcon else bin2hstr(address_src_pk)
            json.dump([address, slave_info, tx.to_json()], f)
        click.echo('Successfully created slaves.json')
        click.echo('Move slaves.json file from current directory to the mining node inside ~/.qrl/')
    except Exception as e:
        click.echo("Unhandled error: {}".format(str(e)))
        quit(1)


@qrl.command(name='token_list')
@click.option('--owner', default='', prompt=True, help='source QRL address')
@click.pass_context
def token_list(ctx, owner):
    """
    Fetch the list of tokens owned by an address.
    """
    try:
        owner_address = parse_qaddress(owner)
    except Exception as e:
        click.echo("Error validating arguments: {}".format(e))
        quit(1)

    try:
        stub = ctx.obj.get_stub_public_api()
        address_state_req = qbit_pb2.GetAddressStateReq(address=owner_address)
        address_state_resp = stub.GetAddressState(address_state_req, timeout=CONNECTION_TIMEOUT)

        for token_hash in address_state_resp.state.tokens:
            get_object_req = qbit_pb2.GetObjectReq(query=bytes(hstr2bin(token_hash)))
            get_object_resp = stub.GetObject(get_object_req, timeout=CONNECTION_TIMEOUT)

            click.echo('Hash: %s' % (token_hash,))
            click.echo('Symbol: %s' % (get_object_resp.transaction.tx.token.symbol.decode(),))
            click.echo('Name: %s' % (get_object_resp.transaction.tx.token.name.decode(),))
            click.echo('Balance: %s' % (address_state_resp.state.tokens[token_hash],))

    except Exception as e:
        print("Error {}".format(str(e)))


@qrl.command(name='state')
@click.pass_context
def state(ctx):
    """
    Shows Information about a Node's State
    """
    stub = ctx.obj.get_stub_public_api()
    nodeStateResp = stub.GetNodeState(qbit_pb2.GetNodeStateReq())

    hstr_block_last_hash = bin2hstr(nodeStateResp.info.block_last_hash).encode()
    if ctx.obj.output_json:
        jsonMessage = MessageToDict(nodeStateResp)
        jsonMessage['info']['blockLastHash'] = hstr_block_last_hash
        click.echo(json.dumps(jsonMessage, indent=2, sort_keys=True))
    else:
        nodeStateResp.info.block_last_hash = hstr_block_last_hash
        click.echo(nodeStateResp)


def main():
    qrl()


if __name__ == '__main__':
    main()
