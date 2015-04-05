from PIL import Image


def update_image(path, status, static_dir):
    original = Image.open(path)
    mark = Image.open('{}/img/{}.jpg'.format(static_dir, status.lower()))
    original.paste(mark, (0, 300))
    original.save(path)