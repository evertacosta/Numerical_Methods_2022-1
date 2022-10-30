import io


def peek(file):
    stream = open(file, 'rb')
    print(type(stream))
    print(stream)

    print(stream.read())

    """
    for i in stream:
        print(type(i), i, '\n')
    """






if __name__ == "__main__":
    pdf = './Hellou World.pdf'
    img = './image.png'

    peek(pdf)
    #peek(img)

