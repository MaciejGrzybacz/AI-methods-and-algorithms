from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont


class GridDrawer:
    def __init__(self, image: Image.Image, grid, header_height: Optional[int] = None):
        self.image = image
        self.header_height = header_height if header_height is not None else max(0, image.height - image.width)
        self.grid = grid
        self.draw = ImageDraw.Draw(self.image)
        self.cell_width, self.cell_height, self.border = self.calculate_cell_params()

    def calculate_cell_params(self):
        cell = int(self.image.width / self.grid.shape[0]), int((self.image.height - self.header_height) / self.grid.shape[1])
        cell_side = min(cell)
        border = int(cell_side / 10)
        return cell_side, cell_side, border

    def draw_grid(self):
        draw = ImageDraw.Draw(self.image)
        for x in range(0, self.image.width, self.cell_width):
            line = ((x, self.header_height), (x, self.image.height))
            draw.line(line, fill="black")

        for y in range(self.header_height, self.image.height, self.cell_height):
            line = ((0, y), (self.image.width, y))
            draw.line(line, fill="black")
 
    def get_cell_coords(self, padding: int, x: int, y: int, grid_x_end: Optional[int] = None, grid_y_end: Optional[int] = None, have_border: bool = True):
        if have_border:
            border = self.border
        else:
            border = 0

        x_start = x * self.cell_width + border + padding
        x_end = (grid_x_end or (x + 1)) * self.cell_width - border - padding
        y_start = y * self.cell_height + border + padding + self.header_height
        y_end = (grid_y_end or (y + 1)) * self.cell_width - border - padding + self.header_height
        return x_start, y_start, x_end, y_end

    def draw_rectangle(self, grid_coords: Tuple[int, ...], fill: Optional[Tuple[int, int, int]] = None, padding=0):
        coords = self.get_cell_coords(padding, *grid_coords)
        self.draw.rectangle(coords, fill)

    def line_through(self, grid_coords_start: Tuple[int, int], 
                           grid_coords_end: Tuple[int, int], 
                           fill: Optional[Tuple[int, int, int]] = None,
                           width: float = 1.0):
        x_start, y_start, _, _ = self.get_cell_coords(-self.border, *grid_coords_start)
        x_end, y_end, _, _ = self.get_cell_coords(-self.border, *grid_coords_end)
        x_pad = self.cell_width * 0.5
        y_pad = self.cell_height * 0.5
        x_start += x_pad
        x_end += x_pad
        y_start += y_pad
        y_end += y_pad
        
        self.draw.line([
            (x_start, y_start),
            (x_end, y_end)
            ],
            fill = fill,
            width=width)

    def draw_header_text(self, text, fill: Tuple[int, int, int], font: ImageFont):
        x_start, y_start, width, height = 0, 0, self.image.width, self.header_height
        self.draw.text((
            x_start + width // 2,
            y_start + height // 2,
        ), text, fill=fill, font=font, anchor='mm')


    def draw_text(self, text: str, grid_coords: Tuple[int, ...], fill: Tuple[int, int, int], font: ImageFont):
        x_start, y_start, _, _ = self.get_cell_coords(-self.border, *grid_coords)
        self.draw.text((
            x_start + (self.cell_width // 2),
            y_start + (self.cell_height // 2)
        ), text, fill=fill, font=font, anchor='mm')

    def draw_circle(self, grid_x: int, grid_y: int, fill: Optional[Tuple[int, int, int]] = None):
        coords = self.get_cell_coords(0, grid_x, grid_y)
        self.draw.ellipse(coords, fill)

    def draw_dot(self, grid_x: int, grid_y: int, fill: Optional[Tuple[int, int, int]] = None):
        x, y = self.get_cell_coords(0, grid_x, grid_y, have_border=False)[0:2]
        self.draw.ellipse((x-self.cell_width//10, y-self.cell_height//10,
                           x+self.cell_width//10, y+self.cell_height//10), fill)

