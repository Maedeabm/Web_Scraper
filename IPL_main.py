from user_interface import main

if __name__ == '__main__':
    try:
        main()
    except AssertionError:
        print('Interface not supported, please use terminal or command prompt.')
