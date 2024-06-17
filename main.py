import test

if __name__ == '__main__':
    input = input('Enter the test type (custom/default): ')
    if input == 'custom':
        test.custom_test()
    elif input == 'default':
        test.default_test()
    else:
        print('Invalid input')