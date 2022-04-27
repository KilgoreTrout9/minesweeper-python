from tkinter import Button, Label, messagebox
import settings
import random
import ctypes
import sys

class Cell:
  all = []
  cell_count = settings.CELL_COUNT
  cell_count_label_object = None
  def __init__(self, x, y, is_mine=False):
    self.is_mine = is_mine
    self.is_open = False
    self.is_marked = False
    self.cell_btn_object = None
    self.x = x
    self.y = y

    # Append the object to the Cell.all list
    Cell.all.append(self)

  def create_btn_object(self, location):
    btn = Button(
      location,
      width=12,
      height=4
    )
    btn.bind('<Button-1>', self.reveal_mine)
    btn.bind('<Button-3>', self.mark_mine)
    self.cell_btn_object = btn

  @staticmethod
  def create_cell_count_label(location):
    lbl = Label(
      location,
      bg='black',
      fg='white',
      text=f'Cells Left:{Cell.cell_count}',
      font=('', 30)
    )
    Cell.cell_count_label_object = lbl

  def reveal_mine(self, event):
    if not self.is_marked:
      if self.is_mine:
        self.show_mine()
      else:
        if self.surrounded_mines == 0:
          for cell_obj in self.surrounded_cells:
            cell_obj.show_number()
        self.show_number()

  def show_mine(self):
    self.cell_btn_object.configure(bg='red', text='KABOOM')
    #should stop game and show that player lost
    messagebox.showinfo('Game Over', 'You found a mine')
    sys.exit()

  def get_cell_by_axis(self, x, y):
    for cell in Cell.all:
      if cell.x == x and cell.y == y:
        return cell

  @property
  def surrounded_cells(self):
    cells = [
      self.get_cell_by_axis(self.x - 1, self.y - 1),
      self.get_cell_by_axis(self.x - 1, self.y),
      self.get_cell_by_axis(self.x - 1, self.y + 1),
      self.get_cell_by_axis(self.x, self.y - 1),
      self.get_cell_by_axis(self.x, self.y + 1),
      self.get_cell_by_axis(self.x + 1, self.y - 1),
      self.get_cell_by_axis(self.x + 1, self.y),
      self.get_cell_by_axis(self.x + 1, self.y + 1)
    ]

    cells = [cell for cell in cells if cell is not None]
    return cells

  @property
  def surrounded_mines(self):
    counter = 0
    for cell in self.surrounded_cells:
      if cell.is_mine:
        counter += 1

    return counter

  def show_number(self):
    if not self.is_open:
      self.is_open = True
      Cell.cell_count -= 1
      self.cell_btn_object.configure(text=self.surrounded_mines)

      # update cell counter
      if Cell.cell_count_label_object:
        Cell.cell_count_label_object.configure(
          text=f'Cells Left:{Cell.cell_count}'
        )

      # you win the game if there are only mines left
      if (Cell.cell_count - settings.MINE_COUNT) == 0:
        messagebox.showinfo('Winner', 'You avoided all the mines')
        sys.exit()

  def mark_mine(self, event):
    if not self.is_open:
      if not self.is_marked:
        self.cell_btn_object.configure(bg='orange', text='Bomb')
      else:
        self.cell_btn_object.configure(bg='SystemButtonFace', text='')
      self.is_marked = not self.is_marked

  @staticmethod
  def randomize_mines():
    mines = random.sample(
      Cell.all, settings.MINE_COUNT
    )
    for mine in mines:
      mine.is_mine = True

  def __repr__(self):
    return f"Cell({self.x}, {self.y})"