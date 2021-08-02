import zx.Snowball as ball

if __name__ == '__main__':
    res = []
    for i in range(10):
        data = ball.symbolComment(symbol='002597',page=i + 1)
        for d in data:
            print(d)
