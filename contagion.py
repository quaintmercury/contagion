"""Simple grid model of contagion"""

import graphics.grid

def main():
    """Just a background grid for now"""
    nrows = 500
    ncols = 500
    grid = graphics.grid.Grid(nrows, ncols,
                              100,100,
                              "Contagion", autoflush=False)
    for row in range(nrows):
        for col in range(ncols):
            grid.fill_cell(row, col, graphics.grid.WHITE,
                           border_color=graphics.grid.GREY,
                           border_width=0.25)
        grid.update(rate=5)
    grid.win.update()
    i = input("Press enter to close")

if __name__ == "__main__":
    main()