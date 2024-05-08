import tkinter as tk
import random
from tkinter import ttk, filedialog
from PIL import Image, ImageTk


class MapEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("2D Games Map Editor")
        self.root.geometry("1150x800")

        # inputs defaults
        self.default_cols = tk.StringVar(value="32")
        self.default_rows = tk.StringVar(value="32")
        self.default_tile_width = tk.StringVar(value="32")
        self.default_tile_height = tk.StringVar(value="32")

        # 2d array for the map design
        self.grid_state = []

        # selected tile for drawing
        self.current_tool = 1

        # image for tiles sprite sheet
        self.sprite_img = None

        # list for images exported from the sprite image file
        self.tiles_images = None

        # sprite sheet file
        self.selected_tiles_file_path = None

        # tiles tool selection box size
        self.tools_rows_count = 4
        self.tools_height = 300

        # lists of images used for tools selection and map grid
        self.images_for_tools = []
        self.grid_images_for_map_grid = []

        # for drawing tiles while holding the mouse button down
        self.is_mouse_pressed = False

        map_canvas_height = 700
        map_canvas_width = 860
        tools_canvas_height = 386
        tools_canvas_width = 148

        # SPRITES CONFIG

        self.box_1 = ttk.Frame(self.root)
        self.box_1.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="ne")

        self.box_1_frame = tk.LabelFrame(self.box_1, text="Tiles")
        self.box_1_frame.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="ne")

        label = ttk.Label(self.box_1_frame, text="Size:")
        label.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))

        self.tile_size_width_input = ttk.Entry(self.box_1_frame, textvariable=self.default_tile_width, width=5)
        self.tile_size_width_input.grid(row=0, column=1, padx=(5, 5), pady=(5, 5))

        label = ttk.Label(self.box_1_frame, text="x")
        label.grid(row=0, column=2, padx=(5, 5), pady=(5, 5))

        self.tile_size_height_input = ttk.Entry(self.box_1_frame, textvariable=self.default_tile_height, width=5)
        self.tile_size_height_input.grid(row=0, column=3, padx=(5, 5), pady=(5, 5))

        self.file_button = ttk.Button(self.box_1_frame, width=10, text="Select sprite...", command=self.choose_file)
        self.file_button.grid(row=1, column=0, columnspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")

        ok_button = ttk.Button(self.box_1_frame, text="OK", width=2, command=self.on_accept_tile_settings_button_click)
        ok_button.grid(row=1, column=3, padx=(5, 5), pady=(5, 5), sticky="ne")

        # MAP DESIGN AND SETTINGS

        self.box_2 = ttk.Frame(self.root)
        self.box_2.grid(row=0, column=1, padx=(5, 5), pady=(5, 5), sticky="ne")

        self.box_2_frame = tk.Frame(self.box_2)
        self.box_2_frame.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="ne")

        label = ttk.Label(self.box_2_frame, text="Size:")
        label.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))

        self.grid_size_cols_input = ttk.Entry(self.box_2_frame, textvariable=self.default_cols, width=4)
        self.grid_size_cols_input.grid(row=0, column=1, padx=(5, 5), pady=(5, 5))

        label = ttk.Label(self.box_2_frame, text="x")
        label.grid(row=0, column=2, padx=(5, 5), pady=(5, 5))

        self.grid_size_rows_input = ttk.Entry(self.box_2_frame, textvariable=self.default_rows, width=4)
        self.grid_size_rows_input.grid(row=0, column=3, padx=(5, 5), pady=(5, 5))

        ok_button = ttk.Button(self.box_2_frame, text="OK", command=self.on_accept_settings_button_click, width=3)
        ok_button.grid(row=0, column=4, padx=(5, 5), pady=(5, 5))

        generate_button = ttk.Button(self.box_2_frame, text="Generate", command=self.on_generate_button_click, width=7)
        generate_button.grid(row=0, column=5, padx=(5, 5), pady=(5, 5))

        self.map_grid_canvas = tk.Canvas(self.box_2, width=map_canvas_width, height=map_canvas_height,
                                         scrollregion=(0, 0, 1200, 1200))
        self.map_grid_canvas.grid(row=1, column=0, padx=(5, 5), pady=(5, 5), sticky="nw")

        self.v_scroll1 = ttk.Scrollbar(self.box_2, orient="vertical", command=self.map_grid_canvas.yview)
        self.v_scroll1.grid(row=1, column=1, padx=(5, 5), pady=(5, 5), sticky="nwes")

        self.h_scroll1 = ttk.Scrollbar(self.box_2, orient="horizontal", command=self.map_grid_canvas.xview)
        self.h_scroll1.grid(row=2, column=0, columnspan=2, padx=(5, 5), pady=(5, 5), sticky="nwes")
        self.map_grid_canvas.config(xscrollcommand=self.h_scroll1.set, yscrollcommand=self.v_scroll1.set)

        # TOOL SELECTOR

        self.box_3 = ttk.Frame(self.box_1_frame)
        self.box_3.grid(row=3, column=0, columnspan=4, padx=(5, 5), pady=(5, 5), sticky="nw")

        self.tiles_canvas = tk.Canvas(self.box_3, width=tools_canvas_width, height=tools_canvas_height,
                                      scrollregion=(0, 0, 148, self.tools_height))
        self.tiles_canvas.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="nw")

        v_scroll1 = ttk.Scrollbar(self.box_3, orient="vertical", command=self.tiles_canvas.yview)
        v_scroll1.grid(row=0, column=1, padx=(5, 5), pady=(5, 5), sticky="nwes")

        self.tiles_canvas.config(yscrollcommand=v_scroll1.set)

        # MAP HASH

        self.box_4_frame_2 = tk.LabelFrame(self.box_1, text="Hash")
        self.box_4_frame_2.grid(row=1, column=0, sticky="nw", padx=(5, 5))

        self.textarea = tk.Text(self.box_4_frame_2, width=13, height=8)
        self.textarea.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nwse")

        get_map_button = ttk.Button(self.box_4_frame_2, text="Save", command=self.on_get_map_button_click)
        get_map_button.grid(row=1, column=0, padx=(5, 5), pady=5, sticky="nw")

        set_map_button = ttk.Button(self.box_4_frame_2, text="Load", command=self.on_set_map_button_click)
        set_map_button.grid(row=1, column=1, padx=(5, 5), pady=5, sticky="nw")

        # ON-CLICK EVENTS

        self.map_grid_canvas.bind("<Button-1>", self.on_grid_click)
        self.tiles_canvas.bind("<Button-1>", self.on_tool_click)
        self.map_grid_canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.map_grid_canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

        # INITIALIZE VIEW

        self.draw_tools_on_tiles_canvas(4, 4, 32, 32)
        self.draw_empty_grid_on_map_canvas(32, 32, 32, 32)

    # HANDLE SPRITE SHEET FILE

    def choose_file(self):
        file_path = filedialog.askopenfilename()
        self.selected_tiles_file_path = file_path

    def load_tiles_from_file(self):
        if self.selected_tiles_file_path:
            self.sprite_img = Image.open(self.selected_tiles_file_path)
            self.tiles_images = self.split_image()
            n1 = len(self.tiles_images)
            k1 = 4
            self.tools_rows_count = n1 // k1
            if n1 % k1 != 0:
                self.tools_rows_count += 1
            self.tiles_canvas.config(scrollregion=(0, 0, 148, self.tools_rows_count * 32))

    def split_image(self):
        tile_w = int(self.tile_size_width_input.get())
        tile_h = int(self.tile_size_height_input.get())
        scaled_tile_size = 32
        images = []
        for y in range(0, self.sprite_img.height, tile_h):
            for x in range(0, self.sprite_img.width, tile_w):
                tile = self.sprite_img.crop((x, y, x + tile_w, y + tile_h))
                tile.thumbnail((scaled_tile_size, scaled_tile_size))
                if tile.size[0] < scaled_tile_size or tile.size[1] < scaled_tile_size:
                    tile = tile.resize((scaled_tile_size, scaled_tile_size))
                images.append(tile)
        return images

    # HANDLE MOUSE MOVES AND CLICKS

    def on_mouse_drag(self, event):
        if self.is_mouse_pressed:
            x_offset = int(self.map_grid_canvas.canvasx(0))
            y_offset = int(self.map_grid_canvas.canvasy(0))
            col = (event.x + x_offset) // 32
            row = (event.y + y_offset) // 32
            self.grid_state[row][col] = self.current_tool
            x1 = col * 32
            y1 = row * 32
            x2 = x1 + 32
            y2 = y1 + 32
            self.map_grid_canvas.create_rectangle(x1, y1, x2, y2, fill="black")
            if self.tiles_images and self.current_tool < len(self.tiles_images):
                photo = ImageTk.PhotoImage(self.tiles_images[self.current_tool - 1])
                self.grid_images_for_map_grid.append(photo)
                self.map_grid_canvas.create_image(x1, y1, anchor=tk.NW, image=photo)
            else:
                self.map_grid_canvas.create_rectangle(x1, y1, x2, y2, fill="black")
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                self.map_grid_canvas.create_text(center_x, center_y, text=str(self.current_tool), fill="white")

    def on_mouse_release(self, event):
        self.is_mouse_pressed = False

    def on_grid_click(self, event):
        self.is_mouse_pressed = True
        x_offset = int(self.map_grid_canvas.canvasx(0))
        y_offset = int(self.map_grid_canvas.canvasy(0))
        col = (event.x + x_offset) // 32
        row = (event.y + y_offset) // 32
        x1 = col * 32
        y1 = row * 32
        x2 = x1 + 32
        y2 = y1 + 32
        if self.grid_state[row][col] != 0:
            self.grid_state[row][col] = 0
            self.map_grid_canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray", width=1)
        else:
            self.grid_state[row][col] = self.current_tool
            if self.tiles_images and self.current_tool < len(self.tiles_images):
                photo = ImageTk.PhotoImage(self.tiles_images[self.current_tool - 1])
                self.grid_images_for_map_grid.append(photo)
                self.map_grid_canvas.create_image(x1, y1, anchor=tk.NW, image=photo)
            else:
                self.map_grid_canvas.create_rectangle(x1, y1, x2, y2, fill="black")
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                self.map_grid_canvas.create_text(center_x, center_y, text=str(self.current_tool), fill="white")

    def on_tool_click(self, event):
        x_offset = int(self.tiles_canvas.canvasx(0))
        y_offset = int(self.tiles_canvas.canvasy(0))
        cols = 4
        col_index = (event.x + x_offset) // 32
        row_index = (event.y + y_offset) // 32
        index = col_index + row_index * cols + 1
        self.current_tool = index
        self.draw_tools_on_tiles_canvas(4, self.tools_rows_count, 32, 32)

    def draw_tools_on_tiles_canvas(self, cols, rows, tile_width, tile_height):
        self.tiles_canvas.delete("all")
        if self.tiles_images:
            self.draw_images_on_tiles_canvas()
            i = 0
            for row in range(rows):
                for col in range(cols):
                    x1 = col * tile_width
                    y1 = row * tile_height
                    x2 = x1 + tile_width
                    y2 = y1 + tile_height
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2
                    i = i + 1
                    if i <= len(self.tiles_images):
                        if i == self.current_tool:
                            self.draw_text_with_border(center_x, center_y, text=str(i), color="red")
                        else:
                            self.draw_text_with_border(center_x, center_y, text=str(i), color="black")
        else:
            i = 0
            for row in range(rows):
                for col in range(cols):
                    x1 = col * tile_width
                    y1 = row * tile_height
                    x2 = x1 + tile_width
                    y2 = y1 + tile_height
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2
                    i = i + 1
                    self.tiles_canvas.create_rectangle(x1, y1, x2, y2, outline="gray", width=1)
                    if i == self.current_tool:
                        self.tiles_canvas.create_text(center_x, center_y, text=str(i), fill="red")
                    else:
                        self.tiles_canvas.create_text(center_x, center_y, text=str(i), fill="black")

    def draw_text_with_border(self, center_x, center_y, text, color):
        # outline
        self.tiles_canvas.create_text(center_x - 1, center_y, text=text, fill="white", font=("Helvetica", 12, "bold"))
        self.tiles_canvas.create_text(center_x + 1, center_y, text=text, fill="white", font=("Helvetica", 12, "bold"))
        self.tiles_canvas.create_text(center_x, center_y - 1, text=text, fill="white", font=("Helvetica", 12, "bold"))
        self.tiles_canvas.create_text(center_x, center_y + 1, text=text, fill="white", font=("Helvetica", 12, "bold"))
        # text
        self.tiles_canvas.create_text(center_x, center_y, text=text, fill=color, font=("Helvetica", 12, "bold"))

    # HANDLE BUTTONS CLICKS

    def on_accept_settings_button_click(self):
        cols = int(self.grid_size_cols_input.get())
        rows = int(self.grid_size_rows_input.get())
        tile_w = 32  # int(self.tile_size_width_input.get())
        tile_h = 32  # int(self.tile_size_height_input.get())
        self.draw_empty_grid_on_map_canvas(cols, rows, 32, 32)
        self.map_grid_canvas.config(scrollregion=(0, 0, cols * tile_w, rows * tile_h))

    @staticmethod
    def generate_maze(width, height):
        maze = [[1] * width for _ in range(height)]

        def create_path(x, y):
            directions = [(x, y - 2), (x + 2, y), (x, y + 2), (x - 2, y)]
            random.shuffle(directions)
            for new_x, new_y in directions:
                if 0 <= new_x < width and 0 <= new_y < height and maze[new_y][new_x] == 1:
                    maze[new_y][new_x] = 0
                    maze[new_y - (new_y - y) // 2][new_x - (new_x - x) // 2] = 0
                    create_path(new_x, new_y)

        create_path(1, 1)

        return maze

    def on_generate_button_click(self):

        cols = int(self.grid_size_cols_input.get())
        rows = int(self.grid_size_rows_input.get())

        self.grid_state = [[0] * cols for _ in range(rows)]

        self.grid_state = self.generate_maze(cols, cols)

        tile_w = 32  # int(self.tile_size_width_input.get())
        tile_h = 32  # int(self.tile_size_height_input.get())

        self.map_grid_canvas.delete("all")

        for row in range(rows):
            for col in range(cols):
                x1 = col * tile_w
                y1 = row * tile_h
                x2 = x1 + tile_w
                y2 = y1 + tile_h
                if self.grid_state[row][col] == 1:

                    if self.tiles_images and self.current_tool < len(self.tiles_images):
                        photo = ImageTk.PhotoImage(self.tiles_images[self.current_tool - 1])
                        self.grid_images_for_map_grid.append(photo)
                        self.map_grid_canvas.create_image(x1, y1, anchor=tk.NW, image=photo)
                    else:
                        self.map_grid_canvas.create_rectangle(x1, y1, x2, y2, fill="black")
                        center_x = (x1 + x2) / 2
                        center_y = (y1 + y2) / 2
                        self.map_grid_canvas.create_text(center_x, center_y, text=str(1), fill="white")
                else:
                    self.map_grid_canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill="white", width=1)

        self.map_grid_canvas.config(scrollregion=(0, 0, cols * tile_w, rows * tile_h))

    def on_accept_tile_settings_button_click(self):
        self.load_tiles_from_file()
        self.draw_tools_on_tiles_canvas(4, self.tools_rows_count, 32, 32)

    def on_set_map_button_click(self):
        cols = int(self.grid_size_cols_input.get())
        rows = int(self.grid_size_rows_input.get())
        self.grid_state = [[0] * cols for _ in range(rows)]
        grid_string = self.textarea.get("1.0", tk.END).strip()
        index = 0
        self.draw_empty_grid_on_map_canvas(cols, rows, 32, 32)
        for row in range(rows):
            for col in range(cols):
                cell_value = int(grid_string[index:index + 4])
                self.grid_state[row][col] = cell_value
                index += 4
                x1 = col * 32
                y1 = row * 32
                x2 = x1 + 32
                y2 = y1 + 32
                if self.grid_state[row][col] != 0:
                    self.current_tool = self.grid_state[row][col]
                    if self.tiles_images and self.current_tool < len(self.tiles_images):
                        photo = ImageTk.PhotoImage(self.tiles_images[self.current_tool - 1])
                        self.grid_images_for_map_grid.append(photo)
                        self.map_grid_canvas.create_image(x1, y1, anchor=tk.NW, image=photo)
                    else:
                        self.map_grid_canvas.create_rectangle(x1, y1, x2, y2, fill="black")
                        center_x = (x1 + x2) / 2
                        center_y = (y1 + y2) / 2
                        self.map_grid_canvas.create_text(center_x, center_y, text=str(self.current_tool), fill="white")

    def on_get_map_button_click(self):
        grid_string = ""
        cols = int(self.grid_size_cols_input.get())
        rows = int(self.grid_size_rows_input.get())
        for row in range(rows):
            for col in range(cols):
                grid_string += str(self.grid_state[row][col]).zfill(4)
        self.textarea.delete(1.0, tk.END)
        self.textarea.insert(tk.END, grid_string)

    # TOOL SELECTION VIEW

    def draw_images_on_tiles_canvas(self):
        self.images_for_tools = []
        for i, img in enumerate(self.tiles_images):
            row = i // 4
            col = i % 4
            photo = ImageTk.PhotoImage(self.tiles_images[i])
            self.images_for_tools.append(photo)
            self.tiles_canvas.create_image(col * 32, row * 32, anchor=tk.NW, image=photo)

    # MAP DESIGN VIEW

    def draw_empty_grid_on_map_canvas(self, cols, rows, tile_width, tile_height):
        self.map_grid_canvas.delete("all")
        self.grid_state = [[0] * cols for _ in range(rows)]
        for row in range(rows):
            for col in range(cols):
                x1 = col * tile_width
                y1 = row * tile_height
                x2 = x1 + tile_width
                y2 = y1 + tile_height
                self.map_grid_canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill="white", width=1)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MapEditor()
    app.run()
