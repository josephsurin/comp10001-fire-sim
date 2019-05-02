from PIL import Image, ImageDraw, ImageFont

black = (0,0,0)
white = (0xff,0xff,0xff)
blue = (190,150,220)
red = (0xe5,0x6e,0x50)

def draw_state(f_grid, h_grid, b_grid, burn_count, timeframe, w_direction, i_threshold, sq_size=100):
    dim = len(f_grid)
    grid_size = sq_size*dim
    base = Image.new('RGB', (grid_size+sq_size, grid_size+sq_size), white)
    f_font = ImageFont.truetype('./Montserrat-Bold.ttf', size=sq_size//3)
    h_font = ImageFont.truetype('./Montserrat-Bold.ttf', size=sq_size//6)
    d = ImageDraw.Draw(base)

    # draw details
    coords = [(i, j) for i in range(dim) for j in range(dim)]
    for (i, j) in coords:
        # colour burning cells
        if b_grid[j][i]:
            d.rectangle([(sq_size*i, sq_size*j), (sq_size*(i+1), sq_size*(j+1))], fill=red)
        # draw fuel load text
        ft = str(f_grid[j][i]) 
        fw, fh = d.textsize(ft, font=f_font)
        d.text((sq_size*i + (sq_size-fw)/2, sq_size*j + (sq_size-fh)/2), ft, fill=black, font=f_font)
        # draw height text
        ht = str(h_grid[j][i])
        hw, hh = d.textsize(ht, font=h_font)
        d.text((sq_size*(i+0.95) - hw, sq_size*(j+0.95) - hh), ht, fill=blue, font=h_font)

    # draw outer rectangle
    d.rectangle([(0,0),(grid_size, grid_size)], outline=black, width=4)

    # draw inner lines
    for i in range(1, dim):
        d.line([(sq_size*i, 0), (sq_size*i, grid_size)], fill=black, width=2)
        d.line([(0, sq_size*i), (grid_size, sq_size*i)], fill=black, width=2)

    # draw burn count
    bt = str(burn_count)
    bw, bh = d.textsize(bt, font=f_font)
    d.text((grid_size + (sq_size-bw)/2, (sq_size-bh)/2), bt, fill=red, font=f_font)

    # draw time frame
    tt = 't = ' + str(timeframe)
    tw, th = d.textsize(tt, font=f_font)
    d.text((grid_size + (sq_size-tw)/2, sq_size + (sq_size-th)/2), tt, fill=black, font=f_font)

    # draw w_direction
    wt = 'wind: ' + (w_direction or '-')
    ww, wh = d.textsize(wt, font=h_font)
    d.text(((sq_size-ww)/2, grid_size + (sq_size-wh)/2), wt, fill=black, font=h_font)

    # draw i_threshold
    it = 'threshold: ' + str(i_threshold)
    iw, ih = d.textsize(it, font=h_font)
    d.text((sq_size + (sq_size-ww)/2, grid_size + (sq_size-ih)/2), it, fill=black, font=h_font)

    return base

from lib import run_model

def generate_sim(f_grid, h_grid, i_threshold, w_direction, burn_seeds, duration, outfile):
    states = run_model(f_grid, h_grid, i_threshold, w_direction, burn_seeds)
    frames = [draw_state(s[0], h_grid, s[1],  s[2], t, w_direction, i_threshold) for t,s in enumerate(states)]
    frames[0].save(outfile, save_all=True, append_images=frames[1:], duration=duration, loop=0)

import random

def random_model(max_size=50, max_fuel=10, max_height=6):
    size = random.randint(2, max_size)
    f_grid = [[random.randint(0, max_fuel) for _ in range(size)] for _ in range(size)]
    h_grid = [[random.randint(1, max_height) for _ in range(size)] for _ in range(size)]
    i_threshold = random.randint(1, 8)
    w_direction = random.choice([None, 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
    fl_coords = [(i, j) for i in range(size) for j in range(size) if f_grid[i][j]]
    burn_seeds = random.sample(fl_coords, random.randint(len(fl_coords)//3, len(fl_coords)//1.75))
    return (f_grid, h_grid, i_threshold, w_direction, burn_seeds)
