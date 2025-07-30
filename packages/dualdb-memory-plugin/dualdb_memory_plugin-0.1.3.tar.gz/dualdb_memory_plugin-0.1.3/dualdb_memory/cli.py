# dualdb_memory/cli.py

def main():
    """
    CLI 入口：直接调用 demo_basic 脚本的 main 函数
    """
    from examples.demo_basic import main as demo_main
    return demo_main()

if __name__ == "__main__":
    main()
