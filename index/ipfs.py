import ipfsApi


def uploadIpfs(src):
    api = ipfsApi.Client('https://ipfs.infura.io', 5001)
    res = api.add(src)
    return res
