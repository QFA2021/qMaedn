import pyglet
from pyglet import shapes

window = pyglet.window.Window()
field = pyglet.graphics.Batch()


shapes.Circle(x=10, y=10, radius=50, color=(255, 0, 255), batch=field)
@window.event
def on_draw():
    window.clear()
    batch.draw()

#pyglet.app.run()


def f2s(i):
  DOTS_PER_Q = 10

  if i < 40: # regular playing field
    quarter = i // DOTS_PER_Q
    i = i % DOTS_PER_Q
    y = max(i-4, min(4, i))
    x = max(0, min(4, 4 - i + 4))
    return rot90(x, y, quarter)
  elif i < 56: # houses
    i = i % 40
    quarter = i // 4
    i = i % 4 # 40 normal fields plus 4 per house
    x = 5
    y = 1 + i
    return rot90(x, y, quarter)

    
def rot90(x, y, times):
  x = x-5
  y = y-5
  for _ in range(times):
    x, y = y, -x
  return x+5, y+5

for i in range(56):
  x, y = f2s(i)
  print(f"{i}: {x},{y}")


