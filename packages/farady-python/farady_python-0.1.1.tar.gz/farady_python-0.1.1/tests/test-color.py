from FDLib.utils import color_maker


def main():
    get_color = color_maker()
    print(get_color("string-abc"))  # 输出如: #eaa5e1（实际值基于哈希计算）
    print(get_color("test_string"))  # 输出如: #d09e9b
    print(get_color("abc-string"))  # 输出如: #e3f604
    print(get_color("test_string"))  # 输出与前一个test_string相同


if __name__ == "__main__":
    main()
