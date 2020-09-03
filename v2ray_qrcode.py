import argparse
import pyqrcode
import base64


def get_vmess_url(uuid, server, port, cipher, obfs, ws_path, tls, client_type):
    if client_type == 'shadowrocket':
        vmess_info = '{}:{}@{}:{}'.format(cipher,uuid,server,port)
        vmess_info_b64 = base64.b64encode(vmess_info.encode('ascii')).decode('ascii').replace('=','')
        return 'vmess://{}?path={}&obfs={}&tls={}'.format(vmess_info_b64,ws_path,obfs,tls)
    elif client_type == 'bifrost':
        ws_path = "%3D{}".format(ws_path.replace('/','%252F'))
        vmess_info = 'bfv://{}:{}/vmess/1?rtype=lanchinacnsite&dns=8.8.8.8&tnet=ws&tsec=tls&ttlssn={}&mux=0&uid={}&aid=64&sec=auto&ws=path{}%26headers%3D#{}'.format(server, port, server, uuid, ws_path, server)
        
        print(vmess_info)
        print(ws_path)
        
        return vmess_info
    else:
        raise NameError('Unknown type')


def get_vmess_qrcode(uuid, server, port, cipher, obfs, ws_path, tls, client_type, path):
    vmess_url = get_vmess_url(uuid, server, port, cipher, obfs, ws_path, tls, client_type)
    vmess_qr = pyqrcode.create(vmess_url, error='H')
    try:
        vmess_qr.png("{}\{}-{}.png".format(path, server, uuid), scale=5)
    except Exception:
        print('Unable to save file!')
    else:
        return True

def main(args):
    vmess_cipher = 'chacha20-poly1305'
    obfs = 'websocket'
    ws_tls = 1
    get_vmess_qrcode(args.uuid, args.server, args.port, vmess_cipher, obfs, args.ws_path, ws_tls, args.client_type, args.savepath)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='v2ray QR-code generator')
    parser.add_argument('--uuid', type=str, action='store', dest="uuid", help='User UUID', required=True)
    parser.add_argument('--server', type=str, action='store', dest="server", help='Server address', required=True)
    parser.add_argument('--port', type=int, action='store', dest="port", help='Server port', required=True)
    parser.add_argument('--wspath', type=str, action='store', dest="ws_path", help='Websocket path', required=True)
    parser.add_argument('--client', type=str, action='store', dest="client_type", help='Client type: bifrost or shadowrocket', required=True)
    parser.add_argument('--savepath', type=str, action='store', dest="savepath", help='Path to directory to save QR-code image', required=True)
    args = parser.parse_args()
    main(args)
