from distutils.core import setup, Extension

def main():
    setup(name="testext",
          version="1.0.0",
          description="Python interface",
          author="Lucas Kirazci",
          author_email="lucaskirazci@gmail.com",
          ext_modules=[Extension("cConnectFour", ["ConnectFour.c"])])

if __name__ == "__main__":
    main()
