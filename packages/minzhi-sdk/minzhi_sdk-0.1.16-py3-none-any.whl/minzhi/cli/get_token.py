import argparse
from minzhi.authorization import CmdbClient, AEClient

def main():
    parser = argparse.ArgumentParser(description="获取 CMDB token")
    parser.add_argument("--type", required=True, help="类型", choices=["cmdb", "ae"])
    parser.add_argument("--server", required=True, help="服务器地址")
    parser.add_argument("--user", required=True, help="用户名")
    parser.add_argument("--password", required=True, help="密码")
    args = parser.parse_args()

    if args.type == "cmdb":
        client = CmdbClient(args.server, args.user, args.password)
        token = client.get_token()
        print(token)
    elif args.type == "ae":
        client = AEClient(args.server, args.user, args.password)
        token = client.get_token()
        print(token)

if __name__ == "__main__":
    main() 