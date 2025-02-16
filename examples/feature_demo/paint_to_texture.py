"""
Paint to a texture
==================

This example shows an application that allows the user to paint an image
onto a texture.

This also demonstrates a custom controller config, that only allows
horizontal panning over the texture, using shift+mouse or scrolling.
"""

from wgpu.gui.auto import WgpuCanvas, run
import pygfx as gfx
import numpy as np

renderer = gfx.renderers.WgpuRenderer(WgpuCanvas())
scene = gfx.Scene()

scene.add(gfx.Background(None, gfx.BackgroundMaterial("#cde")))

data = np.zeros((100, 500), np.uint8)
tex = gfx.Texture(data, dim=2)

image = gfx.Image(
    gfx.Geometry(grid=tex),
    gfx.ImageBasicMaterial(clim=(0, 200)),
)
scene.add(image)


camera = gfx.OrthographicCamera()
camera.show_rect(-5, 105, -5, 105)


@image.add_event_handler("pointer_down", "pointer_move")
def pick(event):
    if event.modifiers:
        return
    if 1 in event.buttons or 2 in event.buttons:
        info = event.pick_info
        if "index" in info:
            x, y = info["index"]
            if 1 in event.buttons:
                tex.data[y, x] = min(200, tex.data[y, x] + 50)
            else:
                tex.data[y, x] = max(0, tex.data[y, x] - 50)
            tex.update_range((x, y, 0), (1, 1, 1))
            renderer.request_draw()


controller = gfx.PanZoomController(camera, register_events=renderer)

controller.controls = {
    "shift+mouse1": ("pan", "drag", (1, 0)),
    "wheel": ("pan", "push", (-0.05, 0)),
    "mouse3": ("quickzoom", "peek", 2),
}

if __name__ == "__main__":
    renderer.request_draw(lambda: renderer.render(scene, camera))
    run()
