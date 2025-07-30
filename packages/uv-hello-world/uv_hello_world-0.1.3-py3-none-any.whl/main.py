# main.py
def hello(args=None):
    print("---------------------")
    if args:
        # 打印接收到的所有参数
        for i, arg in enumerate(args, 1):
            print(f"{i}. {arg}")
    else:
        print("Hello World!")
    print("---------------------")
# 确保可以直接通过命令行调用
if __name__ == "__main__":
    hello()