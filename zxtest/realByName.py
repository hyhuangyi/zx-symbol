import zx.Snowball as ball
import json

name = "露笑科技"
if __name__ == '__main__':
    print(json.dumps(ball.getRealInfoByName(name)[0], indent=2))
